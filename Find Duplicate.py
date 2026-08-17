# Databricks notebook source
# MAGIC %md
# MAGIC Your current employee_silver data is mostly clean, so first let's check for duplicates.
# MAGIC
# MAGIC Scenario: Find employee IDs that appear more than once.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT employee_id,count(*)
# MAGIC FROM workspace.silver.employee_silver
# MAGIC GROUP BY employee_id
# MAGIC HAVING count(*) > 1

# COMMAND ----------

# MAGIC %md
# MAGIC how to display the actual duplicate rows,

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id IN
# MAGIC (SELECT employee_id
# MAGIC FROM workspace.silver.employee_silver
# MAGIC GROUP BY employee_id
# MAGIC HAVING count(*) > 1)

# COMMAND ----------

# MAGIC %md
# MAGIC insert duplicate record.EMP000002.

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.silver.employee_silver
# MAGIC SELECT employee_id,
# MAGIC branch_id,
# MAGIC employee_name,
# MAGIC designation,
# MAGIC salary,
# MAGIC joining_date,
# MAGIC employment_status
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id ='EMP000002'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT employee_id,count(*)
# MAGIC FROM workspace.silver.employee_silver
# MAGIC GROUP BY employee_id
# MAGIC HAVING count(*)>1

# COMMAND ----------

# MAGIC %md
# MAGIC Display the complete rows for those duplicate employee IDs.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id IN
# MAGIC (
# MAGIC     SELECT employee_id
# MAGIC FROM workspace.silver.employee_silver
# MAGIC GROUP BY employee_id
# MAGIC HAVING count(*)>1
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver

# COMMAND ----------

# MAGIC %md
# MAGIC EMP000002 appears twice with exactly the same values. We want to keep one record and remove the extra duplicate.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *,
# MAGIC  ROW_NUMBER() OVER(PARTITION BY employee_id 
# MAGIC  ORDER BY employee_id) AS row_num
# MAGIC FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id = 'EMP000002'

# COMMAND ----------

# MAGIC %md
# MAGIC have 4 identical rows for EMP000002, we want:
# MAGIC
# MAGIC row_num = 1 → KEEP
# MAGIC row_num > 1 → REMOVE

# COMMAND ----------

# MAGIC %md
# MAGIC remove these duplicates using a CTE + ROW_NUMBER()

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH employee_dedup AS
# MAGIC (
# MAGIC     SELECT *,
# MAGIC            ROW_NUMBER() OVER (
# MAGIC                PARTITION BY employee_id
# MAGIC                ORDER BY employee_id
# MAGIC            ) AS row_num
# MAGIC     FROM workspace.silver.employee_silver
# MAGIC )
# MAGIC
# MAGIC SELECT *
# MAGIC FROM employee_dedup
# MAGIC WHERE row_num = 1;
# MAGIC     
# MAGIC

# COMMAND ----------

