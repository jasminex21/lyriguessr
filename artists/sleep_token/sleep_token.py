import streamlit as st

from lyriguessr.components import *

theme_css = {
    "One": {
        "background_color": "#131313", 
        "button_color": "#696969",
        "inputs": "#8C8C8C",
        "text_color": "white"},
    "Two": {
        "background_color": "#815430",
        "button_color": "#58331D",
        "inputs": "#987145",
        "text_color": "black"
    }}

set_global_vars(lyrics_path="./artists/sleep_token/sleep token_lyrics.csv", 
                albums=["One - EP", 
                "Two - EP", 
                "Sundowning", 
                "This Place Will Become Your Tomb",
                "Take Me Back to Eden"],
                leaderboard_path="./artists/sleep_token/leaderboard.db",
                theme_css=theme_css)

config_game(game_title="sleepTokenGuessr")
init_session_states()

ui(game_title="sleepTokenGuessr",
   instructions=[],
   similar_artists=["Bad Omens"],
   guess_placeholder="e.g. Nazareth or Granite",
   default_theme="One")