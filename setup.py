import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotify-mpd-sync",
    version="1.0.2",
    author="Wesley Kerfoot",
    author_email="wes@wesk.tech",
    description="Synchronize Spotify Playlist to MPD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weskerfoot/Spotify-MPD-Sync",
    packages=setuptools.find_packages(),
    install_requires = [
        "spotipy>=2.4.4",
        "python-mpd2>=1.0.0",
        "bottle>=0.12.16",
        "gevent>=1.4.0"
    ],
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts" : [
            "spotsync = spotify_mpd_sync.msplaylist.spotify:run_sync"
        ]
    }
)
