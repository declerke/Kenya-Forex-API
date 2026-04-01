# Project Summary — Kenya Forex Intelligence API

## What This Project Does

Builds an end-to-end data pipeline and REST API for tracking KES exchange rate movements against five major currencies (USD, EUR, GBP, CNY, JPY). Data is fetched hourly from a free public API, validated for quality, stored in DuckDB, and served via FastAPI endpoints covering live rates, historical time-series, volatility metrics, and moving averages.

## Why It Was Built

To demonstrate a modern, lightweight data engineering stack — specifically DuckDB as an embedded analytical database and Great Expectations for data quality validation — without requiring a heavy cloud infrastructure. The Kenya Shilling's real-world volatility makes this a live, continuously relevant dataset rather than a static demo.

## Key Technical Decisions

- **DuckDB over PostgreSQL** for the analytics layer: zero server overhead, columnar storage, and SQL-native window functions — ideal for time-series rate analytics at this scale.
- **Great Expectations ephemeral context**: validation runs in-process without a persistent GE project directory, keeping the stack lean.
- **Self-accumulating historical dataset**: rather than relying on a paid historical API, each hourly Airflow run appends a snapshot to DuckDB, building depth over time.
- **FastAPI with Pydantic response models**: strict response schemas ensure the API contract is explicit and self-documenting via `/docs`.

## Stack

FastAPI · DuckDB · Great Expectations · Apache Airflow · PostgreSQL (Airflow metadata) · Docker Compose

## Portfolio Signal

Demonstrates ability to combine orchestration (Airflow), data quality (Great Expectations), embedded OLAP (DuckDB), and API design (FastAPI) into a single coherent production-grade project — without cloud dependencies.
