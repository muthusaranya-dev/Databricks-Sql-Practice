# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.silver.employee_scd2
# MAGIC (
# MAGIC     employee_id STRING,
# MAGIC     employee_name STRING,
# MAGIC     designation STRING,
# MAGIC     salary INT,
# MAGIC     start_date DATE,
# MAGIC     end_date DATE,
# MAGIC     is_current BOOLEAN
# MAGIC
# MAGIC ) USING DELTA

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.silver.employee_scd2
# MAGIC VALUES
# MAGIC  (
# MAGIC 'EMP000003' ,
# MAGIC     'Ishaan Mishra',
# MAGIC     'Credit Analyst',
# MAGIC     45000,
# MAGIC     DATE '2025-01-01',
# MAGIC     NULL,
# MAGIC     TRUE
# MAGIC );
# MAGIC SELECT * FROM workspace.silver.employee_scd2

# COMMAND ----------

# MAGIC %md
# MAGIC simulate incoming changed data. Imagine HR sends the same employee tomorrow, but designation and salary changed.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW employee_changes AS
# MAGIC SELECT
# MAGIC     'EMP000003' AS employee_id,
# MAGIC     'Ishaan Mishra' AS employee_name,
# MAGIC     'Senior Credit Analyst' AS designation,
# MAGIC     47000 AS salary,
# MAGIC     DATE '2026-08-16' AS start_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM employee_changes;

# COMMAND ----------

# MAGIC %md
# MAGIC -- 1)Expire the old record
# MAGIC --We don't want to overwrite this record. In SCD Type 2, we keep it as history.
# MAGIC --So we need to change:
# MAGIC
# MAGIC --end_date   → 2026-08-15
# MAGIC --is_current → FALSE

# COMMAND ----------

# MAGIC %sql
# MAGIC update workspace.silver.employee_scd2
# MAGIC set
# MAGIC     end_date = DATE '2026-08-15',
# MAGIC     is_current = FALSE
# MAGIC where
# MAGIC     employee_id = 'EMP000003' and
# MAGIC     is_current = TRUE
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_scd2
# MAGIC WHERE employee_id = 'EMP000003';

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC -- 2) Insert the new record
# MAGIC
# MAGIC --We want to insert the new record with the following values:
# MAGIC --EMP000003 | Ishaan Mishra | Senior Credit Analyst | 47000 | 2026-08-16 | NULL | TRUE

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.silver.employee_scd2
# MAGIC SELECT
# MAGIC     employee_id,
# MAGIC     employee_name,
# MAGIC     designation,
# MAGIC     salary,
# MAGIC     start_date,
# MAGIC    NULL AS end_date,
# MAGIC     TRUE AS is_current
# MAGIC FROM
# MAGIC     employee_changes
# MAGIC WHERE
# MAGIC     employee_id = 'EMP000003';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_scd2
# MAGIC WHERE employee_id = 'EMP000003'
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Scenario
# MAGIC
# MAGIC Current target table employee_scd2 has:
# MAGIC
# MAGIC EMP000003 | Ishaan Mishra | Senior Credit Analyst | 47000 | 2026-08-16 | NULL | TRUE
# MAGIC
# MAGIC Tomorrow HR sends:
# MAGIC
# MAGIC EMP000003 | Ishaan Mishra | Lead Credit Analyst | 52000 | 2026-08-17
# MAGIC
# MAGIC end_date = 2026-08-16 is_current = True

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO workspace.silver.employee_scd2 AS target
# MAGIC USING employee_changes AS source
# MAGIC ON target.employee_id = source.employee_id
# MAGIC
# MAGIC WHEN MATCHED AND target.is_current = TRUE THEN
# MAGIC   UPDATE SET
# MAGIC     target.end_date = source.start_date - INTERVAL 1 DAY,
# MAGIC     target.is_current = FALSE
# MAGIC
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (
# MAGIC     employee_id,
# MAGIC     employee_name,
# MAGIC     designation,
# MAGIC     salary,
# MAGIC     start_date,
# MAGIC     end_date,
# MAGIC     is_current
# MAGIC   )
# MAGIC   VALUES (
# MAGIC     source.employee_id,
# MAGIC     source.employee_name,
# MAGIC     source.designation,
# MAGIC     source.salary,
# MAGIC     source.start_date,
# MAGIC     NULL,
# MAGIC     TRUE
# MAGIC   )

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE workspace.silver.employee_scd2
# MAGIC SET
# MAGIC     end_date = NULL,
# MAGIC     is_current = TRUE
# MAGIC WHERE employee_id = 'EMP000003'
# MAGIC   AND start_date = DATE '2026-08-16';
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_scd2
# MAGIC WHERE employee_id = 'EMP000003';

# COMMAND ----------

# MAGIC %md
# MAGIC Current:
# MAGIC Senior Credit Analyst | 47000 | 2026-08-16 | NULL | TRUE
# MAGIC
# MAGIC HR sends:
# MAGIC Lead Credit Analyst | 52000 | 2026-08-17
# MAGIC
# MAGIC Credit Analyst → old/history record → FALSE
# MAGIC Senior Credit Analyst → current record → TRUE
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC Now we can practice the next change:
# MAGIC
# MAGIC Current:
# MAGIC Senior Credit Analyst | 47000 | 2026-08-16 | NULL | TRUE
# MAGIC
# MAGIC HR sends:
# MAGIC Lead Credit Analyst | 52000 | 2026-08-17

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO workspace.silver.employee_scd2 AS t
# MAGIC USING employee_changes AS s
# MAGIC ON t.employee_id = s.employee_id
# MAGIC
# MAGIC WHEN MATCHED AND t.is_current = TRUE THEN
# MAGIC UPDATE SET
# MAGIC     t.end_date = DATE '2026-08-16',
# MAGIC     t.is_current = FALSE
# MAGIC
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     employee_id,
# MAGIC     employee_name,
# MAGIC     designation,
# MAGIC     salary,
# MAGIC     start_date,
# MAGIC     end_date,
# MAGIC     is_current
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.employee_id,
# MAGIC     s.employee_name,
# MAGIC     s.designation,
# MAGIC     s.salary,
# MAGIC     s.start_date,
# MAGIC     NULL,
# MAGIC     TRUE
# MAGIC );
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_scd2
# MAGIC WHERE employee_id = 'EMP000003'

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.silver.employee_scd2
# MAGIC VALUES (
# MAGIC     'EMP000003',
# MAGIC     'Ishaan Mishra',
# MAGIC     'Lead Credit Analyst',
# MAGIC     52000,
# MAGIC     DATE '2026-08-17',
# MAGIC     NULL,
# MAGIC     TRUE
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_scd2
# MAGIC WHERE employee_id = 'EMP000003'
# MAGIC ORDER BY start_date;