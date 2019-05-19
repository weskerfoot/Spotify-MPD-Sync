## Usage

### Please note that this won't work without Spotify Premium because Spotify limits web API access to non-free accounts.
### This also requires you to have set up [mopidy-spotify](https://github.com/mopidy/mopidy-spotify) in order to play spotify tracks.

* Run `pip3 install --user spotify-mpd-sync`.

* Go to [https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications) and create an application. Call it whatever you want.

* Go to "Edit Settings" in your newly created app, then add
  `http://localhost:8080`
  as a redirect URI and hit "Save" (You may choose a different one by setting
  `SPOTIPY_REDIRECT_URI` in your environment if localhost:8080 is unavailable)

* Find your spotify username [here](https://www.spotify.com/us/account/overview/)

* You will have to set up some environment variables in order to run the app.

```
export SPOTIFY_USERNAME="The username you got above"
export SPOTIPY_CLIENT_ID="Your app's client ID"
export SPOTIPY_CLIENT_SECRET="Your app's client secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8080"
```

* Now you can run `spotsync -H my_mpd_host -P 6600` where `my_mpd_host` is the host you
  are running MPD on (host defaults to `localhost` and port defaults to `6600` if you do not include it)

* If this is the first time you are running it, it will direct you to a page in
  your browser to grant permission for the app you just created to access your
  private spotify playlist. You only need to do this once, and then your
  credentials will be cached.

* You will be prompted to grant permission to the app, once that's done, it
  will cache the credentials locally and you should be able to just run
  spotsync.
