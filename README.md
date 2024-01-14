# Data Analyst AI Agent

This repository provides an AI-powered interface for interacting with PrestoDB and PostgreSQL databases. Users can input common language queries and receive SQL statements and results directly from their databases.

## Set Up

### PrestoDB Setup

To run the project with PrestoDB, use the following command:

poetry run turbo_presto --prompt "[Include your prompt here]"
poetry run start_presto --prompt "[Include your prompt here]"

Entry points for running PrestoDB tasks:

- start_presto: Runs the application using main_presto.py.
  start_presto = "da_ai_agent.main_presto:main"
  
- turbo_presto: Runs the application using turbo_main_presto.py.
  turbo_presto = "da_ai_agent.turbo_main_presto:main"

### PostgreSQL Setup

To run the project with a PostgreSQL database, you can use one of the following commands. Each command uses a different main file:

poetry run turbo_postgres --prompt "[Include your prompt here]"
poetry run start_presto --prompt "[Include your prompt here]"

- start_postgres: Runs the application using main_postgres.py.
  start_postgres = "da_ai_agent.main_postgres:main"

- turbo_postgres: Runs the application using turbo_main_postgres.py.
  turbo_postgres = "da_ai_agent.turbo_main_postgres:main"
