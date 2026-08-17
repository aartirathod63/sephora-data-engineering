# 💄 Sephora India — End-to-End Data Engineering & Analytics Platform

> **A production-style retail data engineering pipeline built with PySpark, MySQL, SQL and Tableau to transform raw Sephora India transaction data into analytics-ready business insights.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-4.2.0-orange?logo=apachespark)](https://spark.apache.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)](https://www.mysql.com/)
[![Tableau](https://img.shields.io/badge/Tableau-Public-blue?logo=tableau)](https://public.tableau.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]()

---

## 🚀 Project Overview

## 📊 Live Tableau Dashboard

Explore the interactive **Sephora India Retail Analytics Dashboard**:

👉 **[View Live Dashboard on Tableau Public](https://public.tableau.com/app/profile/aarti.rathod2366/viz/Sephora_India_Analytics/Dashboard2?publish=yes)**

The dashboard includes:

- 💰 Revenue & KPI overview
- 📈 Monthly revenue trends
- 🛍️ Category performance
- 🌐 Online vs Physical Store performance
- 🏆 Top-performing products
- 🏬 Store performance
- 👥 Customer & loyalty analysis

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