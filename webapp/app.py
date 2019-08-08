#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
import sys

import csv
from datetime import datetime

import requests
import json
import logging
import os
from pprint import pprint

from data.playlist_data import playlist_data
import sys
from cmpe_spotify import cmpe_spotify
import utils
from models.knn_model import knn_model
from models.pairwise_cosine_similarity import pairwise_cosine_similarity

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Data.
#----------------------------------------------------------------------------#
ratings_file_path = "./data/ratings.csv"
data_dir_path="<data_directory_path_here>"
data_file_paths = [data_dir_path + s for s in os.listdir(data_dir_path)]

data = playlist_data(data_file_paths)


knn_m = knn_model()
knn_m.train(data)


#----------------------------------------------------------------------------#
# Spotify Api
#----------------------------------------------------------------------------#
clientId = '27cb847c94d3462b84cdb8b371a7690d'
clientSecret = 'd08ddf50c1ea4663a3cf7e1b5324e0b0'

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#
# 'home' routes
#
@app.route('/', methods=['GET'])
def home():
    return render_template('./pages/home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('./pages/about.html')

@app.route('/demo', methods=['GET'])
def demo():
    # add logic to check if user is logged in,
    # if logged in redirect to home page, else show home page
    return render_template('./pages/demo.html')

@app.route('/api/search', methods=['POST'])
def search_api():
    json_data = request.get_json(force=True)
    if not json_data or not 'playlist_url' in json_data.keys():
        return jsonify({'response': 'invalid call, must specify json in the following format=> {"playlist_url": <insert playlist url here>}'}), 400

    playlist_url = 'https://open.spotify.com/playlist/' + json_data['playlist_url']

    model_strategy_method = json_data['method']

    sp = cmpe_spotify(clientId, clientSecret)
    user_playlist_data = sp.playlistGetInfo(playlist_url, 0)


    playlistId = json_data['playlist_url'].split('/')[-1].split(':')[-1]

    # convert playlist data into dataframe of 1 row
    user_df = utils.jsonPlaylistToDataframe([user_playlist_data])


    recomm_list = []
    print("user data")
    print(user_df)
    if data.playlist_data.size != 0:
        if model_strategy_method == "knn":
            recomm_list = knn_m.recommend(data, user_df)
        elif model_strategy_method == "cosine":
            recomm_list = pairwise_cosine_similarity.recommend(data, user_df, 10)
    else:
        print("Not data in data.playlist_data dataframe")

    print("Recommendation list for %s" % json_data['playlist_url'])
    print(recomm_list)

    # ToDo: add logic to recommend here! this is just a random playlist response the format is not final
    response = {
        'currentPlaylist': 'https://open.spotify.com/embed/playlist/' + playlistId,
        'method': model_strategy_method,
        'playlists': [
            {'playlistRanking': '1.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[0]},
            {'playlistRanking': '2.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[1]},
            {'playlistRanking': '3.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[2]},
            {'playlistRanking': '4.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[3]},
            {'playlistRanking': '5.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[4]},
            {'playlistRanking': '6.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[5]},
            {'playlistRanking': '7.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[6]},
            {'playlistRanking': '8.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[7]},
            {'playlistRanking': '9.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[8]},
            {'playlistRanking': '10.', 'playlistUrl': 'https://open.spotify.com/embed/playlist/' + recomm_list[9]}
        ]
    }
    return jsonify(response)

@app.route('/api/submitVote', methods=['POST'])
def submit_vote():
    json_data = request.get_json(force=True)

    timestamp = datetime.now().strftime("%d-%b-%Y-%H:%M:%S")

    with open(ratings_file_path, 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([timestamp, json_data['originalPlaylist'], json_data['recommendedPlaylist'], json_data['score'], json_data['method'] ])

    response = {
        'result': True
    }
    return jsonify(response)

#
# Error handlers.
#
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# import models

# Default port:
if __name__ == '__main__':
    app.run(debug=True, port=8080)
