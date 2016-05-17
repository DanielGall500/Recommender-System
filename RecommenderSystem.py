import numpy as np
import pandas as pd
import theano
import csv

dataset_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u.csv"

data = pd.read_csv(dataset_file, sep='	')

from sklearn.cluster import KMeans

clstr = KMeans(n_clusters=(12), max_iter=300, random_state=42)

clstr.fit(data)










