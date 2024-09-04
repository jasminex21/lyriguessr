import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    clairo_albums = ["diary 001",
                     "Immunity",
                     "Sling",
                     "Charm"]

    clairo = Lyrigetter(API_KEY, album_names=clairo_albums, artist_name="Clairo")
    clairo.store_album_data()
    clairo.save_songs()
    for song in ["2 Hold U", 
                 "Get With U",
                 "Sis",
                 "Bubble Gum",
                 "Heaven"]:
        clairo.add_song(song_name=song, album_name="Original singles")
    clairo.save_counts()
    clairo.add_stats()
