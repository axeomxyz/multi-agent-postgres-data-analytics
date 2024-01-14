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

da_ai_agent/
│
├── main_presto.py         # Used by start_presto
│   └── start_presto = "da_ai_agent.main_presto:main"
│
└── turbo_main_presto.py   # Used by turbo_presto
    └── turbo_presto = "da_ai_agent.turbo_main_presto:main"

### PostgreSQL Setup

To run the project with a PostgreSQL database, use the following commands:

```bash
poetry run turbo_postgres --prompt "[Include your prompt here]"
poetry run start_postgres --prompt "[Include your prompt here]"
```

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

- POSTGRES_DATABASE_URL: Connection string for the PostgreSQL database.
- PRESTO_HTTP_SCHEME: HTTP scheme for PrestoDB (http or https).
- PRESTO_USER: Username for PrestoDB.
- PRESTO_PASSWORD: Password for PrestoDB.
- PRESTO_HOST: Hostname for PrestoDB.
- PRESTO_PORT: Port number for PrestoDB.
- PRESTO_CATALOG: Catalog name for PrestoDB.
- PRESTO_SCHEMA: Schema name for PrestoDB.
- OPENAI_API_KEY: API key for OpenAI services.
- BASE_DIR: Base directory for storing agent results.

Make sure to replace the placeholder values with your actual configuration details.
