import streamlit as st

from lyriguessr.components import *

# TODO: add themes

set_global_vars(lyrics_path="./artists/lana_del_ray/lana del ray_lyrics.csv", 
                albums=["Born to Die (Deluxe)",
                        "Paradise",
                        "Ultraviolence (Deluxe)",
                        "Honeymoon",
                        "Lust for Life",
                        "Norman Fucking Rockwell!",
                        "Chemtrails Over the Country Club",
                        "Blue Banisters",
                        "Did you know that there’s a tunnel under Ocean Blvd"],
                leaderboard_path="./artists/lana_del_ray/leaderboard.db")

config_game(game_title="lanaGuessr")
init_session_states()

ui(game_title="lanaGuessr",
   instructions=['Yes, you do in fact have to type out "Grandfather please stand on the shoulders of my father while he’s deep-sea fishing" in full...apologies. Bring the issue up with Lana, not me!'],
   guess_placeholder="e.g. Video Games or A&W")