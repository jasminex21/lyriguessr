import os
from lyriguessr.Lyrigetter import Lyrigetter

"""Script that tests Lyrigetter.add_song"""
if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    taylor_albums = []

    taylor = Lyrigetter(API_KEY, album_names=taylor_albums, artist_name="Taylor Swift")
    taylor.add_song(song_name="All Of The Girls You Loved Before", album_name="Lover")
