from ast import increment_lineno
from turtle import pd

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import sqlite3

conn = sqlite3.connect('test_database')
c = conn.cursor()

c.execute('''
          DROP TABLE IF EXISTS Ratings''')
c.execute('''
          DROP TABLE IF EXISTS Locations''')

c.execute('''
          CREATE TABLE IF NOT EXISTS Ratings
          ([locationId] INTEGER, 
          [location] INTEGER,
          [category] TEXT, 
          [likes] INTEGER,
          [user, item] PRIMARY KEY)
          ''')

c.execute('''
          INSERT INTO Ratings (locationId, location, category, likes)
                VALUES
                (1,'Tim Hortons','F',2),
                (2,'Waterloo Park','N',0),
                (3,'University of Waterloo','S',3),
                (4,'Crunch Fitness Waterloo','G',1),
                (5,'Conestoga Mall','MF',5)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS Locations
          ([locationId] INTEGER PRIMARY KEY, 
          [location] TEXT,
          [proximity] TEXT,
          [category] FLOAT(10))
          ''')

c.execute('''
          INSERT INTO Locations (locationId, location, category, proximity)
                VALUES
                (1,'Tim Hortons','F',1.0),
                (2,'Waterloo Park','N',1.6),
                (3,'University of Waterloo','S',0.5),
                (4,'Crunch Fitness Waterloo','G',2.9),
                (5,'Conestoga Mall','MF',3.8),
                (6,'McDonalds','F',1.8),
                (7,'Victoria Park','N',5.1),
                (8,'Lazeez','F',0.2),
                (9,'Fairview Mall','MF',10.4),
                (10,'PAC Gym','G',0.8)
          ''')

conn.commit()

sql_query = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM Ratings
                               ''', conn)
sql_query2 = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM Locations
                               ''', conn)

ratings = pd.DataFrame(sql_query, columns = ['locationId', 'location', 'category', 'likes'])
print ("Ratings:")
print (ratings)
print ()

locations = pd.DataFrame(sql_query2, columns = ['locationId', 'location', 'category', 'proximity'])
print ("Locations:")
print (locations)
print ()

def main():
    # First let's make a copy of the locations
    locations_with_categories = locations.copy(deep=True)

    # Let's iterate through locations, then append the location categories as columns of 1s or 0s.
    # 1 if that column contains locations in the categories at the present index and 0 if not.
    x = []
    for index, row in locations.iterrows():
        x.append(index)
        for category in row['category']:
            locations_with_categories.at[index, category] = 1

    # Confirm that every row has been iterated and acted upon
    # print(len(x) == len(locations))

    # print(locations_with_categories)

    #Filling in the NaN values with 0 to show that a location doesn't have that column's category
    locations_with_categories = locations_with_categories.fillna(0)
    # print(locations_with_categories.head(3))

    # print out the shape and first five rows of ratings data.
    # print('Ratings_df shape:', ratings.shape)
    # print(ratings.head())

    # filter the selection by outputing locations that exist in both ratings and locations_with_categories
    user_categories = locations_with_categories[locations_with_categories.locationId.isin(ratings.locationId)]
    # print(user_categories)
    # First, let's reset index to default and drop the existing index.
    user_categories.reset_index(drop=True, inplace=True)

    # Next, let's drop redundant columns
    user_categories.drop(['locationId','location','category','proximity'], axis=1, inplace=True)

    # Let's view chamges
    # print(user_categories)

    # let's confirm the shapes of our data frames to guide us as we do matrix multiplication
    # print('Shape of ratings is:', ratings.shape)
    # print('Shape of user_categories is:', user_categories.shape)

    # Let's find the dot product of transpose of user_categories by ratings likes column
    user_profile = user_categories.T.dot(ratings.likes)

    # Let's see the result
    print("User affinities for each category:")
    print(user_profile)
    print()
    

    # let's set the index to the locationId
    locations_with_categories = locations_with_categories.set_index(locations_with_categories.locationId)

    # let's view the head
    # print(locations_with_categories.head())

    # Deleting three unnecessary columns.
    locations_with_proximities = locations.copy(deep=True)
    locations_with_proximities = locations_with_proximities.set_index(locations_with_categories.locationId)
    locations_with_proximities.drop(['locationId','location','category'], axis=1, inplace=True)
    locations_with_categories.drop(['locationId','location','category','proximity'], axis=1, inplace=True)

    # Viewing changes.
    # print("Location-category matrix:")
    # print(locations_with_categories.head())

    locationsDot = locations_with_categories.dot(user_profile)
    print("Location-category scores:")
    print(locationsDot)
    print()
    print("Location proximities:")
    print(locations_with_proximities)
    print()

    # Multiply the categories by the weights and then take the weighted average.
    recommendation_table_df = locationsDot / user_profile.sum()
    print("Cosine similarities:")
    print(recommendation_table_df)
    print()

    for i in range(0,10) :
        recommendation_table_df[i+1] = recommendation_table_df[i+1] * 1/(1+(float)(locations_with_proximities.iloc[i].iloc[0]))

    # Let's view the recommendation table
    # print(recommendation_table_df.head())

    # Let's sort values from great to small
    recommendation_table_df.sort_values(ascending=False, inplace=True)

    #Just a peek at the values
    print("Recommended locations by highest affinity: cosine similarity / (1+proximity)")
    print(recommendation_table_df.head(20))
    print()

    # first we make a copy of the original locations dataframe
    copy = locations.copy(deep=True)

    # Then we set its index to locationId
    copy = copy.set_index('locationId', drop=True)

    # Next we enlist the top 20 recommended locationIds we defined above
    top_20_index = recommendation_table_df.index[:20].tolist()

    # finally we slice these indices from the copied locations df and save in a variable
    recommended_locations = copy.loc[top_20_index, :]

    # Now we can display the top 20 locations in descending order of preference
    print("Top 20 recommended locations:")
    print(recommended_locations)

if __name__ == "__main__" :
      main()