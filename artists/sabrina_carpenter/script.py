import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    sabrina_albums = ["Eyes Wide Open",
                      "EVOLution",
                      "Singular: Act I",
                      "Singular Act II",
                      "emails i can’t send fwd:",
                      "Short n’ Sweet"]

    sabrina = Lyrigetter(API_KEY, album_names=sabrina_albums, artist_name="Sabrina Carpenter")
    # sabrina.store_album_data()
    # sabrina.save_songs()
    # sabrina.save_counts()
    sabrina.add_stats()