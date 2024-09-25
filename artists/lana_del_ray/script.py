import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    lana_albums = ["Born to Die (Deluxe)",
                   "Paradise",
                   "Ultraviolence (Deluxe)",
                   "Honeymoon",
                   "Lust for Life",
                   "Norman Fucking Rockwell!",
                   "Chemtrails Over the Country Club",
                   "Blue Banisters",
                   "Did you know that there’s a tunnel under Ocean Blvd"]

    lana = Lyrigetter(API_KEY, album_names=lana_albums, artist_name="Lana Del Ray")
    lana.store_album_data()
    lana.save_songs()
    lana.save_counts()
    lana.add_stats()
