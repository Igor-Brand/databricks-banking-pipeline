
# Banking Data Engineering Framework: Medallion Architecture no Databricks

Este projeto implementa uma solução de engenharia de dados de ponta a ponta para o **Neo Bank**, um banco virtual fictício. O objetivo é centralizar dados provenientes de sistemas centrais (**SQL Server**) e fontes externas (**Cloud Storage**) em uma plataforma unificada no Databricks para análises avançadas.

## 📌 Visão Geral
A solução aborda o desafio de dados espalhados em múltiplas plataformas e formatos, o que dificultava uma visão consolidada do negócio. Foi desenvolvido um **framework orientado a metadados (metadata-driven)** que automatiza a ingestão e transformação de dados através das camadas Bronze, Silver e Gold.

### 🏗️ Arquitetura Medallion
O processamento é dividido em três camadas principais utilizando **Delta Lake**:
1.  **Bronze:** Ingestão dos dados brutos com histórico completo.
2.  **Silver:** Dados limpos e integrados, utilizando lógica de *Upsert* (Merge) para manter a consistência com a origem.
3.  **Gold:** Tabelas agregadas e prontas para o consumo de BI.

---

## 🚀 Tecnologias Utilizadas
*   **Databricks:** Plataforma de processamento e governança.
*   **Apache Spark (PySpark & SQL):** Motor de transformação de dados.
*   **Auto Loader:** Ingestão incremental eficiente de arquivos CSV com detecção de novos arquivos.
*   **JDBC:** Conexão segura para extração de dados do Azure SQL Server.
*   **Unity Catalog & Volumes:** Governança de dados e gerenciamento de arquivos.
*   **Databricks Jobs:** Orquestração de workflows complexos e dependências.
*   **Secret Scopes:** Armazenamento seguro de credenciais e tokens.

---

## 🛠️ Framework Metadata-Driven
A pipeline é controlada por quatro tabelas de metadados que permitem a reusabilidade do código:
*   **Tables:** Define nomes, sistemas de origem e camadas de destino.
*   **Table Parameters:** Define estratégias de carga (Merge, Append, Full Load) e chaves primárias.
*   **Table Watermarks:** Armazena valores para controle de cargas incrementais.
*   **Pipeline Runs (Audit):** Registra logs de execução, status e volumetria.

---

## 📂 Dashboards de Negócio
Os dados da camada Gold são consumidos através de Dashboards interativos divididos por áreas de interesse:

### 1. Executive Dashboard
Visão macro dos principais KPIs do banco.
*   **Métricas:** Total de clientes, depósitos totais, volume de transações e clientes de alto risco.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/fd76963e-b0d2-449b-bdb3-d25b5f43ef56" />


### 2. Customer Insights
Análise detalhada da base de clientes.
*   **Visualizações:** Distribuição por segmento (High, Medium, Low value), perfil de risco de crédito (Pie Chart) e lista dos principais clientes por saldo.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/2e8d2570-9eff-46d3-b800-e8942a30c41e" />


### 3. Branch Performance
Desempenho por agência/unidade.
*   **Visualizações:** Depósitos por agência, volume de clientes por unidade e total transacionado por filial.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/ace1d3b6-ec10-4ee7-a75f-5cb70ace5f9a" />


### 4. Gateway & Device Insights
Monitoramento técnico e operacional de transações.
*   **Visualizações:** Sucesso vs. Falhas por Gateway de pagamento e distribuição de transações por tipo de dispositivo (Mobile, Web, etc.).
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/4d3f5058-3230-48ac-a4cf-0349958d4138" />


---

## ⚙️ Configuração e Execução
1.  **Segurança:** Crie um **Secret Scope** no Databricks para armazenar as credenciais do SQL Server (Host, Port, User, Password).
2.  **Setup:** Execute o notebook de configuração de metadados para criar o catálogo, schemas e tabelas de controle.
3.  **Orquestração:** Configure o **Master Job** para executar sequencialmente as ingestões (SQL e Blob), as transformações para Gold e, por fim, o refresh automático dos dashboards.

---
**Autor:** [Seu Nome]
*Projeto baseado no framework de engenharia de dados end-to-end (DataBeli).*
