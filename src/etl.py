"""
Pipeline ETL para preprocesamiento de datos de Churn con PySpark.
"""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

def create_spark_session(app_name="Tokio_Telecom_ETL"):
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def extract_data(spark, filepath):
    df = spark.read.csv(filepath, header=True, inferSchema=True)
    return df

def transform_data(df):
    # CustomerID debe tratarse como CATEGÓRICA y no usarse en los modelos
    df = df.withColumn("CustomerID", F.col("CustomerID").cast("string"))
    
    # Etiqueta: Yes = 1.0, No = 0.0
    df = df.withColumn("label", F.when(F.col("Churn_YesNo") == "Yes", 1.0).otherwise(0.0))
    
    # Cast de campos numéricos a Double
    num_cols = ["Age", "Tenure", "Usage Frequency", "Support Calls", "Payment Delay", "Total Spend", "Last Interaction"]
    for c in num_cols:
        df = df.withColumn(c, F.col(c).cast(DoubleType()))
        
    return df

def load_data(df, output_path):
    df.write.parquet(output_path, mode="overwrite")

if __name__ == "__main__":
    spark = create_spark_session()
    raw_data_path = "../data/raw/customer_churn_10k.csv"
    processed_data_path = "../data/processed/churn_features.parquet"
    
    print("Iniciando pipeline ETL...")
    df_raw = extract_data(spark, raw_data_path)
    df_transformed = transform_data(df_raw)
    load_data(df_transformed, processed_data_path)
    print("ETL completado con éxito. Datos guardados en formato Parquet.")
    spark.stop()
