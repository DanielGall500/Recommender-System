import numpy as np
import pandas as pd
import theano
import csv

rating_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u.csv"
movieinfo_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u_item.csv"

ratings_data = pd.read_csv(rating_file, sep='	')
movies_data = pd.read_csv(movieinfo_file, sep='|')

from sklearn.cluster import KMeans

clstr = KMeans(n_clusters=(12), max_iter=300, random_state=42)

clstr.fit(data)










