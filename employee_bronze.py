# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.bronze.employees_bronze
# MAGIC USING delta
# MAGIC AS
# MAGIC SELECT * FROM 
# MAGIC read_files('/Volumes/workspace/bronze/employee_files',
# MAGIC format=>'csv',
# MAGIC Header=>True,
# MAGIC inferschema=>True);
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.bronze.employees_bronze
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC  Validate Row count

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT count(*) AS total_records
# MAGIC FROM workspace.bronze.employees_bronze

# COMMAND ----------

# MAGIC %md
# MAGIC -- DESCRIBE 

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE workspace.bronze.employees_bronze

# COMMAND ----------

# MAGIC %md
# MAGIC Check null values

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.bronze.employees_bronze
# MAGIC WHERE employee_id IS NULL
# MAGIC OR branch_id IS NULL
# MAGIC OR employee_name IS NULL
# MAGIC OR designation IS NULL
# MAGIC OR salary IS NULL
# MAGIC OR joining_date IS NULL
# MAGIC OR employment_status IS NULL

# COMMAND ----------

# MAGIC %md
# MAGIC Check duplicate

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT employee_id,
# MAGIC COUNT(*) AS duplicate_count
# MAGIC FROM workspace.bronze.employees_bronze
# MAGIC Group by employee_id
# MAGIC Having duplicate_count > 1