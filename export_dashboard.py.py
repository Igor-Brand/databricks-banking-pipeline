# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Export Dashboard - Documentation
# Databricks notebook source
# MAGIC %md
# MAGIC # Export Dashboard to Git Repository
# MAGIC 
# MAGIC This notebook exports the NeoBank_Dashboard to the Git repository as a JSON file.

# COMMAND ----------

# DBTITLE 1,Export Dashboard to Git
# Databricks notebook source
import os
import shutil

# Paths
dashboard_source = "/Workspace/Users/igorbrandaao@gmail.com/NeoBank_Dashboard.lvdash.json"
git_repo = "/Workspace/Users/igorbrandaao@gmail.com/databricks-banking-pipeline"
dashboards_folder = f"{git_repo}/dashboards"
dashboard_destination = f"{dashboards_folder}/NeoBank_Dashboard.lvdash.json"

# Create dashboards folder if it doesn't exist
os.makedirs(dashboards_folder, exist_ok=True)
print(f"📁 Pasta criada/verificada: {dashboards_folder}")

# Copy dashboard file to Git repository
shutil.copy2(dashboard_source, dashboard_destination)
print(f"\n✅ Dashboard exportado com sucesso!")
print(f"📊 Origem: {dashboard_source}")
print(f"📂 Destino: {dashboard_destination}")

# Get file size
file_size = os.path.getsize(dashboard_destination)
print(f"📏 Tamanho do arquivo: {file_size:,} bytes")

# COMMAND ----------

# DBTITLE 1,Next Steps
# Databricks notebook source
# MAGIC %md
# MAGIC ## ✅ Próximos Passos
# MAGIC 
# MAGIC Após executar a célula acima:
# MAGIC 1. Verifique se o arquivo foi criado em `dashboards/NeoBank_Dashboard.lvdash.json`
# MAGIC 2. Volte ao chat com o assistente
# MAGIC 3. Solicite o commit e push do arquivo para o GitHub

# COMMAND ----------


