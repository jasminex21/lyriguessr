import os
import pandas as pd
from lyricsgenius import Genius

class Lyrigetter:

    def __init__(self, genius_token, album_names, artist_name):
        
        self.genius = Genius(genius_token)
        self.album_names = album_names
        self.artist_name = artist_name
        # self.dirpath = os.path.join("/home/jasmine/PROJECTS/lyriguessr/artists", artist_name.lower())
    
    def store_album_data(self):
        
        for album_name in self.album_names:
            album_filename = f"{'_'.join(album_name.split(' '))}.json"
            if os.path.exists(album_filename):
                print(f"File {album_filename} already exists; moving on")
                continue
            album = self.genius.search_album(album_name, self.artist_name)
            album.save_lyrics(filename=album_filename)

if __name__ == "__main__":

    API_KEY = os.environ["GENIUS_API_KEY"]

    parxgetter = Lyrigetter(genius_token=API_KEY, album_names=["Double Dare", "FANDOM"], artist_name="Waterparks")
    parxgetter.store_album_data()