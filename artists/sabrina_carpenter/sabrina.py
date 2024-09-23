import streamlit as st

from lyriguessr.components import *

theme_css = {
    "emails i can't send": {
        "background_color": "#e6c8b8", 
        "button_color": "#8b6c5c",
        "inputs": "#d9b487",
        "text_color": "black"},
    "Short n' Sweet": {
        "background_color": "#7484b4",
        "button_color": "#5C739B",
        "inputs": "#EBD6B7",
        "text_color": "black"
    }}

set_global_vars(lyrics_path="./artists/sabrina_carpenter/sabrina carpenter_lyrics.csv", 
                albums=["Eyes Wide Open",
                        "EVOLution",
                        "Singular: Act I",
                        "Singular Act II",
                        "emails i can’t send fwd:",
                        "Short n’ Sweet"],
                leaderboard_path="./artists/sabrina_carpenter/leaderboard.db",
                theme_css=theme_css)

config_game(game_title="sabrinaGuessr")
init_session_states()

ui(game_title="sabrinaGuessr",
   instructions=[],
   guess_placeholder="e.g. Thumbs or Espresso",
   default_theme="Short n' Sweet")