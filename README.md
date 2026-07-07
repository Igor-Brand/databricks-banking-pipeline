
# Banking Data Engineering Framework: Medallion Architecture no Databricks

Este projeto consiste em uma solução de engenharia de dados ponta a ponta desenvolvida para o **Neo Bank**, um banco virtual fictício. O objetivo é consolidar dados provenientes de sistemas bancários centrais (SQL Server) e fontes externas (Cloud Storage/Arquivos CSV) em uma plataforma de análise unificada no Databricks.

## 📌 Visão Geral do Projeto
O Neo Bank gera grandes volumes de dados que estavam espalhados em múltiplas plataformas, dificultando a análise de negócios. Esta solução implementa um **framework orientado a metadados (metadata-driven)** que automatiza a ingestão e transformação de dados, garantindo governança e escalabilidade.

### 🏗️ Arquitetura
O projeto segue a **Medallion Architecture**, dividindo o processamento em três camadas: **Bronze, Silver e Gold**.

> **[ESPAÇO PARA PRINT: Diagrama da Arquitetura do Projeto]**
> *Sugestão: Inclua o diagrama mostrando as fontes (SQL Server/Blob), as camadas Medallion e o consumo final.*

---

## 🚀 Tecnologias Utilizadas
*   **Databricks (Free Edition):** Plataforma principal de processamento.
*   **Apache Spark (PySpark & SQL):** Processamento e transformações de dados.
*   **Auto Loader:** Ingestão incremental e eficiente de arquivos CSV.
*   **JDBC:** Conexão com Azure SQL Server.
*   **Unity Catalog:** Governança e controle de acesso.
*   **Databricks Jobs:** Orquestração de workflows complexos.
*   **Gmail API:** Notificações customizadas por e-mail.
*   **Databricks Dashboards & Genie AI:** Consumo de dados e análises em linguagem natural.

---

## 🛠️ O Framework Metadata-Driven
A inteligência da pipeline reside em quatro tabelas de metadados que controlam a reusabilidade do código:
1.  **Tables:** Armazena nomes de tabelas, sistemas de origem e camadas de destino.
2.  **Table Parameters:** Define estratégias de carga (Merge, Append, Full Load) e chaves primárias.
3.  **Table Watermarks:** Controla o progresso de cargas incrementais.
4.  **Audit (Pipeline Runs):** Registra logs de execução, status, tempo e contagem de registros.

---

## 📂 Estrutura das Camadas (Medallion)
1.  **Bronze:** Dados brutos ingeridos das fontes. Arquivos CSV são processados via Auto Loader com captura de dados corrompidos (_rescued data_).
2.  **Silver:** Dados limpos e integrados. Aplica-se lógica de *Upsert* (Merge) baseada nos metadados para manter a consistência com a origem.
3.  **Gold:** Tabelas agregadas prontas para análise de negócios, como Performance de Agências e Visão 360 do Cliente.

> **[ESPAÇO PARA PRINT: Visualização das Tabelas no Unity Catalog (Banking Catalog)]**
> *Sugestão: Mostre as schemas bronze, silver e gold criadas.*

---

## 📊 Dashboards e Insights AI
Foram criados painéis interativos para executivos e gerentes de agência, cobrindo KPIs como depósitos totais, transações e segmentação de clientes por risco de crédito. Além disso, o **Databricks Genie** permite que usuários façam perguntas aos dados usando linguagem natural.

> **[ESPAÇO PARA PRINT: Dashboard do Neo Bank]**
> *Sugestão: Print do Executive Dashboard com os contadores de clientes e depósitos.*

> **[ESPAÇO PARA PRINT: Demonstração do Databricks Genie]**
> *Sugestão: Print de uma pergunta em linguagem natural sendo respondida pela IA.*

---

## 📧 Orquestração e Monitoramento
A pipeline mestra orquestra a ingestão simultânea de múltiplas fontes e, ao final, dispara um e-mail formatado em HTML com o resumo da execução.

> **[ESPAÇO PARA PRINT: Workflow do Databricks Jobs (Master Pipeline)]**
> *Sugestão: Mostre a árvore de dependências das tarefas no Databricks.*

> **[ESPAÇO PARA PRINT: Exemplo de E-mail de Notificação Recebido]**
> *Sugestão: Print da tabela HTML com o status de sucesso da carga.*

---

## ⚙️ Como Executar
1.  Configure o **Secret Scope** no Databricks para armazenar as credenciais do SQL Server e a API do Gmail.
2.  Execute o notebook de **Setup Metadata** para criar as tabelas de controle e volumes.
3.  Configure os **Databricks Jobs** apontando para os notebooks de ingestão (Source to Silver) e transformações (Silver to Gold).
4.  Acione o **Master Job** para processar os dados históricos e incrementais.

---

---

# 🔧 Problemas Enfrentados: Conectando Azure SQL Database ao Databricks

## 📌 Contexto

