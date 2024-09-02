import streamlit as st

from lyriguessr.components import *

theme_css = {
    "SOUR / GUTS": {
        "background_color": "#64507D", 
        "button_color": "#5B417D",
        "inputs": "#85739D",
        "text_color": "black"}}

set_global_vars(lyrics_path="./artists/olivia_rodrigo/olivia rodrigo_lyrics.csv", 
                albums=["SOUR", 
                        "GUTS (spilled)"],
                leaderboard_path="./artists/olivia_rodrigo/leaderboard.db",
                theme_css=theme_css)

config_game(game_title="oliviaRodriguessr")
init_session_states()

ui(game_title="oliviaRodriguessr",
   instructions=[],
   guess_placeholder="e.g. drivers license or get him back!",
   default_theme="SOUR / GUTS")