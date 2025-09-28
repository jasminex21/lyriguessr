import os
from lyriguessr.Lyrigetter import Lyrigetter

API_KEY = os.environ["GENIUS_API_KEY"]
token_albums = ["One - EP", 
                "Two - EP", 
                "Sundowning", 
                "This Place Will Become Your Tomb",
                "Take Me Back to Eden"]

token = Lyrigetter(API_KEY, album_names=token_albums, artist_name="Sleep Token")
token.store_album_data()
token.save_songs()
token.save_counts()
token.add_stats()