Durante a implementação do pipeline de ingestão de dados do Azure SQL Database para o Databricks (camada Bronze), foram encontrados múltiplos desafios relacionados à conectividade e compatibilidade entre as plataformas.

---

## ❌ Problema 1: JDBC não suportado no Databricks Serverless

### Sintoma
```python
[FAILED_JDBC.CONNECTION] Failed JDBC jdbc: 
Client with IP address 'X.X.X.X' is not allowed to access the server
```

### Tentativa Inicial
O código original tentava usar JDBC direto:
```python
jdbc_url = f"jdbc:sqlserver://{host}:{port};database={database}"
source_df = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_properties)
```

### Causa Raiz
- **Databricks Serverless NÃO suporta JDBC** para fontes externas
- Apenas clusters clássicos suportam JDBC
- Workspace tinha policy que bloqueava criação de clusters clássicos

### ✅ Solução
Migrar para **Lakehouse Federation** (foreign catalogs):

1. **Criar Connection no Databricks UI:**
   ```
   Catalog → External Data → Connections
   - Nome: azure_sql_banking
   - Tipo: Azure SQL Database
   - Host: banki.database.windows.net
   - Port: 1433
   - User: [from secret]
   - Password: [from secret]
   ```

2. **Criar Foreign Catalog via SDK:**
   ```python
   from databricks.sdk import WorkspaceClient
   
   w = WorkspaceClient()
   w.catalogs.create(
       name="azure_sql_banking_catalog",
       connection_name="azure_sql_banking",
       options={"database": "banking"}
   )
   ```

3. **Atualizar código do notebook:**
   ```python
   # ❌ ANTES (JDBC - não funciona no serverless)
   source_df = spark.read.jdbc(url=jdbc_url, table=query, properties=props)
   
   # ✅ DEPOIS (Lakehouse Federation)
   foreign_table = f"azure_sql_banking_catalog.{schema}.{table}"
   spark.sql(f"""
       CREATE OR REPLACE TABLE {bronze_table}
       AS SELECT *, CURRENT_TIMESTAMP() as insert_timestamp
       FROM {foreign_table}
   """)
   ```

---

## ❌ Problema 2: Firewall do Azure SQL bloqueando IPs do Databricks Serverless

### Sintoma
```
Client with IP address '3.145.247.173' is not allowed to access the server
```

### Causa Raiz
- **IP do Databricks Serverless é dinâmico** e muda entre execuções
- Azure SQL Firewall precisa liberar especificamente os IPs do Databricks

### Tentativas e IPs Observados
Durante as tentativas, observamos os seguintes IPs:
- `3.145.247.175` (primeira tentativa)
- `3.145.247.173` (segunda tentativa)
- `3.145.247.170` (após recriar a conexão)

### ✅ Solução Final

**Opção 1: Range de IPs (Recomendado)**
```
Nome da Regra: databricks_serverless
IP Inicial: 3.145.247.0
IP Final: 3.145.247.255
```

**Opção 2: Descobrir IP dinamicamente**
```python
import requests
response = requests.get('https://api.ipify.org?format=json')
current_ip = response.json()['ip']
print(f"IP atual do Databricks: {current_ip}")
```

**Opção 3: "Allow Azure services and resources to access this server"**
- No Azure Portal → SQL Server → Networking → Firewall rules
- Habilitar: "Allow Azure services and resources to access this server"
- ⚠️ Menos seguro, mas funciona

---

## ❌ Problema 3: Foreign Catalog perdendo conexão

### Sintoma
```
UnknownException: (java.lang.reflect.InvocationTargetException)
```
Catalog existia, mas qualquer query (SHOW SCHEMAS, SELECT) falhava.

### Causa Raiz
- Credenciais na connection ficaram "presas" após atualização do firewall
- Catalog não reconectava automaticamente

### ✅ Solução
**Recriar a connection e o catalog:**

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import ConnectionType
import json

w = WorkspaceClient()

# 1. Pegar credenciais do secret
secret_json = dbutils.secrets.get(scope="banking-scope", key="sqlserver-connection-json")
credentials = json.loads(secret_json)

# 2. Atualizar connection
w.connections.update(
    name="azure_sql_banking",
    options={
        "host": credentials['host'],
        "port": "1433",
        "user": credentials['user'],
        "password": credentials['password'],
        "trustServerCertificate": "true"
    }
)

# 3. Dropar e recriar catalog
w.catalogs.delete("azure_sql_banking_catalog", force=True)
w.catalogs.create(
    name="azure_sql_banking_catalog",
    connection_name="azure_sql_banking",
    options={"database": "banking"}
)
```

---

## ❌ Problema 4: Schema Mismatch ao escrever na Bronze

### Sintoma
```
[DELTA_METADATA_MISMATCH] A metadata mismatch was detected
```

### Causa Raiz
- Tabela `banking.bronze.customers` tinha schema antigo (de testes anteriores)
- Schema do Azure SQL era diferente (mais colunas)

### ✅ Solução
Usar `CREATE OR REPLACE TABLE` em vez de `APPEND`:

```python
# ❌ ANTES (falhava com schema mismatch)
source_df.write.mode("append").saveAsTable(bronze_table)

