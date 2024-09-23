import streamlit as st

from lyriguessr.components import *

theme_css = {
    "Double Dare": {
        "background_color": "#DCCF7D",
        "button_color": "#838A9A", 
        "inputs": "#FFEF8A", 
        "text_color": "black"},
    "Entertainment": {
        "background_color": "#E7E5D8", 
        "button_color": "#74708E",
        "inputs": "#9693A4",
        "text_color": "black"}, 
    "FANDOM": {
        "background_color": "#5A7B53",
        "button_color": "#FFBD6C",
        "inputs": "#F5DC9D",
        "text_color": "black"},
    "Greatest Hits": {
        "background_color": "#4C7A9D",
        "button_color": "#F5B464",
        "inputs": "#FCC98B",
        "text_color": "black"},
    "INTELLECTUAL PROPERTY": {
        "background_color": "#B85151",
        "button_color": "#52557A",
        "inputs": "#747AB8",
        "text_color": "black"}}

acceptable_answers = {"Hawaii (Stay Awake)": ["Hawaii"],
                      "Peach (Lobotomy)": ["Peach"], 
                      "[Reboot]": ["Reboot"],
                      "I Miss Having Sex But at Least I Don’t Wanna Die Anymore": ["I Miss Having Sex"],
                      "You’d Be Paranoid Too (If Everyone Was Out to Get You)": ["You’d Be Paranoid Too"],
                      "Gladiator (Interlude)": ["Gladiator"],
                      "END OF THE WATER (FEEL)": ["END OF THE WATER"]}

set_global_vars(lyrics_path="./artists/waterparks/waterparks_lyrics.csv", 
                albums=["Airplane Conversations",
                        "Black Light",
                        "Cluster",
                        "Double Dare",
                        "Entertainment",
                        "FANDOM", 
                        "Greatest Hits",
                        "INTELLECTUAL PROPERTY"],
                leaderboard_path="./artists/waterparks/leaderboard.db",
                theme_css=theme_css,
                acceptable_answers=acceptable_answers)

config_game(game_title="waterparksGuessr")
init_session_states()

ui(game_title="waterparksGuessr",
   instructions=["Candy, What We Do For Fun, and Silver (Acoustic) are not included!"],
   guess_placeholder="e.g. 21 Questions or Numb",
   default_theme="Entertainment")