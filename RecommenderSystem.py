import PIL.Image #was acting weird so had to import like this
from PIL import ImageTk
from StringIO import StringIO
import numpy as np
import pandas as pd


from Tkinter import *
from ttk import *


import django
import sys
import collections
import operator
import requests
import urllib
import base64
import io
import web

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

def preference_set(usr_ratings, movies): #finds the category preferences of each user
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

def find_similar(target_prefs, prefs_collection): #finds the similarity between users
    user_similarity = {}

    for u_id, u_prefs in prefs_collection.iteritems():
        similarity = np.sqrt(np.abs(sum(u_prefs - target_prefs)))  #a measure of how similar user x and the target user are
        user_similarity[u_id] = np.round(similarity, 5)

    ordered_dict = sorted(user_similarity.items(), key=operator.itemgetter(1))

    cut_off = int(len(ordered_dict) * 0.10) + 1 #only taking top 10 percent so that we have the most similar users

    return ordered_dict[:cut_off]

def find_recommendations(sim_users, target_user, watched_movies):
    rcmnd = {}
    rcmnd_count = {}

    for idx, users in enumerate(sim_users): #sim_users already in order so index will tell us whos the most similar
        u_id = users[0]
        rated_movies = [x[1] for x in ratings_data[ratings_data['user_id'] == u_id].iterrows()] #each movie this user has rated

        highly_rated = [x for x in rated_movies if x[2] >= 4] #each movie that they rated 4 or 5

        for movie in highly_rated:
            if idx in rcmnd:
                rcmnd.setdefault(idx, [])
                rcmnd[idx].append(movie[1])
            else:
                rcmnd[idx] = [movie[1]]

    for idx, recomm in rcmnd.iteritems():
        for r in recomm:
            if r in rcmnd_count:
                rcmnd_count[r] += 1
            else:
                rcmnd_count[r] = 1

    #filtering movies that the user has already seen
    for mov_id, votes in rcmnd_count.iteritems():
        if mov_id in watched_movies:
            rcmnd_count[mov_id] = 0

    #a list of the movies with the most recommendations
    highly_recommended = [x for x in sorted(rcmnd_count.items(), \
                   key=operator.itemgetter(1))[::-1] if x[1] != 0]

    cutoff = int(len(highly_recommended) * 0.10) + 1
    return highly_recommended[:cutoff]

def target_info(user_id):
    rated_movies = [x for x in ratings_data[ratings_data['user_id'] == user_id]['item_id']]
    return rated_movies

#user_ratings = ratings_set(ratings_data)

#user_prefs = preference_set(user_ratings, movies_data)

target_prefs = np.array(([ -7.,  -8., -41.,  -4.,  -8.,  -1.,   0.,  -3., -12.,  -7.,  -1.,
       -11., -12., -13.,   0.,  -3.]))

watched_movies = target_info(933)

#similar_users = find_similar(target_prefs, user_prefs)

