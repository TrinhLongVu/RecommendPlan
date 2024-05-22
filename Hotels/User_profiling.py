import pandas as pd
import random
import unicodedata

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return len(lst3)

def normalize_string(s):
    # Normalize to NFC, convert to lowercase, and strip whitespace
    return unicodedata.normalize('NFC', s).strip().lower()

def user_profile(amenities_input, user_id):
    allhotels = pd.read_csv('Hotels/combined_hotel_data2.csv', encoding='utf-8')
    amenities_map = {
        0: 'Bữa sáng',
        1: 'Wifi miễn phí',
        2: 'Bãi đậu xe',
        3: 'Nước uống chào đón',
        4: 'Nhận phòng nhanh',
        5: 'Phòng tập miễn phí',
        6: 'Bữa sáng món chay',
        7: 'Vào hồ bơi miễn phí',
        8: 'Đưa ra sân bay',
        9: 'Nhận phòng trễ',
        10: 'Thuê xe máy',
        11: 'Giảm giá spa',
        12: 'Bao gồm bữa tối',
        13: 'Free mini bar',
        14: 'Thuê xe đạp'
    }

    preferred_amenities = [normalize_string(amenities_map[i]) for i in amenities_input]
    total_num = len(amenities_input)
    
    user_rating_df = []
    print(f"User {user_id} preferred amenities: {preferred_amenities}")
    
    for ind, row in allhotels.iterrows():
        if pd.isna(row['Benefits']):  # Kiểm tra cột 'Benefits'
            continue
        raw_amenities = row['Benefits']
        row_amenities = [normalize_string(a) for a in raw_amenities.split(", ")]
        
        match_count = intersection(row_amenities, preferred_amenities)
        interValue = round((match_count / total_num) * 5, 2)
        
        user_rating_df.append({
            'userID': user_id,
            'hotelID': row['HotelID'],
            'ratings': interValue,
            'city': row['Location']
        })

    return pd.DataFrame(user_rating_df)

# if __name__ == "__main__":
#     num_users = 100  # Adjust the number of users as needed
#     num_amenities = 15  # Total number of amenities available
    
#     # Generate random amenities input for each user
#     amenities_inputs = [random.sample(range(num_amenities), k=random.randint(1, num_amenities)) for _ in range(num_users)]
    
#     allhotels = pd.read_csv('combined_hotel_data2.csv', encoding='utf-8')
    
#     all_user_ratings = pd.DataFrame()
    
#     for i in range(num_users):
#         print(f"Generating profile for user {i + 1}")
#         user_ratings = user_profile(amenities_inputs[i], i + 1)
#         all_user_ratings = pd.concat([all_user_ratings, user_ratings], ignore_index=True)
    
#     print(all_user_ratings)
    
#     # Save the aggregated DataFrame to a new CSV file
#     all_user_ratings.to_csv('user_profiling_updated.csv', index=False)
