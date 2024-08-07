import os
import json
import re
import pandas as pd
from lyricsgenius import Genius

class Lyrigetter:

    def __init__(self, genius_token, album_names, artist_name):
        
        self.genius = Genius(genius_token)
        self.album_names = album_names
        self.artist_name = artist_name
        self.album_filenames = [f"{'_'.join(album_name.split(' '))}.json" for album_name in self.album_names]
    
    def store_album_data(self):
        
        for album_name in self.album_names:
            album_filename = f"{'_'.join(album_name.split(' '))}.json"
            if os.path.exists(album_filename):
                print(f"File {album_filename} already exists; moving on")
                continue
            album = self.genius.search_album(album_name, self.artist_name)
            album.save_lyrics(filename=album_filename)
    
    def _clean_lyrics(self, df):

        # removes everything up to the first square bracket (indicating first section)
        df["lyrics_full"] = df["lyrics_full"].replace(r"^.*?\[", "[", regex=True)
        # removes the nEmbed or Embed at the end of the string
        df["lyrics_full"] = df["lyrics_full"].replace(r"\d*Embed\'*\"*$", "", regex=True)
        # removes unicode character \u2005
        df["lyrics_full"] = df["lyrics_full"].replace(r"\u2005", " ", regex=True)

        return df
    
    def _split_by_section(self, row): 
        lyrics = row["lyrics_full"]
        sections = []
        pattern = re.compile(r"\[.*?\]")

        for match in pattern.finditer(lyrics):
            section = match.group(0)
            start = match.end()
            end = pattern.search(lyrics, start)
            if end:
                section_lyrics = lyrics[start:end.start()]
            else:
                section_lyrics = lyrics[start:]

            sections.append({
                'track_name': row["track_name"],
                'element': section,
                'album_name': row["album_name"],
                'section_lyrics': section_lyrics
            })

        return sections
    
    def save_songs(self):
        # TODO: this is very messy, clean it up!! Works tho.

        all_songs = []

        for filename, album_name in zip(self.album_filenames, self.album_names):
            json_file = open(filename)
            album_data = json.load(json_file)
            album_songs = [track_dict["song"] for track_dict in album_data["tracks"]]
            for song in album_songs:
                song_dict = {"track_name": song["title"],
                             "album_name": album_name,
                             "lyrics_full": song["lyrics"]}
                all_songs.append(song_dict)
        
        all_songs_df = pd.DataFrame(all_songs)
        all_songs_df = self._clean_lyrics(all_songs_df)

        all_sections = []
        for _, row in all_songs_df.iterrows():
            song_sections = self._split_by_section(row)
            all_sections.append(song_sections)
        
        lyrics_by_section = pd.DataFrame([x for xs in all_sections for x in xs])
        full_lyrics = lyrics_by_section.assign(lyric=lyrics_by_section["section_lyrics"].str.split("\n")).explode("lyric").drop(columns=["section_lyrics"])
        full_lyrics = full_lyrics[full_lyrics['lyric'].str.strip() != '']
        full_lyrics['element'] = full_lyrics['element'].str.strip('[]')

        full_lyrics = full_lyrics[full_lyrics['lyric'] != "You might also like"]
        full_lyrics["lyric"] = full_lyrics["lyric"].replace(r'^You might also like(?=\S)', "", regex=True)
        full_lyrics["lyric"] = full_lyrics["lyric"].replace(r"(?<=\S)You might also like$", "", regex=True)

        full_lyrics = full_lyrics.reset_index()
        full_lyrics['line'] = full_lyrics.groupby('track_name').cumcount() + 1

        full_lyrics = full_lyrics[["track_name", "element", "album_name", "lyric", "line"]]
        full_lyrics.to_csv(f"{self.artist_name.lower()}_lyrics.csv", index=False)
        print(f"Lyrics written to {self.artist_name.lower()}_lyrics.csv.")