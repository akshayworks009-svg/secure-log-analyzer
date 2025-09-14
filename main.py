from fastapi import FastAPI
from pyspark.sql import SparkSession
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spark session lazily
spark = None

def get_spark():
    global spark
    if not spark:
        spark = SparkSession.builder \
            .appName("SecureLogAnalyzer") \
            .master("local[*]") \
            .getOrCreate()
    return spark

@app.get("/")
def home():
    return {"message": "Hello, This is Secure Log Analyzer with PySpark!"}

@app.get("/spark")
def get_spark_data():
    try:
        spark = get_spark()
        data = [("Akshay", 30), ("Sonu",28), ("User",25)]
        columns = ["Name", "Age"]
        df = spark.createDataFrame(data, columns)
        result = df.toPandas().to_dict(orient="records") 
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}