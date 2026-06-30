
# Databricks Banking Data Pipeline (End-to-End)

## 📝 Descrição do Projeto
Este projeto demonstra a construção de uma **plataforma de dados completa e orientada a metadados** usando o **Databricks (Free Edition)**. O objetivo foi resolver os desafios de ingestão, processamento e análise de grandes volumes de dados de um setor bancário fictício (*Neo Bank*), integrando fontes heterogêneas em um ambiente unificado.

## 🚀 Principais Tecnologias
* **Plataforma:** Databricks (Medallion Architecture).
* **Linguagem:** PySpark & Spark SQL.
* **Governança:** Unity Catalog & Secret Scopes.
* **Orquestração:** Databricks Workflows (Jobs).
* **Consumo:** Databricks Dashboards & Genie Workspace (IA).

## 🏗️ Arquitetura (Medallion)
O pipeline segue o padrão de camadas para garantir a qualidade e a confiabilidade dos dados:
1. **Bronze (Raw):** Ingestão bruta de dados vindos de *SQL Server* (via JDBC) e *Arquivos CSV* (via Auto Loader).
2. **Silver (Refined):** Processamento incremental, limpeza e estruturação dos dados.
3. **Gold (Analytics):** Transformações agregadas prontas para consumo de negócio, com tabelas prontas para relatórios.

## ⚙️ Diferenciais do Projeto
* **Framework Metadata-Driven:** Estrutura reutilizável que permite adicionar novas tabelas ao pipeline apenas configurando metadados, sem alterar o código principal.
* **Orquestração Inteligente:** Master pipeline que gerencia dependências e auditoria de cada execução.
* **Governança e Segurança:** Implementação de *Secret Scopes* para manuseio seguro de credenciais e *Unity Catalog* para controle de acesso.
* **Self-Service Analytics:** Dashboards interativos e interface de IA (*Genie Workspace*) permitindo consultas em linguagem natural.

## 📂 Estrutura do Repositório
text
├── metadata/          # Configuração dos metadados e tabelas de auditoria
├── ingestion/         # Notebooks para carregamento (Bronze/Silver)
├── transformation/    # Notebooks de transformação (Gold)
├── orchestration/     # Scripts de automação e envio de emails
└── dashboard/         # Queries para construção dos dashboards
