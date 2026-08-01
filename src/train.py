"""
Script de entrenamiento de modelos de Machine Learning (Random Forest) con PySpark.
"""
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

def create_spark_session(app_name="Tokio_Telecom_Train"):
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def build_pipeline():
    numeric_cols = ["Age", "Tenure", "Usage Frequency", "Support Calls", "Payment Delay", "Total Spend", "Last Interaction"]
    categorical_cols = ["Gender", "Subscription Type", "Contract Length"]
    
    indexers = [StringIndexer(inputCol=c, outputCol=c+"_idx", handleInvalid="keep") for c in categorical_cols]
    encoders = [OneHotEncoder(inputCol=c+"_idx", outputCol=c+"_ohe") for c in categorical_cols]
    assembler = VectorAssembler(inputCols=numeric_cols + [c+"_ohe" for c in categorical_cols], outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)
    
    rf = RandomForestClassifier(labelCol="label", featuresCol="features", seed=42)
    
    pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, rf])
    return pipeline, rf

def train_model(spark, data_path):
    df = spark.read.parquet(data_path)
    train, test = df.randomSplit([0.7, 0.3], seed=42)
    
    pipeline, rf = build_pipeline()
    
    grid = (ParamGridBuilder()
            .addGrid(rf.numTrees, [50, 120])
            .addGrid(rf.maxDepth, [5, 8])
            .build())
            
    evaluator = BinaryClassificationEvaluator(labelCol="label", metricName="areaUnderROC")
    
    cv = CrossValidator(estimator=pipeline, 
                        estimatorParamMaps=grid,
                        evaluator=evaluator, 
                        numFolds=3, 
                        parallelism=2, 
                        seed=42)
                        
    print("Entrenando modelo Random Forest...")
    cv_model = cv.fit(train)
    best_model = cv_model.bestModel
    
    auc_test = evaluator.evaluate(best_model.transform(test))
    print(f"Entrenamiento completado. AUC en Test: {auc_test:.4f}")
    
    # Opcional: Guardar modelo
    # best_model.save("../model/rf_churn_model")

if __name__ == "__main__":
    spark = create_spark_session()
    processed_data_path = "../data/processed/churn_features.parquet"
    train_model(spark, processed_data_path)
    spark.stop()
