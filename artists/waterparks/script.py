import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    waterparks_albums = ["Airplane Conversations",
                         "Black Light",
                         "Cluster",
                         "Double Dare",
                         "Entertainment",
                         "FANDOM", 
                         "Greatest Hits",
                         "INTELLECTUAL PROPERTY"]

    waterparks = Lyrigetter(API_KEY, album_names=waterparks_albums, artist_name="Waterparks")
    # waterparks.store_album_data()
    # waterparks.save_songs()
    waterparks.save_counts()