import pandas as pd

# Read the CSV file
df = pd.read_csv('Hotels/combined_hotel_data2.csv', encoding='utf-8')

# Print the data types of all columns
print(df.dtypes)