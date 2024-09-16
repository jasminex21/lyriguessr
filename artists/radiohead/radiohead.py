import streamlit as st

from lyriguessr.components import *

acceptable_answers = {"Street Spirit (Fade Out)": ["Street Spirit"],
                      "Exit Music (For A Film)": ["Exit Music"],
                      "2 + 2 = 5": ["2+2=5"],
                      "Weird Fishes/Arpeggi": ["Weird Fishes"]}

set_global_vars(lyrics_path="./artists/radiohead/radiohead_lyrics.csv", 
                albums=["Pablo Honey",
                        "The Bends",
                        "OK Computer",
                        "Kid A",
                        "Amnesiac",
                        "Hail To the Thief",
                        "In Rainbows",
                        "The King Of Limbs", 
                        "A Moon Shaped Pool"],
                leaderboard_path="./artists/radiohead/leaderboard.db",
                acceptable_answers=acceptable_answers)

config_game(game_title="radioheadGuessr")
init_session_states()

ui(game_title="radioheadGuessr",
   instructions=[],
   guess_placeholder="e.g. Creep or No Surprises")