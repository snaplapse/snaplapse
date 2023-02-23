from turtle import pd
from sklearn.neighbors import NearestNeighbors

import requests
import json
import pandas as pd
import time
import sys

st = time.time()

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.max_columns = None

def load_data(latitude, longitude, radius):
    # Get locations
    nearby_locations_url = ("http://localhost:8000/api/nearbyLocations?coordinates={},{}&radius={}").format(latitude, longitude, radius)
    get_locations = json.loads(requests.get(nearby_locations_url).content.decode("utf-8"))
    locations_list = []
    counter = 0
    for location in get_locations["results"]:
        categories = []
        
        # HARDCODED CATEGORY SETTING UNTIL CATEGORIES ARE IMPLEMENTED IN LOCATIONS ROUTE
        if counter == 0:
            categories = ['food','restaurant']
        elif counter == 1:
            categories = ['university', 'point_of_interest', 'establishment']
        elif counter == 2:
            categories = ['food','restaurant']
        elif counter == 3:
            categories = ['food','point_of_interest']
        locations_list.append((location['id'], location['name'], location['latitude'], location['longitude'], categories))
        # print(location)
        counter = counter + 1
    locations = pd.DataFrame(locations_list, columns = ['location_id', 'name', 'latitude', 'longitude', 'categories']).sort_values(by=['location_id'])
    locations.set_index('location_id', drop=False, inplace=True)
    # print(locations)

    # Get likes
    get_likes = json.loads(requests.get("http://localhost:8000/api/locationsLikeCountsAllUsers/").content.decode("utf-8"))
    likes_list = []
    for like in get_likes["results"]:
        likes_list.append((like["user_id"], like["location_id"], like["likes"]))
    likes = pd.DataFrame(likes_list, columns = ['user_id', 'location_id', 'likes'])
    likes.set_index('location_id', drop=False, inplace=True)
    # print(likes)
    
    return likes, locations

def generate_affinity_recommendations(user_id, likes, locations, num_recs):
    locations_with_categories = locations.copy(deep=True)

    # Iterate through locations and append the location categories as columns of 1s or 0s. 1 if the location at the present index contains the category and 0 if not.
    for index, row in locations.iterrows():
        for category in row['categories']:
            locations_with_categories.at[index, category] = 1
    # Fill in the NaN values with 0
    locations_with_categories = locations_with_categories.fillna(0)

    # Grab the likes of the indicated user
    user_likes = likes[likes['user_id'] == user_id]
    # Filter to only the relevant categories by selecting locations that exist in both user_likes and locations_with_categories
    user_categories = locations_with_categories[locations_with_categories.location_id.isin(user_likes.location_id)]
    # Drop redundant columns
    user_categories.drop(['location_id','name','latitude', 'longitude','categories'], axis=1, inplace=True)

    # Take dot product of transpose of user_categories by user_likes column to get user category affinities
    user_affinities = user_categories.T.dot(user_likes.likes)

    # Delete unnecessary columns
    locations_with_categories.drop(['location_id','name','categories','latitude','longitude'], axis=1, inplace=True)

    user_affinities_reshaped = user_affinities.values.reshape(1, -1)
    # technically we don't need to normalize since only the angle matters in cosine similarity
    # user_affinities_normalized = (user_affinities_reshaped-user_affinities_reshaped.min())/(user_affinities_reshaped.max()-user_affinities_reshaped.min())
    # print(user_affinities_normalized)

    # Create KNN nearest neighbors model with cosine distance to find the nearest neighbor locations based on category affinity
    model = NearestNeighbors()
    model.set_params(**{
        'n_neighbors': 10,
        'algorithm': 'brute',
        'metric': 'cosine',
        'n_jobs': -1})
    model.fit(locations_with_categories.values)
    indices = model.kneighbors(user_affinities_reshaped, n_neighbors=num_recs, return_distance=False)
    knn_index_to_loc_index = list(locations_with_categories.index.values[indices])[0]

    # Create list of recommendations
    affinity_recs = []
    locations.rename(columns={'location_id': 'id'}, inplace=True)
    for location_id in knn_index_to_loc_index:
        row = locations[locations['id'] == location_id].to_json(orient='records')
        affinity_recs.append(json.loads(row[1:len(row)-1]))
    
    return affinity_recs

def make_recommendations(user_id, latitude, longitude, radius):
    likes, locations = load_data(latitude, longitude, radius)
    num_recs = 10
    if len(locations) < num_recs:
        num_recs = len(locations)

    affinity_recs = generate_affinity_recommendations(user_id, likes, locations, num_recs)
    return affinity_recs

def print_recommendations(recommendations):
    print('Recommendations based on user category affinity:')
    for i, rec in enumerate(recommendations):
        print('{0}: {1}'.format(i, rec['name']))

def main():
    if len(sys.argv) == 5:
        user_id = int(sys.argv[1])
        latitude = sys.argv[2]
        longitude = sys.argv[3]
        radius = sys.argv[4]
    else:
        print("Usage: python recommender.py [user_id] [latitude] [longitude] [radius]")
        return -1    
        
    affinity_recs = make_recommendations(user_id, latitude, longitude, radius)
    print_recommendations(affinity_recs)

    et = time.time()
    print("\nRuntime: ", et-st)

if __name__ == "__main__" :
    main()