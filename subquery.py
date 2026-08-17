# Databricks notebook source
# MAGIC %md
# MAGIC scenario 1 — Salary above average
# MAGIC
# MAGIC Question: Find employees whose salary is greater than the average salary of all employees.
# MAGIC
# MAGIC Think about it as two steps:

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary>
# MAGIC (
# MAGIC     SELECT AVG(salary)
# MAGIC FROM workspace.silver.employee_silver
# MAGIC )

# COMMAND ----------

# MAGIC %md
# MAGIC Find the employee(s) who have the highest salary.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary=
# MAGIC (
# MAGIC     SELECT Max(salary)
# MAGIC     FROM workspace.silver.employee_silver
# MAGIC )

# COMMAND ----------

# MAGIC %md
# MAGIC Next scenario
# MAGIC
# MAGIC Find employees whose salary is less than the average salary.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE salary=
# MAGIC (
# MAGIC     SELECT Min(salary)
# MAGIC     FROM workspace.silver.employee_silver
# MAGIC )