import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    nbhd_albums = ["I'm Sorry",
                   "I Love You.",
                   "The Love Collection",
                   "#000000 & #FFFFFF",
                   "Wiped Out!",
                   "Hard to Imagine the Neighbourhood Ever Changing",
                   "Chip Chrome & the Mono-Tones (Deluxe)"]

    nbhd = Lyrigetter(API_KEY, album_names=nbhd_albums, artist_name="The Neighbourhood")
    nbhd.store_album_data()
    nbhd.save_songs()
    nbhd.remove_songs(["Ye Interlude", "H8M4CH1N3"])
    nbhd.save_counts()