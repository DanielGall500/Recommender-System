import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

rating_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u.csv"
movieinfo_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u_item.csv"

ratings_data = pd.read_csv(rating_file, sep='	')
movies_data = pd.read_csv(movieinfo_file, sep='\t')

mov_categories = ['Adventure', 'Animation', 'Children', 'Comedy', 'Crime','Documentary',
                  'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                  'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

rating_samples, rating_features = ratings_data.shape
movie_samples, movie_features = movies_data.shape

num_categories = 16

def ratings_set(users):
    user_info = {}

    for idx, user in users.iterrows():
        user_id = user['user_id']
        rating = user['rating']
        movie_id = user['item_id']

        if user_id in user_info:
            user_info[user_id].append([movie_id, rating])
        else:
            user_info[user_id] = [[movie_id, rating]]

    return user_info

def preference_set(usr_ratings, movies):
    user_prefs = {}
    for user, ratings in usr_ratings.iteritems():
        user_prefs[user] = np.zeros(16)

        for rating in ratings:
            mov_id = int(rating[0]) - 1 #check
            rate = rating[1]

            title = movies.iloc[mov_id][1]
            categories = movies.iloc[mov_id][4:]

            try:
                categ_prefs = [float(x) for x in categories.values]
            except ValueError:
                continue

            if rate > 3:
                user_prefs[user] += categ_prefs
            else:
                user_prefs[user] -= categ_prefs

    return user_prefs


user_ratings = ratings_set(ratings_data)

user_prefs = preference_set(user_ratings, movies_data)


"""
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

pca = PCA().fit_transform(ratings_data)

clstr = KMeans(n_clusters=(12), max_iter=300, random_state=42)

clstr.fit(pca)
"""











