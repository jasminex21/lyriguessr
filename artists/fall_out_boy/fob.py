import streamlit as st

from lyriguessr.components import *

theme_css = {
    "The Worst In Me": {
        "background_color": "#6E5A4E", 
        "button_color": "#513E32",
        "inputs": "#7F534B",
        "text_color": "white"},
    "Dethrone": {
        "background_color": "#909BA2",
        "button_color": "#686E75",
        "inputs": "#dcdee0",
        "text_color": "black"
    },
    "THE DEATH OF PEACE OF MIND": {
        "background_color": "#AC4735",
        "button_color": "#82332A",
        "inputs": "#B58B6F",
        "text_color": "black"
    }}

acceptable_answers = {"Sending Postcards from a Plane Crash (Wish You Were Here)": ["Sending Postcards from a Plane Crash"],
                      "I’ve Got a Dark Alley and a Bad Idea That Says You Should Shut Your Mouth (Summer Song)": ["I’ve Got a Dark Alley and a Bad Idea That Says You Should Shut Your Mouth"],
                      "7 Minutes in Heaven (Atavan Halen)": ["7 Minutes in Heaven"]}

set_global_vars(lyrics_path="./artists/fall_out_boy/fall out boy_lyrics.csv", 
                albums=["Take This to Your Grave",
                        "From Under the Cork Tree",
                        "Infinity on High",
                        "Folie à Deux",
                        "Save Rock and Roll",
                        "American Beauty / American Psycho",
                        "MANIA",
                        "So Much (For) Stardust"],
                leaderboard_path="./artists/fall_out_boy/leaderboard.db",
                # theme_css=theme_css,
                acceptable_answers=acceptable_answers)

config_game(game_title="fobGuessr")
init_session_states()

ui(game_title="fobGuessr",
   instructions=[""],
   guess_placeholder="e.g. Immortals or Love From The Other Side",
   # default_theme="THE DEATH OF PEACE OF MIND"
   )