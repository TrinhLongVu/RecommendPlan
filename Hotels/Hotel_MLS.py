from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.shell import spark
from pyspark.sql.functions import col, explode
from pyspark.sql import SparkSession
import Preprosessing
import json


def create_spark_session():
    return SparkSession.builder \
        .appName("MyApp") \
        .config("spark.local.dir", "E:/SparkTemp") \
        .getOrCreate()


def preprocess_hotel_data(csvHotelInfo):
    # Initialize Spark session
    spark = create_spark_session()
    
    # Clean the hotel data
    cleaned_csvHotelInfo = Preprosessing.clean_hotel_data(csvHotelInfo)
    
    # Load the cleaned hotel data from CSV
    hotels = spark.read.csv(cleaned_csvHotelInfo, header=True)
    
    return hotels

def initial_files (csvHotelInfo, csvRatingInfo):
    hotels = spark.read.csv(csvHotelInfo, header=True)
    ratingsSpark = spark.read.option("header", True) \
        .csv(csvRatingInfo)
     # Cast the Price column to float
    hotels = hotels.withColumn('Price', col('Price').cast('float'))
    # ratingsSpark.show()
    print(ratingsSpark.head())
    return ratingsSpark,hotels

def calculateSparsity(rating):
    # Count the total number of ratings in the dataset
    numerator = rating.select("ratings").count()

    # Count the number of distinct userIds and distinct hotelIds
    num_users = rating.select("userID").distinct().count()
    num_hotels = rating.select("hotelID").distinct().count()
    print(str(num_users) + ' users')
    print(str(num_hotels) + ' hotels')
    # Set the denominator equal to the number of users multiplied by the number of hotels
    denominator = num_users * num_hotels

    # Divide the numerator by the denominator
    sparsity = (1.0 - (numerator * 1.0) / denominator) * 100
    print("The ratings dataframe is ", "%.2f" % sparsity + "% empty.")

def dataSplit (rating):
    rat = rating.select(col("userID").cast("int").alias("userID"), col("hotelID").cast("int").alias("hotelID"),
                              col("ratings").cast("int").alias("ratings"))
    # Create test and train set
    (train, test) = rat.randomSplit([0.8, 0.2])
    return train,test

# we should save here
def MF_ALS (train,test):

    # initial
    ranks = [6,7,8,9,10,1,2,3,4,5]
    min_error = 0.5
    best_model = None

    for rank in ranks:
        als = ALS(maxIter=5, regParam=0.01,rank=rank, userCol="userID", itemCol="hotelID", ratingCol="ratings",
                  coldStartStrategy="drop")
        model = als.fit(train)
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse", labelCol="ratings", predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print('RMSE OUT={}'.format(rmse))

        if rmse < min_error:
            min_error = rmse
            best_rank = rank
            best_model = model
            print('RMSE IN= {}'.format(min_error))
            print('\nThe best model has {} latent factors'.format(best_rank))
            return best_model



def recommendations(model, userID, hotels, city, budget):
    # Generate recommendations for all users
    userRecs = model.recommendForAllUsers(10)
    nrecommendations = userRecs \
        .withColumn("rec_exp", explode('recommendations')) \
        .select('userID', col("rec_exp.hotelID").alias("rec_hotelID"), col("rec_exp.rating").alias("rec_rating"))

    recsforArr = nrecommendations.join(
        hotels, nrecommendations.rec_hotelID == hotels.HotelID, "inner"
    ).select(
        'userID', 'rec_hotelID', 'Name', 'Price', col("Rating").alias("hotel_rating"), 'Benefits', 'Location'
    )

    recsforArr = recsforArr.filter(col('userID') == userID).filter(col('Location') == city)
    recsforArr = recsforArr.filter(col('Price') <= float(budget))
    recsforArr = recsforArr.orderBy(col('rec_rating').desc())
    recsforArr_json_strings = recsforArr.toJSON().collect()
    
    # Parse JSON strings into a list of dictionaries
    recsforArr_json_list = [json.loads(json_str) for json_str in recsforArr_json_strings]
    
    # Convert the list of dictionaries to a JSON array string
    recsforArr_json = json.dumps(recsforArr_json_list, ensure_ascii=False, indent=4)
    
    return recsforArr_json
