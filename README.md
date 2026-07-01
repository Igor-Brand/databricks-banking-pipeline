Este é um modelo de **README.md** estruturado para o seu projeto no GitHub, baseado no framework de engenharia de dados para o **Neo Bank** utilizando a arquitetura Medallion no Databricks.

---

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
**Autor:** [Seu Nome]
*Projeto baseado no tutorial de Narendra Kumar (DataBeli).*
