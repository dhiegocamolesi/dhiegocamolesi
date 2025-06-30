from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, datediff, max as spark_max

spark = SparkSession.builder.appName("FeatureEngineering_Churn").getOrCreate()

# Carregar tabelas
pedidos = spark.table("ecommerce.pedidos")
clientes = spark.table("ecommerce.clientes")
pagamentos = spark.table("ecommerce.pagamentos")
itens = spark.table("ecommerce.itens")
reviews = spark.table("ecommerce.reviews")

# Criar base com último pedido por cliente
pedidos_filtrados = pedidos.select("customer_id", "order_id", "order_status", "order_purchase_timestamp")
ultimo_pedido = pedidos_filtrados.groupBy("customer_id").agg(
    spark_max("order_purchase_timestamp").alias("ultima_compra")
)

# Contagem de pedidos por cliente
pedidos_por_cliente = pedidos_filtrados.groupBy("customer_id").agg(
    count("order_id").alias("qtd_pedidos")
)

# Valor total gasto por cliente
pagamentos_total = pagamentos.join(pedidos.select("order_id", "customer_id"), on="order_id") \
    .groupBy("customer_id").agg(sum("payment_value").alias("valor_total"))

# Média de avaliação por cliente
reviews_avg = reviews.join(pedidos.select("order_id", "customer_id"), on="order_id") \
    .groupBy("customer_id").agg(avg("review_score").alias("media_avaliacao"))

# Juntar todas
base = pedidos_por_cliente \
    .join(pagamentos_total, on="customer_id", how="left") \
    .join(reviews_avg, on="customer_id", how="left") \
    .join(ultimo_pedido, on="customer_id", how="left")


# Criar variável alvo de churn: churn = 1 se a última compra foi há mais de 180 dias
from pyspark.sql.functions import current_date, when
base = base.withColumn("dias_desde_ultima_compra", datediff(current_date(), col("ultima_compra")))
base = base.withColumn("churn", when(col("dias_desde_ultima_compra") > 180, 1).otherwise(0))

# Salvar como tabela Delta no catálogo
base.write.format("delta").mode("overwrite").saveAsTable("ecommerce.churn_features")

print("Base de churn criada com sucesso: ecommerce.churn_features")
