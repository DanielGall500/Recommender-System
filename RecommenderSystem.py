import numpy as np
import pandas as pd
import theano
import csv

movieID_filename = "/Users/dannyg/Desktop/Projects/Datasets/NetflixMovies/movie_titles.csv"
testset_filename = "/Users/dannyg/Desktop/Projects/Datasets/NetflixMovies/probe.csv"
customerID_filename = "/Users/dannyg/Desktop/Projects/Datasets/NetflixMovies/qualifying.csv"

movie_dataset = pd.read_csv(movieID_filename, sep=',')
customer_dataset = pd.read_csv(customerID_filename, sep=',')








