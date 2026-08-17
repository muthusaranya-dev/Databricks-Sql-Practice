# Databricks notebook source
# MAGIC %md
# MAGIC -- Create incoming employee data
# MAGIC
# MAGIC --Imagine tomorrow HR sends us two records:
# MAGIC
# MAGIC --EMP000001 → already exists, but salary changed to 65000
# MAGIC --EMP000501 → completely new employee

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW employee_update AS
# MAGIC SELECT
# MAGIC 'EMP000001' As employee_id,
# MAGIC     'BR0002' AS branch_id,
# MAGIC     'Aarav Kumar' AS employee_name,
# MAGIC     'Assistant Manager' AS designation,
# MAGIC     65000 AS salary,
# MAGIC     DATE '2020-10-02' AS joining_date,
# MAGIC     'Active' AS employment_status
# MAGIC     UNION ALL
# MAGIC SELECT 
# MAGIC 'EMP000501' As employee_id,
# MAGIC     'BR0005' AS branch_id,
# MAGIC     'John David'AS employee_name,
# MAGIC     'Data Analyst' AS designation,
# MAGIC     70000 AS salary,
# MAGIC     DATE '2026-08-16' AS joining_date,
# MAGIC     'Active' AS employment_status
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC     SELECT * FROM employee_update

# COMMAND ----------

# MAGIC %sql
# MAGIC Merge into workspace.silver.employee_silver as target
# MAGIC using employee_update as source
# MAGIC on target.employee_id = source.employee_id
# MAGIC WHEN MATCHED THEN UPDATE SET 
# MAGIC target.branch_id = source.branch_id,
# MAGIC target.employee_name = source.employee_name,
# MAGIC target.designation = source.designation,
# MAGIC target.salary = source.salary,
# MAGIC target.joining_date = source.joining_date,
# MAGIC target.employment_status = source.employment_status
# MAGIC WHEN NOT MATCHED THEN INSERT 
# MAGIC (
# MAGIC     employee_id,
# MAGIC     branch_id,
# MAGIC     employee_name,
# MAGIC     designation,
# MAGIC     salary,
# MAGIC     joining_date,
# MAGIC     employment_status
# MAGIC )
# MAGIC VALUES (
# MAGIC     source.employee_id,
# MAGIC     source.branch_id,
# MAGIC     source.employee_name,
# MAGIC     source.designation,
# MAGIC     source.salary,
# MAGIC     source.joining_date,
# MAGIC     source.employment_status
# MAGIC )
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id IN ('EMP000001','EMP000501');

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC --Today HR sends these 2 records:
# MAGIC
# MAGIC --employee_id	employee_name	designation	salary
# MAGIC --EMP000002	Meera Nair	Branch Manager	135000
# MAGIC --EMP000502	Priya Shah	Data Engineer	80000

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW employee_update2 AS
# MAGIC
# MAGIC SELECT
# MAGIC     'EMP000002' AS employee_id,
# MAGIC     'BR0028' AS branch_id,
# MAGIC     'Meera Nair' AS employee_name,
# MAGIC     'Branch Manager' AS designation,
# MAGIC     135000 AS salary,
# MAGIC     DATE '2015-04-09' AS joining_date,
# MAGIC     'Active' AS employment_status
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'EMP000502',
# MAGIC     'BR0010',
# MAGIC     'Priya Shah',
# MAGIC     'Data Engineer',
# MAGIC     80000,
# MAGIC     DATE '2026-08-16',
# MAGIC     'Active';
# MAGIC
# MAGIC     SELECT * FROM employee_update2;

# COMMAND ----------

# MAGIC %sql
# MAGIC Merge into workspace.silver.employee_silver as target
# MAGIC using employee_update2 as source
# MAGIC on target.employee_id = source.employee_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id IN ('EMP000002','EMP000502');

# COMMAND ----------

# MAGIC %md
# MAGIC -- Employee: EMP000003
# MAGIC --Old designation: Credit Analyst
# MAGIC --New designation: Senior Credit Analyst
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW employee_scd1 AS
# MAGIC
# MAGIC SELECT
# MAGIC     'EMP000003' AS employee_id,
# MAGIC     'BR0029' AS branch_id,
# MAGIC     'Ishaan Mishra' AS employee_name,
# MAGIC     'Senior Credit Analyst' AS designation,
# MAGIC     47000 AS salary,
# MAGIC     DATE '2012-08-20' AS joining_date,
# MAGIC     'Active' AS employment_status;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE into workspace.silver.employee_silver as target
# MAGIC using employee_scd1 as source
# MAGIC on target.employee_id = source.employee_id
# MAGIC WHEN MATCHED THEN UPDATE SET*
# MAGIC WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.silver.employee_silver
# MAGIC WHERE employee_id ='EMP000003'