# Databricks notebook source
# MAGIC %md
# MAGIC Find employees who joined after January 1, 2020.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE joining_date > '2020-01-01';

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees who joined before January 1, 2015.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE joining_date < '2015-01-01';

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees who joined between January 1, 2020 and December 31, 2022.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE joining_date BETWEEN '2020-01-01' AND '2022-12-31'

# COMMAND ----------

# MAGIC %md
# MAGIC Find all employees who joined in the year 2022.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE YEAR(joining_date)=2022

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees who joined in the month of December.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE MONTH(joining_date) = 12

# COMMAND ----------

# MAGIC %md
# MAGIC Find employees who joined in December 2022.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE YEAR(joining_date) = 2022
# MAGIC   AND MONTH(joining_date) = 12;