"""
Clone of da_ai_agent/agents/turbo4.py
"""

import json
import os
import openai
import time
from typing import Callable, Dict, Any, List, Optional, Union, Tuple
import dotenv
from dataclasses import dataclass, asdict
from openai import OpenAI
from openai.types.beta import Thread, Assistant
from openai.types import FileObject
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from modules import llm
from modules.models import Chat, TurboTool

dotenv.load_dotenv()


class Turbo4:
    """
    Simple, chainable class for the OpenAI's GPT-4 Assistant APIs.
    """

    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.client: openai = OpenAI()

        self.map_function_tools: Dict[str, TurboTool] = {}
        self.current_thread_id = None
        self.thread_messages: List[ThreadMessage] = []
        self.local_messages = []
        self.file_ids = []
        self.assistant_id = None
        self.polling_interval = (
            0.5  # Interval in seconds to poll the API for thread run completion
        )
        self.model = "gpt-4-1106-preview"

    @property
    def chat_messages(self) -> List[Chat]:
        return [
            Chat(
                from_name=msg.role,
                to_name="assistant" if msg.role == "user" else "user",
                message=llm.safe_get(msg.model_dump(), "content.0.text.value"),
                created=msg.created_at,
            )
            for msg in self.thread_messages
        ]

    @property
    def tool_config(self):
        return [tool.config for tool in self.map_function_tools.values()]

    # ------------- Additional Utility Functions -----------------

    def run_validation(self, validation_func: Callable):
        print(f"run_validation({validation_func.__name__})")
        validation_func()
        return self

    def spy_on_assistant(self, output_file: str):
        sorted_messages = sorted(
            self.chat_messages, key=lambda msg: msg.created, reverse=False
        )
        messages_as_json = [asdict(msg) for msg in sorted_messages]
        with open(output_file, "w") as f:
            json.dump(messages_as_json, f, indent=2)

        return self

    def get_costs_and_tokens(self, output_file: str) -> Tuple[float, float]:
        """
        Get the estimated cost and token usage for the current thread.

        https://openai.com/pricing

        Open questions - how to calculate retrieval and code interpreter costs?
        """

        retrival_costs = 0
        code_interpreter_costs = 0

        msgs = [
            llm.safe_get(msg.model_dump(), "content.0.text.value")
            for msg in self.thread_messages
        ]
        joined_msgs = " ".join(msgs)

        msg_cost, tokens = llm.estimate_price_and_tokens(joined_msgs, self.model)

        with open(output_file, "w") as f:
            json.dump(
                {
                    "cost": msg_cost,
                    "tokens": tokens,
                },
                f,
                indent=2,
            )

        return self

    # ------------- CORE ASSISTANTS API FUNCTIONS -----------------

    def get_or_create_assistant(self, name: str, model: str = "gpt-4-1106-preview"):
        print(f"get_or_create_assistant({name}, {model})")
        # Retrieve the list of existing assistants
        assistants: List[Assistant] = self.client.beta.assistants.list().data

        # Check if an assistant with the given name already exists
        for assistant in assistants:
            if assistant.name == name:
                self.assistant_id = assistant.id

                # update model if different
                if assistant.model != model:
                    print(f"Updating assistant model from {assistant.model} to {model}")
                    self.client.beta.assistants.update(
                        assistant_id=self.assistant_id, model=model
                    )
                break
        else:  # If no assistant was found with the name, create a new one
            assistant = self.client.beta.assistants.create(model=model, name=name)
            self.assistant_id = assistant.id

        self.model = model

        return self

    def set_instructions(self, instructions: str):
        print(f"set_instructions()")
        if self.assistant_id is None:
            raise ValueError(
                "No assistant has been created or retrieved. Call get_or_create_assistant() first."
            )
        # Update the assistant with the new instructions
        updated_assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant_id, instructions=instructions
        )
        return self

    def equip_tools(
        self, turbo_tools: List[TurboTool], equip_on_assistant: bool = False
    ):
        print(f"equip_tools({turbo_tools}, {equip_on_assistant})")
        if self.assistant_id is None:
            raise ValueError(
                "No assistant has been created or retrieved. Call get_or_create_assistant() first."
            )

        # Update the functions dictionary with the new tools
        self.map_function_tools = {tool.name: tool for tool in turbo_tools}

        if equip_on_assistant:
            # Update the assistant with the new list of tools, replacing any existing tools
            updated_assistant = self.client.beta.assistants.update(
                tools=self.tool_config, assistant_id=self.assistant_id
            )

        return self

    def make_thread(self):
        print(f"make_thread()")

        if self.assistant_id is None:
            raise ValueError(
                "No assistant has been created. Call create_assistant() first."
            )

        response = self.client.beta.threads.create()
        self.current_thread_id = response.id
        self.thread_messages = []
        return self

    def add_message(
        self,
        message: str,
        file_ids: Optional[List[str]] = None,
        refresh_threads: bool = False,
    ):
        print(f"add_message(message={message}, file_ids={file_ids})")
        self.local_messages.append(message)
        self.client.beta.threads.messages.create(
            thread_id=self.current_thread_id,
            content=message,
            role="user",
            file_ids=file_ids or [],
        )
        if refresh_threads:
            self.load_threads()
        return self

    def load_threads(self):
        self.thread_messages = self.client.beta.threads.messages.list(
            thread_id=self.current_thread_id
        ).data

    def list_steps(self):
        print(f"list_steps()")
        steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.current_thread_id,
            run_id=self.run_id,
        )
        print("steps", steps)
        return steps

    def run_thread(self, toolbox: Optional[List[str]] = None):
        print(f"run_thread(toolbox={toolbox})")
        if self.current_thread_id is None:
            raise ValueError("No thread has been created. Call make_thread() first.")
        if self.local_messages == []:
            raise ValueError("No messages have been added to the thread.")

        if toolbox is None:
            tools = None
        else:
            # get tools from toolbox
            tools = [self.map_function_tools[tool_name].config for tool_name in toolbox]

            # throw if tool not found
            if len(tools) != len(toolbox):
                raise ValueError(
                    f"Tool not found in toolbox. toolbox={toolbox}, tools={tools}. Make sure all tools are equipped on the assistant."
                )

        # refresh current thread
        self.load_threads()

        # Start the thread running
        run = self.client.beta.threads.runs.create(
            thread_id=self.current_thread_id,
            assistant_id=self.assistant_id,
            tools=tools,
        )
        self.run_id = run.id

        # Polling mechanism to wait for thread's run completion or required actions
        while True:
            # self.list_steps()

            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.current_thread_id, run_id=self.run_id
            )
            if run_status.status == "requires_action":
                tool_outputs: List[ToolOutput] = []
                for (
                    tool_call
                ) in run_status.required_action.submit_tool_outputs.tool_calls:
                    tool_function = tool_call.function
                    tool_name = tool_function.name

                    # Check if tool_arguments is already a dictionary, if so, proceed directly
                    if isinstance(tool_function.arguments, dict):
                        tool_arguments = tool_function.arguments
                    else:
                        # Assume the arguments are JSON string and parse them
                        tool_arguments = json.loads(tool_function.arguments)

                    print(f"run_thread() Calling {tool_name}({tool_arguments})")

                    # Assuming arguments are passed as a dictionary
                    function_output = self.map_function_tools[tool_name].function(
                        **tool_arguments
                    )

                    tool_outputs.append(
                        ToolOutput(tool_call_id=tool_call.id, output=function_output)
                    )

                # Submit the tool outputs back to the API
                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.current_thread_id,
                    run_id=self.run_id,
                    tool_outputs=[to for to in tool_outputs],
                )
            elif run_status.status == "completed":
                self.load_threads()
                return self

            time.sleep(self.polling_interval)  # Wait a little before polling again

    def enable_retrieval(self):
        print(f"enable_retrieval()")
        if self.assistant_id is None:
            raise ValueError(
                "No assistant has been created or retrieved. Call get_or_create_assistant() first."
            )

        # Update the assistant with the new list of tools, replacing any existing tools
        updated_assistant = self.client.beta.assistants.update(
            tools=[{"type": "retrieval"}], assistant_id=self.assistant_id
        )

        return self

    def upsert_files(self, file_paths: List[str]) -> List[str]:
        """

        Upserts files to the file api - does not attach to assistant at all

        1. Get all current files from the files api
        2. Check if file exists
        3. If file exists, look for byte size differences if changed: update it
        4. If file does not exist, create it
        """
        print(f"upsert_file({file_paths})")

        # confirm all files exist
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise ValueError(f"File does not exist: {file_path}")

        if self.assistant_id is None:
            raise ValueError(
                "No assistant has been created or retrieved. Call get_or_create_assistant() first."
            )

        existing_files: List[FileObject] = self.client.files.list().data

        print("existing_files", existing_files)

        matched_files: List[FileObject] = []

        # create file objects
        for i in file_paths:
            file_name = os.path.basename(i)
            file_object = open(i, "rb")

            print("file_object", file_object)

            local_file_size = os.path.getsize(i)

            file_found = False  # Flag to check if file was found

            # check if file exists
            for existing_file in existing_files:
                if existing_file.filename == file_name:
                    print(f"Found existing file {file_name}")
                    file_found = True  # Set flag to True since file is found

                    # check if file has changed - delete and reupload if so
                    if existing_file.bytes != local_file_size:
                        print(f"File {file_name} has changed - updating")
                        self.client.files.delete(file_id=existing_file)
                        updated_file_object: FileObject = self.client.files.create(
                            file=file_object,
                            purpose="assistants",
                        )
                        matched_files.append(updated_file_object)
                    break  # Exit the loop after handling the existing file

            # If the file was not found, create it
            if not file_found:
                print(f"Creating file {file_name}")
                new_file_object: FileObject = self.client.files.create(
                    file=file_object,
                    purpose="assistants",
                )
                matched_files.append(new_file_object)
            else:
                print(f"File {file_name} already exists - no updates needed")
                matched_files.append(existing_file)

        return [f.id for f in matched_files]

    def get_files(self, file_ids: Optional[List[str]] = None):
        print(f"list_files()")
        files = self.client.files.list().data
        if file_ids is not None:
            print(f"filtering files by {file_ids}")
            files = [file for file in files if file.id in file_ids]
        print("files", files)
        return files

    def get_files_by_name(self, file_names: List[str]):
        print(f"get_files_by_name({file_names})")
        files: List[FileObject] = self.client.files.list().data

        output_files = []

        for file_name in file_names:
            for file in files:
                print("file.filename", file.filename)
                if file.filename == file_name:
                    output_files.append(file)
                    break

        print("files", files)

        return output_files

    def get_file_ids_by_name(self, file_paths: List[str]):
        print(f"get_file_ids_by_name({file_paths})")
        file_names = [os.path.basename(file_path) for file_path in file_paths]
        print("file_names", file_names)
        files = self.get_files_by_name(file_names)
        print("files", files)
        file_ids = [file.id for file in files]
        print("file_ids", file_ids)
        return file_ids
