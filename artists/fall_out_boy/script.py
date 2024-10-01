import os
from lyriguessr.Lyrigetter import Lyrigetter

if __name__ == "__main__":
    API_KEY = os.environ["GENIUS_API_KEY"]
    fob_albums = ["Take This to Your Grave",
                  "From Under the Cork Tree",
                  "Infinity on High",
                  "Folie à Deux",
                  "Save Rock and Roll",
                  "American Beauty / American Psycho",
                  "MANIA",
                  "So Much (For) Stardust"]
    songs_to_remove = ["Roxanne", 
                       "Snitches and Talkers Get Stitches and Walkers", 
                       "The Music or the Misery", 
                       "My Heart is the Worst Kind of Weapon (Demo)",
                       "Dance, Dance (Live From Hammersmith Palais)",
                       "This Ain’t A Scene, It’s An Arms Race (Live From Hammersmith Palais)",
                       "Thriller (Live From Hammersmith Palais)",
                       "Pavlove",
                       "Untitled 1 (Colorado Song) (unfinished demo)",
                       "Untitled 2 (Jakus Song) (unfinished demo)"]

    fob = Lyrigetter(API_KEY, album_names=fob_albums, artist_name="Fall Out Boy")
    # fob.store_album_data()
    # fob.save_songs()
    fob.remove_songs(songs_to_remove)
    fob.save_counts()
    fob.add_stats()