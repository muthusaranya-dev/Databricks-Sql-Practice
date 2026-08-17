# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %md
# MAGIC Question:
# MAGIC
# MAGIC Find all employees whose branch_id is NULL.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE branch_id IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees whose salary is missing.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC Multiple NULL columns
# MAGIC
# MAGIC Question: Find employees where either salary OR joining_date is NULL.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL
# MAGIC    OR joining_date IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees where both salary AND joining_date are NULL.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL
# MAGIC    AND joining_date IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC Count NULL values
# MAGIC
# MAGIC Scenario: How many employees have a NULL salary?
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) AS total_salary
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL
# MAGIC   
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Replace NULL values
# MAGIC
# MAGIC Even though your salary currently has no NULLs,Scenario: Suppose some employees have NULL salary. While displaying the data, replace NULL salary with 0.

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE workspace.silver.employee_silver
# MAGIC SET salary = NULL
# MAGIC WHERE employee_id = 'EMP000002';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT employee_id,
# MAGIC salary,
# MAGIC coalesce(salary,0) AS salary
# MAGIC From workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %md
# MAGIC Remove null values

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM workspace.silver.employee_silver
# MAGIC WHERE salary IS NULL;