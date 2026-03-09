# Data Engineering Quality Engineering
## Document 6: Building Complete Test Suites From Scratch
### A Step-by-Step Walkthrough for Teams New to Data Test Automation

**Document Owner:** Chief Data Office — Data Engineering  
**Domain:** Quality Engineering / Data Testing  
**Version:** 1.0  
**Who This Is For:** Engineers who have never built a data test suite before, or teams that have written some tests but want a complete, production-grade framework.  
**Prerequisite:** Documents 1–5 of this series (highly recommended, but this document is designed to stand alone)

---

## A Letter to the Reader

If you have never automated data testing before, the gap between "I know I should test my data" and "I have a working test suite in production" feels enormous. This document closes that gap completely.

By the end of this document you will have built — from scratch, line by line — a complete test suite for a realistic data pipeline. You will understand not just *what* each test does, but *why* it is structured that way, *when* it fires, and *how* to read the results.

No prior testing experience is required. Every concept is explained as if you are encountering it for the first time.

---

## Table of Contents

1. [The Mental Model — What We Are Actually Building](#1-the-mental-model--what-we-are-actually-building)
2. [The Scenario — A Real Pipeline to Test](#2-the-scenario--a-real-pipeline-to-test)
3. [Setting Up the Project From Zero](#3-setting-up-the-project-from-zero)
4. [Layer 1 — Schema Tests (Is the Data Shaped Correctly?)](#4-layer-1--schema-tests-is-the-data-shaped-correctly)
5. [Layer 2 — Row-Level Tests (Is Every Row Valid?)](#5-layer-2--row-level-tests-is-every-row-valid)
6. [Layer 3 — Aggregate Tests (Does the Data Add Up?)](#6-layer-3--aggregate-tests-does-the-data-add-up)
7. [Layer 4 — Referential Integrity Tests (Do Tables Agree?)](#7-layer-4--referential-integrity-tests-do-tables-agree)
8. [Layer 5 — Business Rule Tests (Is the Data Correct?)](#8-layer-5--business-rule-tests-is-the-data-correct)
9. [Layer 6 — Freshness and Volume Tests (Is the Data Current?)](#9-layer-6--freshness-and-volume-tests-is-the-data-current)
10. [Layer 7 — Statistical Tests (Has Something Quietly Changed?)](#10-layer-7--statistical-tests-has-something-quietly-changed)
11. [Assembling the Full Test Suite](#11-assembling-the-full-test-suite)
12. [Test Result Storage and Reporting](#12-test-result-storage-and-reporting)
13. [The Test Config File — Making It Repeatable](#13-the-test-config-file--making-it-repeatable)
14. [Reading Test Output and Debugging Failures](#14-reading-test-output-and-debugging-failures)
15. [Common Mistakes and How to Avoid Them](#15-common-mistakes-and-how-to-avoid-them)
16. [How to Scale From One Table to Fifty](#16-how-to-scale-from-one-table-to-fifty)

---

## 1. The Mental Model — What We Are Actually Building

### 1.1 The Core Idea

A data test suite is nothing more than a collection of questions about your data that should always have the right answer. Each test is one question. The suite is the full set of questions for a table or pipeline.

Here are some examples of questions in plain English:

- "Is the `customer_id` column ever null?" → A **completeness test**
- "Does every `customer_id` exist in the customers table?" → A **referential integrity test**
- "Is every `amount` greater than zero?" → A **validity test**
- "Did we receive data today?" → A **freshness test**
- "Is the total revenue in this table within 5% of yesterday's total?" → A **volume/consistency test**

Each of these questions becomes a Python function that:
1. Queries your data
2. Applies a rule
3. Returns a structured result (pass/fail + details)

### 1.2 What Makes a Test Suite Different From a Script

A one-off script checks something once. A **test suite**:

| Feature | One-Off Script | Test Suite |
|---|---|---|
| Runs automatically on every pipeline execution | ❌ | ✅ |
| Results are stored for trending over time | ❌ | ✅ |
| Failures block downstream processing | ❌ | ✅ |
| Alerts the right people on failure | ❌ | ✅ |
| Tests are version-controlled and reviewed | ❌ | ✅ |
| Anyone can add a test without touching pipeline code | ❌ | ✅ |
| Produces a pass/fail report for governance | ❌ | ✅ |

### 1.3 The Three Questions Every Test Must Answer

Before writing any test, answer these three questions:

1. **What rule am I checking?** (Be specific: "order_amount must be > 0", not "check amounts")
2. **What does a failure mean for the business?** (This determines severity)
3. **What should happen when it fails?** (Block pipeline? Alert? Log and continue?)

If you cannot answer all three, the test is not ready to be written.

---

## 2. The Scenario — A Real Pipeline to Test

### 2.1 Our Pipeline

We will build tests for an **orders pipeline** that processes e-commerce order data through the Medallion Architecture. The pipeline looks like this:

```
Source System (PostgreSQL)
    │  orders table: raw transactional data
    │
    ▼  (Ingestion — runs hourly)
Bronze Layer: raw_orders
    │  Exact copy of source. No transformations. Append-only.
    │
    ▼  (Transformation — dbt Silver model)
Silver Layer: stg_orders
    │  Cleansed, deduplicated, typed. One row per order.
    │
    ▼  (Transformation — dbt Gold model)
Gold Layer: fact_orders
    │  Business-ready. Currency converted. Status normalized.
    │
    ▼  (Aggregation — dbt Gold model)
Gold Layer: agg_daily_revenue
    │  One row per day. Total revenue, order count, avg order value.
    │
    ▼  (Consumed by BI dashboards and ML features)
```

### 2.2 The Table Schemas

```python
# This is the data our tests will run against.
# In production these would be Snowflake / Databricks Delta tables.
# For local testing we use pandas DataFrames.

# BRONZE: raw_orders
# Columns: order_id, customer_id, product_id, amount, currency,
#          status, created_at, updated_at, _ingested_at, _source

# SILVER: stg_orders
# Columns: order_id, customer_id, product_id, amount_usd, currency,
#          status, created_at, updated_at, _dbt_updated_at

# GOLD: fact_orders
# Columns: order_id, customer_id, product_id, amount_usd, status_normalized,
#          order_date, fiscal_quarter, _created_at

# GOLD: agg_daily_revenue
# Columns: order_date, total_revenue_usd, order_count, avg_order_value_usd,
#          _computed_at
```

### 2.3 What Can Go Wrong?

Before writing a single test, list every way this pipeline could silently produce wrong data:

| Failure Mode | Layer | Impact |
|---|---|---|
| Source system sends duplicate `order_id`s | Bronze | Double-counted revenue in Gold |
| `amount` is null for some orders | Bronze/Silver | Revenue understated |
| `currency` is an unknown code (e.g. 'XXX') | Bronze | FX conversion fails silently |
| Status codes change in source (e.g. 'COMPLETED' becomes 'complete') | Silver | Aggregations break |
| `created_at` is in the future | Silver | Orders appear in wrong period |
| Referential integrity: `customer_id` not in customers table | Gold | Orphaned orders |
| Daily revenue drops 80% with no business explanation | Gold agg | Silent pipeline failure |
| No data loaded today | Any | Stale dashboards |

**Each row in this table should become at least one test.** This is how you build a test plan before writing code.

---

## 3. Setting Up the Project From Zero

### 3.1 Directory Structure

```
data_quality/
├── config/
│   ├── bronze/
│   │   └── raw_orders.yaml          ← Test definitions for raw_orders
│   ├── silver/
│   │   └── stg_orders.yaml          ← Test definitions for stg_orders
│   └── gold/
│       ├── fact_orders.yaml          ← Test definitions for fact_orders
│       └── agg_daily_revenue.yaml
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   ← Shared fixtures (sample DataFrames)
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_schema.py            ← Layer 1: Schema tests
│   │   ├── test_row_level.py         ← Layer 2: Row-level tests
│   │   └── test_aggregates.py        ← Layer 3: Aggregate tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_referential.py       ← Layer 4: Referential integrity
│   │   └── test_business_rules.py    ← Layer 5: Business rules
│   └── monitoring/
│       ├── __init__.py
│       ├── test_freshness.py         ← Layer 6: Freshness & volume
│       └── test_statistical.py       ← Layer 7: Statistical tests
│
├── framework/
│   ├── __init__.py
│   ├── result.py                     ← TestResult class
│   ├── validators.py                 ← All validator functions
│   ├── runner.py                     ← Suite runner
│   ├── reporter.py                   ← Result storage & reporting
│   └── loader.py                     ← Config loader
│
├── requirements.txt
├── pytest.ini
└── README.md
```

### 3.2 Install Dependencies

```bash
# requirements.txt — exact versions for reproducibility
pandas==2.1.4
pytest==7.4.4
pytest-cov==4.1.0
pyyaml==6.0.1
sqlalchemy==2.0.23
snowflake-sqlalchemy==1.5.1       # If using Snowflake
databricks-connect==13.3.2        # If using Databricks
scipy==1.11.4                     # Statistical tests
great-expectations==0.18.8        # Optional: GX integration
dbt-core==1.7.3                   # If using dbt
```

```bash
# Install
pip install -r requirements.txt

# Verify pytest works
pytest --version
# pytest 7.4.4
```

### 3.3 Build the Core Framework First

Before writing a single test, build the reusable framework components. Every test in the suite will use these. Building them first means every test is consistent.

```python
# framework/result.py
"""
The TestResult class.

WHAT IT IS:
    A standardized container for the outcome of any data test.
    Every test function in the suite returns exactly one TestResult.

WHY IT MATTERS:
    If every test returns the same shape, the runner can process
    any test the same way — store it, alert on it, report on it.
    This is what makes the suite composable.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TestResult:
    """Standardized result for any data quality test."""

    # ── Identity ───────────────────────────────────────────────────
    test_name: str
    """A unique, human-readable name. E.g. 'raw_orders.order_id.not_null'"""

    table: str
    """The fully-qualified table name. E.g. 'bronze.raw_orders'"""

    column: str | None
    """The column being tested. None for table-level tests."""

    # ── Result ─────────────────────────────────────────────────────
    passed: bool
    """True = test passed (data is good). False = test failed (data has issues)."""

    severity: str
    """
    What to do when this test fails:
      CRITICAL — block the pipeline, page on-call, do not proceed
      HIGH     — alert the team, log the failure, block downstream T1 consumers
      MEDIUM   — alert the team, log the failure, continue pipeline
      LOW      — log the failure, include in daily report only
    """

    # ── Details ────────────────────────────────────────────────────
    failing_count: int = 0
    """How many rows / records failed the test. 0 = all passed."""

    total_count: int = 0
    """Total rows evaluated. Used to compute failure percentage."""

    failing_pct: float = 0.0
    """Percentage of rows that failed. Computed automatically."""

    sample_failing_values: list[Any] = field(default_factory=list)
    """Up to 5 example values that failed, for debugging."""

    message: str = ""
    """Human-readable summary. Auto-generated if not provided."""

    details: dict = field(default_factory=dict)
    """Extra context: thresholds, comparison values, etc."""

    # ── Metadata ───────────────────────────────────────────────────
    run_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    """ISO timestamp of when this test ran."""

    pipeline_run_id: str = ""
    """The pipeline execution ID this test belongs to."""

    environment: str = "dev"
    """dev | staging | prod"""

    def __post_init__(self):
        """Auto-compute failure percentage and message after creation."""
        if self.total_count > 0:
            self.failing_pct = round(self.failing_count / self.total_count * 100, 4)

        if not self.message:
            if self.passed:
                self.message = f"PASS: {self.test_name} ({self.total_count:,} rows checked)"
            else:
                self.message = (
                    f"FAIL: {self.test_name} — "
                    f"{self.failing_count:,} of {self.total_count:,} rows failed "
                    f"({self.failing_pct:.2f}%)"
                )

    def to_dict(self) -> dict:
        """Convert to flat dict for storage in a database or CSV."""
        return {
            "test_name":             self.test_name,
            "table":                 self.table,
            "column":                self.column or "",
            "passed":                self.passed,
            "severity":              self.severity,
            "failing_count":         self.failing_count,
            "total_count":           self.total_count,
            "failing_pct":           self.failing_pct,
            "message":               self.message,
            "run_at":                self.run_at,
            "pipeline_run_id":       self.pipeline_run_id,
            "environment":           self.environment,
        }
```

---

## 4. Layer 1 — Schema Tests (Is the Data Shaped Correctly?)

### 4.1 What Schema Tests Check

Before testing any values, check that the data *structure* is correct. Schema tests answer:
- "Does this column exist?"
- "Is this column the right data type?"
- "Are all expected columns present?"
- "Are there unexpected extra columns that shouldn't be here?"

Schema tests are the fastest and cheapest tests — they don't scan rows, they check metadata. **Always run these first.**

### 4.2 Why This Matters

A source system can silently rename a column (`customer_id` → `cust_id`) or change a type (`amount` from `FLOAT` to `STRING`). Without schema tests, this causes silent failures — NULL values, wrong aggregations, or type errors — that can take hours to diagnose.

### 4.3 Building the Schema Validator

```python
# framework/validators.py  — Part 1: Schema Validators
"""
This file contains all validator functions used in the test suite.

HOW VALIDATORS WORK:
    Each function takes a DataFrame (or connection + table name for SQL-based tests),
    applies one specific rule, and returns exactly one TestResult.

    Think of each function as a question:
        test_schema_has_column()  →  "Does this column exist?"
        test_schema_column_type() →  "Is this column the right type?"

NAMING CONVENTION:
    test_{category}_{what_it_checks}
    
    Category options: schema, completeness, uniqueness, validity,
                      consistency, referential, freshness, volume, statistical
"""

import pandas as pd
import numpy as np
from typing import Any
from .result import TestResult


# ─────────────────────────────────────────────────────────────────────────────
# SCHEMA VALIDATORS
# ─────────────────────────────────────────────────────────────────────────────

def test_schema_has_column(
    df: pd.DataFrame,
    column: str,
    table: str,
    severity: str = "CRITICAL"
) -> TestResult:
    """
    Check that a required column exists in the DataFrame.

    WHY CRITICAL BY DEFAULT:
        If a required column is missing, all downstream tests for that column
        will error out with KeyError. Running this test first prevents cascading
        errors and gives a clear root cause.

    USAGE:
        result = test_schema_has_column(df, "order_id", "bronze.raw_orders")
        # result.passed = True if "order_id" exists in df.columns
    """
    exists = column in df.columns

    return TestResult(
        test_name=f"{table}.{column}.has_column",
        table=table,
        column=column,
        passed=exists,
        severity=severity,
        total_count=1,
        failing_count=0 if exists else 1,
        message=(
            f"PASS: Column '{column}' exists in {table}"
            if exists
            else f"FAIL: Column '{column}' is MISSING from {table}. "
                 f"Found columns: {sorted(df.columns.tolist())}"
        )
    )


def test_schema_all_columns_present(
    df: pd.DataFrame,
    expected_columns: list[str],
    table: str,
    severity: str = "CRITICAL"
) -> TestResult:
    """
    Check that ALL expected columns are present.

    This is the 'full schema check' — run once for each table to
    confirm the complete contract is met.

    USAGE:
        result = test_schema_all_columns_present(
            df,
            expected_columns=["order_id", "customer_id", "amount", "status"],
            table="bronze.raw_orders"
        )
    """
    present = set(df.columns)
    expected = set(expected_columns)
    missing = sorted(expected - present)
    unexpected = sorted(present - expected)  # Extra columns (informational)

    passed = len(missing) == 0

    return TestResult(
        test_name=f"{table}.schema.all_columns_present",
        table=table,
        column=None,
        passed=passed,
        severity=severity,
        total_count=len(expected_columns),
        failing_count=len(missing),
        message=(
            f"PASS: All {len(expected_columns)} expected columns present in {table}"
            if passed
            else f"FAIL: {len(missing)} columns missing from {table}: {missing}"
        ),
        details={
            "missing_columns":     missing,
            "unexpected_columns":  unexpected,   # Not a failure, but logged
            "expected_count":      len(expected_columns),
            "actual_count":        len(df.columns)
        }
    )


def test_schema_column_type(
    df: pd.DataFrame,
    column: str,
    expected_dtype: str,
    table: str,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that a column has the expected pandas dtype.

    IMPORTANT — dtype mapping:
        "string" or "object"  → pd.api.types.is_string_dtype()
        "integer"             → pd.api.types.is_integer_dtype()
        "float"               → pd.api.types.is_float_dtype()
        "numeric"             → is_integer or is_float (either is fine)
        "datetime"            → pd.api.types.is_datetime64_any_dtype()
        "boolean"             → pd.api.types.is_bool_dtype()

    USAGE:
        result = test_schema_column_type(df, "amount", "float", "bronze.raw_orders")
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.dtype",
            table=table, column=column,
            passed=False, severity=severity,
            total_count=1, failing_count=1,
            message=f"FAIL: Cannot check dtype — column '{column}' not found in {table}"
        )

    actual_dtype = str(df[column].dtype)

    # Flexible type checking
    type_checks = {
        "string":   pd.api.types.is_string_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]),
        "object":   pd.api.types.is_object_dtype(df[column]),
        "integer":  pd.api.types.is_integer_dtype(df[column]),
        "float":    pd.api.types.is_float_dtype(df[column]),
        "numeric":  pd.api.types.is_numeric_dtype(df[column]),
        "datetime": pd.api.types.is_datetime64_any_dtype(df[column]),
        "boolean":  pd.api.types.is_bool_dtype(df[column]),
    }

    passed = type_checks.get(expected_dtype.lower(), actual_dtype == expected_dtype)

    return TestResult(
        test_name=f"{table}.{column}.dtype",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=1, failing_count=0 if passed else 1,
        message=(
            f"PASS: Column '{column}' has expected dtype '{expected_dtype}' (actual: {actual_dtype})"
            if passed
            else f"FAIL: Column '{column}' dtype mismatch — expected '{expected_dtype}', got '{actual_dtype}'"
        ),
        details={"expected_dtype": expected_dtype, "actual_dtype": actual_dtype}
    )
```

### 4.4 Writing Schema Tests

```python
# tests/unit/test_schema.py
"""
Layer 1: Schema Tests for the orders pipeline.

HOW TO READ THESE TESTS:
    Each test function corresponds to one rule about the table structure.
    The test_* naming prefix is required by pytest — it's how pytest finds tests.

    conftest.py provides shared sample DataFrames so every test
    doesn't have to create its own data.
"""

import pytest
import pandas as pd
from framework.validators import (
    test_schema_has_column,
    test_schema_all_columns_present,
    test_schema_column_type
)


# ── The expected schemas for each table ───────────────────────────────────────
# Defining schemas here as constants means:
# 1. If the schema changes, there's one place to update
# 2. It documents the contract in plain Python

BRONZE_RAW_ORDERS_SCHEMA = {
    "order_id":     "string",
    "customer_id":  "string",
    "product_id":   "string",
    "amount":       "numeric",    # Can be int or float
    "currency":     "string",
    "status":       "string",
    "created_at":   "datetime",
    "updated_at":   "datetime",
    "_ingested_at": "datetime",
    "_source":      "string",
}

SILVER_STG_ORDERS_SCHEMA = {
    "order_id":       "string",
    "customer_id":    "string",
    "product_id":     "string",
    "amount_usd":     "float",    # Must be float — FX conversion applied
    "currency":       "string",
    "status":         "string",
    "created_at":     "datetime",
    "updated_at":     "datetime",
    "_dbt_updated_at":"datetime",
}


class TestBronzeRawOrdersSchema:
    """Schema tests for bronze.raw_orders."""

    @pytest.fixture
    def sample_df(self):
        """Minimal valid sample of raw_orders for schema tests."""
        return pd.DataFrame({
            "order_id":     ["ORD-001", "ORD-002"],
            "customer_id":  ["CUST-A", "CUST-B"],
            "product_id":   ["PROD-1", "PROD-2"],
            "amount":       [99.99, 149.00],
            "currency":     ["USD", "EUR"],
            "status":       ["pending", "completed"],
            "created_at":   pd.to_datetime(["2024-01-15", "2024-01-16"]),
            "updated_at":   pd.to_datetime(["2024-01-15", "2024-01-16"]),
            "_ingested_at": pd.to_datetime(["2024-01-15 08:00", "2024-01-15 08:00"]),
            "_source":      ["orders_api", "orders_api"],
        })

    def test_all_expected_columns_present(self, sample_df):
        """
        TEST INTENT: The complete schema contract is met.
        FAILURE MEANING: A source system change or ingestion bug dropped a column.
        SEVERITY: CRITICAL — schema gaps cause all downstream tests to fail.
        """
        result = test_schema_all_columns_present(
            df=sample_df,
            expected_columns=list(BRONZE_RAW_ORDERS_SCHEMA.keys()),
            table="bronze.raw_orders",
            severity="CRITICAL"
        )
        assert result.passed, result.message

    def test_amount_is_numeric(self, sample_df):
        """
        TEST INTENT: The amount column holds numbers, not strings.
        FAILURE MEANING: Source system changed type. SUM(amount) will error.
        SEVERITY: HIGH — revenue calculations break if amount is a string.
        """
        result = test_schema_column_type(
            df=sample_df,
            column="amount",
            expected_dtype="numeric",
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_created_at_is_datetime(self, sample_df):
        """
        TEST INTENT: created_at holds timestamps, not strings.
        FAILURE MEANING: Date filtering and partitioning will break.
        SEVERITY: HIGH — all time-based queries depend on this.
        """
        result = test_schema_column_type(
            df=sample_df,
            column="created_at",
            expected_dtype="datetime",
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_schema_rejects_missing_column(self):
        """
        META-TEST: Verify the validator correctly detects a missing column.

        WHY THIS EXISTS:
            We test the test itself. This ensures our validator doesn't
            silently pass when it should fail — a false pass is worse
            than a false failure.
        """
        df_missing_column = pd.DataFrame({
            "order_id":   ["ORD-001"],
            "customer_id":["CUST-A"],
            # "amount" is intentionally absent
        })
        result = test_schema_has_column(
            df=df_missing_column,
            column="amount",
            table="bronze.raw_orders",
            severity="CRITICAL"
        )
        # This SHOULD fail — the validator is working correctly when passed=False
        assert not result.passed, "Validator should detect missing column but passed!"
        assert "amount" in result.message
```

---

## 5. Layer 2 — Row-Level Tests (Is Every Row Valid?)

### 5.1 What Row-Level Tests Check

Row-level tests examine each individual record. They answer questions like:
- "Is any value in this column null when it shouldn't be?"
- "Is any value outside the allowed range?"
- "Does any value match a forbidden pattern?"

Row-level tests are the workhorse of data quality — most of your tests will be at this level.

### 5.2 The Complete Row-Level Validator Library

```python
# framework/validators.py — Part 2: Row-Level Validators
# (continuing from Part 1)

# ─────────────────────────────────────────────────────────────────────────────
# COMPLETENESS VALIDATORS
# "Is anything missing that shouldn't be?"
# ─────────────────────────────────────────────────────────────────────────────

def test_completeness_not_null(
    df: pd.DataFrame,
    column: str,
    table: str,
    severity: str = "HIGH",
    max_null_pct: float = 0.0      # Default: zero nulls allowed
) -> TestResult:
    """
    Check that a column has no null (missing) values, or fewer than a threshold.

    THE max_null_pct PARAMETER EXPLAINED:
        Sometimes a small number of nulls is acceptable. For example:
        - A phone number column might be nullable (max_null_pct=100)
        - A loyalty_points column might be NULL for non-loyalty customers (max_null_pct=30)
        - An order_id column must never be null (max_null_pct=0)

        Set max_null_pct to match your business rule.
        The test FAILS if the actual null % EXCEEDS max_null_pct.

    USAGE:
        # Strict: zero nulls allowed
        test_completeness_not_null(df, "order_id", "bronze.raw_orders")

        # Tolerant: up to 5% nulls acceptable
        test_completeness_not_null(df, "phone", "gold.customers", max_null_pct=5.0)
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.not_null",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found — cannot test completeness"
        )

    null_mask = df[column].isna()
    null_count = int(null_mask.sum())
    total = len(df)
    null_pct = (null_count / total * 100) if total > 0 else 0.0

    # Get sample of rows with nulls for debugging
    sample_rows = df[null_mask].head(5).index.tolist()

    passed = null_pct <= max_null_pct

    return TestResult(
        test_name=f"{table}.{column}.not_null",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=total,
        failing_count=null_count,
        failing_pct=round(null_pct, 4),
        sample_failing_values=sample_rows,
        message=(
            f"PASS: '{column}' has {null_count} nulls ({null_pct:.2f}%) — within {max_null_pct}% threshold"
            if passed
            else
            f"FAIL: '{column}' has {null_count} nulls ({null_pct:.2f}%) — exceeds {max_null_pct}% threshold"
        ),
        details={"max_null_pct": max_null_pct, "actual_null_pct": round(null_pct, 4)}
    )


# ─────────────────────────────────────────────────────────────────────────────
# UNIQUENESS VALIDATORS
# "Is anything duplicated that shouldn't be?"
# ─────────────────────────────────────────────────────────────────────────────

def test_uniqueness_no_duplicates(
    df: pd.DataFrame,
    columns: list[str],
    table: str,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that a column or combination of columns has no duplicate values.

    SINGLE COLUMN vs COMPOSITE KEY:
        - Single column: test_uniqueness_no_duplicates(df, ["order_id"], ...)
          → Each order_id must be unique

        - Composite key: test_uniqueness_no_duplicates(df, ["order_id", "line_item_id"], ...)
          → The COMBINATION of order_id + line_item_id must be unique.
            order_id=1, line_item_id=1 is fine alongside order_id=1, line_item_id=2.
            But order_id=1, line_item_id=1 appearing TWICE is a duplicate.

    USAGE:
        # Check order_id is unique
        test_uniqueness_no_duplicates(df, ["order_id"], "bronze.raw_orders")

        # Check composite key
        test_uniqueness_no_duplicates(df, ["order_id", "line_item_id"], "bronze.raw_order_items")
    """
    # Validate all columns exist
    missing = [c for c in columns if c not in df.columns]
    if missing:
        return TestResult(
            test_name=f"{table}.{'_'.join(columns)}.unique",
            table=table, column=str(columns),
            passed=False, severity=severity,
            message=f"FAIL: Columns {missing} not found — cannot test uniqueness"
        )

    total = len(df)
    if total == 0:
        return TestResult(
            test_name=f"{table}.{'_'.join(columns)}.unique",
            table=table, column=str(columns),
            passed=True, severity=severity,
            total_count=0, failing_count=0,
            message=f"PASS: Empty DataFrame — no duplicates possible"
        )

    dup_mask = df.duplicated(subset=columns, keep=False)
    dup_count = int(dup_mask.sum())

    # Sample the duplicate values for debugging
    sample_dups = df[dup_mask][columns].head(5).to_dict(orient="records")

    passed = dup_count == 0

    return TestResult(
        test_name=f"{table}.{'__'.join(columns)}.unique",
        table=table, column=str(columns),
        passed=passed, severity=severity,
        total_count=total,
        failing_count=dup_count,
        sample_failing_values=sample_dups,
        message=(
            f"PASS: {'+'.join(columns)} is unique across all {total:,} rows"
            if passed
            else
            f"FAIL: {dup_count:,} duplicate rows found on {'+'.join(columns)} in {table}"
        )
    )


# ─────────────────────────────────────────────────────────────────────────────
# VALIDITY VALIDATORS
# "Are the values within the allowed set or range?"
# ─────────────────────────────────────────────────────────────────────────────

def test_validity_in_set(
    df: pd.DataFrame,
    column: str,
    allowed_values: list,
    table: str,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that all values in a column belong to an allowed set.

    USE FOR:
        - Status codes: ["pending", "processing", "shipped", "completed", "cancelled"]
        - Currency codes: ["USD", "EUR", "GBP", "CAD"]
        - Country codes: ["US", "UK", "CA", "AU"]
        - Category enums: ["standard", "premium", "enterprise"]

    WHY THIS MATTERS:
        A source system might add a new status ("partially_shipped") without
        telling the data team. Without this test, the new status silently
        passes through and breaks downstream aggregations that expected
        a fixed set of statuses.
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.in_set",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    non_null_series = df[column].dropna()
    invalid_mask = ~non_null_series.isin(allowed_values)
    invalid_count = int(invalid_mask.sum())
    invalid_values = sorted(non_null_series[invalid_mask].unique().tolist())

    passed = invalid_count == 0

    return TestResult(
        test_name=f"{table}.{column}.in_set",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=invalid_count,
        sample_failing_values=invalid_values[:5],
        message=(
            f"PASS: All values in '{column}' are in the allowed set"
            if passed
            else
            f"FAIL: {invalid_count:,} rows in '{column}' have invalid values: {invalid_values[:10]}"
        ),
        details={"allowed_values": allowed_values, "invalid_values_found": invalid_values}
    )


def test_validity_range(
    df: pd.DataFrame,
    column: str,
    table: str,
    min_value: float | None = None,
    max_value: float | None = None,
    inclusive: bool = True,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that numeric values fall within an allowed range.

    PARAMETERS:
        min_value: Values below this are invalid. None = no minimum.
        max_value: Values above this are invalid. None = no maximum.
        inclusive: If True, min_value and max_value themselves are valid.

    EXAMPLES:
        # Amount must be positive (> 0)
        test_validity_range(df, "amount", "orders", min_value=0.01)

        # Discount must be between 0% and 100%
        test_validity_range(df, "discount_pct", "orders", min_value=0, max_value=100)

        # Rating must be 1–5
        test_validity_range(df, "rating", "reviews", min_value=1, max_value=5)
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.range",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    series = df[column].dropna()
    invalid_mask = pd.Series([False] * len(series), index=series.index)

    if min_value is not None:
        below = series < min_value if inclusive else series <= min_value
        invalid_mask = invalid_mask | below

    if max_value is not None:
        above = series > max_value if inclusive else series >= max_value
        invalid_mask = invalid_mask | above

    invalid_count = int(invalid_mask.sum())
    sample_vals = series[invalid_mask].head(5).tolist()
    passed = invalid_count == 0

    range_desc = f"[{min_value or '-∞'}, {max_value or '+∞'}]"

    return TestResult(
        test_name=f"{table}.{column}.range",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=invalid_count,
        sample_failing_values=sample_vals,
        message=(
            f"PASS: All values in '{column}' are within range {range_desc}"
            if passed
            else
            f"FAIL: {invalid_count:,} values in '{column}' are outside range {range_desc}. "
            f"Sample: {sample_vals}"
        ),
        details={"min_value": min_value, "max_value": max_value, "range": range_desc}
    )


def test_validity_regex(
    df: pd.DataFrame,
    column: str,
    pattern: str,
    table: str,
    pattern_description: str = "",
    severity: str = "MEDIUM"
) -> TestResult:
    """
    Check that string values match a regular expression pattern.

    USE FOR:
        - Email format: r'^[^@]+@[^@]+\.[^@]+$'
        - UUID: r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        - Phone: r'^\+?[0-9]{10,15}$'
        - Order ID format: r'^ORD-[0-9]{6}$'
        - ISO date: r'^\d{4}-\d{2}-\d{2}$'

    REGEX EXPLAINED FOR NON-REGEX USERS:
        ^ = start of string
        $ = end of string
        [A-Z] = any uppercase letter
        [0-9] = any digit
        {3} = exactly 3 of the preceding
        + = one or more of the preceding
        * = zero or more of the preceding
        ? = zero or one of the preceding
        \d = any digit (same as [0-9])
        \w = any word character (letter, digit, underscore)
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.regex",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    non_null = df[column].dropna().astype(str)
    invalid_mask = ~non_null.str.match(pattern, na=False)
    invalid_count = int(invalid_mask.sum())
    sample_vals = non_null[invalid_mask].head(5).tolist()
    passed = invalid_count == 0
    desc = pattern_description or pattern

    return TestResult(
        test_name=f"{table}.{column}.regex",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=invalid_count,
        sample_failing_values=sample_vals,
        message=(
            f"PASS: All values in '{column}' match pattern '{desc}'"
            if passed
            else
            f"FAIL: {invalid_count:,} values in '{column}' don't match pattern '{desc}'. "
            f"Sample invalid: {sample_vals}"
        ),
        details={"pattern": pattern, "description": desc}
    )
```

### 5.3 Writing Row-Level Tests

```python
# tests/unit/test_row_level.py
"""
Layer 2: Row-level tests for the orders pipeline.

READING GUIDE:
    - Tests are grouped by table, then by rule category.
    - Each test has a docstring explaining:
        1. What rule it enforces
        2. What a failure means for the business
    - Both PASS and FAIL scenarios are tested to confirm the validator works.
"""

import pytest
import pandas as pd
from framework.validators import (
    test_completeness_not_null,
    test_uniqueness_no_duplicates,
    test_validity_in_set,
    test_validity_range,
    test_validity_regex,
)

# ─────────────────────────────────────────────────────────────────────────────
# SHARED TEST FIXTURES
# A fixture is reusable test data. Define once, use in many tests.
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_orders_df():
    """
    A clean, valid sample of order data.
    Every test that expects PASS uses this fixture.
    It represents what correct data looks like.
    """
    return pd.DataFrame({
        "order_id":     ["ORD-000001", "ORD-000002", "ORD-000003"],
        "customer_id":  ["CUST-A001", "CUST-B002", "CUST-C003"],
        "product_id":   ["PROD-001", "PROD-002", "PROD-001"],
        "amount":       [99.99, 149.00, 29.95],
        "currency":     ["USD", "EUR", "USD"],
        "status":       ["completed", "pending", "shipped"],
        "created_at":   pd.to_datetime(["2024-01-15", "2024-01-15", "2024-01-16"]),
    })


@pytest.fixture
def orders_with_null_amounts():
    """Orders with NULL amounts — for testing completeness failures."""
    return pd.DataFrame({
        "order_id":  ["ORD-000001", "ORD-000002", "ORD-000003"],
        "amount":    [99.99, None, None],   # 2 of 3 are null
        "status":    ["completed", "pending", "shipped"],
    })


@pytest.fixture
def orders_with_duplicates():
    """Orders with duplicate order_ids — for testing uniqueness failures."""
    return pd.DataFrame({
        "order_id":  ["ORD-000001", "ORD-000001", "ORD-000003"],  # ORD-000001 appears twice
        "amount":    [99.99, 99.99, 29.95],
        "status":    ["completed", "completed", "shipped"],
    })


# ─────────────────────────────────────────────────────────────────────────────
# COMPLETENESS TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestBronzeOrdersCompleteness:

    def test_order_id_never_null(self, valid_orders_df):
        """
        RULE: order_id must never be null.
        BUSINESS IMPACT: A null order_id means we cannot identify or track the order.
                         Revenue could be double-counted or lost entirely.
        SEVERITY: CRITICAL — we cannot process an order without an ID.
        """
        result = test_completeness_not_null(
            df=valid_orders_df,
            column="order_id",
            table="bronze.raw_orders",
            severity="CRITICAL",
            max_null_pct=0.0
        )
        assert result.passed, result.message

    def test_customer_id_never_null(self, valid_orders_df):
        """
        RULE: customer_id must never be null.
        BUSINESS IMPACT: Cannot attribute the order to a customer.
                         CRM, support, and churn models all break.
        SEVERITY: CRITICAL.
        """
        result = test_completeness_not_null(
            df=valid_orders_df,
            column="customer_id",
            table="bronze.raw_orders",
            severity="CRITICAL"
        )
        assert result.passed, result.message

    def test_amount_never_null(self, valid_orders_df):
        """
        RULE: amount must never be null.
        BUSINESS IMPACT: Null amounts cause revenue to be understated.
                         Finance reports will be wrong.
        SEVERITY: HIGH (not CRITICAL because we might be able to recover from source).
        """
        result = test_completeness_not_null(
            df=valid_orders_df,
            column="amount",
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    # ── NEGATIVE TEST: Verify the validator actually catches nulls ─────────────

    def test_null_detection_works_correctly(self, orders_with_null_amounts):
        """
        META-TEST: Confirm the null detector catches real nulls.

        WHY THIS MATTERS:
            A silent bug in the validator could cause it to always return PASS,
            even when nulls are present. This test ensures our validator actually
            works by intentionally running it against data we KNOW has nulls,
            and asserting it FAILS.

            A validator that always passes is worse than no validator.
        """
        result = test_completeness_not_null(
            df=orders_with_null_amounts,
            column="amount",
            table="bronze.raw_orders",
            severity="HIGH"
        )
        # This SHOULD fail — data has 2 nulls
        assert not result.passed, "Validator should have caught nulls but returned PASS!"
        assert result.failing_count == 2, f"Expected 2 failures, got {result.failing_count}"
        assert abs(result.failing_pct - 66.67) < 0.01, f"Expected ~66.67% failure rate"


# ─────────────────────────────────────────────────────────────────────────────
# UNIQUENESS TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestBronzeOrdersUniqueness:

    def test_order_id_is_unique(self, valid_orders_df):
        """
        RULE: order_id must be unique within a load batch.
        BUSINESS IMPACT: Duplicates cause double-counted revenue, duplicate
                         shipments, and incorrect order counts.
        SEVERITY: CRITICAL for billing/revenue models; HIGH for operational.
        """
        result = test_uniqueness_no_duplicates(
            df=valid_orders_df,
            columns=["order_id"],
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_duplicate_detection_works_correctly(self, orders_with_duplicates):
        """
        META-TEST: Confirm the duplicate detector catches real duplicates.
        """
        result = test_uniqueness_no_duplicates(
            df=orders_with_duplicates,
            columns=["order_id"],
            table="bronze.raw_orders",
            severity="HIGH"
        )
        # Should FAIL — ORD-000001 appears twice
        assert not result.passed, "Validator missed duplicates!"
        assert result.failing_count == 2  # Both instances of the duplicate are flagged


# ─────────────────────────────────────────────────────────────────────────────
# VALIDITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestBronzeOrdersValidity:

    ALLOWED_STATUSES = ["pending", "processing", "shipped", "completed", "cancelled"]
    ALLOWED_CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]

    def test_status_in_allowed_set(self, valid_orders_df):
        """
        RULE: status must be one of the known valid values.
        BUSINESS IMPACT: New status values from source system break
                         aggregations, BI dashboards, and ML features
                         that expect a fixed set of statuses.
        """
        result = test_validity_in_set(
            df=valid_orders_df,
            column="status",
            allowed_values=self.ALLOWED_STATUSES,
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_currency_in_allowed_set(self, valid_orders_df):
        """
        RULE: currency must be a known ISO currency code.
        BUSINESS IMPACT: Unknown currency codes cause FX conversion to fail.
                         Revenue in reporting may be wrong or NULL.
        """
        result = test_validity_in_set(
            df=valid_orders_df,
            column="currency",
            allowed_values=self.ALLOWED_CURRENCIES,
            table="bronze.raw_orders",
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_amount_is_positive(self, valid_orders_df):
        """
        RULE: amount must be > 0.
        BUSINESS IMPACT: Zero or negative amounts distort revenue metrics
                         and can indicate data corruption or billing errors.
        NOTE: Refunds/credits are handled in a separate returns table,
              not as negative amounts in the orders table.
        """
        result = test_validity_range(
            df=valid_orders_df,
            column="amount",
            table="bronze.raw_orders",
            min_value=0.01,
            severity="HIGH"
        )
        assert result.passed, result.message

    def test_order_id_format(self, valid_orders_df):
        """
        RULE: order_id must match the format 'ORD-' followed by 6 digits.
        BUSINESS IMPACT: Malformed IDs cannot be used for lookups in the
                         source system or for joining with other tables.
        """
        result = test_validity_regex(
            df=valid_orders_df,
            column="order_id",
            pattern=r'^ORD-\d{6}$',
            table="bronze.raw_orders",
            pattern_description="ORD-######",
            severity="MEDIUM"
        )
        assert result.passed, result.message
```

---

## 6. Layer 3 — Aggregate Tests (Does the Data Add Up?)

### 6.1 What Aggregate Tests Check

While row-level tests check individual records, aggregate tests check the dataset as a whole. They answer:
- "Does the total row count make sense?"
- "Is the sum of revenue within expected range?"
- "Do we have at least N records?"

```python
# framework/validators.py — Part 3: Aggregate Validators

def test_aggregate_row_count(
    df: pd.DataFrame,
    table: str,
    min_rows: int | None = None,
    max_rows: int | None = None,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that a DataFrame has an expected number of rows.

    USE FOR:
        - Ensuring a minimum number of records loaded (data didn't vanish)
        - Ensuring a maximum isn't exceeded (no runaway duplication)
        - Combined: "We should load between 10,000 and 200,000 orders per day"

    USAGE:
        # At least 1,000 rows (catch empty loads)
        test_aggregate_row_count(df, "bronze.raw_orders", min_rows=1000)

        # Between 5,000 and 100,000 rows (daily batch bounds)
        test_aggregate_row_count(df, "bronze.raw_orders", min_rows=5000, max_rows=100000)
    """
    actual_rows = len(df)
    failures = []

    if min_rows is not None and actual_rows < min_rows:
        failures.append(f"row_count {actual_rows:,} < min {min_rows:,}")

    if max_rows is not None and actual_rows > max_rows:
        failures.append(f"row_count {actual_rows:,} > max {max_rows:,}")

    passed = len(failures) == 0

    return TestResult(
        test_name=f"{table}.row_count",
        table=table, column=None,
        passed=passed, severity=severity,
        total_count=actual_rows,
        failing_count=0 if passed else 1,
        message=(
            f"PASS: Row count {actual_rows:,} is within expected range "
            f"[{min_rows or 0}, {max_rows or '∞'}]"
            if passed
            else
            f"FAIL: Row count {actual_rows:,} out of range: {'; '.join(failures)}"
        ),
        details={"actual_rows": actual_rows, "min_rows": min_rows, "max_rows": max_rows}
    )


def test_aggregate_sum(
    df: pd.DataFrame,
    column: str,
    table: str,
    min_sum: float | None = None,
    max_sum: float | None = None,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that the sum of a numeric column falls within an expected range.

    USE FOR:
        - Revenue: total daily revenue should be > $0 and < some ceiling
        - Units: total units shipped should be > 0
        - Credits: total credits should not exceed some known threshold

    IMPORTANT — Setting thresholds:
        Don't guess. Look at your historical data to understand the typical range.
        A good starting point: use mean ± 3 standard deviations from your
        historical daily values as your min/max.
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.sum",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    actual_sum = float(df[column].sum())
    failures = []

    if min_sum is not None and actual_sum < min_sum:
        failures.append(f"sum {actual_sum:,.2f} < min {min_sum:,.2f}")

    if max_sum is not None and actual_sum > max_sum:
        failures.append(f"sum {actual_sum:,.2f} > max {max_sum:,.2f}")

    passed = len(failures) == 0

    return TestResult(
        test_name=f"{table}.{column}.sum",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        message=(
            f"PASS: SUM({column}) = {actual_sum:,.2f} — within expected range"
            if passed
            else
            f"FAIL: SUM({column}) = {actual_sum:,.2f} out of range: {'; '.join(failures)}"
        ),
        details={"actual_sum": actual_sum, "min_sum": min_sum, "max_sum": max_sum}
    )
```

---

## 7. Layer 4 — Referential Integrity Tests (Do Tables Agree?)

### 7.1 What Referential Integrity Tests Check

These tests check relationships *between* tables:
- "Does every `customer_id` in orders exist in the customers table?"
- "Does every `product_id` in orders exist in the products table?"
- "Are there any orders in the Gold table that don't exist in Silver?"

These are the tests that catch **join failures** before they happen.

```python
# framework/validators.py — Part 4: Referential Integrity

def test_referential_integrity(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_key: str,
    parent_key: str,
    child_table: str,
    parent_table: str,
    severity: str = "HIGH",
    max_orphan_pct: float = 0.0
) -> TestResult:
    """
    Check that all values in child_key exist in parent_key.

    ANALOGY:
        In a database with a foreign key constraint:
            orders.customer_id → customers.customer_id

        This test enforces that same constraint in your pipeline,
        even if the database doesn't have the constraint enforced.

    USAGE:
        # Every order must have a valid customer
        test_referential_integrity(
            child_df=orders_df,
            parent_df=customers_df,
            child_key="customer_id",
            parent_key="customer_id",
            child_table="gold.fact_orders",
            parent_table="gold.dim_customers"
        )

    THE max_orphan_pct PARAMETER:
        Sometimes a small number of orphans is acceptable — e.g., if customers
        can be deleted (GDPR) but orders must be retained.
        Set max_orphan_pct > 0 to allow for this.
    """
    parent_keys = set(parent_df[parent_key].dropna().unique())
    child_series = child_df[child_key].dropna()

    orphan_mask = ~child_series.isin(parent_keys)
    orphan_count = int(orphan_mask.sum())
    total = len(child_df)
    orphan_pct = (orphan_count / total * 100) if total > 0 else 0.0

    sample_orphans = child_series[orphan_mask].head(5).tolist()
    passed = orphan_pct <= max_orphan_pct

    return TestResult(
        test_name=f"{child_table}.{child_key}.refs.{parent_table}",
        table=child_table, column=child_key,
        passed=passed, severity=severity,
        total_count=total,
        failing_count=orphan_count,
        failing_pct=round(orphan_pct, 4),
        sample_failing_values=sample_orphans,
        message=(
            f"PASS: All {child_key} values in {child_table} exist in {parent_table}"
            if passed
            else
            f"FAIL: {orphan_count:,} orphaned {child_key} values in {child_table} "
            f"not found in {parent_table}. Sample: {sample_orphans}"
        ),
        details={
            "parent_table":    parent_table,
            "orphan_pct":      round(orphan_pct, 4),
            "max_orphan_pct":  max_orphan_pct
        }
    )
```

---

## 8. Layer 5 — Business Rule Tests (Is the Data Correct?)

### 8.1 What Business Rule Tests Check

Business rules are the most domain-specific tests. They encode knowledge about how your business works:
- "If `status` is 'shipped', then `shipped_at` must not be null"
- "If `status` is 'completed', then `amount_usd` must be greater than 0"
- "A 'cancelled' order must not also have a 'shipped_at' timestamp"

```python
# framework/validators.py — Part 5: Business Rule Validators

def test_conditional_rule(
    df: pd.DataFrame,
    table: str,
    condition_col: str,
    condition_values: list,
    required_col: str,
    rule_description: str,
    check_type: str = "not_null",    # "not_null" | "is_null" | "positive" | "zero"
    severity: str = "HIGH"
) -> TestResult:
    """
    Test a conditional business rule: "IF condition THEN required_col must be X"

    EXAMPLES:
        # "If status is 'shipped', then shipped_at must not be null"
        test_conditional_rule(
            df, "orders",
            condition_col="status",
            condition_values=["shipped", "completed"],
            required_col="shipped_at",
            rule_description="shipped orders must have a shipped_at timestamp",
            check_type="not_null"
        )

        # "If status is 'pending', then shipped_at must be null"
        test_conditional_rule(
            df, "orders",
            condition_col="status",
            condition_values=["pending", "processing"],
            required_col="shipped_at",
            rule_description="pending orders must NOT have a shipped_at timestamp",
            check_type="is_null"
        )
    """
    condition_mask = df[condition_col].isin(condition_values)
    subset = df[condition_mask]

    if len(subset) == 0:
        return TestResult(
            test_name=f"{table}.rule.{required_col}_when_{condition_col}",
            table=table, column=required_col,
            passed=True, severity=severity,
            total_count=0, failing_count=0,
            message=f"PASS: No rows matched condition {condition_col} in {condition_values} — rule not applicable"
        )

    if check_type == "not_null":
        violations = subset[subset[required_col].isna()]
    elif check_type == "is_null":
        violations = subset[subset[required_col].notna()]
    elif check_type == "positive":
        violations = subset[subset[required_col] <= 0]
    elif check_type == "zero":
        violations = subset[subset[required_col] != 0]
    else:
        violations = pd.DataFrame()

    violation_count = len(violations)
    passed = violation_count == 0
    sample_indices = violations.index[:5].tolist()

    return TestResult(
        test_name=f"{table}.rule.{required_col}_when_{condition_col}",
        table=table, column=required_col,
        passed=passed, severity=severity,
        total_count=len(subset),
        failing_count=violation_count,
        sample_failing_values=sample_indices,
        message=(
            f"PASS: Business rule satisfied — {rule_description} ({len(subset):,} rows checked)"
            if passed
            else
            f"FAIL: {violation_count:,} violations of rule: {rule_description}"
        ),
        details={
            "rule":             rule_description,
            "condition_col":    condition_col,
            "condition_values": condition_values,
            "required_col":     required_col,
            "check_type":       check_type
        }
    )
```

---

## 9. Layer 6 — Freshness and Volume Tests (Is the Data Current?)

### 9.1 What Freshness Tests Check

These tests ensure your pipeline actually ran and data is up to date:
- "Was data loaded within the last 2 hours?"
- "Is there data for today's date?"
- "Has the row count changed significantly vs. yesterday?"

```python
# framework/validators.py — Part 6: Freshness & Volume

from datetime import datetime, timezone, timedelta

def test_freshness_max_age(
    df: pd.DataFrame,
    timestamp_column: str,
    table: str,
    max_age_hours: float,
    severity: str = "HIGH"
) -> TestResult:
    """
    Check that the most recent record is not older than max_age_hours.

    USE FOR:
        - Detecting pipeline failures (no data loaded today)
        - Detecting upstream source system delays
        - SLA monitoring for time-sensitive tables

    USAGE:
        # Orders should load within 2 hours
        test_freshness_max_age(df, "_ingested_at", "bronze.raw_orders", max_age_hours=2)

        # Daily table: data should exist for today (within 26 hours to allow for timezone variance)
        test_freshness_max_age(df, "order_date", "gold.agg_daily_revenue", max_age_hours=26)
    """
    if timestamp_column not in df.columns:
        return TestResult(
            test_name=f"{table}.freshness",
            table=table, column=timestamp_column,
            passed=False, severity=severity,
            message=f"FAIL: Timestamp column '{timestamp_column}' not found"
        )

    now = datetime.now(timezone.utc)
    ts_series = pd.to_datetime(df[timestamp_column], utc=True, errors="coerce")
    latest = ts_series.max()

    if pd.isna(latest):
        return TestResult(
            test_name=f"{table}.freshness",
            table=table, column=timestamp_column,
            passed=False, severity=severity,
            message=f"FAIL: No valid timestamps in '{timestamp_column}' — table may be empty"
        )

    age_hours = (now - latest).total_seconds() / 3600
    passed = age_hours <= max_age_hours

    return TestResult(
        test_name=f"{table}.freshness",
        table=table, column=timestamp_column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=0 if passed else 1,
        message=(
            f"PASS: Most recent record is {age_hours:.1f} hours old — within {max_age_hours}h SLA"
            if passed
            else
            f"FAIL: Most recent record is {age_hours:.1f} hours old — exceeds {max_age_hours}h SLA. "
            f"Latest: {latest}"
        ),
        details={
            "latest_timestamp":  str(latest),
            "age_hours":         round(age_hours, 2),
            "max_age_hours":     max_age_hours,
            "checked_at":        now.isoformat()
        }
    )


def test_volume_day_over_day(
    today_count: int,
    yesterday_count: int,
    table: str,
    max_drop_pct: float = 30.0,
    max_spike_pct: float = 200.0,
    severity: str = "HIGH"
) -> TestResult:
    """
    Compare today's row count to yesterday's. Alert on abnormal changes.

    WHY THIS MATTERS:
        A pipeline that loads 50,000 orders every day silently loading
        50 orders is a failure — but no row-level test will catch it
        because all 50 rows might be perfectly valid.
        Only a volume comparison catches this class of failure.

    THRESHOLDS GUIDANCE:
        max_drop_pct: How much can volume drop before we alert?
            - 30% drop is a reasonable starting point
            - For critical financial tables, use 10%
            - For volatile event tables, you might allow 50%

        max_spike_pct: How much can volume grow before we alert?
            - 200% means "more than double" triggers an alert
            - A spike can indicate runaway duplication
    """
    if yesterday_count == 0:
        return TestResult(
            test_name=f"{table}.volume_dod",
            table=table, column=None,
            passed=True, severity=severity,
            message=f"PASS (SKIP): No yesterday count to compare against"
        )

    pct_change = ((today_count - yesterday_count) / yesterday_count) * 100
    drop_pct = -pct_change if pct_change < 0 else 0
    spike_pct = pct_change if pct_change > 0 else 0

    failures = []
    if drop_pct > max_drop_pct:
        failures.append(f"volume dropped {drop_pct:.1f}% (threshold: {max_drop_pct}%)")
    if spike_pct > max_spike_pct:
        failures.append(f"volume spiked {spike_pct:.1f}% (threshold: {max_spike_pct}%)")

    passed = len(failures) == 0

    return TestResult(
        test_name=f"{table}.volume_dod",
        table=table, column=None,
        passed=passed, severity=severity,
        total_count=today_count,
        failing_count=0 if passed else 1,
        message=(
            f"PASS: Volume {today_count:,} (yesterday: {yesterday_count:,}, "
            f"change: {pct_change:+.1f}%)"
            if passed
            else
            f"FAIL: Abnormal volume detected — {'; '.join(failures)}. "
            f"Today: {today_count:,}, Yesterday: {yesterday_count:,}"
        ),
        details={
            "today_count":    today_count,
            "yesterday_count":yesterday_count,
            "pct_change":     round(pct_change, 2),
            "max_drop_pct":   max_drop_pct,
            "max_spike_pct":  max_spike_pct
        }
    )
```

---

## 10. Layer 7 — Statistical Tests (Has Something Quietly Changed?)

### 10.1 Why Statistical Tests Exist

Row-level tests check individual values. Volume tests check counts. But some failures are invisible to both:

- The **distribution** of amounts shifts (average order value drops from $150 to $80 with no business explanation)
- The **proportion** of one status increases dramatically (suddenly 40% of orders are "cancelled" vs. the usual 8%)
- A **column's variance** collapses (all amounts are now exactly $99.99 — suspiciously uniform)

Statistical tests catch these *distribution-level* anomalies.

```python
# framework/validators.py — Part 7: Statistical Validators

from scipy import stats

def test_statistical_mean_stability(
    df: pd.DataFrame,
    column: str,
    table: str,
    reference_mean: float,
    reference_std: float,
    z_score_threshold: float = 3.0,
    severity: str = "MEDIUM"
) -> TestResult:
    """
    Check that the column mean hasn't shifted more than z_score_threshold standard
    deviations from the historical reference mean.

    HOW IT WORKS:
        1. Compute the mean of the current data
        2. Compute the z-score: (current_mean - reference_mean) / reference_std
        3. If |z_score| > threshold (default: 3.0), it's a statistical anomaly

        A z-score of 3.0 means "this value is 3 standard deviations from normal."
        Under a normal distribution, this happens by chance only 0.3% of the time.

    GETTING reference_mean AND reference_std:
        Compute these from your last 30–90 days of historical data:
            reference_mean = df_historical["amount"].mean()
            reference_std = df_historical["amount"].std()
        Store these in your test config YAML and update them monthly.
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.mean_stability",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    current_mean = float(df[column].dropna().mean())
    if reference_std == 0:
        passed = current_mean == reference_mean
        z_score = 0.0
    else:
        z_score = abs(current_mean - reference_mean) / reference_std
        passed = z_score <= z_score_threshold

    return TestResult(
        test_name=f"{table}.{column}.mean_stability",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=0 if passed else 1,
        message=(
            f"PASS: '{column}' mean {current_mean:.4f} is within {z_score_threshold} std devs "
            f"of reference {reference_mean:.4f} (z={z_score:.2f})"
            if passed
            else
            f"FAIL: '{column}' mean {current_mean:.4f} has shifted {z_score:.2f} std devs "
            f"from reference {reference_mean:.4f} — statistical anomaly detected"
        ),
        details={
            "current_mean":      round(current_mean, 4),
            "reference_mean":    reference_mean,
            "reference_std":     reference_std,
            "z_score":           round(z_score, 4),
            "threshold":         z_score_threshold
        }
    )


def test_statistical_category_distribution(
    df: pd.DataFrame,
    column: str,
    table: str,
    reference_distribution: dict[str, float],
    max_deviation_pct: float = 15.0,
    severity: str = "MEDIUM"
) -> TestResult:
    """
    Check that the distribution of a categorical column hasn't shifted significantly.

    USE FOR:
        - Order status distribution (% cancelled, % completed, % pending)
        - Payment method mix (% credit card, % paypal, % bank transfer)
        - Product category mix

    USAGE:
        test_statistical_category_distribution(
            df, "status", "gold.fact_orders",
            reference_distribution={
                "completed": 0.72,
                "cancelled": 0.08,
                "pending": 0.12,
                "processing": 0.08
            },
            max_deviation_pct=15.0  # Alert if any category shifts by >15pp
        )

    max_deviation_pct EXPLAINED:
        15.0 means: if "cancelled" is normally 8% but today is 24% (a 16pp shift),
        alert. A 15pp shift in cancellation rate is a real business signal.
    """
    if column not in df.columns:
        return TestResult(
            test_name=f"{table}.{column}.category_distribution",
            table=table, column=column,
            passed=False, severity=severity,
            message=f"FAIL: Column '{column}' not found"
        )

    current_dist = df[column].value_counts(normalize=True).to_dict()
    deviations = {}

    for category, expected_pct in reference_distribution.items():
        actual_pct = current_dist.get(category, 0.0)
        deviation = abs(actual_pct - expected_pct) * 100  # Convert to percentage points
        deviations[category] = {
            "expected_pct": round(expected_pct * 100, 2),
            "actual_pct":   round(actual_pct * 100, 2),
            "deviation_pp": round(deviation, 2)
        }

    violations = {
        k: v for k, v in deviations.items()
        if v["deviation_pp"] > max_deviation_pct
    }
    passed = len(violations) == 0

    return TestResult(
        test_name=f"{table}.{column}.category_distribution",
        table=table, column=column,
        passed=passed, severity=severity,
        total_count=len(df),
        failing_count=len(violations),
        message=(
            f"PASS: '{column}' distribution is stable (all categories within {max_deviation_pct}pp)"
            if passed
            else
            f"FAIL: '{column}' distribution shifted for: "
            + ", ".join(
                f"{k}: expected {v['expected_pct']}%, got {v['actual_pct']}% "
                f"({v['deviation_pp']}pp shift)"
                for k, v in violations.items()
            )
        ),
        details={
            "max_deviation_pp": max_deviation_pct,
            "distributions":    deviations,
            "violations":       violations
        }
    )
```

---

## 11. Assembling the Full Test Suite

### 11.1 The Suite Runner

```python
# framework/runner.py
"""
The test suite runner.

WHAT IT DOES:
    1. Collects all TestResult objects from every test function
    2. Determines which are CRITICAL failures (pipeline blockers)
    3. Stores all results for reporting
    4. Sends alerts for failures above the severity threshold
    5. Returns a summary that the pipeline can act on

DESIGN PRINCIPLE:
    The runner is the ONLY place where severity → action logic lives.
    Individual test functions just return results — they never raise exceptions
    or send alerts directly. This separation makes the suite composable and testable.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Callable
from datetime import datetime, timezone

from .result import TestResult
from .reporter import ResultReporter


@dataclass
class SuiteResult:
    """Summary of a complete test suite run."""
    suite_name: str
    run_at: str
    environment: str
    total_tests: int
    passed: int
    failed: int
    critical_failures: int
    high_failures: int
    medium_failures: int
    low_failures: int
    all_results: list[TestResult] = field(default_factory=list)
    pipeline_should_proceed: bool = True

    @property
    def pass_rate(self) -> float:
        if self.total_tests == 0:
            return 100.0
        return round(self.passed / self.total_tests * 100, 2)


class DataQualitySuiteRunner:
    """
    Runs a collection of data quality tests and produces a suite result.
    """

    def __init__(
        self,
        suite_name: str,
        environment: str = "dev",
        pipeline_run_id: str = "",
        block_on_severity: list[str] = None,
        reporter: ResultReporter | None = None
    ):
        self.suite_name = suite_name
        self.environment = environment
        self.pipeline_run_id = pipeline_run_id
        # Default: CRITICAL failures block the pipeline; HIGH/MEDIUM/LOW do not
        self.block_on_severity = block_on_severity or ["CRITICAL"]
        self.reporter = reporter
        self.logger = logging.getLogger(f"DQSuite.{suite_name}")
        self._results: list[TestResult] = []

    def run(self, test_fn: Callable, *args, **kwargs) -> TestResult:
        """
        Run a single test function and collect its result.

        USAGE:
            runner.run(test_completeness_not_null, df, "order_id", "bronze.raw_orders")
        """
        result = test_fn(*args, **kwargs)
        result.pipeline_run_id = self.pipeline_run_id
        result.environment = self.environment
        self._results.append(result)

        # Log immediately so failures are visible in pipeline logs
        level = logging.INFO if result.passed else logging.WARNING
        self.logger.log(level, result.message)

        return result

    def finalize(self) -> SuiteResult:
        """
        Produce the final SuiteResult and determine if the pipeline should proceed.
        """
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in self._results:
            if not r.passed:
                counts[r.severity] = counts.get(r.severity, 0) + 1

        # Pipeline should NOT proceed if any blocking severities have failures
        should_proceed = not any(
            counts.get(sev, 0) > 0
            for sev in self.block_on_severity
        )

        suite = SuiteResult(
            suite_name=self.suite_name,
            run_at=datetime.now(timezone.utc).isoformat(),
            environment=self.environment,
            total_tests=len(self._results),
            passed=sum(1 for r in self._results if r.passed),
            failed=sum(1 for r in self._results if not r.passed),
            critical_failures=counts.get("CRITICAL", 0),
            high_failures=counts.get("HIGH", 0),
            medium_failures=counts.get("MEDIUM", 0),
            low_failures=counts.get("LOW", 0),
            all_results=self._results,
            pipeline_should_proceed=should_proceed
        )

        # Persist results
        if self.reporter:
            self.reporter.save(suite)

        # Summary log
        status = "✅ PASSED" if should_proceed else "🚨 FAILED — PIPELINE BLOCKED"
        self.logger.info(
            f"\n{'='*60}\n"
            f"  Suite: {self.suite_name}\n"
            f"  Status: {status}\n"
            f"  Pass rate: {suite.pass_rate}% ({suite.passed}/{suite.total_tests})\n"
            f"  Failures: CRITICAL={counts['CRITICAL']} HIGH={counts['HIGH']} "
            f"MEDIUM={counts['MEDIUM']} LOW={counts['LOW']}\n"
            f"{'='*60}"
        )

        if not should_proceed:
            failed_tests = [r.test_name for r in self._results
                           if not r.passed and r.severity in self.block_on_severity]
            raise DataQualityError(
                f"Suite '{self.suite_name}' blocked pipeline. "
                f"Failing tests: {failed_tests}"
            )

        return suite


class DataQualityError(Exception):
    """Raised when critical data quality tests fail and pipeline must be blocked."""
    pass
```

---

## 12. Test Result Storage and Reporting

### 12.1 The Reporter

```python
# framework/reporter.py
"""
Persists test results to a database table for trending and reporting.

WHY STORE RESULTS:
    Individual pass/fail is useful. A trend of pass rates over 30 days
    is invaluable — it shows you whether quality is improving or degrading,
    and lets you answer regulatory questions like "what was the data quality
    on January 15th?"
"""

import pandas as pd
from datetime import datetime, timezone
from .result import TestResult


class ResultReporter:
    """Saves suite results to a Snowflake or SQLite table."""

    def __init__(self, connection, table: str = "data_quality.test_results"):
        """
        connection: A SQLAlchemy engine or Snowflake session
        table: Fully qualified table name for storing results
        """
        self.connection = connection
        self.table = table

    def save(self, suite_result) -> None:
        """Save all results from a suite run to the results table."""
        records = [r.to_dict() for r in suite_result.all_results]
        # Add suite-level metadata
        for r in records:
            r["suite_name"] = suite_result.suite_name
        df = pd.DataFrame(records)
        df.to_sql(
            self.table.split(".")[-1],
            self.connection,
            schema=self.table.split(".")[0] if "." in self.table else None,
            if_exists="append",
            index=False
        )


# SQL DDL to create the results table
CREATE_RESULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS data_quality.test_results (
    test_name       VARCHAR(500) NOT NULL,
    table_name      VARCHAR(500),
    column_name     VARCHAR(200),
    passed          BOOLEAN,
    severity        VARCHAR(20),
    failing_count   INTEGER,
    total_count     INTEGER,
    failing_pct     FLOAT,
    message         TEXT,
    run_at          TIMESTAMP_TZ,
    pipeline_run_id VARCHAR(200),
    environment     VARCHAR(50),
    suite_name      VARCHAR(200)
);
"""
```

---

## 13. The Test Config File — Making It Repeatable

### 13.1 The Complete Config File

```yaml
# config/gold/fact_orders.yaml
# This file defines ALL tests for gold.fact_orders.
# Adding a test = adding entries here. No code changes needed.

table: gold.fact_orders
layer: gold
priority: CRITICAL          # Highest priority — T1 consumers depend on this table

schema:
  required_columns:
    - order_id
    - customer_id
    - amount_usd
    - status_normalized
    - order_date
  column_types:
    order_id:       string
    customer_id:    string
    amount_usd:     float
    status_normalized: string
    order_date:     datetime

completeness:
  - column: order_id
    max_null_pct: 0.0
    severity: CRITICAL

  - column: customer_id
    max_null_pct: 0.0
    severity: CRITICAL

  - column: amount_usd
    max_null_pct: 0.0
    severity: HIGH

uniqueness:
  - columns: [order_id]
    severity: CRITICAL

validity:
  - column: status_normalized
    type: in_set
    allowed_values: [completed, cancelled, pending, processing, shipped, returned]
    severity: HIGH

  - column: amount_usd
    type: range
    min_value: 0.01
    max_value: 100000.00
    severity: HIGH

  - column: order_id
    type: regex
    pattern: '^ORD-\d{6}$'
    pattern_description: "ORD-######"
    severity: MEDIUM

business_rules:
  - description: "completed orders must have a non-null, positive amount_usd"
    condition_col: status_normalized
    condition_values: [completed]
    required_col: amount_usd
    check_type: positive
    severity: CRITICAL

volume:
  min_rows: 500
  max_rows: 500000
  day_over_day_max_drop_pct: 30.0
  day_over_day_max_spike_pct: 200.0
  severity: HIGH

freshness:
  timestamp_column: _created_at
  max_age_hours: 26
  severity: HIGH

statistical:
  - column: amount_usd
    reference_mean: 148.50
    reference_std: 62.30
    z_score_threshold: 3.0
    severity: MEDIUM

  - column: status_normalized
    type: distribution
    reference_distribution:
      completed: 0.72
      cancelled: 0.08
      pending: 0.12
      processing: 0.06
      shipped: 0.02
    max_deviation_pct: 15.0
    severity: MEDIUM
```

### 13.2 The Config Loader

```python
# framework/loader.py
"""
Loads test config YAML and converts it into runnable test functions.

HOW THIS WORKS:
    1. You define test rules in YAML (no Python required)
    2. The loader reads the YAML and creates TestResult-returning functions
    3. The suite runner executes those functions

    This means adding a new test to a table = editing a YAML file.
    No Python changes required. Any analyst can add tests.
"""

import yaml
from pathlib import Path
from typing import Callable
import pandas as pd
from .validators import (
    test_schema_all_columns_present, test_schema_column_type,
    test_completeness_not_null, test_uniqueness_no_duplicates,
    test_validity_in_set, test_validity_range, test_validity_regex,
    test_conditional_rule, test_aggregate_row_count,
    test_freshness_max_age, test_volume_day_over_day,
    test_statistical_mean_stability, test_statistical_category_distribution
)


def load_tests_from_config(config_path: str, df: pd.DataFrame) -> list[Callable]:
    """
    Load a test config YAML and return a list of zero-argument callables.
    Each callable runs one test and returns a TestResult.

    USAGE:
        tests = load_tests_from_config("config/gold/fact_orders.yaml", df)
        for test_fn in tests:
            result = test_fn()     # Returns a TestResult
            print(result.message)
    """
    with open(config_path) as f:
        config = yaml.safe_load(f)

    table = config["table"]
    tests = []

    # Schema tests
    if "schema" in config:
        schema_cfg = config["schema"]
        if "required_columns" in schema_cfg:
            tests.append(lambda: test_schema_all_columns_present(
                df, schema_cfg["required_columns"], table
            ))
        for col, dtype in schema_cfg.get("column_types", {}).items():
            _col, _dtype = col, dtype  # closure capture
            tests.append(lambda c=_col, d=_dtype: test_schema_column_type(df, c, d, table))

    # Completeness tests
    for rule in config.get("completeness", []):
        _rule = rule
        tests.append(lambda r=_rule: test_completeness_not_null(
            df, r["column"], table,
            severity=r.get("severity", "HIGH"),
            max_null_pct=r.get("max_null_pct", 0.0)
        ))

    # Uniqueness tests
    for rule in config.get("uniqueness", []):
        _rule = rule
        tests.append(lambda r=_rule: test_uniqueness_no_duplicates(
            df, r["columns"], table, severity=r.get("severity", "HIGH")
        ))

    # Validity tests
    for rule in config.get("validity", []):
        _rule = rule
        def _make_validity_test(r):
            if r["type"] == "in_set":
                return lambda: test_validity_in_set(
                    df, r["column"], r["allowed_values"], table,
                    severity=r.get("severity", "HIGH")
                )
            elif r["type"] == "range":
                return lambda: test_validity_range(
                    df, r["column"], table,
                    min_value=r.get("min_value"),
                    max_value=r.get("max_value"),
                    severity=r.get("severity", "HIGH")
                )
            elif r["type"] == "regex":
                return lambda: test_validity_regex(
                    df, r["column"], r["pattern"], table,
                    pattern_description=r.get("pattern_description", ""),
                    severity=r.get("severity", "MEDIUM")
                )
        tests.append(_make_validity_test(_rule))

    # Volume tests
    if "volume" in config:
        vol = config["volume"]
        tests.append(lambda: test_aggregate_row_count(
            df, table,
            min_rows=vol.get("min_rows"),
            max_rows=vol.get("max_rows"),
            severity=vol.get("severity", "HIGH")
        ))

    # Freshness tests
    if "freshness" in config:
        fresh = config["freshness"]
        tests.append(lambda: test_freshness_max_age(
            df, fresh["timestamp_column"], table,
            max_age_hours=fresh["max_age_hours"],
            severity=fresh.get("severity", "HIGH")
        ))

    return tests
```

---

## 14. Reading Test Output and Debugging Failures

### 14.1 How to Read Pytest Output

```
$ pytest tests/ -v

tests/unit/test_schema.py::TestBronzeRawOrdersSchema::test_all_expected_columns_present PASSED [ 12%]
tests/unit/test_schema.py::TestBronzeRawOrdersSchema::test_amount_is_numeric PASSED          [ 25%]
tests/unit/test_row_level.py::TestBronzeOrdersCompleteness::test_order_id_never_null PASSED  [ 37%]
tests/unit/test_row_level.py::TestBronzeOrdersValidity::test_status_in_allowed_set FAILED    [ 50%]

FAILURES
========
FAILED tests/unit/test_row_level.py::TestBronzeOrdersValidity::test_status_in_allowed_set

AssertionError: FAIL: 243 rows in 'status' have invalid values: ['partially_shipped', 'COMPLETED', 'in_transit']
```

**How to interpret this:**
1. `FAIL` — This test failed
2. `243 rows` — 243 records in the batch have invalid status values
3. `['partially_shipped', 'COMPLETED', 'in_transit']` — These are the new/unexpected values

**What to do:**
- `'partially_shipped'` and `'in_transit'` — new statuses added by the source team without coordination → coordinate with source team; update `allowed_values` if these are valid
- `'COMPLETED'` — same as `'completed'` but uppercase → source system changed casing → fix in Silver transformation: `LOWER(status)`

### 14.2 The Debug-First Instinct

When a test fails, the first question is not "how do I fix the test?" It is "is the data actually wrong?"

```python
# Quick debugging workflow
import pandas as pd

# Step 1: Reproduce the failure locally
df = pd.read_csv("sample_orders.csv")   # or load from your warehouse

# Step 2: Isolate the failing rows
invalid_mask = ~df["status"].isin(["pending", "processing", "shipped", "completed", "cancelled"])
failing_rows = df[invalid_mask]

# Step 3: Examine the failing rows
print(failing_rows[["order_id", "status", "created_at"]].head(20))
print(f"\nUnique invalid statuses: {sorted(failing_rows['status'].unique())}")
print(f"\nRow count: {len(failing_rows)} / {len(df)} total ({len(failing_rows)/len(df)*100:.1f}%)")

# Step 4: Check if this is new or historical
print(f"\nOldest failing order: {failing_rows['created_at'].min()}")
print(f"Newest failing order:  {failing_rows['created_at'].max()}")
# If only recent orders are failing → source system recently changed
# If historical orders also fail → the allowed_values list was always incomplete
```

---

## 15. Common Mistakes and How to Avoid Them

| Mistake | Problem | Fix |
|---|---|---|
| Testing only the happy path (PASS cases) | Validator might always return True silently | Always write a FAIL test that confirms the validator catches violations |
| Hardcoding thresholds in test functions | Tests break when business changes | Put all thresholds in YAML config; tests read from config |
| Running tests against production data with no limit | Tests are slow; costs money | Add `LIMIT 10000` or use a sampled fixture for unit tests |
| A single test that checks everything | Hard to debug; slow to run | One test = one rule. Prefer 20 small tests over 1 large one |
| Not storing test results | No historical trend; no audit evidence | Always persist results to a table, even if they all pass |
| Blocking pipeline on MEDIUM failures | Too much noise; team ignores alerts | Only CRITICAL failures block. HIGH = alert. MEDIUM = log. |
| Updating the test to match wrong data | You've hidden a bug | Never change an expected value to match bad data without root cause analysis |
| No tests on empty DataFrames | Validator raises `KeyError` or `ZeroDivisionError` | Add early-exit handling for zero-row DataFrames in every validator |

---

## 16. How to Scale From One Table to Fifty

### 16.1 The Scaling Pattern

```
Week 1: 1 table, all 7 layers of tests
Week 2: Add 2 more tables using the same config pattern
Week 3: Build the CI/CD integration (auto-run on pipeline trigger)
Week 4: Add statistical baselines from historical data
Month 2: Cover all Gold tables
Month 3: Cover all Silver tables
Month 4: Automated baseline refresh pipeline
```

### 16.2 Generating Config Files for New Tables

```python
# scripts/generate_config_skeleton.py
"""
Given a table name and a sample DataFrame, generate a starter YAML config
with all columns, auto-detected types, and placeholder thresholds.
This gives a 70% complete config that a human completes with business knowledge.
"""

import pandas as pd
import yaml
import sys

def generate_config_skeleton(df: pd.DataFrame, table_name: str, layer: str) -> dict:
    """Auto-generate a starter test config from a DataFrame's schema."""
    dtype_map = {
        "object":         "string",
        "int64":          "integer",
        "float64":        "float",
        "datetime64[ns]": "datetime",
        "bool":           "boolean"
    }
    column_types = {
        col: dtype_map.get(str(df[col].dtype), "string")
        for col in df.columns
    }

    config = {
        "table": table_name,
        "layer": layer,
        "priority": "TODO: CRITICAL | HIGH | MEDIUM",
        "schema": {
            "required_columns": list(df.columns),
            "column_types": column_types
        },
        "completeness": [
            {"column": col, "max_null_pct": 0.0, "severity": "HIGH",
             "comment": f"TODO: Adjust null tolerance for {col}"}
            for col in df.columns
        ],
        "uniqueness": [
            {"columns": ["TODO: specify primary key"], "severity": "CRITICAL"}
        ],
        "validity": [],   # TODO: Add domain-specific rules
        "volume": {
            "min_rows": "TODO: Set from historical min",
            "max_rows": "TODO: Set from historical max",
            "severity": "HIGH"
        },
        "freshness": {
            "timestamp_column": "TODO: Set to _ingested_at or updated_at",
            "max_age_hours": "TODO: Set to pipeline SLA hours",
            "severity": "HIGH"
        }
    }
    return config


if __name__ == "__main__":
    # Usage: python generate_config_skeleton.py my_table gold
    import argparse
    # (In practice, connect to warehouse and sample 1000 rows)
    print("Config skeleton generator ready. Load a DataFrame and call generate_config_skeleton().")
```

---

*This document is part of the Data Engineering Quality Engineering library. Maintained by the Data Engineering team. Questions: data-engineering@company.com*
