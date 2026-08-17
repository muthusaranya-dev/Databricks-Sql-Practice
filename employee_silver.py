# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.silver.employee_silver
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT 
# MAGIC employee_id,
# MAGIC branch_id,
# MAGIC TRIM(employee_name) AS employee_name,
# MAGIC TRIM(designation) AS designation,
# MAGIC salary,
# MAGIC joining_date,
# MAGIC TRIM(employment_status) AS employment_status
# MAGIC FROM workspace.bronze.employees_bronze
# MAGIC WHERE employee_id Is NOT NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) AS total_count
# MAGIC  FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %md
# MAGIC DESCRIBE

# COMMAND ----------

# MAGIC %sql
# MAGIC  Describe History workspace.silver.employee_silver
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Time Travel

# COMMAND ----------

# MAGIC %sql
# MAGIC  SELECT * FROM workspace.silver.employee_silver
# MAGIC  WHERE employee_id='EMP000001'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver VERSION AS OF 0
# MAGIC  WHERE employee_id='EMP000001'