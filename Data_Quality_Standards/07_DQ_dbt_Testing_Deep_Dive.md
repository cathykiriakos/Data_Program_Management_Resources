# Data Engineering Quality Engineering
## Document 7: dbt Testing — The Complete In-Depth Guide
### From Built-in Tests to Custom Macros to Full Test Suites

**Document Owner:** Chief Data Office — Data Engineering  
**Domain:** Quality Engineering / dbt Testing  
**Version:** 1.0  
**Who This Is For:** Data engineers and analytics engineers using dbt as their transformation framework. This covers dbt testing from first principles to advanced production patterns.

---

## Why a Dedicated dbt Testing Document?

dbt (data build tool) has a built-in testing framework that integrates tests directly into the transformation pipeline. When used correctly, it means:

- Tests run *inside* the warehouse — no data movement, no extra infrastructure
- Tests are version-controlled alongside your models
- Test results are part of the dbt run manifest — queryable, storable, reportable
- Tests block downstream models from running if their parent data fails
- Tests are automatically documented alongside the models they test

This document covers everything from the first `dbt test` command to building a comprehensive test library that catches every class of data failure.

---

## Table of Contents

1. [dbt Testing Fundamentals — How It Works](#1-dbt-testing-fundamentals--how-it-works)
2. [The Four Built-In dbt Tests](#2-the-four-built-in-dbt-tests)
3. [YAML Test Configuration — Every Option Explained](#3-yaml-test-configuration--every-option-explained)
4. [dbt-utils — The Essential Test Extension Library](#4-dbt-utils--the-essential-test-extension-library)
5. [Writing Custom Generic Tests (Macros)](#5-writing-custom-generic-tests-macros)
6. [Writing Singular Tests — SQL-Based Business Rule Tests](#6-writing-singular-tests--sql-based-business-rule-tests)
7. [Testing Strategies for Each Medallion Layer](#7-testing-strategies-for-each-medallion-layer)
8. [Test Severity and Pipeline Gates](#8-test-severity-and-pipeline-gates)
9. [Storing and Querying Test Results](#9-storing-and-querying-test-results)
10. [Test Performance — Making Tests Fast](#10-test-performance--making-tests-fast)
11. [Building a Complete dbt Test Library](#11-building-a-complete-dbt-test-library)
12. [CI/CD Integration for dbt Tests](#12-cicd-integration-for-dbt-tests)
13. [Governance and Coverage Reporting](#13-governance-and-coverage-reporting)

---

## 1. dbt Testing Fundamentals — How It Works

### 1.1 What dbt Tests Actually Are

A dbt test is a SQL query that is expected to return **zero rows**.

If the query returns zero rows → **test passes** (no violations found).  
If the query returns any rows → **test fails** (violations detected; each row is one failing record).

That's the entire mechanism. It's beautifully simple.

Here's what a `not_null` test looks like when dbt compiles it into SQL:

```sql
-- This is the SQL dbt generates for a not_null test on orders.order_id
-- Source: compiled/my_project/models/silver/stg_orders.sql (not_null test)

SELECT order_id
FROM silver.stg_orders
WHERE order_id IS NULL
-- If this returns 0 rows: PASS. If it returns any rows: FAIL.
```

You never write this SQL yourself — dbt generates it from your YAML config. But understanding the underlying SQL helps you debug failures and write better custom tests.

### 1.2 Where Tests Live in a dbt Project

```
models/
├── bronze/
│   ├── raw_orders.sql
│   └── _bronze_sources.yml       ← Tests for source tables (raw data)
├── silver/
│   ├── stg_orders.sql
│   └── _silver_models.yml        ← Tests for Silver models
├── gold/
│   ├── fact_orders.sql
│   ├── dim_customers.sql
│   └── _gold_models.yml          ← Tests for Gold models
tests/
│   ├── assert_revenue_not_negative.sql    ← Singular tests
│   └── assert_completed_orders_shipped.sql
macros/
│   └── tests/
│       ├── test_is_positive.sql            ← Custom generic tests
│       ├── test_in_range.sql
│       └── test_category_distribution.sql
```

### 1.3 Running dbt Tests

```bash
# Run ALL tests in the project
dbt test

# Run tests for a specific model only
dbt test --select stg_orders

# Run tests for a model AND all models it depends on
dbt test --select +stg_orders

# Run tests for a model AND all downstream models
dbt test --select stg_orders+

# Run only tests of a specific type (by tag)
dbt test --select tag:critical

# Run tests for the entire Gold layer
dbt test --select path:models/gold/

# Run a specific singular test
dbt test --select assert_revenue_not_negative

# Run, then store results to a table (essential for production)
dbt test --store-failures
```

---

## 2. The Four Built-In dbt Tests

dbt ships with four built-in tests. They cover the most common quality dimensions and work on any column in any model.

### 2.1 `not_null` — Completeness

**What it does:** Ensures no values in the column are NULL.

**The SQL it compiles to:**
```sql
SELECT column_name FROM model WHERE column_name IS NULL
```

**YAML configuration:**
```yaml
# models/silver/_silver_models.yml

version: 2

models:
  - name: stg_orders
    description: "Cleansed, deduplicated orders from the source system."

    columns:
      - name: order_id
        description: "Unique identifier for the order. Never null."
        tests:
          - not_null         # Simplest form: no configuration needed

      - name: amount_usd
        description: "Order amount converted to USD."
        tests:
          - not_null:
              severity: error   # 'error' = fail and block. 'warn' = log and continue.
```

### 2.2 `unique` — Uniqueness

**What it does:** Ensures all values in the column are unique (no duplicates).

**The SQL it compiles to:**
```sql
SELECT order_id, COUNT(*) as n
FROM silver.stg_orders
WHERE order_id IS NOT NULL
GROUP BY order_id
HAVING COUNT(*) > 1
-- Returns the duplicate order_ids (and how many times they appear)
```

**YAML:**
```yaml
columns:
  - name: order_id
    tests:
      - unique
      - not_null
```

### 2.3 `accepted_values` — Validity (Set Membership)

**What it does:** Ensures all values are in a defined set of allowed values.

**The SQL it compiles to:**
```sql
SELECT status
FROM silver.stg_orders
WHERE status NOT IN ('pending', 'processing', 'shipped', 'completed', 'cancelled')
  AND status IS NOT NULL
-- Returns any status value not in the allowed set
```

**YAML:**
```yaml
columns:
  - name: status
    description: "Order status. Must be one of the allowed values."
    tests:
      - accepted_values:
          values:
            - pending
            - processing
            - shipped
            - completed
            - cancelled
          severity: error

  - name: currency
    tests:
      - accepted_values:
          values: [USD, EUR, GBP, CAD, AUD, JPY]
          # quote: true  ← Add this if values need quoting (strings)
```

### 2.4 `relationships` — Referential Integrity

**What it does:** Ensures every value in a column exists as a key in another table (like a foreign key constraint).

**The SQL it compiles to:**
```sql
SELECT o.customer_id
FROM silver.stg_orders o
LEFT JOIN silver.stg_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND o.customer_id IS NOT NULL
-- Returns order customer_ids that don't exist in the customers table
```

**YAML:**
```yaml
columns:
  - name: customer_id
    description: "Must exist in stg_customers."
    tests:
      - relationships:
          to: ref('stg_customers')      # dbt ref() — uses the model's actual name
          field: customer_id             # The column to check against in the parent table
          severity: warn                 # warn = log but don't block (GDPR deletions allowed)
```

---

## 3. YAML Test Configuration — Every Option Explained

```yaml
# Complete example showing every configuration option

version: 2

models:
  - name: fact_orders
    description: "Gold layer orders fact table."

    # ── Model-level tests ──────────────────────────────────────────
    # These test the whole model, not a specific column
    tests:
      - dbt_utils.equal_rowcount:        # Rowcount matches Silver source
          compare_model: ref('stg_orders')

    columns:
      - name: order_id
        tests:
          - not_null:
              # severity: controls what happens on failure
              # 'error' = test fails, dbt exits with non-zero code (blocks CI/CD)
              # 'warn'  = test logs a warning but dbt continues
              severity: error

              # config: additional dbt configuration
              config:
                severity: error
                store_failures: true          # Save failing rows to a table
                store_failures_as: table      # 'table' | 'view' | 'ephemeral'
                tags: ['critical', 'pii']     # Tag this test for filtering

                # Limit how many rows are checked (for performance on huge tables)
                limit: 100000                 # Check a sample of 100K rows

                # where clause: restrict which rows are tested
                # Useful for: only testing recent data, or excluding known-bad partitions
                where: "order_date >= DATEADD('day', -90, CURRENT_DATE())"

          - unique:
              config:
                severity: error
                where: "status != 'test_order'"    # Exclude test orders from uniqueness check

      - name: amount_usd
        tests:
          - not_null

          # Custom test with full configuration
          - is_positive:                 # A custom generic test (covered in Section 5)
              severity: error

          - dbt_utils.accepted_range:   # From dbt-utils package
              min_value: 0
              max_value: 999999.99
              inclusive: true
              severity: error

      - name: status_normalized
        tests:
          - accepted_values:
              values:
                - completed
                - cancelled
                - pending
                - processing
                - shipped
                - returned
              # quote: false   ← set false if comparing to numeric values
              config:
                severity: error
```

---

## 4. dbt-utils — The Essential Test Extension Library

`dbt-utils` extends dbt's built-in tests with 20+ additional tests. It is the most widely used dbt package.

### 4.1 Installing dbt-utils

```yaml
# packages.yml (in your dbt project root)
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations  # Additional test library (highly recommended)
    version: 0.10.1
```

```bash
dbt deps   # Install packages
```

### 4.2 The Most Useful dbt-utils Tests

```yaml
models:
  - name: fact_orders
    tests:

      # ── Rowcount tests ────────────────────────────────────────────
      # Ensure fact table has same rowcount as its staging source
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_orders')
          # CATCHES: Rows being dropped in the Gold transformation

      # ── Freshness tests ───────────────────────────────────────────
      - dbt_utils.recency:
          datepart: hour
          field: created_at
          interval: 26
          # MEANING: The most recent created_at must be within 26 hours.
          # CATCHES: Pipeline failures that result in no new data loading.
          config:
            severity: error

    columns:
      - name: order_id
        tests:
          # ── Not-empty: at least one non-null value ─────────────────
          - dbt_utils.not_empty_string:
              # CATCHES: order_id = '' (empty string) which passes not_null
              #          but is functionally null

      - name: amount_usd
        tests:
          # ── Range test ────────────────────────────────────────────
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100000
              inclusive: false      # Exclusive: 0 and 100000 are NOT allowed
              # CATCHES: Zero, negative, or unrealistically large amounts

      - name: order_date
        tests:
          # ── Date in expected range ────────────────────────────────
          - dbt_utils.accepted_range:
              min_value: "'2020-01-01'"    # Earliest valid business date
              max_value: "current_date()" # Can't be in the future
              inclusive: true

      - name: customer_id
        tests:
          # ── Relationship with condition ───────────────────────────
          - dbt_utils.relationships_where:
              to: ref('dim_customers')
              field: customer_id
              from_condition: "status_normalized != 'test'"  # Exclude test orders
              to_condition: "is_active = true"               # Only check against active customers
```

### 4.3 dbt_expectations — The Power User Test Library

`dbt_expectations` ports Great Expectations concepts into dbt. It has the most comprehensive test library.

```yaml
models:
  - name: fact_orders
    columns:
      - name: amount_usd
        tests:
          # ── Exact value tests ─────────────────────────────────────
          - dbt_expectations.expect_column_values_to_not_be_null

          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 50000
              strictly: false   # inclusive

          - dbt_expectations.expect_column_mean_to_be_between:
              # Mean should be between $100 and $300
              # CATCHES: Silent distribution shift
              min_value: 100
              max_value: 300
              config:
                severity: warn    # warn: alert but don't block

          - dbt_expectations.expect_column_stdev_to_be_between:
              min_value: 10
              max_value: 500
              # CATCHES: Variance collapse (all values becoming identical)

          - dbt_expectations.expect_column_quantile_values_to_be_between:
              quantile: 0.5      # Median
              min_value: 80
              max_value: 200
              # CATCHES: Median shifting significantly

          - dbt_expectations.expect_column_proportion_of_unique_values_to_be_between:
              min_value: 0.5     # At least 50% of amounts should be unique
              max_value: 1.0     # (catches cases where all amounts become identical)

      - name: status_normalized
        tests:
          - dbt_expectations.expect_column_value_lengths_to_be_between:
              min_value: 4       # Shortest valid status: 'paid' (4 chars)
              max_value: 20      # Longest: 'partially_refunded' (18 chars)

          - dbt_expectations.expect_column_values_to_match_regex:
              regex: "^[a-z_]+$"   # Status must be lowercase with underscores only
              # CATCHES: Uppercase statuses, special characters, SQL injection attempts

      - name: order_id
        tests:
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: "^ORD-[0-9]{6}$"

  - name: agg_daily_revenue
    tests:
      # ── Table-level: count matches ────────────────────────────────
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 1          # At least one row (not empty)
          max_value: 400        # At most 400 days of history (sanity check)

      - dbt_expectations.expect_table_columns_to_match_ordered_list:
          column_list:          # Exact column order + names (schema contract)
            - order_date
            - total_revenue_usd
            - order_count
            - avg_order_value_usd
            - _computed_at
```

---

## 5. Writing Custom Generic Tests (Macros)

### 5.1 When to Write a Custom Test

Write a custom generic test when:
1. The built-in tests don't cover your rule
2. The same rule applies to multiple columns or models
3. You need a configurable, parameterized test

### 5.2 Anatomy of a Custom Generic Test Macro

```sql
-- macros/tests/test_is_positive.sql
{% test is_positive(model, column_name) %}
/*
    Custom generic test: is_positive
    
    PURPOSE:
        Check that all non-null values in column_name are greater than zero.
        This is more specific than accepted_range because it explicitly says
        "positive" in the test name, making YAML self-documenting.
    
    HOW IT WORKS:
        - dbt injects 'model' (the table being tested) and 'column_name' (the column)
        - Returns rows where the value is <= 0
        - Zero rows returned = PASS; any rows = FAIL
    
    USAGE IN YAML:
        columns:
          - name: amount_usd
            tests:
              - is_positive    # No additional config needed
    
    WHAT dbt COMPILES THIS TO (approximately):
        SELECT amount_usd
        FROM {{ model }}
        WHERE amount_usd IS NOT NULL AND amount_usd <= 0
*/

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND {{ column_name }} <= 0

{% endtest %}
```

### 5.3 A Custom Test with Parameters

```sql
-- macros/tests/test_in_range.sql
{% test in_range(model, column_name, min_value, max_value, include_min=true, include_max=true) %}
/*
    Custom generic test: in_range

    PURPOSE:
        Flexible range test with configurable inclusivity.
        More readable than dbt_utils.accepted_range for teams unfamiliar with that package.

    PARAMETERS:
        min_value (required): Minimum acceptable value
        max_value (required): Maximum acceptable value
        include_min (default true): Whether min_value itself is acceptable
        include_max (default true): Whether max_value itself is acceptable

    USAGE:
        # Discount must be 0–100% (inclusive)
        - in_range:
            min_value: 0
            max_value: 100

        # Amount must be > 0 and < 1,000,000 (exclusive bounds)
        - in_range:
            min_value: 0
            max_value: 1000000
            include_min: false
            include_max: false
*/

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND (
    {% if include_min %}
      {{ column_name }} < {{ min_value }}
    {% else %}
      {{ column_name }} <= {{ min_value }}
    {% endif %}
    OR
    {% if include_max %}
      {{ column_name }} > {{ max_value }}
    {% else %}
      {{ column_name }} >= {{ max_value }}
    {% endif %}
  )

{% endtest %}
```

### 5.4 A Custom Test Using Jinja Logic

```sql
-- macros/tests/test_conditional_not_null.sql
{% test conditional_not_null(model, column_name, condition_column, condition_values) %}
/*
    Custom generic test: conditional_not_null

    PURPOSE:
        Test that column_name is NOT NULL when condition_column is one of condition_values.
        Encodes "if-then" business rules.

    EXAMPLE RULES THIS TEST CAN ENFORCE:
        "If status is 'shipped' or 'completed', then shipped_at must not be null"
        "If payment_method is 'credit_card', then card_last_four must not be null"
        "If is_refunded is true, then refund_amount must not be null"

    USAGE:
        columns:
          - name: shipped_at
            tests:
              - conditional_not_null:
                  condition_column: status
                  condition_values: ["'shipped'", "'completed'"]
                  # Note the inner quotes — these are SQL string values
*/

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ condition_column }} IN (
    {% for val in condition_values %}
        {{ val }}{% if not loop.last %},{% endif %}
    {% endfor %}
)
AND {{ column_name }} IS NULL

{% endtest %}
```

**Using it in YAML:**
```yaml
columns:
  - name: shipped_at
    description: "Timestamp when the order shipped. Required for shipped/completed orders."
    tests:
      - conditional_not_null:
          condition_column: status_normalized
          condition_values: ["'shipped'", "'completed'"]
          config:
            severity: error
```

### 5.5 A Distribution Test

```sql
-- macros/tests/test_category_distribution.sql
{% test category_distribution_not_shifted(
    model,
    column_name,
    category,
    expected_pct,
    max_deviation_pct=15
) %}
/*
    Custom generic test: category_distribution_not_shifted

    PURPOSE:
        Detect when a specific category's proportion has shifted significantly
        from its expected historical proportion.

    EXAMPLE:
        'cancelled' orders are normally ~8% of volume.
        If they suddenly become 40%, that's a pipeline or business problem.

    USAGE:
        tests:                       ← model-level test (not column-level)
          - category_distribution_not_shifted:
              column_name: status_normalized
              category: "'cancelled'"
              expected_pct: 8.0
              max_deviation_pct: 15
              # FAILS if cancelled% shifts by more than 15 percentage points from 8%

    HOW IT WORKS:
        1. Compute the actual % for the category in today's data
        2. Compute the absolute deviation from the expected %
        3. Return a row if deviation exceeds the threshold
        (Returning rows = FAIL in dbt test logic)
*/

WITH category_counts AS (
    SELECT
        COUNT(*) AS total_rows,
        SUM(CASE WHEN {{ column_name }} = {{ category }} THEN 1 ELSE 0 END) AS category_rows
    FROM {{ model }}
),
proportions AS (
    SELECT
        category_rows,
        total_rows,
        ROUND(category_rows * 100.0 / NULLIF(total_rows, 0), 4) AS actual_pct,
        {{ expected_pct }} AS expected_pct,
        ABS(category_rows * 100.0 / NULLIF(total_rows, 0) - {{ expected_pct }}) AS deviation_pp
    FROM category_counts
)
SELECT
    {{ category }} AS category_value,
    actual_pct,
    expected_pct,
    deviation_pp,
    {{ max_deviation_pct }} AS threshold_pp,
    'DISTRIBUTION SHIFT: ' || {{ category }} || ' is ' || actual_pct || '% (expected ' || expected_pct || '%, deviation ' || deviation_pp || 'pp)' AS failure_reason
FROM proportions
WHERE deviation_pp > {{ max_deviation_pct }}

{% endtest %}
```

---

## 6. Writing Singular Tests — SQL-Based Business Rule Tests

### 6.1 What Singular Tests Are

A singular test is a plain SQL file in your `tests/` directory. It runs as a single test with no parameterization.

Use singular tests for:
- Complex business rules that don't generalize to other models
- Rules that join multiple tables
- Rules that require CTEs for readability
- One-off data quality assertions

### 6.2 Complete Singular Test Examples

```sql
-- tests/assert_completed_orders_have_amount.sql
/*
    BUSINESS RULE: Every order with status 'completed' must have a positive amount_usd.

    WHY A SINGULAR TEST (not a conditional_not_null custom test):
        This checks both that amount_usd is not null AND that it's > 0.
        The combined rule is specific enough to this domain that a custom
        generic test would be over-engineered.

    EXPECTED RESULT: Zero rows (no completed orders with null/zero amount)
*/

SELECT
    order_id,
    customer_id,
    amount_usd,
    status_normalized,
    order_date
FROM {{ ref('fact_orders') }}
WHERE status_normalized = 'completed'
  AND (amount_usd IS NULL OR amount_usd <= 0)
```

```sql
-- tests/assert_no_future_orders.sql
/*
    BUSINESS RULE: No order can have an order_date in the future.

    A future-dated order indicates:
    - A timezone conversion error (UTC vs. local time)
    - A source system data entry error
    - A pipeline processing anomaly

    Both Bronze and Gold are checked because this rule is critical enough
    to catch at both layers.
*/

SELECT
    order_id,
    order_date,
    CURRENT_DATE() AS today,
    DATEDIFF('day', CURRENT_DATE(), order_date) AS days_in_future
FROM {{ ref('fact_orders') }}
WHERE order_date > CURRENT_DATE()
```

```sql
-- tests/assert_silver_gold_rowcount_match.sql
/*
    BUSINESS RULE: The Gold fact_orders table must have the same number of
    rows as the Silver stg_orders table after deduplication.

    WHY THIS MATTERS:
        If the Gold transformation has a bug (unintentional cross-join, missing
        WHERE clause, or accidental DISTINCT dropping rows), this test catches it.

    APPROACH:
        Count rows in each model and return a row if they don't match.
        A row returned = FAIL.
*/

WITH silver_count AS (
    SELECT COUNT(*) AS n FROM {{ ref('stg_orders') }}
),
gold_count AS (
    SELECT COUNT(*) AS n FROM {{ ref('fact_orders') }}
)
SELECT
    s.n AS silver_rows,
    g.n AS gold_rows,
    g.n - s.n AS difference,
    'Row count mismatch: Silver=' || s.n || ', Gold=' || g.n AS failure_reason
FROM silver_count s
CROSS JOIN gold_count g
WHERE s.n != g.n
```

```sql
-- tests/assert_daily_revenue_matches_fact.sql
/*
    BUSINESS RULE: The pre-aggregated agg_daily_revenue table must match
    a direct aggregation from fact_orders for the same date range.

    This is a reconciliation test between a derived aggregate and its source.
    It ensures the aggregation pipeline hasn't introduced errors.

    TOLERANCE: Within 1 cent (to handle floating point rounding)
*/

WITH fact_agg AS (
    SELECT
        order_date,
        SUM(amount_usd)  AS computed_revenue,
        COUNT(order_id)  AS computed_order_count
    FROM {{ ref('fact_orders') }}
    WHERE status_normalized = 'completed'
    GROUP BY order_date
),
precomputed AS (
    SELECT
        order_date,
        total_revenue_usd,
        order_count
    FROM {{ ref('agg_daily_revenue') }}
),
comparison AS (
    SELECT
        f.order_date,
        f.computed_revenue,
        p.total_revenue_usd AS precomputed_revenue,
        ABS(f.computed_revenue - p.total_revenue_usd) AS revenue_diff,
        f.computed_order_count,
        p.order_count AS precomputed_order_count,
        ABS(f.computed_order_count - p.order_count) AS order_count_diff
    FROM fact_agg f
    INNER JOIN precomputed p USING (order_date)
)
SELECT *
FROM comparison
WHERE revenue_diff > 0.01         -- Tolerance: 1 cent for floating point
   OR order_count_diff > 0        -- Zero tolerance on order counts
```

```sql
-- tests/assert_no_orphaned_orders.sql
/*
    BUSINESS RULE: Every order in fact_orders must have a customer in dim_customers.

    Orphaned orders (orders with no matching customer) cause:
    - NULL joins in downstream BI dashboards
    - Inaccurate customer-level metrics
    - ML features computed on orders to return NULL for the customer dimension

    NOTE: We use LEFT JOIN + WHERE NULL pattern (faster than NOT IN for large tables)
*/

SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.amount_usd
FROM {{ ref('fact_orders') }} o
LEFT JOIN {{ ref('dim_customers') }} c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND o.customer_id IS NOT NULL  -- Exclude orders where customer_id is already null
                                  -- (covered by a separate not_null test)
LIMIT 100                         -- Return at most 100 examples in the failure output
```

---

## 7. Testing Strategies for Each Medallion Layer

### 7.1 Bronze Layer — Source Fidelity Tests

The Bronze layer is a raw copy of source data. Tests here check that ingestion worked correctly.

```yaml
# models/bronze/_bronze_sources.yml
version: 2

sources:
  - name: raw
    description: "Raw source data from the orders application database."
    schema: bronze
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 26, period: hour}
    loaded_at_field: _ingested_at    # dbt uses this column for freshness checks

    tables:
      - name: raw_orders
        description: "Raw orders from source system. Append-only. No transformations."
        freshness:
          error_after: {count: 2, period: hour}   # Override: orders must be < 2h old

        columns:
          - name: order_id
            tests:
              - not_null:
                  config:
                    severity: error
              # Note: NOT testing unique at Bronze — duplicates may exist from source
              # Deduplication happens in Silver. We only test for nulls at Bronze.

          - name: amount
            tests:
              - not_null:
                  config:
                    severity: warn    # warn only — source might legitimately have nulls

          - name: currency
            tests:
              - not_null
              - accepted_values:
                  values: [USD, EUR, GBP, CAD, AUD, JPY, CHF, SEK, NOK, DKK]
                  config:
                    severity: warn   # warn: new currencies shouldn't block, but should alert

          - name: status
            tests:
              - not_null

          - name: _ingested_at
            description: "Ingestion timestamp added by the pipeline. Required for freshness."
            tests:
              - not_null:
                  config:
                    severity: error  # If this is null, the ingestion framework broke
```

### 7.2 Silver Layer — Transformation Correctness Tests

Silver transforms raw data into a clean, deduplicated, correctly-typed form. Tests here validate the transformation logic.

```yaml
# models/silver/_silver_models.yml
version: 2

models:
  - name: stg_orders
    description: "Cleansed and deduplicated orders. One row per order_id."
    config:
      tags: ['silver', 'orders']

    # Model-level tests
    tests:
      # Silver must have same or fewer rows than Bronze (deduplication can reduce)
      # It must NOT have MORE rows than Bronze (transformation created extra rows)
      - dbt_utils.expression_is_true:
          expression: "(SELECT COUNT(*) FROM {{ this }}) <= (SELECT COUNT(*) FROM {{ source('raw', 'raw_orders') }})"
          config:
            severity: error

      # Check that deduplication actually reduced some rows
      # (only run if we know Bronze has duplicates — adjust as needed)
      # - dbt_utils.expression_is_true:
      #     expression: "(SELECT COUNT(*) FROM {{ this }}) < (SELECT COUNT(*) FROM {{ source('raw', 'raw_orders') }})"

    columns:
      - name: order_id
        tests:
          - not_null:
              config:
                severity: error
          - unique:
              # Silver must be deduplicated — order_id must now be unique
              config:
                severity: error

      - name: amount_usd
        description: "Amount in USD after FX conversion. Must be positive."
        tests:
          - not_null:
              config:
                severity: error
          - is_positive:             # Custom generic test
              config:
                severity: error
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100000
              inclusive: false

      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
              config:
                severity: warn       # warn: GDPR deletions may cause valid orphans

      - name: status
        tests:
          - not_null
          - accepted_values:
              values: [pending, processing, shipped, completed, cancelled]
              config:
                severity: error

      - name: created_at
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: "'2020-01-01'"
              max_value: "current_date()"
              config:
                severity: error
```

### 7.3 Gold Layer — Business Logic Tests

Gold models implement business logic. Tests verify that logic is correct.

```yaml
# models/gold/_gold_models.yml
version: 2

models:
  - name: fact_orders
    description: "Gold facts — business-ready, enriched orders."

    tests:
      # Gold must have EXACTLY the same rowcount as deduplicated Silver
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_orders')
          config:
            severity: error

      # Freshness: Gold table must be up to date
      - dbt_utils.recency:
          datepart: hour
          field: _created_at
          interval: 26
          config:
            severity: error

      # Distribution: status mix shouldn't shift dramatically
      - category_distribution_not_shifted:
          column_name: status_normalized
          category: "'completed'"
          expected_pct: 72.0
          max_deviation_pct: 20
          config:
            severity: warn

    columns:
      - name: order_id
        tests:
          - not_null:
              config: {severity: error}
          - unique:
              config: {severity: error}

      - name: customer_id
        tests:
          - not_null:
              config: {severity: error}
          - relationships:
              to: ref('dim_customers')
              field: customer_id
              config:
                severity: warn

      - name: amount_usd
        tests:
          - not_null:
              config: {severity: error}
          - is_positive:
              config: {severity: error}
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 500000
              inclusive: false
          - dbt_expectations.expect_column_mean_to_be_between:
              min_value: 50
              max_value: 500
              config:
                severity: warn
                # Note: warn not error — distribution shift is an alert, not a hard block

      - name: status_normalized
        tests:
          - not_null
          - accepted_values:
              values: [completed, cancelled, pending, processing, shipped, returned]
              config: {severity: error}

      - name: fiscal_quarter
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: "^FY[0-9]{4}Q[1-4]$"   # e.g., FY2024Q1
              config: {severity: error}

  - name: agg_daily_revenue
    description: "One row per calendar day. Pre-aggregated revenue."

    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [order_date]    # One row per date

      - dbt_utils.recency:
          datepart: hour
          field: _computed_at
          interval: 26

    columns:
      - name: order_date
        tests:
          - not_null
          - unique

      - name: total_revenue_usd
        tests:
          - not_null
          - is_positive

      - name: order_count
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
              inclusive: true
```

---

## 8. Test Severity and Pipeline Gates

### 8.1 Severity Configuration Reference

```yaml
# The two severity levels in dbt:
# 'error' — dbt exits with a non-zero status code. 
#            In CI/CD this blocks the pipeline.
# 'warn'  — dbt logs a warning but exits with code 0.
#            The pipeline continues but the warning is recorded.

# Best practice severity mapping:
# 
# CRITICAL business impact   → severity: error
# HIGH business impact       → severity: error (for Gold) or warn (for Bronze/Silver)
# MEDIUM business impact     → severity: warn
# LOW / informational        → severity: warn
# Distribution / statistical → severity: warn (alert but don't block)
```

### 8.2 The `--warn-error` Flag for Stricter CI

```bash
# In production CI/CD, you may want to treat ALL warnings as errors
# to prevent "warn and continue" from masking real problems

dbt test --warn-error           # Treats all warn as error

# Or more granular: only treat specific tests as errors
dbt test --warn-error-options '{"include": ["unique", "not_null"]}'
```

### 8.3 Pipeline Gate Pattern

```python
# orchestration/dbt_gate.py
"""
Use this as a gate in Airflow / Prefect / Dagster to block downstream
processing when dbt tests fail.
"""

import subprocess
import json
from pathlib import Path


def run_dbt_tests_with_gate(
    models: list[str] | None = None,
    tags: list[str] | None = None,
    profiles_dir: str = "~/.dbt",
    project_dir: str = ".",
    block_on_warnings: bool = False
) -> dict:
    """
    Run dbt tests and return a structured result dict.
    Raises DataQualityGateError if tests fail.
    """
    cmd = ["dbt", "test",
           "--profiles-dir", profiles_dir,
           "--project-dir", project_dir,
           "--store-failures"]

    if models:
        cmd += ["--select", " ".join(models)]
    elif tags:
        cmd += ["--select", " ".join(f"tag:{t}" for t in tags)]

    if block_on_warnings:
        cmd += ["--warn-error"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse the dbt run_results.json for structured output
    run_results_path = Path(project_dir) / "target" / "run_results.json"
    if run_results_path.exists():
        with open(run_results_path) as f:
            run_results = json.load(f)
        summary = _parse_run_results(run_results)
    else:
        summary = {"parsed": False, "stderr": result.stderr}

    if result.returncode != 0:
        raise DataQualityGateError(
            f"dbt tests failed. {summary.get('failed_count', '?')} tests failed.\n"
            f"Failed tests: {summary.get('failed_tests', [])}"
        )

    return summary


def _parse_run_results(run_results: dict) -> dict:
    """Parse dbt run_results.json into a summary dict."""
    results = run_results.get("results", [])
    failed = [r for r in results if r["status"] in ("fail", "error")]
    passed = [r for r in results if r["status"] == "pass"]
    warned = [r for r in results if r["status"] == "warn"]

    return {
        "total_tests":   len(results),
        "passed_count":  len(passed),
        "failed_count":  len(failed),
        "warned_count":  len(warned),
        "pass_rate":     round(len(passed) / len(results) * 100, 2) if results else 100,
        "failed_tests":  [r["unique_id"] for r in failed],
        "warned_tests":  [r["unique_id"] for r in warned],
    }


class DataQualityGateError(Exception):
    pass
```

---

## 9. Storing and Querying Test Results

### 9.1 Enabling `--store-failures`

When you run `dbt test --store-failures`, dbt saves the failing rows of each test to a table in your warehouse. This is essential for:
- Debugging: See exactly which rows failed, not just the count
- Trending: Track whether failures are improving over time
- Auditing: Evidence of historical test results

```yaml
# dbt_project.yml — enable store-failures project-wide
name: my_project
version: "1.0.0"

tests:
  my_project:
    +store_failures: true         # Store ALL test failures
    +store_failures_as: table     # Use 'table' (persistent) not 'view' (ephemeral)
    +schema: dq_test_results      # Store in a dedicated schema

    # Override for specific severity levels
    error:
      +store_failures: true
    warn:
      +store_failures: true
```

### 9.2 Querying the Stored Results

```sql
-- After running dbt test --store-failures, dbt creates tables like:
-- dq_test_results.not_null_stg_orders_order_id
-- dq_test_results.unique_stg_orders_order_id
-- dq_test_results.accepted_values_stg_orders_status__completed__cancelled

-- Query all stored failure tables to build a consolidated DQ report
SELECT
    'stg_orders' AS model,
    'order_id'   AS column_name,
    'not_null'   AS test_type,
    COUNT(*)     AS failing_row_count,
    CURRENT_TIMESTAMP() AS queried_at
FROM dq_test_results.not_null_stg_orders_order_id

UNION ALL

SELECT
    'stg_orders',
    'status',
    'accepted_values',
    COUNT(*),
    CURRENT_TIMESTAMP()
FROM dq_test_results.accepted_values_stg_orders_status__completed__cancelled
```

### 9.3 Parsing the dbt Artifacts for a Governance Dashboard

```python
# scripts/parse_dbt_results.py
"""
Parse dbt's run_results.json and manifest.json to produce a
governance-ready test coverage report.

WHERE THESE FILES LIVE:
    After any dbt run or dbt test command:
    - target/run_results.json  → Results of the last run
    - target/manifest.json     → Metadata about all models and tests
"""

import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd


def parse_test_results(target_dir: str = "target") -> pd.DataFrame:
    """
    Parse dbt run_results.json into a DataFrame of test results.
    Suitable for loading into a DQ tracking table.
    """
    results_path = Path(target_dir) / "run_results.json"
    manifest_path = Path(target_dir) / "manifest.json"

    with open(results_path) as f:
        run_results = json.load(f)
    with open(manifest_path) as f:
        manifest = json.load(f)

    rows = []
    generated_at = run_results.get("metadata", {}).get("generated_at", "")

    for result in run_results["results"]:
        node_id = result["unique_id"]
        node = manifest["nodes"].get(node_id, {})

        # Extract model name and column from test node ID
        # Format: test.project_name.test_type_model_column.hash
        parts = node_id.split(".")
        test_node_name = parts[2] if len(parts) > 2 else node_id

        rows.append({
            "run_at":           generated_at,
            "test_id":          node_id,
            "test_name":        test_node_name,
            "status":           result["status"],          # pass | fail | warn | error
            "passed":           result["status"] == "pass",
            "failures":         result.get("failures", 0),
            "execution_time":   result.get("execution_time", 0),
            "model":            node.get("attached_node", ""),
            "test_type":        node.get("test_metadata", {}).get("name", "singular"),
            "column_name":      node.get("test_metadata", {}).get("kwargs", {}).get("column_name", ""),
            "severity":         node.get("config", {}).get("severity", "error"),
            "tags":             ",".join(node.get("tags", [])),
            "description":      node.get("description", ""),
        })

    return pd.DataFrame(rows)


def build_coverage_report(manifest_path: str = "target/manifest.json") -> pd.DataFrame:
    """
    Analyze the manifest to find models with and without tests.
    Produces a test coverage report.
    """
    with open(manifest_path) as f:
        manifest = json.load(f)

    models = {k: v for k, v in manifest["nodes"].items() if v.get("resource_type") == "model"}
    tests = {k: v for k, v in manifest["nodes"].items() if v.get("resource_type") == "test"}

    # Count tests per model
    tested_models = {}
    for test_id, test_node in tests.items():
        model_id = test_node.get("attached_node", "")
        if model_id:
            tested_models[model_id] = tested_models.get(model_id, 0) + 1

    rows = []
    for model_id, model_node in models.items():
        test_count = tested_models.get(model_id, 0)
        rows.append({
            "model":         model_id,
            "model_name":    model_node.get("name", ""),
            "schema":        model_node.get("schema", ""),
            "layer":         model_node.get("config", {}).get("tags", ["unknown"])[0],
            "test_count":    test_count,
            "has_tests":     test_count > 0,
            "columns_count": len(model_node.get("columns", {})),
        })

    return pd.DataFrame(rows)
```

---

## 10. Test Performance — Making Tests Fast

### 10.1 The Problem

dbt tests run SQL against your warehouse. On large tables, some tests scan every row. At scale this gets slow and expensive.

### 10.2 Performance Strategies

```yaml
# Strategy 1: WHERE clause to test only recent data
# For daily-loaded tables, only test today's partition
columns:
  - name: amount_usd
    tests:
      - not_null:
          config:
            where: "DATE(created_at) = CURRENT_DATE()"
            severity: error
      # Reasoning: If today's data passes, yesterday's was verified yesterday.
      # Don't re-scan all historical data on every run.

# Strategy 2: LIMIT to test a sample
# For very high-volume tables where full scans are expensive
      - is_positive:
          config:
            limit: 100000    # Test 100K randomly sampled rows
            severity: error
```

```sql
-- Strategy 3: Optimize singular tests with LIMIT and sampling
-- tests/assert_no_future_orders_fast.sql

SELECT order_id, order_date
FROM {{ ref('fact_orders') }}
WHERE order_date > CURRENT_DATE()
  AND created_at >= DATEADD('day', -7, CURRENT_DATE())  -- Only recent data
LIMIT 10   -- Return at most 10 examples (we only need to know if any exist)
```

### 10.3 Test Scheduling Strategy

```
Every pipeline run (blocking):    CRITICAL severity tests only
Daily (non-blocking):             HIGH severity tests
Weekly (non-blocking):            MEDIUM severity, statistical tests
Monthly:                          Full distribution audits, cross-table reconciliations
```

---

## 11. Building a Complete dbt Test Library

### 11.1 The Standard Test Set for Every Table

Every production table should have at minimum:

```yaml
# Minimum test set for any production table
columns:
  - name: {primary_key}
    tests:
      - not_null:       { config: { severity: error } }
      - unique:         { config: { severity: error } }

  - name: {every_required_column}
    tests:
      - not_null:       { config: { severity: error } }

  - name: {every_status_column}
    tests:
      - accepted_values: { values: [...], config: { severity: error } }

  - name: {every_foreign_key}
    tests:
      - relationships:  { to: ref('...'), field: '...', config: { severity: warn } }

  - name: {every_amount_column}
    tests:
      - not_null
      - is_positive

# Table-level
tests:
  - dbt_utils.recency:
      datepart: hour
      field: _loaded_at
      interval: 26
```

### 11.2 The Coverage Checklist

Use this to review any model's test completeness:

```
□ Primary key: not_null + unique
□ Every NOT NULL column: not_null test
□ Every categorical column: accepted_values or custom enum test
□ Every foreign key: relationships test
□ Every numeric column: range test (is_positive at minimum)
□ Every date column: date range test (not future, not too historical)
□ Every string column with a pattern: regex test
□ Freshness: recency test on the load timestamp column
□ Row count: at least min_rows check
□ At least one singular test: the most important business rule for this model
□ Distribution: mean_between or distribution_not_shifted for key metrics
```

---

## 12. CI/CD Integration for dbt Tests

```yaml
# .github/workflows/dbt_test_ci.yml
name: dbt Test Gate

on:
  pull_request:
    paths: ['models/**', 'tests/**', 'macros/**']
  push:
    branches: [main]

jobs:
  dbt-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dbt
        run: |
          pip install dbt-snowflake==1.7.3   # or dbt-databricks, dbt-bigquery
          dbt deps

      - name: Run dbt tests (error only — fast gate)
        env:
          DBT_SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          DBT_SNOWFLAKE_USER:    ${{ secrets.SNOWFLAKE_USER }}
          DBT_SNOWFLAKE_PASS:    ${{ secrets.SNOWFLAKE_PASS }}
        run: |
          dbt test \
            --select tag:critical \
            --store-failures \
            --target ci \
            2>&1 | tee dbt_test_output.txt
          exit ${PIPESTATUS[0]}   # Preserve dbt's exit code

      - name: Parse and report test results
        if: always()
        run: |
          python scripts/parse_dbt_results.py \
            --output dbt_test_report.json \
            --format github_comment

      - name: Post test summary as PR comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('dbt_test_report.json'));
            const status = report.failed_count === 0 ? '✅' : '🚨';
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `${status} **dbt Test Results**\n\n` +
                    `| Metric | Value |\n|---|---|\n` +
                    `| Total Tests | ${report.total_tests} |\n` +
                    `| Passed | ${report.passed_count} |\n` +
                    `| Failed | ${report.failed_count} |\n` +
                    `| Warnings | ${report.warned_count} |\n` +
                    `| Pass Rate | ${report.pass_rate}% |\n` +
                    (report.failed_count > 0 ?
                      `\n**Failed tests:**\n${report.failed_tests.map(t => `- \`${t}\``).join('\n')}` : '')
            });
```

---

## 13. Governance and Coverage Reporting

### 13.1 Test Coverage SQL Report

```sql
-- Query this in your BI tool to show test coverage across all models
-- Requires the output of parse_dbt_results.py stored in your warehouse

SELECT
    layer,
    COUNT(DISTINCT model_name)                                    AS total_models,
    COUNT(DISTINCT CASE WHEN has_tests THEN model_name END)       AS models_with_tests,
    ROUND(
        COUNT(DISTINCT CASE WHEN has_tests THEN model_name END) * 100.0
        / NULLIF(COUNT(DISTINCT model_name), 0), 1
    )                                                             AS coverage_pct,
    SUM(test_count)                                               AS total_tests
FROM data_quality.dbt_model_coverage
GROUP BY layer
ORDER BY
    CASE layer
        WHEN 'gold'   THEN 1
        WHEN 'silver' THEN 2
        WHEN 'bronze' THEN 3
        ELSE 4
    END
```

### 13.2 Weekly DQ Health Summary

```sql
-- Weekly test pass rate trend
SELECT
    DATE_TRUNC('week', run_at) AS week,
    COUNT(*)                   AS total_tests,
    SUM(CASE WHEN passed THEN 1 ELSE 0 END) AS passed_tests,
    ROUND(AVG(CASE WHEN passed THEN 100.0 ELSE 0 END), 2) AS pass_rate_pct,
    SUM(CASE WHEN NOT passed AND severity = 'error' THEN 1 ELSE 0 END) AS error_failures,
    SUM(CASE WHEN NOT passed AND severity = 'warn'  THEN 1 ELSE 0 END) AS warn_failures
FROM data_quality.dbt_test_results
WHERE run_at >= DATEADD('week', -12, CURRENT_DATE())
GROUP BY 1
ORDER BY 1 DESC
```

---

*This document is part of the Data Engineering Quality Engineering library. For questions: data-engineering@company.com*
