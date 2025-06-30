# app/app.py

import streamlit as st
import pandas as pd
import altair as alt
import mlflow.pyfunc
from datetime import datetime
from pyspark.sql import SparkSession

st.set_page_config(page_title="Churn de Clientes - E-commerce Olist", layout="wide")
st.title("🔍 Painel de Churn de Clientes - Olist")

# Iniciar Spark
spark = SparkSession.builder.appName("AppChurn").getOrCreate()

# Carregar dados de features
df_spark = spark.table("ecommerce.churn_features")
df = df_spark.toPandas()

# Sidebar
st.sidebar.header("🔎 Filtros")
faixa_pedidos = st.sidebar.slider("Qtde de Pedidos", int(df.qtd_pedidos.min()), int(df.qtd_pedidos.max()), (1, 10))
faixa_valor = st.sidebar.slider("Valor Total Gasto (R$)", float(df.valor_total.min()), float(df.valor_total.max()), (100.0, 500.0))

# Filtrar dados
df_filtros = df[
    (df["qtd_pedidos"].between(*faixa_pedidos)) &
    (df["valor_total"].between(*faixa_valor))
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Clientes", f"{len(df):,}")
col2.metric("Clientes em Churn", f"{df['churn'].sum():,}")
col3.metric("Taxa de Churn", f"{100 * df['churn'].mean():.2f}%")

# Gráfico: Distribuição de churn
st.subheader("Distribuição do Churn por Qtde de Pedidos")
churn_chart = alt.Chart(df_filtros).mark_bar().encode(
    x=alt.X("qtd_pedidos:O", title="Quantidade de Pedidos"),
    y=alt.Y("count():Q", title="Clientes"),
    color=alt.Color("churn:N", scale=alt.Scale(domain=[0, 1], range=["#4CAF50", "#F44336"]), legend=alt.Legend(title="Churn"))
).properties(width=700, height=400)
st.altair_chart(churn_chart)

# Tabela detalhada
st.subheader("Base de Clientes com Churn")
st.dataframe(df_filtros[df_filtros["churn"] == 1].sort_values(by="dias_desde_ultima_compra", ascending=False))
