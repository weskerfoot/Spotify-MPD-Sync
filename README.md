## Usage

### Please note that this won't work without Spotify Premium because Spotify limits web API access to non-free accounts.

* Run `pip install --user .` in this repo.

* Go to [https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications) and create an application. Call it whatever you want.

* Create a `.env` or `.envrc` file with contents like this, put it wherever you
  want.

```
export SPOTIPY_CLIENT_ID='YOUR_CLIENT_ID'
export SPOTIPY_CLIENT_SECRET='YOUR_CLIENT_SECRET'
export SPOTIPY_REDIRECT_URI='http://localhost'
export SPOTIFY_USERNAME='YOUR_SPOTIFY_USERNAME'
```

* You can find the values for `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`
  on the page for your application that you just created.

* You can find your spotify username [here](https://www.spotify.com/us/account/overview/)

* Now you can run `spotsync` with your `.env` file sourced (e.g. `source .env`)
