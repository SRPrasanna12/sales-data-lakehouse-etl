
# Sales Data Lakehouse ETL Pipeline

## Project Overview

Developed a Python-based ETL pipeline to process raw sales data using a Bronze, Silver, and Gold architecture.

The project demonstrates data ingestion, data cleaning, validation, transformation, SQL analysis, and automated testing.

## Architecture

Raw CSV Data
     |
     v
Bronze Layer
(Preserves original records)
     |
     v
Silver Layer
(Data cleaning and validation)
     |
     +----> Rejected Records
     |
     v
Gold Layer
(Product-level sales aggregation)
     |
     v
SQLite Database
     |
     v
SQL Analysis

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Pytest
- Logging
- Git and GitHub

## Project Features

1. CSV data ingestion using Pandas.
2. Bronze layer for preserving raw data.
3. Silver layer for cleaning and validation.
4. Duplicate order detection.
5. Missing and invalid value handling.
6. Separate rejected records dataset.
7. Gold layer for business-level aggregation.
8. Revenue calculation.
9. SQLite database integration.
10. SQL-based sales analysis.
11. Logging for pipeline execution.
12. Automated tests using Pytest.

## SQL Analysis

The project includes queries for:

- Revenue by product.
- Total quantity sold.
- Total sales revenue.
- Total number of valid orders.

## Sample Results

| Product | Quantity | Revenue |
|---|---:|---:|
| AirPods | 3 | 36000 |
| MacBook | 1 | 120000 |
| iPad | 2 | 90000 |
| iPhone | 1 | 80000 |

Total Revenue: 326000

## Installation

Install dependencies:

pip install -r requirements.txt

## Run the ETL Pipeline

python src/pipeline.py

## Run SQL Analysis

python src/sql_analysis.py

## Run Automated Tests

python -m pytest tests/ -v

## Testing Results

6 automated tests passed.

## Author

Prasanna
