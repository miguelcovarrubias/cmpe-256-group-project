#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
import sys

import requests
import json
import logging
import os
from pprint import pprint

from data.PlaylistData import PlaylistData
import sys
from cmpe_spotify import cmpe_spotify
import utils
from models.knn_model import knn_model
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Data.
#----------------------------------------------------------------------------#

data = PlaylistData("./data/nortenans_and_regue_list.txt.json")
data.load_new_data("")

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

    #playlist_url = 'https://open.spotify.com/playlist/' + "37i9dQZF1DX10zKzsJ2jva" #json_data['playlist_url']
    playlist_url = 'https://open.spotify.com/playlist/' + json_data['playlist_url']
    sp = cmpe_spotify(clientId, clientSecret)
    user_playlist_data = sp.playlistGetInfo(playlist_url, 0)

    # convert playlist data into dataframe of 1 row
    user_df = utils.jsonPlaylistToDataframe(user_playlist_data)

    knn_m = knn_model()
    recomm_list = knn_m.train_and_recommend(data, user_df)

    # ToDo: add logic to recommend here! this is just a random playlist response the format is not final
    response = {
        'playlists': [
            {'playlistName': '1', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[0]},
            {'playlistName': '2', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[1]},
            {'playlistName': '3', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[2]},
            {'playlistName': '4', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[3]},
            {'playlistName': '5', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[4]},
            {'playlistName': '6', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[5]},
            {'playlistName': '7', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[6]},
            {'playlistName': '8', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[7]},
            {'playlistName': '9', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[8]},
            {'playlistName': '10', 'playlistUrl': 'https://open.spotify.com/playlist/' + recomm_list[9]}
        ]
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
