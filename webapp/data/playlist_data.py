import json
import pandas as pd
import os.path
from os import path

#singleton data holder
class playlist_data:

    class __PlaylistData:
        def __init__(self, arg):
            self.playlist_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo']
            self.playlist_data = pd.DataFrame()
            self.playlist_names = []
            self.file_source_path = arg
            self.load_new_data()

        def __str__(self):
            return repr(self)

        # file_source_path is a list
        def load_new_data(self):
            for file in self.file_source_path:

                feature_keys = self.playlist_features.copy()

                if path.exists(file) and ".txt.json" in file :
                    print("Loading data in file... : ", file)
                else:
                    print("Data File does not exist, continuing...: ", file)
                    continue

                with open(file, 'r') as myfile:
                    data = myfile.read()

                playlist_data = json.loads(data)['playlists']

                self.construct_dataframe(playlist_data, feature_keys)
                if self.playlist_data.size > 0:
                    self.playlist_data.drop_duplicates(subset='playlist_uri', inplace=True)

        def construct_dataframe(self, data, feature_keys):
            processed_data = {}
            for playlist in data:

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
                    #print(cumulative_track_features[feature])
                    playlist_track_features[feature] = sum(
                        cumulative_track_features[feature])/len(cumulative_track_features[feature])
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

            self.playlist_data = self.playlist_data.append(df)

            self.playlist_names.extend(playlist_names)


    instance = None

    def __init__(self, arg):

        if not playlist_data.instance:
            playlist_data.instance = playlist_data.__PlaylistData(arg)
        else:
            playlist_data.instance.file_source = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)