
import joblib
import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, from_unixtime, avg, count, to_json, udf, window, corr
from pyspark.sql.types import StructType, StructField, StringType, LongType, FloatType, DecimalType, TimestampType
from datetime import datetime, timedelta

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
kafka_topic = config['kafka_topic']

spark = SparkSession.builder.appName("KafkaStructuredStreaming").master("local[*]").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
spark.conf.set("spark.sql.repl.eagerEval.maxNumRows", 1000)

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", kafka_topic)
    .option("startingOffsets", "earliest")
    .load()
)

value_df = kafka_stream.selectExpr("CAST(value as STRING)")

trade_schema = StructType([
    StructField("id", LongType(), True),
    StructField("c", StringType(), True),
    StructField("p", FloatType(), True),
    StructField("s", StringType(), True),
    StructField("t", TimestampType(), True),
    StructField("v", DecimalType(38,10), True),
    StructField("type", StringType(), True)
])

trade = value_df.select(from_json(col("value"), trade_schema).alias("data"))
trade = trade.selectExpr("data.*")

windowed_trade = trade.groupBy(window("t", "5 seconds"), "s").agg(
    count("*").alias("trade_count"),
    avg("p").alias("average_price"),
    avg("v").alias("average_volume"),
    corr("p", "v").alias("price_volume_correlation")
)

def send_data_to_flask(json_data_list):
    flask_url = "http://localhost:5001/updateData"
    headers = {"Content-Type": "application/json"}
    data = json.dumps(json_data_list)
    requests.post(flask_url, data=data, headers=headers)

# def load_model(model_path):
#     return joblib.load(model_path)

# btc_model = load_model('btc_model-price-predict.pkl')

# predict_udf = udf(lambda volume: float(btc_model.predict([[volume]])[0]), FloatType())

# def process_and_predict(batch_df, batch_id):
#     batch_df_with_predictions = batch_df.withColumn("predicted_price", predict_udf(batch_df['average_volume']))
#     send_data_to_flask(batch_df_with_predictions.toJSON().collect())

# query = (windowed_trade.writeStream
#     .outputMode("update")
#     .format("console")
#     .option("truncate", "false")
#     .foreachBatch(process_and_predict)
#     .start())

query = (windowed_trade.writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", "false")
    .foreachBatch(lambda batch_df, batch_id: send_data_to_flask(batch_df.toJSON().collect()))
    .start())

query.awaitTermination()