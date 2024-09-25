import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    omens_albums = ["Bad Omens",
                    "Finding God Before God Finds Me (Deluxe)",
                    "THE DEATH OF PEACE OF MIND",
                    "CONCRETE JUNGLE [THE OST]"]

    omens = Lyrigetter(API_KEY, album_names=omens_albums, artist_name="Bad Omens")
    omens.store_album_data()
    omens.save_songs()
    omens.save_counts()
