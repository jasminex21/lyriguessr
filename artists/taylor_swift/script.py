import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    taylor_albums = [""]

    taylor = Lyrigetter(API_KEY, album_names=taylor_albums, artist_name="Taylor Swift")
    taylor.add_song("If This Was a Movie (Taylor’s Version)", "Fearless")
    taylor.save_counts()
