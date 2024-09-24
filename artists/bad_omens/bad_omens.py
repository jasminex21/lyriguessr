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

acceptable_answers = {"F E R A L": ["FERAL", "F.E.R.A.L"],
                      "Reprise (The Sound of the End)": ["Reprise"],
                      "V.A.N": ["VAN"]}

set_global_vars(lyrics_path="./artists/bad_omens/bad omens_lyrics.csv", 
                albums=["Bad Omens",
                        "Finding God Before God Finds Me (Deluxe)",
                        "THE DEATH OF PEACE OF MIND",
                        "CONCRETE JUNGLE [THE OST]"],
                leaderboard_path="./artists/bad_omens/leaderboard.db",
                theme_css=theme_css,
                acceptable_answers=acceptable_answers)

config_game(game_title="badOmensGuessr")
init_session_states()

ui(game_title="badOmensGuessr",
   instructions=["Only *V.A.N*, *THE DRAIN*, *TERMS & CONDITIONS*, *EVEN*, *ANYTHING > HUMAN*, and *NERVOUS SYSTEM* are included from *CONCRETE JUNGLE [THE OST]*."],
   guess_placeholder="e.g. Like a Villain or Dethrone",
   default_theme="THE DEATH OF PEACE OF MIND"
   )