# ✅ DEPOIS (recria tabela com schema correto)
spark.sql(f"""
    CREATE OR REPLACE TABLE {bronze_table}
    USING DELTA
    AS SELECT *, CURRENT_TIMESTAMP() as insert_timestamp
    FROM {foreign_table}
""")
```

---

## ❌ Problema 5: `.cache()` não suportado no Serverless

### Sintoma
```
[NOT_SUPPORTED_WITH_SERVERLESS] PERSIST TABLE is not supported on serverless compute
```

### Causa Raiz
Serverless compute não permite operações de cache/persist

### ✅ Solução
Remover `.cache()` e usar SQL puro para leitura + escrita em uma operação atômica:

```python
# ❌ ANTES (tentativa de materializar)
source_df = source_df.cache()
row_count = source_df.count()

# ✅ DEPOIS (SQL puro, sem cache)
spark.sql(f"CREATE OR REPLACE TABLE {bronze_table} AS SELECT * FROM {foreign_table}")
```

---

## 📚 Lições Aprendidas

### 1. Databricks Serverless vs Clusters Clássicos

| Recurso | Serverless | Clusters Clássicos |
|---------|-----------|-------------------|
| JDBC Externo | ❌ Não suportado | ✅ Suportado |
| Lakehouse Federation | ✅ Suportado | ✅ Suportado |
| .cache() / .persist() | ❌ Não suportado | ✅ Suportado |
| Custo | 💰 Paga por segundo | 💰💰 Paga por hora |
| Setup | ⚡ Instantâneo | 🐌 5-10 minutos |

**Recomendação:** Use Lakehouse Federation para ingestão de dados externos no Serverless.

### 2. Firewall do Azure SQL

- **IPs do Databricks Serverless são dinâmicos** — sempre use um range
- **Teste a conexão** antes de executar o pipeline completo
- **Considere "Allow Azure services"** para ambientes de dev/test (menos seguro)

### 3. Foreign Catalogs (Lakehouse Federation)

**Vantagens:**
- ✅ Funciona no Serverless
- ✅ Query pushdown automático (filtra no source)
- ✅ Sem necessidade de gerenciar drivers JDBC
- ✅ Metadados sincronizados automaticamente

**Desvantagens:**
- ⚠️ Read-only (não pode fazer INSERT/UPDATE direto no Azure SQL)
- ⚠️ Pode ter latência maior para queries complexas
- ⚠️ Requer Unity Catalog habilitado

### 4. Estratégia de Debug

**Ordem de troubleshooting:**
1. Verificar se catalog existe: `SHOW CATALOGS`
2. Testar acesso básico: `SHOW SCHEMAS IN <catalog>`
3. Testar leitura simples: `SELECT COUNT(*) FROM <foreign_table>`
4. Verificar IP do compute: `requests.get('https://api.ipify.org')`
5. Verificar firewall do Azure SQL
6. Recriar connection e catalog se necessário

---

## 🎯 Código Final Funcional

```python
# =====================================================
# Ingestão Azure SQL → Bronze usando Lakehouse Federation
# =====================================================

try:
    if source_system == "sqlserver":
        # Ler via Foreign Catalog
        foreign_table = f"azure_sql_banking_catalog.{source_schema}.{source_table}"
        
        # Filtro incremental (opcional)
        where_clause = ""
        if load_type in ["APPEND", "MERGE"] and last_watermark:
            where_clause = f"WHERE {watermark_column} > TIMESTAMP('{last_watermark}')"
        
        # Criar/substituir tabela bronze diretamente via SQL
        spark.sql(f"""
            CREATE OR REPLACE TABLE {bronze_table_fqn}
            USING DELTA
            AS
            SELECT *, CURRENT_TIMESTAMP() as insert_timestamp
            FROM {foreign_table}
            {where_clause}
        """)
        
        records_read = spark.table(bronze_table_fqn).count()
        print(f"✅ Carregados {records_read} registros do Azure SQL")

except Exception as e:
    print(f"❌ Erro: {e}")
    raise
```

---

## 📊 Resultado Final

- ✅ **4.000 registros** carregados com sucesso
- ✅ Pipeline **Azure SQL → Bronze** operacional
- ✅ Tempo de execução: **~5 segundos**
- ✅ Arquitetura: **Lakehouse Federation** no Serverless

---

## 🔗 Links Úteis

- [Databricks Lakehouse Federation Docs](https://docs.databricks.com/en/query-federation/index.html)
- [Azure SQL Firewall Rules](https://learn.microsoft.com/en-us/azure/azure-sql/database/firewall-configure)
- [Databricks Serverless Limitations](https://docs.databricks.com/en/compute/serverless.html#limitations)

---
