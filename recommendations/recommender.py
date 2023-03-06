import json
import time
import sys
import pandas as pd
import requests

from sklearn.neighbors import NearestNeighbors

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.max_columns = None

def load_data(host, latitude, longitude, radius):
    # Get locations
    nearby_locations_url = f"http://{host}/api/locations/nearby?coordinates={latitude},{longitude}&radius={radius}"
    get_locations = json.loads(requests.get(nearby_locations_url, timeout=10).content.decode("utf-8"))
    locations_list = []
    for location in get_locations['results']:
        locations_list.append((location['id'], location['name'], location['latitude'], location['longitude'], location['categories'], location['google_id']))
    locations = pd.DataFrame(locations_list, columns = ['location_id', 'name', 'latitude', 'longitude', 'categories', 'google_id']).sort_values(by=['location_id'])
    locations.set_index('location_id', drop=False, inplace=True)
    # print(locations)

    # Get likes
    likes_url = f"http://{host}/api/locations/likes/"
    get_likes = json.loads(requests.get(likes_url, timeout=10).content.decode("utf-8"))
    likes_list = []
    for like in get_likes["results"]:
        likes_list.append((like["user_id"], like["location_id"], like["likes"]))
    likes = pd.DataFrame(likes_list, columns = ['user_id', 'location_id', 'likes'])
    likes.set_index('location_id', drop=False, inplace=True)
    # print(likes)

    return likes, locations

def dataframe_to_json_list(dataframe, indices):
    result = []
    for index in indices:
        row = dataframe[dataframe['id'] == index].to_json(orient='records')
        result.append(json.loads(row[1:len(row)-1])) # removes square brackets messing with format

    return result

def generate_affinity_recommendations(user_id, likes, locations, num_recs):
    locations_with_categories = locations.copy(deep=True)

    # Iterate through locations and append the location categories as columns of 1s or 0s. 1 if the location at the present index contains the category and 0 if not.
    for index, row in locations.iterrows():
        for category in row['categories']:
            locations_with_categories.at[index, category] = 1
    # Fill in the NaN values with 0
    locations_with_categories = locations_with_categories.fillna(0)

    # Get only the likes of the indicated user
    user_likes = likes[likes['user_id'] == user_id]
    # Filter to only the relevant categories by selecting locations that exist in both user_likes and locations_with_categories
    user_categories = locations_with_categories[locations_with_categories.location_id.isin(user_likes.location_id)]

    # Return locations as is if no matching categories with likes
    if user_categories.empty: 
        locations = locations.rename(columns={'location_id': 'id'})
        return dataframe_to_json_list(locations, locations.index)

    # Drop redundant columns
    user_categories.drop(['location_id','name','latitude', 'longitude','categories','google_id'], axis=1, inplace=True)
    # Take dot product of transpose of user_categories by user_likes column to get user category affinities
    user_affinities = user_categories.T.dot(user_likes.likes)

    # Delete unnecessary columns
    locations_with_categories.drop(['location_id','name','latitude','longitude','categories','google_id'], axis=1, inplace=True)

    user_affinities = user_affinities.values.reshape(1, -1)

    # Create KNN nearest neighbors model with cosine distance to find the nearest neighbor locations based on category affinity
    model = NearestNeighbors()
    model.set_params(**{
        'algorithm': 'brute',
        'metric': 'cosine',
        'n_jobs': -1})
    model.fit(locations_with_categories.values)
    indices = model.kneighbors(user_affinities, n_neighbors=num_recs, return_distance=False)
    knn_index_to_loc_index = list(locations_with_categories.index.values[indices])[0]

    # Create list of recommendations
    locations = locations.rename(columns={'location_id': 'id'})
    affinity_recs = dataframe_to_json_list(locations, knn_index_to_loc_index)
    
    return affinity_recs

