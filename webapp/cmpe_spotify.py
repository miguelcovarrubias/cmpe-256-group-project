from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from itertools import zip_longest
import pprint  # for debug
import json
import datetime
from tqdm import tqdm


class cmpe_spotify(Spotify):
    def __init__(self, clientId, clientSecret):

        client_credentials_manager = SpotifyClientCredentials(clientId, clientSecret)
        Spotify.__init__(self, client_credentials_manager=client_credentials_manager)

    def urlGetPlaylist(self, url):
        playlistId = url.split('/')[-1].split(':')[-1]
        try:
            playlist = self._get("playlists/%s" % playlistId)
        except Exception:
            playlist = False
        return playlist

    # Use as : sp.userGetPlaylists('spotify')
    # Also use : Indiemono, Soundplate, Spingrey, Simon Field, Soave, Daily Playlists
    def userGetPlaylists(self, user):
        playlists = self.user_playlists(user)
        d_playlist = []
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                d_playlist.append({
                    'pid': i + playlists['offset'],
                    'name': playlist['name'],
                    'uri': playlist['uri']
                })
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

                return d_playlist

    # Ref : https://spotipy.readthedocs.io/en/latest/#api-reference
    # playlist and tracks return as paging object, have to use while and next.
    def playlistGetTracks(self, playlist):
        tracks = playlist['tracks']
        d_tracks = []
        while tracks:
            for i, item in enumerate(tracks['items']):
                track = item['track']
                # Filter out local (saved on disk tracks) their URI is spotify.local
                if track and track['uri'].split(':')[1] != 'local':
                    d_tracks.append({'pos': i + tracks['offset'],
                                     'artist_name': track['artists'][0]['name'],
                                     'track_uri': track['uri'],
                                     'artist_uri': track['uri'],
                                     'track_name': track['name'],
                                     'album_uri': track['album']['uri'],
                                     'album_name': track['album']['name'],
                                     # 'track_features' : self.audio_features([track['uri']]),
                                     # Audio analysis is too detailed and takes long time.
                                     # 'track_analysis' : self.audio_analysis(track['uri'])
                                     })
            if tracks['next']:
                tracks = self.next(tracks)
            else:
                tracks = None

        # Get audio_features seperately, because we can send 100 track_ids in one Web API call.
        # Ref: https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks?page=1&tab=votes#tab-top
        def grouper(iterable, n, fillvalue=None):
            args = [iter(iterable)] * n
            return zip_longest(*args, fillvalue=fillvalue)

        audio_features = []
        for item in grouper(d_tracks, 100, False):
            tid = filter(lambda x: x, item)
            tid = [t['track_uri'] for t in tid]
            audio_features.extend(self.audio_features(tid))
        for track, features in zip(d_tracks, audio_features):
            track.update({'track_features': features})
        # End of audio_features
        return d_tracks

    # sp.playlistGetInfo(playlistUrl, 1)
    def playlistGetInfo(self, url, pid):
        playlist = self.urlGetPlaylist(url)
        if playlist:
            trackInfo = self.playlistGetTracks(playlist)
            return {
                'name': playlist['name'],
                'playlist_uri': playlist['uri'],
                'collaborative': playlist['collaborative'],
                'pid': pid,
                'num_tracks': len(trackInfo),
                'num_followers': playlist['followers']['total'],
                'tracks': trackInfo,
            }
        else:
            return False

    def generatePlaylistDetails(self, file):
        data = {
            'info': {
                "generated_on": datetime.datetime.now().isoformat(),
                "slice": file,
                "version": "v1"
            },
            'playlists': []
        }
        with open(file, 'r') as fh:
            for i, line in enumerate(tqdm(fh)):
                playlistUrl = line.strip('\n')
                playlist = self.playlistGetInfo(playlistUrl, i)
                if playlist:
                    data['playlists'].append(playlist)

        with open(file + '.json', 'w') as fw:
            json.dump(data, fw, indent=4, sort_keys=False)
        return True