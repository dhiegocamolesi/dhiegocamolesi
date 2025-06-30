# Databricks notebook source
from pyspark.sql.functions import col, to_date

#display(dbutils.fs.ls("dbfs:/Volumes/workspace/ecommerce_olist/ecommerce_olist/"))

df = spark.read.csv("dbfs:/Volumes/workspace/ecommerce_olist/ecommerce_olist/customers_dataset.csv", header=True, inferSchema=True)
df.display()


# COMMAND ----------

# src/etl.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
import os

TABELAS = {
    "pedidos": "orders_dataset.csv",
    "clientes": "customers_dataset.csv",
    "pagamentos": "order_payments_dataset.csv",
    "produtos": "products_dataset.csv",
    #"categorias": "product_category_name_translation.csv",
    "itens": "order_items_dataset.csv",
    "vendedores": "sellers_dataset.csv",
    "reviews": "order_reviews_dataset.csv"
}

RAW_PATH = "dbfs:/Volumes/workspace/ecommerce_olist/ecommerce_olist/"
PROCESSED_PATH = "dbfs:/Volumes/workspace/ecommerce_olist/processed"

#sessão Spark com nome “ETL_Ecommerce”. Essencial para usar o PySpark.
def iniciar_spark(app_name="ETL_Ecommerce"):
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    return spark

def carregar_dados(spark, arquivo):
    caminho_completo = os.path.join(RAW_PATH, arquivo)
    return spark.read.csv(caminho_completo, header=True, inferSchema=True)

def limpar_dados(df):
    return df.dropna(how='all')

#Salva o DataFrame no formato Delta Lake, que permite controle de versões e performance melhor que CSV
def salvar_delta(df, nome_tabela):
    destino = os.path.join(PROCESSED_PATH, nome_tabela)
    df.write.format("delta").mode("overwrite").save(destino)

def tratar_colunas(df, nome_tabela):
    if nome_tabela == "pedidos":
        df = df.withColumn("order_purchase_timestamp", to_date(col("order_purchase_timestamp")))
    return df

if __name__ == "__main__":
    spark = iniciar_spark()

    for nome, arquivo in TABELAS.items():
        print(f"Processando: {nome}")
        df = carregar_dados(spark, arquivo)
        df = limpar_dados(df)
        df = tratar_colunas(df, nome)
        salvar_delta(df, nome)

    spark.stop()



# COMMAND ----------

#Carregar um DataFrame com Spark e visualizar
df_pedidos = spark.read.format("delta").load("dbfs:/Volumes/workspace/ecommerce_olist/processed/pedidos")
#df_pedidos.display()
df_pedidos.limit(5).toPandas()




# COMMAND ----------

#Registrar suas tabelas Delta no catálogo Unity, para consultas sql

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Registrar_Tabelas_Olist").getOrCreate()

# Dicionário das tabelas e seus caminhos Delta
tabelas = {
    "pedidos": "dbfs:/Volumes/workspace/ecommerce_olist/processed/pedidos",
    "clientes": "dbfs:/Volumes/workspace/ecommerce_olist/processed/clientes",
    "pagamentos": "dbfs:/Volumes/workspace/ecommerce_olist/processed/pagamentos",
    "produtos": "dbfs:/Volumes/workspace/ecommerce_olist/processed/produtos",
    "itens": "dbfs:/Volumes/workspace/ecommerce_olist/processed/itens",
    "vendedores": "dbfs:/Volumes/workspace/ecommerce_olist/processed/vendedores",
    "reviews": "dbfs:/Volumes/workspace/ecommerce_olist/processed/reviews"
}

# Nome do banco/schema
database = "ecommerce"

# Cria schema se não existir
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

# Registra as tabelas no catálogo
for nome, caminho in tabelas.items():
    print(f"Registrando tabela: {nome}")
    df = spark.read.format("delta").load(caminho)
    df.write.format("delta").mode("overwrite").saveAsTable(f"{database}.{nome}")

print("Tabelas registradas com sucesso!")
