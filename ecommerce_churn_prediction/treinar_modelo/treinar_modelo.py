# src/train_model.py

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline
import mlflow
import mlflow.spark

# Iniciar Spark
spark = SparkSession.builder.appName("TreinarModeloChurn").getOrCreate()

# Carregar base de features
df = spark.table("ecommerce.churn_features")

# Selecionar colunas
colunas_features = ["qtd_pedidos", "valor_total", "media_avaliacao", "dias_desde_ultima_compra"]
coluna_target = "churn"

# Remover registros com valores nulos nas features
df = df.select(colunas_features + [coluna_target]).dropna()

# Separar treino e teste
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

# Preparar pipeline
assembler = VectorAssembler(inputCols=colunas_features, outputCol="features")
rf = RandomForestClassifier(labelCol=coluna_target, featuresCol="features", numTrees=50)

pipeline = Pipeline(stages=[assembler, rf])

# Iniciar experimento MLflow
mlflow.set_experiment("/ecommerce_olist/churn_model")

with mlflow.start_run():
    modelo = pipeline.fit(train_df)
    predicoes = modelo.transform(test_df)

    # Avaliação
    evaluator = BinaryClassificationEvaluator(labelCol=coluna_target, metricName="areaUnderROC")
    auc = evaluator.evaluate(predicoes)

    # Logar no MLflow
    mlflow.log_param("num_trees", 50)
    mlflow.log_metric("AUC", auc)
    mlflow.spark.log_model(modelo, "model")

    print(f"Modelo treinado e registrado com AUC = {auc:.4f}")
