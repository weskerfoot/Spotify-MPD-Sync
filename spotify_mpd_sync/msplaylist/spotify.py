#! /usr/bin/env python
import gevent.monkey
gevent.monkey.patch_all()

from collections import defaultdict
from mpd import MPDClient
from mpd.base import CommandError
from os import environ
from re import sub
from spotify_mpd_sync.msplaylist.authenticate import prompt_for_user_token
from spotipy.oauth2 import SpotifyClientCredentials
from sys import stderr
import argparse
import spotipy
import spotipy.util as util

class Spotify():
    def __init__(self, host="localhost", port=6600):
        self.username = environ.get("SPOTIFY_USERNAME")

        scope = "playlist-read-private"

        token = prompt_for_user_token(self.username, scope)
        if token:
            self.sp = spotipy.Spotify(auth=token)

        self.mpd_client = MPDClient()
        self.mpd_client.connect(host, port)

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
                    try:
                        self._playlists[self.sanitize_playlist(playlist["name"])].append(
                                self.fmt_track(track["track"]["id"])
                            )
                    except BaseException:
                        stderr.write("Error parsing track {0}".format(repr(track)))
                        continue

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


def run_sync():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H",
                        "--host",
                        default="localhost",
                        help="The MPD server you would like spotsync to use, defaults localhost")

    parser.add_argument("-P",
                        "--port",
                        type=int,
                        default=6600,
                        help="The MPD port you would like spotsync to use, defaults to 6600")

    args = parser.parse_args()

    spotify = Spotify(host=args.host,
                      port=args.port)

    spotify.persist_playlists()
