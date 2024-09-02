import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    olivia_albums = ["SOUR",
                     "GUTS (spilled)"]

    olivia = Lyrigetter(API_KEY, album_names=olivia_albums, artist_name="Olivia Rodrigo")
    olivia.store_album_data()
    olivia.save_songs()
    olivia.save_counts()
