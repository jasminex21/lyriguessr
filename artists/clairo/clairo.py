import streamlit as st

from lyriguessr.components import *

theme_css = {
    "Immunity": {
        "background_color": "#eae2ca", 
        "button_color": "#c7a97c",
        "inputs": "#e3d3a1",
        "text_color": "black"},
    "Sling": {
        "background_color": "#735346",
        "button_color": "#443c3a",
        "inputs": "#ca966f",
        "text_color": "black"
    },
    "Charm": {
        "background_color": "#624324",
        "button_color": "#85633f",
        "inputs": "#695e2c",
        "text_color": "black"
    }}

set_global_vars(lyrics_path="./artists/clairo/clairo_lyrics.csv", 
                albums=["diary 001",
                        "Immunity",
                        "Sling",
                        "Charm"],
                leaderboard_path="./artists/clairo/leaderboard.db",
                theme_css=theme_css
                )

config_game(game_title="clairoGuessr")
init_session_states()

ui(game_title="clairoGuessr",
   instructions=['*2 Hold U*, *Get With U*, *Sis*, *Bubble Gum*, and *Heaven* <u>are</u> included in the game, under the album "Original singles."'],
   guess_placeholder="e.g. Bags or Second Nature",
   default_theme="Charm"
   )