import os
from lyriguessr.lyrics import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    radiohead_albums = ["Pablo Honey", 
                        "The Bends",
                        "OK Computer",
                        "Kid A",
                        "Amnesiac",
                        "Hail To the Thief",
                        "In Rainbows",
                        "The King Of Limbs", 
                        "A Moon Shaped Pool"]

    radiohead = Lyrigetter(API_KEY, album_names=radiohead_albums, artist_name="Radiohead")
    radiohead.store_album_data()
    radiohead.save_songs_df()
