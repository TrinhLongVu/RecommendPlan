import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, explode
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from Hotel_MLS import initial_files, calculateSparsity, dataSplit, MF_ALS, recommendations
import User_profiling
def create_spark_session():
    return SparkSession.builder \
        .appName("MyApp") \
        .config("spark.local.dir", "E:/SparkTemp") \
        .getOrCreate()

def recommend_hotel(user_id, amenities_input, city, budget):
    # Create user profile based on preferred amenities
    user_ratings = User_profiling.user_profile(amenities_input, user_id)
    user_ratings.to_csv('user_profiling_updated.csv', mode='a', header=False, index=False)
    csvHotelInfo = "Hotels/combined_hotel_data2.csv"
    csvRatingInfo = "Hotels/user_profiling_updated.csv"
    
    # Load and preprocess initial files
    ratingsSpark, hotels = initial_files(csvHotelInfo, csvRatingInfo)
    
    # Calculate sparsity
    calculateSparsity(ratingsSpark)
    
    # Split data into training and test sets
    train, test = dataSplit(ratingsSpark)
    
    # Train the model using ALS
    best_model = MF_ALS(train, test)
    
    # Generate recommendations for the new user
    recommendations_df = recommendations(best_model, user_id, hotels, city, budget)
    # recommendations_df.toPandas().to_csv('recommended_hotels.csv', index=False)
    
    return recommendations_df

# if __name__ == "__main__":
#     user_id = 2
#     amenities_input = [0, 1, 2]  # Assuming the user prefers 'Bữa sáng', 'Wifi miễn phí', 'Bãi đậu xe'
#     city = 'Đà Nẵng'
#     budget = 100000000  # Assuming the user has a budget of 100000

#     # Call the recommend_hotel function with the example input
#     recommendations = recommend_hotel(user_id, amenities_input, city, budget)
    
#     # Print the recommendations
#     print(recommendations)
