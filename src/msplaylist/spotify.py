#! /usr/bin/env python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mpd import MPDClient
from mpd.base import CommandError
from collections import defaultdict
from re import sub
from os import environ

class Spotify():
    def __init__(self):
        self.username = environ.get("SPOTIFY_USERNAME")
        self.client_credentials_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(
                client_credentials_manager=self.client_credentials_manager
                )

        self.mpd_client = MPDClient()
        self.mpd_client.connect("ismeta.local", 6600)

        self._playlists = defaultdict(lambda: [])

    def fmt_track(self, track_id):
        return "spotify:track:{0}".format(track_id)

    def sanitize_playlist(self, playlist):
        return sub(r'[\/\n\r]', "", playlist)

    @property
    def playlists(self):
        if self._playlists:
            return self._playlists

        playlists = self.sp.user_playlists(self.username)

        while playlists:
            for playlist in playlists['items']:
                for track in self.sp.user_playlist(self.username,
                                                   playlist["id"],
                                                   fields="tracks,next")["tracks"]["items"]:

                    self._playlists[self.sanitize_playlist(playlist["name"])].append(
                            self.fmt_track(track["track"]["id"])
                        )

            if playlists["next"]:
                playlists = self.sp.next(playlists)
            else:
                playlists = None

        return self._playlists

    def persist_playlists(self):
        for playlist in self.playlists:
            try:
                # The actual MPD playlist as it currently is
                current_playlist_stored = set(self.mpd_client.listplaylist(playlist))
            except CommandError as e:
                print(e)
                current_playlist_stored = set()

            # The spotify playlist as it currently is
            new_playlist = self.playlists[playlist]

            if set(new_playlist) != current_playlist_stored:
                print("{0} has missing tracks, trying to add them".format(playlist))
                try:
                    self.mpd_client.playlistclear(playlist)
                except CommandError as e:
                    print(e)

                # Now it should be safe to add any new playlist items
                for track_id in new_playlist:
                    try:
                        self.mpd_client.playlistadd(playlist, track_id)
                    except CommandError as e:
                        print(e)
                        print("Could not add {0}".format(track_id))
                        continue
