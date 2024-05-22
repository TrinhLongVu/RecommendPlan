import sys
import os
import pandas as pd
import ast
from Transport.Shuttle import PriceShuttle

sys.path.append(os.path.join(os.path.dirname(__file__), 'Hotels'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Activity'))
                                 
from Activity import recommendActivity
from Hotels.final_hotel_recc import recommend_hotel
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/handle', methods=['POST'])
def recommendation():
## input Activity
    ## ## HERE 
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON data"}), 400
    days = int(data['days'])
    end_point = data['city']
    user_id = int(data['id'])
    types = data['types']
    amenities_input = data['amenities_input']  # Assuming the user prefers 'Bữa sáng', 'Wifi miễn phí', 'Bãi đậu xe'
    budget = data['budget'] # Assuming the user has a budget of 100000

    df =  pd.read_csv('./Activity/data/activity.csv')
    cost_activity = budget * 70 / 100 
    activity = recommendActivity.ActivityRecommend(days, end_point, types , cost_activity, df)
    activity.perform()
    
    ##input Hotel
    recommendations = recommend_hotel(user_id, amenities_input, end_point, (budget - activity.spendingPlan1) / days)
    
    response = {
        'message': 'Data received successfully',
        'data': []
    }

    recommendations_list = ast.literal_eval(recommendations)
    num_recommendations = min(len(recommendations_list), 3)

    # Fill the data list with actual recommendations first
    for i in range(num_recommendations):
        rec = recommendations_list[i]
        response['data'].append({
            'activity': list(getattr(activity, f'finalPlan{i+1}')),
            'total': getattr(activity, f'spendingPlan{i+1}') + rec.get('Price') * days,
            'hotel': rec.get('rec_hotelID')
        })

    # Fill the data list with default values if there are fewer than 3 recommendations
    for i in range(num_recommendations, 3):
        response['data'].append({
            'activity': list(getattr(activity, f'finalPlan{i+1}')),
            'total': getattr(activity, f'spendingPlan{i+1}'),
            'hotel': recommendations_list[0].get('rec_hotelID')
        })
   
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=3005)