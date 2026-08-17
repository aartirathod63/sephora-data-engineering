# 💄 Sephora India — End-to-End Data Engineering & Analytics Platform

> **A production-style retail data engineering pipeline built with PySpark, MySQL, SQL and Tableau to transform raw Sephora India transaction data into analytics-ready business insights.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-4.2.0-orange?logo=apachespark)](https://spark.apache.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)](https://www.mysql.com/)
[![Tableau](https://img.shields.io/badge/Tableau-Public-blue?logo=tableau)](https://public.tableau.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]()

---

## 🚀 Project Overview

This project simulates a **real-world Sephora India retail data platform** designed to process customer, product, store and transaction data at scale.

The pipeline ingests raw CSV datasets, performs data-quality validation and business transformations using **PySpark**, stores curated data in **Parquet**, loads analytical data into a **MySQL star-schema warehouse**, and exposes business metrics through SQL views and Tableau.

The goal is to demonstrate how a Data Engineer builds a complete pipeline from:

**Raw Data → ETL → Data Quality → Data Warehouse → Analytics → BI**

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │     RAW CSV DATA    │
                    │                     │
                    │ Customers           │
                    │ Products            │
                    │ Stores              │
                    │ Orders              │
                    │ Order Items         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      PySpark        │
                    │      ETL Layer      │
                    │                     │
                    │ • Ingestion         │
                    │ • Cleaning         │
                    │ • Validation       │
                    │ • Transformation   │
                    │ • Joins            │
                    │ • Revenue Logic    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Processed Parquet  │
                    │                     │
                    │ Analytics-ready     │
                    │ datasets            │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       MySQL Data Warehouse     │
              │                                │
              │        STAR SCHEMA             │
              │                                │
              │  dim_customer                  │
              │  dim_product                   │
              │  dim_store                     │
              │  dim_date                      │
              │             │                  │
              │             ▼                  │
              │        fact_sales               │
              └────────────────┬───────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SQL Analytics    │
                    │                     │
                    │ • CTEs             │
                    │ • Window Functions  │
                    │ • Aggregations      │
                    │ • Views             │
                    │ • MoM Growth       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Tableau       │
                    │                     │
                    │ Revenue Dashboard   │
                    │ Customer Analytics  │
                    │ Product Analytics   │
                    │ Store Performance   │
                    └─────────────────────┘