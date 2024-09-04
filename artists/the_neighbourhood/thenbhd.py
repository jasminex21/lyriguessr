import streamlit as st

from lyriguessr.components import *

set_global_vars(lyrics_path="./artists/the_neighbourhood/the neighbourhood_lyrics.csv", 
                albums=["I'm Sorry",
                        "I Love You.",
                        "The Love Collection",
                        "#000000 & #FFFFFF",
                        "Wiped Out!",
                        "Hard to Imagine the Neighbourhood Ever Changing",
                        "Chip Chrome & the Mono-Tones (Deluxe)"],
                leaderboard_path="./artists/the_neighbourhood/leaderboard.db")

config_game(game_title="nbhdGuessr")
init_session_states()

ui(game_title="nbhdGuessr",
   instructions=[],
   guess_placeholder="e.g. Sweater Weather or Single")