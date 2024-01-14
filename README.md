# Data Analyst AI Agent

This repository provides an AI-powered interface for interacting with PrestoDB and PostgreSQL databases. Users can input common language queries and receive SQL statements and results directly from their databases.

## Project Description

[Provide a more detailed description of your project, its purpose, and key features.]

## Requirements

[List prerequisites needed to run the project.]

## Installation

1. Clone the repository:

```bash
   git clone [repository URL]
   cd postgres-da-ai-agent
```

2. Install dependencies:

```bash
poetry install
```   

3. Set up environment variables:
Create a .env file in the root directory with the necessary environment variables.


## Set Up

### Environment Variables

```dotenv
POSTGRES_DATABASE_URL="your_postgres_database_url"
PRESTO_HTTP_SCHEME="http_or_https"
PRESTO_USER="your_presto_username"
PRESTO_PASSWORD="your_presto_password"
PRESTO_HOST="your_presto_hostname"
PRESTO_PORT="your_presto_port"
PRESTO_CATALOG="your_presto_catalog"
PRESTO_SCHEMA="your_presto_schema"
OPENAI_API_KEY="your_openai_api_key"
BASE_DIR='./agent_results'
```

## Usage

### PrestoDB Setup

To run the project with PrestoDB, use the following commands:

```bash

poetry run turbo_presto --prompt "[Include your prompt here]"
poetry run start_presto --prompt "[Include your prompt here]"
```

Entry points for running PrestoDB tasks:

```tree
da_ai_agent/
│
├── main_presto.py         # Used by start_presto
│   └── start_presto = "da_ai_agent.main_presto:main"
│
└── turbo_main_presto.py   # Used by turbo_presto
    └── turbo_presto = "da_ai_agent.turbo_main_presto:main"
```

### PostgreSQL Setup


To run the project with a PostgreSQL database, use the following commands:

```bash
poetry run turbo_postgres --prompt "[Include your prompt here]"
poetry run start_postgres --prompt "[Include your prompt here]"
```

Entry points for running PostgreSQL tasks:
```tree
da_ai_agent/
│
├── main_postgres.py       # Used by start_postgres
│   └── start_postgres = "da_ai_agent.main_postgres:main"
│
└── turbo_main_postgres.py # Used by turbo_postgres
    └── turbo_postgres = "da_ai_agent.turbo_main_postgres:main"
```

## Configuration

[Include detailed instructions on how to configure your project, if applicable.]

## Testing

[Provide instructions on how to run tests, if your project includes them.]

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

Licensed under the MIT License.

## Acknowledgments

Thanks to all the contributors who have helped with this project. You can see a list of contributors [here](https://github.com/axeomxyz/multi-agent-postgres-data-analytics/contributors).


## Contact

[Provide contact information for project maintainers or contributors.]
