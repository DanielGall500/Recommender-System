import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

rating_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u.csv"
movieinfo_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u_item.csv"

ratings_data = pd.read_csv(rating_file, sep='	')
movies_data = pd.read_csv(movieinfo_file, sep='|')

rating_samples, rating_features = ratings_data.shape
movie_samples, movie_features = movies_data.shape

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

pca = PCA().fit_transform(ratings_data)

clstr = KMeans(n_clusters=(12), max_iter=300, random_state=42)

clstr.fit(pca)