def generate_user_recommendations(likes, locations, affinity_recs, num_recs):
    locations = locations.rename(columns={'location_id': 'id'})
    num_locations = len(locations.index)

    pivot_likes = likes.pivot(columns='user_id', values='likes')

    # Append locations without likes as 0 likes for all users
    for index in locations.index:
        if index not in pivot_likes.index: 
            location = pd.DataFrame(0, index=[index], columns=pivot_likes.columns)
            pivot_likes = pd.concat([pivot_likes, location])

    # Fill in the NaN values with 0
    pivot_likes = pivot_likes.fillna(0)
    pivot_likes.sort_index(inplace=True)

    # Create KNN nearest neighbors model with cosine distance to find the nearest neighbor locations based on similar user likes
    model = NearestNeighbors()
    model.set_params(**{
        'algorithm': 'brute',
        'metric': 'cosine',
        'n_jobs': -1})
    model.fit(pivot_likes.values)
    
    user_rec_ids = []
    for i in range(0, num_recs):
        seed_id = affinity_recs[i]['id']
        seed = pivot_likes.loc[[seed_id]]

        found = False
        n = 10 if num_locations > 10 else num_locations
        while True:
            # Generate nearest neighbours
            indices = model.kneighbors(seed, n_neighbors=n, return_distance=False)
            
            # Check list of neighbors for a non-duplicate to add as rec
            for id in list(locations.index.values[indices])[0]:
                if not any(r['id'] == id for r in affinity_recs) and id not in user_rec_ids:
                    user_rec_ids.append(id)
                    found = True
                    break

            if found:
                break

            if n < num_locations: # if still not found, generate 10 more and keep checking
                n = n + 10 if num_locations > n + 10 else num_locations
            else: # if out of locations return as is
                user_recs = dataframe_to_json_list(locations, user_rec_ids)
                return user_recs

    user_recs = dataframe_to_json_list(locations, user_rec_ids)

    return user_recs

def make_recommendations(host, user_id, latitude, longitude, radius, num_recs):
    likes, locations = load_data(host, latitude, longitude, radius)
    if len(locations) == 0:
        return locations.to_dict('records')
    if len(likes) == 0:
        return locations.rename(columns={'location_id': 'id'}).head(num_recs).to_dict('records')

    if len(locations) < num_recs:
        num_recs = len(locations)

    num_affinity_recs = num_recs//2 if num_recs%2 == 0 else num_recs//2 + 1
    num_user_recs = num_recs//2

    affinity_recs = generate_affinity_recommendations(user_id, likes, locations, num_affinity_recs)
    user_recs = generate_user_recommendations(likes, locations, affinity_recs, num_user_recs)

    recommendations = []
    alength = len(affinity_recs)
    ulength = len(user_recs)
    
    for i in range (0, alength + ulength):
        if i // 2 > ulength:    # if run out of user recs just append affinity recs (affinity recs > user recs)
            recommendations.append(affinity_recs.pop(0))
        else: 
            if i % 2 == 0:  # alternates between affinity and user recs
                recommendations.append(affinity_recs.pop(0))
            elif i % 2 == 1:
                recommendations.append(user_recs.pop(0))

    return recommendations

def print_recommendations(recommendations):
    print('Recommendations based on user category affinity:')
    for i, rec in enumerate(recommendations):
        print(f"{i+1}: {rec['name']}")

def main():
    start = time.time()

    host = "localhost:8000"
    num_recs = 10 # default
    if len(sys.argv) == 5 or len(sys.argv) == 6:
        user_id = int(sys.argv[1])
        latitude = float(sys.argv[2])
        longitude = float(sys.argv[3])
        radius = float(sys.argv[4])
        if len(sys.argv) == 6:
            num_recs = int(sys.argv[5])
    else:
        print("Usage: python recommender.py [user_id] [latitude] [longitude] [radius] [num_recs]")
        sys.exit()

    recommendations = make_recommendations(host, user_id, latitude, longitude, radius, num_recs)
    print_recommendations(recommendations)

    end = time.time()
    print("\nRuntime: ", end-start)

if __name__ == "__main__" :
    main()
