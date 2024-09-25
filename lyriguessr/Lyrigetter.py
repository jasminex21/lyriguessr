import os
import json
import re
import pandas as pd
from lyricsgenius import Genius

class Lyrigetter:

    def __init__(self, genius_token, album_names, artist_name,
                 filenames=None):
        
        self.genius = Genius(genius_token)
        self.album_names = album_names
        self.artist_name = artist_name

        self.album_filenames = []
        if filenames: 
            for fname, album_name in zip(filenames, self.album_names): 
                if fname: 
                    self.album_filenames.append(fname)
                else: 
                    self.album_filenames.append(f"{'_'.join(album_name.split(' '))}.json")
        else:
            filenames = [re.sub(r'[^\w\s]','', name) for name in self.album_names]
            self.album_filenames = [f"{'_'.join(album_name.split(' '))}.json" for album_name in filenames]
    
    def store_album_data(self):
        """Using search_album from lyricsgenius to obtain songs from each 
           provided album"""
        
        for album_name, album_filename in zip(self.album_names, self.album_filenames):
            if os.path.exists(album_filename):
                print(f"File {album_filename} already exists; moving on")
                continue
            album = self.genius.search_album(album_name, self.artist_name)
            album.save_lyrics(filename=album_filename)
    
    def _clean_lyrics(self, df):
        """Preliminary cleaning of each lyrics string"""

        # removes everything up to the first square bracket (indicating first section)
        df["lyrics_full"] = df["lyrics_full"].replace(r"^.*?\[", "[", regex=True)
        # removes the nEmbed or Embed at the end of the string
        df["lyrics_full"] = df["lyrics_full"].replace(r"\d*Embed\'*\"*$", "", regex=True)
        # removes unicode character \u2005
        df["lyrics_full"] = df["lyrics_full"].replace(r"\u2005", " ", regex=True)

        return df
    
    def _split_by_section(self, row): 
        """Splits the chunk containing all lyrics into smaller chunks determined
           by section"""

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
    
    def _expand_sections(self, all_sections):
        """Internal method that splits chunks of section lyrics into individual 
           lines. Also does some cleaning, as scraping the lyrics results in 
           occasional adverts."""

        lyrics_by_section = pd.DataFrame([x for xs in all_sections for x in xs])

        # split each whole section into lines split by \n
        full_lyrics = lyrics_by_section.assign(lyric=lyrics_by_section["section_lyrics"].str.split("\n")).explode("lyric").drop(columns=["section_lyrics"])
        # remove empty rows
        full_lyrics = full_lyrics[full_lyrics['lyric'].str.strip() != '']
        # remove square brackets from section indicator
        full_lyrics['element'] = full_lyrics['element'].str.strip('[]')

        # ads/recommendations are occasionally scraped; remove them
        full_lyrics = full_lyrics[full_lyrics['lyric'] != "You might also like"]
        full_lyrics["lyric"] = full_lyrics["lyric"].replace(r'^You might also like(?=\S)', "", regex=True)
        full_lyrics["lyric"] = full_lyrics["lyric"].replace(r"(?<=\S)You might also like$", "", regex=True)
        full_lyrics = full_lyrics[~full_lyrics['lyric'].str.contains("Get tickets as low")]

        # add line number
        full_lyrics = full_lyrics.reset_index()
        full_lyrics['line'] = full_lyrics.groupby('track_name').cumcount() + 1

        full_lyrics = full_lyrics[["track_name", "element", "album_name", "lyric", "line"]]

        return full_lyrics
    
    def save_songs(self):
        """Stores all album songs into a CSV file"""

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
        
        full_lyrics = self._expand_sections(all_sections)

        full_lyrics.to_csv(f"{self.artist_name.lower()}_lyrics.csv", index=False)
        print(f"Lyrics written to {self.artist_name.lower()}_lyrics.csv.")
    
    def add_song(self, song_name, album_name): 
        """Adds a song to the original artist dataset. Useful if adding non-album singles."""

        song = self.genius.search_song(song_name, self.artist_name)
        lyrics = song.lyrics
        song_dict = {
            "track_name": [song_name],
            "album_name": [album_name],
            "lyrics_full": [lyrics]
        }

        song_df = self._clean_lyrics(pd.DataFrame(song_dict))
        song_sections = [self._split_by_section(song_df.iloc[0])]

        full_lyrics = self._expand_sections(song_sections)

        current_lyrics = pd.read_csv(f"{self.artist_name.lower()}_lyrics.csv")
        all_lyrics = pd.concat([current_lyrics, full_lyrics])
        all_lyrics.to_csv(f"{self.artist_name.lower()}_lyrics.csv", index=False)
        print(f"Song {song_name} added to {self.artist_name.lower()}_lyrics.csv")
    
    def remove_songs(self, song_names):

        current_lyrics = pd.read_csv(f"{self.artist_name.lower()}_lyrics.csv")
        filtered_lyrics = current_lyrics[~current_lyrics["track_name"].isin(song_names)]
        filtered_lyrics.to_csv(f"{self.artist_name.lower()}_lyrics.csv", index=False)
        print(f"Songs {song_names} removed from {self.artist_name.lower()}_lyrics.csv")

    def save_counts(self):
        """Creates CSV file containing counts of the top 5 most common lyrics
           in the artist dataset"""
        all_lyrics = pd.read_csv(f"{self.artist_name.lower()}_lyrics.csv")

        counts = all_lyrics["lyric"].value_counts()
        counts = pd.DataFrame(counts).head(5).reset_index()
        counts.columns = ['lyric', 'count']

        counts["song"] = [all_lyrics[all_lyrics["lyric"] == lyr]["track_name"].values[0] 
                          for lyr in counts["lyric"].values]
        counts["lyric"] = [f'"{lyr}"' for lyr in counts["lyric"].values]
        row_count = all_lyrics.shape[0]
        counts["%"] = [f"{round(num * 100 / row_count, 2)}%" for num in counts["count"].values]
        
        counts.to_csv(f"{self.artist_name.lower()}_counts.csv", index=False)
        print(f"Counts added to {self.artist_name.lower()}_counts.csv")
    
    def add_stats(self): 

        current_stats = pd.read_csv("/home/jasmine/PROJECTS/lyriguessr/artist_dataset_statistics.csv")
        all_lyrics = pd.read_csv(f"{self.artist_name.lower()}_lyrics.csv")

        stats = {"artist": [self.artist_name],
                 "nlines": [all_lyrics.shape[0]],
                 "songs": [all_lyrics['track_name'].nunique()],
                 "albums": [all_lyrics['album_name'].nunique()],
                 "avg_words_per_line": [round(all_lyrics['lyric'].apply(lambda x: len(x.split())).mean(), 2)]} 
        artist_df = pd.DataFrame(stats, 
                                 columns=["artist", "nlines", "songs", "albums", "avg_words_per_line"])
        all_stats = pd.concat([current_stats, artist_df])
        all_stats = all_stats.sort_values(by='nlines', ascending=False)
        all_stats.to_csv("/home/jasmine/PROJECTS/lyriguessr/artist_dataset_statistics.csv", index=False)