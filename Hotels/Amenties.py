import pandas as pd
from collections import Counter

def calculate_benefits_rank(file_path):
    # Load the cleaned data
    df = pd.read_csv(file_path)
    
    # Ensure all values in the Benefits column are strings
    df['Benefits'] = df['Benefits'].astype(str)
    
    # Extract the benefits column and convert it to a list of lists
    benefits_list = df['Benefits'].apply(lambda x: x.split(', ') if x != 'nan' else [])
    
    # Flatten the list of lists into a single list
    all_benefits = [benefit for sublist in benefits_list for benefit in sublist]
    
    # Count the frequency of each benefit
    benefits_counter = Counter(all_benefits)
    
    # Convert the counter to a DataFrame
    benefits_freq_df = pd.DataFrame(benefits_counter.items(), columns=['Benefit', 'Frequency'])
    
    # Sort the DataFrame by frequency in descending order and rank
    benefits_freq_df = benefits_freq_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
    benefits_freq_df['Rank'] = benefits_freq_df.index + 1
    
    return benefits_freq_df

cleaned_file_path = r'E:\Grab Final Prj\combined_hotel_data2.csv'  # Use raw string
benefits_rank_df = calculate_benefits_rank(cleaned_file_path)
file_path = 'Amentities_rank2.csv'
benefits_rank_df.to_csv(file_path, index=True)
print(benefits_rank_df)

