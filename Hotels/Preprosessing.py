import pandas as pd
import ast
import re

def clean_benefits(benefits_str):
    # Check for NaN values
    if pd.isna(benefits_str):
        return ''
    
    try:
        # Convert string representation of list to actual list
        benefits_list = ast.literal_eval(benefits_str)
        # Remove items with "+.."
        cleaned_benefits = [benefit.strip() for benefit in benefits_list if not benefit.strip().startswith('+')]
        # Convert list to comma-separated string
        return ', '.join(cleaned_benefits)
    except (ValueError, SyntaxError):
        # If there's an error in conversion, return an empty string
        return ''
def clean_price(price):
    # Replace commas with dots to handle decimal points correctly
    cleaned_price = re.sub(r'[^\d,]', '', price).replace(',', '.')
    if cleaned_price.count('.') > 1:
        cleaned_price = cleaned_price.replace('.', '', cleaned_price.count('.') - 1)
    return float(cleaned_price) if cleaned_price else None


def clean_rating(rating):
    try:
        # Convert rating to float, ensuring correct format
        return float(rating.replace(',', '.')) if isinstance(rating, str) else rating
    except ValueError:
        return None

def clean_hotel_data(file_path):
    # Load the data
    df = pd.read_csv(file_path)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Remove the "đ" character from the Price column but keep it as string
    df['Price'] = df['Price'].apply(clean_price)
    
    # Apply the clean_benefits function to clean the benefits column
    df['Benefits'] = df['Benefits'].apply(clean_benefits)
    # Clean the Rating column
    df['Rating'] = df['Rating'].apply(clean_rating)
    
    # Add a Hotel ID column
    df.reset_index(drop=True, inplace=True)
    df['HotelID'] = df.index + 1
    # Load the existing combined hotel data
    output_path = 'TRAVELPLANNING\Hotels\combined_hotel_data2.csv'
    combined_hotel_df = pd.read_csv(output_path)
    
    # Append the new cleaned hotel data
    updated_combined_hotel_df = pd.concat([combined_hotel_df, df], ignore_index=True)
    
    # Save the updated DataFrame back to the combined CSV file
    updated_combined_hotel_df.to_csv(output_path, index=False)
    
    return updated_combined_hotel_df



# Example usage
# file_path = r'E:\Grab Final Prj\TRAVELPLANNING\Hotels\hotel_data3.csv'  # Use raw string
# # df = pd.read_csv(file_path)
# # df['Rating'] = df['Rating'].astype(str).str.replace(',', '.').str.strip()
# # df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
# # cleaned_file_path = "cleaned_hotel_data19.csv"
# # df.to_csv(cleaned_file_path, index=False)

# # # # or file_path = 'E:\\Grab Final Prj\\TRAVELPLANNING\\Hotels\\Hotel_data_DN.csv'  # Use double backslashes

# df, cleaned_file_path = clean_hotel_data(file_path)
# print(df.head())
# print(f"Cleaned data saved to {cleaned_file_path}")