test_sim = np.array([(933, 0.0), (21, 1.0), (682, 1.7320500000000001), (207, 2.4494899999999999), (13, 3.8729800000000001), (699, 3.8729800000000001), (116, 4.1231099999999996), (222, 4.1231099999999996), (790, 4.3589000000000002),
                     (454, 4.5825800000000001), (417, 4.6904199999999996), (262, 4.7958299999999996), (254, 4.8989799999999999), (795, 5.0), (275, 5.2915000000000001), (104, 5.4772299999999996), (269, 5.4772299999999996), (868, 5.91608),
                     (486, 6.2450000000000001), (363, 6.32456), (425, 6.32456), (497, 6.32456), (445, 6.4031200000000004), (246, 6.4807399999999999), (268, 6.4807399999999999), (637, 6.4807399999999999), (833, 6.7081999999999997),
                     (26, 6.78233), (650, 6.78233), (639, 6.9282000000000004), (782, 6.9282000000000004), (92, 7.0), (916, 7.0710699999999997), (201, 7.1414299999999997), (521, 7.1414299999999997), (552, 7.2801099999999996),
                     (727, 7.2801099999999996), (698, 7.3484699999999998), (896, 7.3484699999999998), (496, 7.4161999999999999), (393, 7.4833100000000004), (724, 7.6157700000000004), (336, 7.6811499999999997), (224, 7.9372499999999997), (442, 7.9372499999999997), (5, 8.0), (733, 8.0), (766, 8.0), (161, 8.0622600000000002), (255, 8.0622600000000002), (788, 8.0622600000000002),
                     (847, 8.0622600000000002), (865, 8.2462099999999996), (617, 8.3066200000000006), (63, 8.4261499999999998), (429, 8.4261499999999998), (693, 8.4261499999999998), (871, 8.4261499999999998), (279, 8.4852799999999995),
                     (401, 8.4852799999999995), (49, 8.5440000000000005), (110, 8.5440000000000005), (798, 8.6023300000000003), (206, 8.6602499999999996), (646, 8.7749600000000001), (15, 8.8317599999999992), (198, 8.8317599999999992), (587, 8.8881899999999998), (653, 8.8881899999999998), (435, 8.9442699999999995), (101, 9.0), (463, 9.1104299999999991), (498, 9.1104299999999991), (483, 9.2195400000000003), (854, 9.2195400000000003), (828, 9.2736199999999993), (3, 9.4868299999999994), (446, 9.5393899999999991), (490, 9.5393899999999991), (618, 9.5393899999999991), (685, 9.5393899999999991), (756, 9.5393899999999991), (595, 9.6436499999999992), (683, 9.6436499999999992), (690, 9.6436499999999992), (778, 9.6436499999999992), (586, 9.6953600000000009),
                     (930, 9.6953600000000009), (385, 9.7979599999999998), (757, 9.7979599999999998), (656, 9.8488600000000002), (660, 9.8488600000000002), (20, 9.8994900000000001), (380, 9.8994900000000001), (155, 9.9498700000000007), (814, 9.9498700000000007), (900, 9.9498700000000007), (129, 10.0), (510, 10.0), (627, 10.0), (149, 10.04988), (526, 10.04988), (544, 10.04988), (832, 10.04988), (713, 10.099500000000001), (719, 10.099500000000001), (561, 10.14889), (827, 10.14889), (40, 10.198040000000001), (82, 10.24695), (326, 10.24695), (328, 10.24695), (797, 10.24695), (217, 10.295629999999999), (223, 10.295629999999999), (302, 10.295629999999999), (485, 10.295629999999999), (515, 10.295629999999999),
                     (194, 10.34408), (293, 10.34408), (509, 10.34408), (578, 10.34408), (633, 10.34408), (745, 10.34408), (853, 10.34408), (451, 10.392300000000001), (626, 10.392300000000001), (922, 10.392300000000001), (197, 10.44031), (609, 10.44031), (702, 10.44031), (648, 10.48809), (721, 10.48809), (787, 10.48809), (824, 10.48809), (100, 10.53565), (193, 10.53565), (202, 10.53565), (229, 10.53565), (410, 10.53565), (761, 10.53565), (769, 10.53565), (153, 10.63015),
                     (378, 10.63015), (630, 10.63015), (634, 10.63015), (805, 10.63015), (885, 10.63015), (920, 10.63015), (183, 10.67708), (289, 10.67708), (921, 10.67708), (925, 10.67708), (35, 10.72381), (133, 10.72381), (418, 10.72381), (570, 10.72381), (860, 10.72381), (461, 10.77033), (505, 10.77033), (614, 10.77033), (839, 10.77033), (869, 10.77033), (61, 10.816649999999999), (238, 10.816649999999999), (792, 10.816649999999999), (172, 10.862780000000001), (205, 10.862780000000001), (382, 10.862780000000001), (726, 10.862780000000001), (873, 10.862780000000001), (914, 10.862780000000001), (27, 10.908709999999999), (81, 10.908709999999999), (199, 10.908709999999999), (346, 10.908709999999999),
                     (669, 10.908709999999999), (760, 10.908709999999999), (820, 10.908709999999999), (863, 10.908709999999999), (905, 10.908709999999999), (124, 10.95445), (305, 10.95445), (525, 10.95445), (872, 10.95445), (32, 11.0), (159, 11.0), (290, 11.0), (594, 11.0), (635, 11.0), (714, 11.0), (741, 11.0), (910, 11.0), (281, 11.045360000000001), (304, 11.045360000000001)])

recommended_movies = find_recommendations(test_sim, target_prefs, watched_movies=watched_movies)

print recommended_movies

sys.path.append("C:/Users/dano/Desktop/Theory of Everything/IMDBPy")

from imdb import IMDb

mov_access = IMDb()

#final_recommends = [x for idx, x in enumerate(movies_data[movies_data['movie_id'] == \
#((recommended_movies[0])[0])]['movie_title'].iloc[0])]

final_recommends = []

for i in range(len(recommended_movies)):

    r = movies_data[movies_data['movie_id'] == \
    ((recommended_movies[i])[0])]['movie_title'].iloc[0]

    final_recommends.append(r)

print 'Rec Mov:', final_recommends

window = Tk()

window.title("Recommendation System")
window.geometry("1000x500")

app = Frame(window)
app.grid()


row = 0
column = 0
max_columns = 5
images = []

for idx, rec in enumerate(final_recommends[0:10]):

    mov_id = mov_access.search_movie(rec)[0].movieID
    movie = mov_access.get_movie(mov_id)
    mov_img_url = movie['cover url']


    mov_img_url = urllib.urlopen(mov_img_url)
    img = io.BytesIO(mov_img_url.read())
    movie_img = PIL.Image.open(img)

    converted_img = ImageTk.PhotoImage(movie_img)

    images.append(converted_img)

    movie_view = Label(master=app, image=images[idx])
    movie_view.grid(row=row, column=column)

    button = Button(master=app, text=rec)
    button.grid(row=row, column=column)

    if column == max_columns:
        row += 1
        column = 0
    else:
        column += 1

window.mainloop()







































