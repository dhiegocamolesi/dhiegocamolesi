# Databricks notebook source
# Notebook explora as tabelas tratadas do dataset Olist no Databricks.
# Ele gera estatísticas descritivas e visualizações com foco em pedidos, clientes e pagamentos.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, avg, max, min, sum, count, year, month
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



# COMMAND ----------

spark = SparkSession.builder.getOrCreate()

# Carregar tabelas Delta
pedidos = spark.table("ecommerce.pedidos")
clientes = spark.table("ecommerce.clientes")
pagamentos = spark.table("ecommerce.pagamentos")
itens = spark.table("ecommerce.itens")
reviews = spark.table("ecommerce.reviews")

# 1. Contagem de registros
print("\nTotal de Pedidos:", pedidos.count())
print("Total de Clientes:", clientes.select("customer_unique_id").distinct().count())
print("Total de pagamentos:", pagamentos.count())

# 2. Status dos pedidos
pedidos.groupby("order_status").count().orderBy("count", ascending=False).display()

# 3. Pedidos ao longo do tempo
pedidos_data = pedidos.withColumn("ano", year("order_purchase_timestamp"))\
                      .withColumn("mes", month("order_purchase_timestamp"))
pedidos_mes = pedidos_data.groupBy("ano", "mes").count().orderBy("ano", "mes")

pd_pedidos_mes = pedidos_mes.toPandas()
plt.figure(figsize=(12, 6))
sns.lineplot(data=pd_pedidos_mes, x=pd_pedidos_mes.index, y="count")
plt.title("Pedidos por M\u00eas")
plt.ylabel("Qtde de Pedidos")
plt.xlabel("Tempo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Valor médio por pedido
pagamentos_grouped = pagamentos.groupBy("order_id").agg(sum("payment_value").alias("valor_total"))

stats_valor = pagamentos_grouped.select(
    avg("valor_total").alias("media"),
    min("valor_total").alias("minimo"),
    max("valor_total").alias("maximo")
)
print("\nEstat\u00edsticas de valor total por pedido:")
stats_valor.display()

# 5. Reviews (avalia\u00e7\u00f5es)
reviews.groupBy("review_score").count().orderBy("review_score").display()

# 6. Atrasos na entrega
pedidos = pedidos.withColumn("atraso", (col("order_delivered_customer_date") > col("order_estimated_delivery_date")))
pedidos.groupBy("atraso").count().display()

print("\n--- Fim da An\u00e1lise Explorat\u00f3ria Inicial ---")


