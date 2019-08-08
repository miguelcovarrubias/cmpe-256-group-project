import json
import pandas as pd


def jsonPlaylistToDataframe(user_playlist_data):

    processed_data = {}
    feature_keys = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo']

    for playlist in user_playlist_data:
        cumulative_track_features = {}
        # go through each track and get the features
        for track in playlist['tracks']:

            if 'track_features' not in track or track['track_features'] is None:
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
            playlist_track_features[feature] = sum(
                cumulative_track_features[feature]) / len(cumulative_track_features[feature])
        processed_data[playlist['playlist_uri'].split(':')[-1]] = playlist_track_features

    playlist_names = []
    data_matrix = []
    indices = {}
    cnt = 0
    for playlist in processed_data:
        indices[cnt] = playlist
        cnt = cnt + 1
        playlist_names.append(playlist)
        row = []
        data = processed_data[playlist]
        for i in range(len(feature_keys)):
            row.append(data[feature_keys[i]])
        row.insert(0, playlist)
        data_matrix.append(row)

    df = pd.DataFrame(data_matrix)
    feature_keys.insert(0, 'playlist_uri')
    df.columns = feature_keys
    df.set_index('playlist_uri')
    return df

