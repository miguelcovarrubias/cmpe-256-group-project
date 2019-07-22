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

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

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

    playlist_url = json_data['playlist_url']

    # ToDo: add logic to recommend here! this is just a random playlist response the format is not final
    response = {
        'playlists': [
            {'playlistName': 'De Todo', 'playlistUrl': 'https://open.spotify.com/playlist/279mvwpXne6W5Bka5KLeYg?si=h3A4rm4zSFe-mDlFIfIRcw'},
            {'playlistName': 'Banda Romanticas', 'playlistUrl': 'https://open.spotify.com/playlist/2IaO5zGq7O560teYVr4yM3?si=WjaAfGqcTR-j97OAz4TgIw'}
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
