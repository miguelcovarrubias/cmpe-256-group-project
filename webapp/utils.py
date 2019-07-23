import json
import pandas as pd


def jsonPlaylistToDataframe(user_playlist_data):
    cumulative_track_features = {}
    feature_keys = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo']
    print(user_playlist_data)
    for track in user_playlist_data['tracks']:
        if track['track_features'] is None:
            # print("skipping track")
            continue

        for feature in track['track_features']:

            if feature in ['type', 'id', 'uri', 'track_href', 'analysis_url']:
                continue  # we skip these since they're non-numeric

            # if we haven't seen the feature, init a list
            if not feature in cumulative_track_features:
                cumulative_track_features[feature] = []

                cumulative_track_features[feature].append(track['track_features'][feature])

            if cumulative_track_features == {}:
                # print("skip playlist")
                continue  # skip, no features found

            playlist_track_features = {}
            for feature in cumulative_track_features:
                # print(cumulative_track_features[feature])
                playlist_track_features[feature] = sum(cumulative_track_features[feature]) / len(
                    cumulative_track_features[feature])
                # playlist_track_features[feature] = min(cumulative_track_features[feature])

    print(cumulative_track_features)
    row = []
    for i in range(len(feature_keys)):
        row.append(cumulative_track_features[feature_keys[i]])

    return  pd.DataFrame(row).T

