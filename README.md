# Data Analyst AI Agent

This repository provides an AI-powered interface for interacting with PrestoDB and PostgreSQL databases. Users can input common language queries and receive SQL statements and results directly from their databases.

## Set Up

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

## Environment Variables

To properly configure the Data Analyst AI Agent, you need to set the following environment variables in a .env file:

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

Make sure to replace the placeholder values with your actual configuration details.
