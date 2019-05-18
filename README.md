## Usage

### Please note that this won't work without Spotify Premium because Spotify limits web API access to non-free accounts.
### This also requires you to have set up [mopidy-spotify](https://github.com/mopidy/mopidy-spotify) in order to play spotify tracks.

* Run `pip install --user .` in this repo.

* Go to [https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications) and create an application. Call it whatever you want.

* Go to "Edit Settings" in your newly created app, then add `http://localhost`
  as a redirect URI and hit "Save"

* Find your spotify username [here](https://www.spotify.com/us/account/overview/)

* Now you can run `spotsync --username=username --host=my_mpd_host` where
  `username` is your username from before, and `my_mpd_host` is the host you
  are running MPD on (defaults to `localhost` if you do not pass it)

* You will be prompted to grant permission to the app, once that's done, it
  will cache the credentials locally and you should be able to just run
  spotsync.
