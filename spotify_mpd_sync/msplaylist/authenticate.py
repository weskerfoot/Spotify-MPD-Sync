# shows a user's playlists (need to be authenticated via oauth)

import threading
import spotipy.oauth2 as oauth2
import spotipy
import queue
from bottle import route, run, response, request

auth_token_queue = queue.Queue()
event_queue = queue.Queue()

@route('/')
def index():
    auth_code = request.query.code
    if auth_code:
        auth_token_queue.put(auth_code)
        return "It worked! You may close this tab now"

    return "Oops! Something went wrong. Please file a bug report"

def wait_for_done(task):
    server = threading.Thread(target=task)
    server.daemon = True
    server.start()
    while True:
        event = event_queue.get()
        if event == "done":
            break

def run_server():
    threading.Thread(target= lambda: wait_for_done(lambda: run(quiet=True,
                                                               host='localhost',
                                                               port=8080))).start()

def prompt_for_user_token(username, scope=None, client_id = None,
        client_secret = None, redirect_uri = None, cache_path = None):
    """
    prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor

        Parameters:

         - username - the Spotify username
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app
         - cache_path - path to location to save tokens
    """

    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        print('''
            You need to set your Spotify API credentials. You can do this by
            setting environment variables like so:

            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

            Get your credentials at     
                https://developer.spotify.com/my-applications
        ''')
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope, cache_path=cache_path)

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        run_server()
        auth_url = sp_oauth.get_authorize_url()
        try:
            import webbrowser
            webbrowser.open(auth_url)
        except:
            print("Please navigate here: %s" % auth_url)

        response = "localhost:8080?code=%s" % auth_token_queue.get()
        print(response)
        event_queue.put("done")

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    # Auth'ed API request
    if token_info:
        return token_info['access_token']
    else:
        return None
