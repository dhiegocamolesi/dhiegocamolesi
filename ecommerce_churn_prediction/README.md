# 🛒 Churn de Clientes no E-commerce Olist com Databricks

Este projeto analisa e prevê o churn (abandono) de clientes em um e-commerce, utilizando a base pública da Olist. O pipeline completo foi desenvolvido na plataforma **Databricks**, 
aproveitando **PySpark**, **Delta Lake**, **MLflow** e um painel interativo com **Streamlit**.

## 🔍 Visão Geral

O objetivo foi identificar padrões de comportamento de clientes que deixam de comprar, criando uma base robusta de features e treinando um modelo de machine learning para prever churn. 

## Pipeline de Dados
ETL: Ingestão de múltiplos datasets do e-commerce Olist e persistência em Delta Lake.

Engenharia de Atributos: Criação de variáveis agregadas por cliente e definição de churn (>180 dias inativo).

Análise Exploratória: Comportamento de pedidos ao longo do tempo, avaliação de clientes, atrasos na entrega.

Modelagem: Treinamento com Random Forest e avaliação via AUC.

## Principais Resultados
Base de churn criada com mais de 90 mil clientes.

Modelo de machine learning com AUC ≈ 0.86 (exemplo).

Dashboard interativo com filtros por volume de compras e gasto total.

Processo rastreável e reprodutível com MLflow e Spark.
---

## 📁 Estrutura do Projeto

```text
├── ETL_Pedidos.py              # Pipeline de ingestão e transformação com Delta Lake
├── engenharia_recursos.py      # Criação da base de features para churn
├── analises_exploratorias.py   # Análise descritiva dos dados (pedidos, clientes, pagamentos)
├── treinar_modelo.py           # Treinamento de modelo Random Forest + MLflow
├── app.py                      # Aplicação Streamlit com filtros e visualizações
├── churn_features.csv          # Amostra da base final usada no app
