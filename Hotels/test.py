# import unittest
# from unittest.mock import patch, MagicMock
# import pandas as pd
# import User_profiling
# import Hotel_MLS
# class TestRecommendHotel(unittest.TestCase):

#     @patch('User_profiling.user_profile')
#     @patch('Hotel_MLS.initial_files')
#     @patch('Hotel_MLS.create_spark_session')
#     def test_recommend_hotel(self, mock_create_spark_session, mock_initial_files, mock_user_profile):
#         # Mock Spark session
#         mock_spark = MagicMock()
#         mock_create_spark_session.return_value = mock_spark
        
#         # Mock initial files
#         ratingsSpark_mock = MagicMock()
#         hotels_mock = MagicMock()
#         mock_initial_files.return_value = (ratingsSpark_mock, hotels_mock)
        
#         # Create a dummy DataFrame for allhotels
#         allhotels_mock = pd.DataFrame({
#             'HotelID': [1, 2, 3],
#             'Benefits': ['Bữa sáng, Wifi miễn phí', 'Bãi đậu xe, Nước uống chào đón', 'Phòng tập miễn phí, Bữa sáng'],
#             'Location': ['Đà Nẵng', 'Nha Trang', 'TPHCM']
#         })
#         hotels_mock.toPandas.return_value = allhotels_mock
        
#         # Mock user profile creation
#         mock_user_profile.return_value = pd.DataFrame({
#             'userID': [1],
#             'hotelID': [1],
#             'ratings': [5.0],
#             'city': ['Đà Nẵng']
#         })

#         from final_hotel_recc import recommend_hotel
        
#         # Call the function
#         recommend_hotel(user_id=1, amenities_input=[0, 1, 2], city='Đà Nẵng', budget=100000)
        
#         # Check if the user profile was created correctly
#         mock_user_profile.assert_called_once_with([0, 1, 2], 1, allhotels_mock)
        
#         # Check if the DataFrame was saved correctly
#         pd.testing.assert_frame_equal(mock_user_profile.return_value, pd.DataFrame({
#             'userID': [1],
#             'hotelID': [1],
#             'ratings': [5.0],
#             'city': ['Đà Nẵng']
#         }))

# if __name__ == '__main__':
#     unittest.main()
