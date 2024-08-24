import os
import streamlit as st
import pandas as pd
from time import strftime, gmtime

from lyriguessr.Lyrics import Lyrics
from lyriguessr.Leaderboard import Leaderboards

### GLOBAL VARS ###
ALL_LYRICS = pd.read_csv("./artists/radiohead/radiohead_lyrics.csv")
ALL_ALBUMS = ["Pablo Honey",
              "The Bends",
              "OK Computer",
              "Kid A",
              "Amnesiac",
              "Hail To the Thief",
              "In Rainbows",
              "The King Of Limbs", 
              "A Moon Shaped Pool"]
DIFFICULTIES = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]
GAME_MODES = ["Survival (with 5 lives)",
              "Casual (no lives)"]
POINTS_MAPPING = {"Easy (an entire section, e.g. chorus)": 1, 
                  "Medium (2 lines)": 3, 
                  "Hard (1 line)": 5}
DIFFICULTY_MAPPING = {"Easy (an entire section, e.g. chorus)": "Easy", 
                      "Medium (2 lines)": "Medium", 
                      "Hard (1 line)": "Hard"}
MODE_MAPPING = {"Survival (with 5 lives)": "Survival",
                "Casual (no lives)": "Casual"}
THEME = {"background_color": "#222222",
        "button_color": "#000000",
        "inputs": "#4C4949",
        "text_color": "white"}
LEADERBOARD = "./artists/radiohead/leaderboard.db"

### PAGE CONFIG
st.set_page_config(layout='wide',
                   page_title="radioheadGuessr",
                   page_icon="./favicon.png",
                   initial_sidebar_state="collapsed",)
                   # menu_items={'About': "#### tayLyrics: A lyrics guessing game for Swifties"})

### SESSION STATES ###
if "game_in_progress" not in st.session_state: 
    st.session_state.game_in_progress = False
if "lyrics" not in st.session_state: 
    st.session_state.lyrics = Lyrics(data=ALL_LYRICS)
if "generated_lyrics" not in st.session_state: 
    st.session_state.generated_lyrics = None
if "correct_song" not in st.session_state: 
    st.session_state.correct_song = None
if "correct_album" not in st.session_state: 
    st.session_state.correct_album = None
if "correct_section" not in st.session_state: 
    st.session_state.correct_section = None
if "next_line" not in st.session_state: 
    st.session_state.next_line = None
if "prev_line" not in st.session_state: 
    st.session_state.prev_line = None
if "round_count" not in st.session_state: 
    st.session_state.round_count = 1
if "guess" not in st.session_state:
    st.session_state.guess = None
if "disable_buttons" not in st.session_state: 
    st.session_state.disable_buttons = False
if "correct_feedback" not in st.session_state: 
    st.session_state.correct_feedback = ""
if "incorrect_feedback" not in st.session_state: 
    st.session_state.incorrect_feedback = ""
if "points" not in st.session_state: 
    st.session_state.points = 0
if "round_results" not in st.session_state:
    st.session_state.round_results = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "streaks" not in st.session_state:
    st.session_state.streaks = []
if "album_counter" not in st.session_state: 
    st.session_state.album_counter = {}
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "game_mode" not in st.session_state:
    st.session_state.game_mode = None
if "albums" not in st.session_state:
    st.session_state.albums = []
if "lives" not in st.session_state:
    st.session_state.lives = 5
if "hints" not in st.session_state:
    st.session_state.hints = 0
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "gameover_feedback" not in st.session_state:
    st.session_state.gameover_feedback = ""
if "disable_hint_btn" not in st.session_state:
    st.session_state.disable_hint_btn = False
if "hint_feedback" not in st.session_state:
    st.session_state.hint_feedback = ""
if "giveup_feedback" not in st.session_state:
    st.session_state.giveup_feedback = ""
if "album_accs" not in st.session_state:
    st.session_state.album_accs = {}
if "past_game_stats" not in st.session_state:
    st.session_state.past_game_stats = ""
if "enable_leaderboard" not in st.session_state:
    st.session_state.enable_leaderboard = False
if "disable_name_input" not in st.session_state: 
    st.session_state.disable_name_input = False
if "submitted_datetime" not in st.session_state: 
    st.session_state.submitted_datetime = None
if "rank_msg" not in st.session_state:
    st.session_state.rank_msg = ""
if "start_btn_clicked" not in st.session_state:
    st.session_state.start_btn_clicked = False
if "hide_buttons" not in st.session_state:
    st.session_state.hide_buttons = False

### FUNCTIONS ###
def apply_theme(selected_theme):
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

    .stApp > header {{
        background-color: transparent;
    }}
    .stApp {{
        background: {selected_theme['background_color']};
        color: {selected_theme["text_color"]};
        font-family: 'Outfit', sans-serif;
    }}
    button[data-baseweb="tab"] {{
        background-color: transparent !important;
    }}
    [data-baseweb="popover"], div[data-baseweb="popover"] > div {{
        background-color: {"grey" if selected_theme["text_color"] == "black" else "#262730"};
    }}
    [data-testid="stSidebar"] {{
        background: {selected_theme['background_color']};
    }}
    button {{
        background-color: {selected_theme['button_color']} !important;
    }}
    button:disabled {{
        background-color: transparent !important;
    }}
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > input {{
        background-color: {selected_theme["inputs"]};
        color: {selected_theme["text_color"]};
        -webkit-text-fill-color: {selected_theme["text_color"]} !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif;
    }}
    p, ul, li {{
        color: {selected_theme["text_color"]};
        font-weight: 600 !important;
        font-size: large !important;
        font-family: 'Outfit', sans-serif;
    }}
    h3, h2, h1, strong, .lyrics, h4 {{
        color: {selected_theme["text_color"]};
        font-weight: 900 !important;
        font-family: 'Outfit', sans-serif;
    }}
    .lyrics {{
        font-size: 20px;
    }}
    [data-baseweb="tag"] {{
        background: {selected_theme['button_color']} !important;
        color: {selected_theme["text_color"]};
        font-family: 'Outfit', sans-serif;
    }}
    th {{
        color: {selected_theme["text_color"]} !important;
        font-weight: 900 !important;
        text-align: left !important;
        font-family: 'Outfit', sans-serif;
    }}
    td {{
        color: {selected_theme["text_color"]} !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def clear_guess(): 
    """Clears the guess text input once an answer is submitted"""
    st.session_state.guess = st.session_state.temp_guess
    st.session_state.temp_guess = ""

def clear_feedback():
    st.session_state.correct_feedback = ""
    st.session_state.incorrect_feedback = ""
    st.session_state.giveup_feedback = ""
    st.session_state.hint_feedback = ""
    st.session_state.gameover_feedback = ""

def filter_lyrics():
    """Resets the lyrics generator such that it only generates lyrics from the selected albums"""
    filtered_lyrics = ALL_LYRICS[ALL_LYRICS["album_name"].isin(st.session_state.albums)].reset_index()
    st.session_state.lyrics = Lyrics(data=filtered_lyrics)

def game_started(): 
    
    st.session_state.game_in_progress = True

    clear_feedback()

    if len(st.session_state.albums) != len(ALL_ALBUMS):
        filter_lyrics()
    
    else: 
        st.session_state.lyrics = Lyrics(data=ALL_LYRICS)

    (st.session_state.generated_lyrics, 
    st.session_state.correct_song, 
    st.session_state.correct_album, 
    st.session_state.next_line, 
    st.session_state.prev_line, 
    st.session_state.correct_section) = regenerate()
    
    st.session_state.album_counter = {album_name: [] for album_name in st.session_state.albums}
    st.session_state.enable_leaderboard = False
    st.session_state.disable_name_input = False
    st.session_state.submitted_datetime = None
    st.session_state.rank_msg = ""
    st.session_state.round_count = 1
    st.session_state.round_results = []
    st.session_state.disable_buttons = False
    st.session_state.disable_hint_btn = False
    st.session_state.points = 0
    st.session_state.streak = 0
    st.session_state.streaks = []
    st.session_state.hints = 0
    st.session_state.hints_used = 0
    st.session_state.lives = 5
    st.session_state.guess = None
    st.session_state.hide_buttons = False

def new_round():
    st.session_state.round_count += 1
    st.session_state.disable_buttons = False
    st.session_state.disable_hint_btn = False
    st.session_state.hints = 0
    st.session_state.guess = None
    st.session_state.hide_buttons = False

    clear_feedback()

    (st.session_state.generated_lyrics, 
     st.session_state.correct_song, 
     st.session_state.correct_album, 
     st.session_state.next_line, 
     st.session_state.prev_line, 
     st.session_state.correct_section) = regenerate()

def regenerate():
    generated_lyrics = f'<div class="lyrics">{st.session_state.lyrics.generate(st.session_state.difficulty)}</div>'
    correct_song = st.session_state.lyrics.get_track_name()
    correct_album = st.session_state.lyrics.get_album_name()
    next_line = st.session_state.lyrics.get_next_line()
    prev_line = st.session_state.lyrics.get_previous_line()
    section = st.session_state.lyrics.get_section()

    return generated_lyrics, correct_song, correct_album, next_line, prev_line, section

def answered_correctly():
    st.session_state.incorrect_feedback = ""
    st.session_state.points += POINTS_MAPPING[st.session_state.difficulty]
    st.session_state.correct_feedback = f"""That is correct! The answer is indeed **{st.session_state.correct_song}**, 
                                            {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.
                                            \n\nYou earned {POINTS_MAPPING[st.session_state.difficulty]} points and have 
                                            {st.session_state.points} total points."""
    st.session_state.round_results.append(True)
    st.session_state.guess = None
    st.session_state.disable_buttons = True
    st.session_state.disable_hint_btn = True
    st.session_state.streak += 1
    st.session_state.album_counter[st.session_state.correct_album].append(True)
    st.session_state.hide_buttons = True

def answered_incorrectly():
    st.session_state.points -= 1
    st.session_state.incorrect_feedback = f'''"{st.session_state.guess}" is not correct. Please try again!\n\nYou lost 1 point and have **{st.session_state.points} total points**.'''
    st.session_state.lives -= 1
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0

    if st.session_state.game_mode == "Survival (with 5 lives)":
        st.session_state.incorrect_feedback += f"\n\nYou lost a life and have **{st.session_state.lives} lives** left."
        if st.session_state.lives == 0:
            st.session_state.disable_buttons = True
            st.session_state.round_results.append(False)
            st.session_state.album_counter[st.session_state.correct_album].append(False)
            st.session_state.gameover_feedback = f'''"{st.session_state.guess}" is not correct.
                                                     \n\n**GAME OVER**: You ran out of lives! Please start a new game.
                                                     \n\nThe correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.'''
            st.session_state.incorrect_feedback = ""
            end_game()
            st.rerun()
    st.session_state.guess = None

def hint():
    st.session_state.hints += 1
    st.session_state.hints_used += 1
    st.session_state.points -= 1

    if st.session_state.hints == 1: 
        st.session_state.hint_feedback += f"Hint 1: this song comes from the album **{st.session_state.correct_album}**"
    if st.session_state.hints == 2: 
        st.session_state.hint_feedback += f'\n\nHint 2: the next line of this song is *"{st.session_state.next_line}"*'
    if st.session_state.hints == 3: 
        st.session_state.disable_hint_btn = True
        st.session_state.hint_feedback += f'\n\nHint 3: the previous line of this song is *"{st.session_state.prev_line}"*'

def giveup():
    st.session_state.incorrect_feedback = ""
    st.session_state.disable_buttons = True
    st.session_state.disable_hint_btn = True
    st.session_state.points -= 2
    st.session_state.lives -= 1
    st.session_state.round_results.append(False)
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0
    st.session_state.hide_buttons = True
    st.session_state.album_counter[st.session_state.correct_album].append(False)

    st.session_state.giveup_feedback = f"""The correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**\n\nYou lost 2 points and have **{st.session_state.points} total points**."""        

    if st.session_state.game_mode == "Survival (with 5 lives)":
        st.session_state.giveup_feedback += f"\n\nYou lost a life and have **{st.session_state.lives} lives** left."
        if st.session_state.lives == 0: 
            st.session_state.gameover_feedback = f'''**GAME OVER**: You ran out of lives! Please start a new game.
                                                      \n\nThe correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.'''
            st.session_state.giveup_feedback = ""
            end_game()
            return

def end_game():
    # if the game is ended before an answer is provided, count it as incorrect
    if len(st.session_state.round_results) != st.session_state.round_count: 
        st.session_state.round_results.append(False)
        st.session_state.album_counter[st.session_state.correct_album].append(False)

    accuracy_pct = round((sum(st.session_state.round_results) * 100 /st.session_state.round_count), 2)
    possible_pct = round(st.session_state.points * 100 / (st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]), 2)
    accuracy_str = f"{sum(st.session_state.round_results)}/{st.session_state.round_count} ({accuracy_pct}%)"
    possible_str = f"{st.session_state.points}/{st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]} ({possible_pct}%)"

    accs = {album: (round(sum(ls) * 100/len(ls), 2), sum(ls), len(ls)) 
            if len(ls) else (0.0, 0, 0) for album, ls in st.session_state.album_counter.items()}
    st.session_state.album_accs = dict(sorted(accs.items(), 
                                       key=lambda x: (x[1][0], x[1][2], x[1][1]),
                                       reverse=True))
    st.session_state.enable_leaderboard = True if ((st.session_state.game_mode == "Survival (with 5 lives)") and
                                                   (len(st.session_state.albums) == len(ALL_ALBUMS)) and
                                                   (st.session_state.round_count >= 5)) else False
    
    
    st.session_state.past_game_stats = f"""
{DIFFICULTY_MAPPING[st.session_state.difficulty]} difficulty, {MODE_MAPPING[st.session_state.game_mode]} mode, {st.session_state.round_count} rounds played
* :dart: Accuracy: {accuracy_str}
* :100: Points out of total possible: {possible_str}
* :bulb: Hints used: {st.session_state.hints_used}
* :fire: Max streak: {max(st.session_state.streaks) if len(st.session_state.streaks) else 0}
* :moneybag: Total points: {st.session_state.points}
"""
    
    st.session_state.game_in_progress = False

def name_submitted():
    
    st.session_state.disable_name_input = True
    st.session_state.submitted_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    game_results = (st.session_state.leaderboard_name,
                    st.session_state.points,
                    st.session_state.round_count,
                    st.session_state.submitted_datetime)
    
    # clear the name input text box
    st.session_state.name = st.session_state.leaderboard_name
    st.session_state.leaderboard_name = ""

    with Leaderboards(db_path=LEADERBOARD) as leaderboard:
        leaderboard.add_to_leaderboard(st.session_state.difficulty, game_results)
        current_leaderboards = leaderboard.get_leaderboards()

    added_to_df = current_leaderboards[st.session_state.difficulty]
    filtered_row = added_to_df[added_to_df["Datetime (UTC)"].astype(str) == str(st.session_state.submitted_datetime)]
    added_rank = int(filtered_row.index[0])
    out_of = added_to_df.shape[0]

    st.session_state.rank_msg = f"Your game results were added to the leaderboard!\nYou ranked in position {added_rank} out of {out_of} total results."


def highlight_new_row(row):
    """Highlights the row that was just added to the leaderboard in green"""
    if str(row["Datetime (UTC)"]) == str(st.session_state.submitted_datetime):
        return ['background-color: #4D6D4D'] * len(row)
    else:
        return [''] * len(row)
    
def get_database(path=LEADERBOARD):
    with open(path, "rb") as f:
        return f.read()

### UI ###
with st.sidebar:

    st.markdown(f"Made with :heart: by Jasmine Xu")
    st.markdown(f"Contact me at <jasminexu@utexas.edu>")

    if os.path.exists(LEADERBOARD):

        st.divider()

        db = get_database()
        st.download_button(label="Download leaderboard",
                        data=db,
                        file_name="leaderboard.db",
                        mime="application/octet-stream")

apply_theme(THEME)
buffer1, main_col, buffer2 = st.columns([1, 3, 1])
with main_col:
    st.title("Welcome to :guitar:radioheadGuessr:guitar:!")
    if st.session_state.game_in_progress == False: 

        start_tab, past_stats_tab, leaderboard_tab = st.tabs(["Start New Game", "Past Game Statistics", "Leaderboard"])

        with start_tab: 
            exp = st.expander(":pencil2: Instructions (click to expand)", expanded=False)
            b1, c, b2 = exp.columns(3)
            with exp:
                c.image("./website/logo_cropped.png")
                st.markdown(f"Lyrics range from *{ALL_ALBUMS[0]}* to *{ALL_ALBUMS[-1]}*.")
                st.markdown(f"Return to [lyriguessr](https://jasminex21.github.io/lyriguessr/) for more artist games!")
                st.markdown("### IMPORTANT GUIDELINES:")
                st.markdown(f"Capitalization and minor spelling errors do NOT matter!")
            
            start_form = st.form("game_settings")
            with start_form:
                st.markdown("### Start a New Game")
                st.selectbox("Select a game difficulty", 
                            options=DIFFICULTIES,
                            index=DIFFICULTIES.index(st.session_state.difficulty) if st.session_state.difficulty else 0,
                            key="difficulty0")
                st.selectbox("Select a game mode",
                            options=GAME_MODES,
                            index=GAME_MODES.index(st.session_state.game_mode) if st.session_state.game_mode else 0,
                            key="game_mode0")
                with st.expander("Advanced options"):
                    st.multiselect("Select albums to generate lyrics from",
                                options=ALL_ALBUMS,
                                default=st.session_state.albums if st.session_state.albums else ALL_ALBUMS,
                                key="albums0")
                started = st.form_submit_button(":large_green_square: Start new game")

            if started: 
                st.session_state.difficulty = st.session_state.difficulty0
                st.session_state.game_mode = st.session_state.game_mode0
                st.session_state.albums = st.session_state.albums0

                if len(st.session_state.albums) == 0: 
                    start_form.error("Please select at least one album.")
                else:
                    st.session_state.start_btn_clicked = True
                
            if st.session_state.gameover_feedback: 
                st.error(st.session_state.gameover_feedback, icon="😢")

            if st.session_state.enable_leaderboard:
                st.info("You can add your scores to the leaderboard!", icon="ℹ️")

        with past_stats_tab:
            if st.session_state.past_game_stats: 
                st.markdown("### Past Game Statistics")
                st.markdown(st.session_state.past_game_stats)
                if st.session_state.album_accs:
                    with st.expander("**Per-album accuracies (click to expand)**"):
                        s = ""
                        for album_name, tup in st.session_state.album_accs.items(): 
                            s += f"* {album_name}: {tup[0]}% ({tup[1]}/{tup[2]})\n"
                        st.markdown(s)
            else: 
                st.markdown("#### You must start a game before viewing past game statistics!")

        with leaderboard_tab: 
            st.markdown("### Leaderboards")
            if st.session_state.enable_leaderboard:
                with st.popover(f"Add your results to the leaderboard"):
                    st.markdown("#### Add your results")
                    st.markdown(f"Points: {st.session_state.points}")
                    st.text_input("Enter your name",
                                key="leaderboard_name",
                                disabled=st.session_state.disable_name_input,
                                on_change=name_submitted)
                st.markdown(st.session_state.rank_msg)
            else: 
                st.markdown(f"Your game results can only be added to the leaderboard if you played 5+ rounds in Survival mode with all albums enabled.")

            with Leaderboards(db_path=LEADERBOARD) as leaderboard:
                current_leaderboards = leaderboard.get_leaderboards()
            
            leaderboard_to_show = st.selectbox("Select leaderboard to display",
                                            options=DIFFICULTIES,
                                            index=DIFFICULTIES.index(st.session_state.difficulty) if st.session_state.difficulty else 0)
            shown_leaderboard = current_leaderboards[leaderboard_to_show]
            shown_leaderboard = shown_leaderboard.style.apply(highlight_new_row, axis=1)
            st.markdown(f"### {DIFFICULTY_MAPPING[leaderboard_to_show]} Leaderboard")
            st.table(shown_leaderboard) #, use_container_width=True)

    if st.session_state.start_btn_clicked:
        game_started()
        
        st.session_state.start_btn_clicked = False
        st.rerun()

    if st.session_state.game_in_progress == True: 
        with st.container(border=True):
            game_tab, stats_tab = st.tabs(["Game", "Current Game Statistics"])
            with game_tab:
                st.write(f"<h4><u>Round {st.session_state.round_count}<u/></h4>", unsafe_allow_html=True)
                st.write(st.session_state.generated_lyrics, unsafe_allow_html=True)
                st.text("")
                st.text_input("Enter your guess",
                            placeholder="e.g. Creep or No Surprises",
                            key="temp_guess",
                            on_change=clear_guess,
                            disabled=st.session_state.disable_buttons)
                if st.session_state.guess: 
                    if st.session_state.lyrics.get_guess_feedback(st.session_state.guess): 
                        answered_correctly()
                    else: 
                        answered_incorrectly()
                
                if not st.session_state.hide_buttons:
                    col1, col2, col3, col4 = st.columns([1.5, 3, 1, 1])
                    hint_btn = col1.button(":bulb: Hint", on_click=hint, disabled=st.session_state.disable_hint_btn,help="You get 3 hints per round; Hint 1 gives the album, and Hint 2 and 3 give the next and previous lines, respectively. Each hint deducts 1 point from your total.")
                    giveup_btn = col2.button(":no_entry: Give up", on_click=giveup, 
                                            disabled=st.session_state.disable_buttons)
                
                if st.session_state.hint_feedback:
                    st.info(f"{st.session_state.hint_feedback}", icon="ℹ️")

                if st.session_state.incorrect_feedback:
                    st.error(f"{st.session_state.incorrect_feedback}", icon="🚨")

                if st.session_state.correct_feedback:
                    st.success(f"{st.session_state.correct_feedback}", icon="✅")
                    st.button(":arrow_right: Next round", on_click=new_round)
                
                if (st.session_state.giveup_feedback) and not (st.session_state.gameover_feedback):
                    st.error(f"{st.session_state.giveup_feedback}", icon="🚨")
                    st.button(":arrow_right: Next round", on_click=new_round)
                
                col1, col2, col4 = st.columns(3)
                col4.button(":octagonal_sign: End current game", on_click=end_game, key="end_game")

            with stats_tab:
                st.markdown(f"### In-Game Statistics")
                st.markdown(f"**{DIFFICULTY_MAPPING[st.session_state.difficulty]} difficulty, {MODE_MAPPING[st.session_state.game_mode]} mode**")
                st.markdown(f"* :large_green_circle: Round: {st.session_state.round_count}")

                accuracy_pct = round((sum(st.session_state.round_results) * 100 /st.session_state.round_count), 2)
                possible_pct = round(st.session_state.points * 100 / (st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]), 2)
                accuracy_str = f"{sum(st.session_state.round_results)}/{st.session_state.round_count} ({accuracy_pct}%)"
                possible_str = f"{st.session_state.points}/{st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]} ({possible_pct}%)"
                
                st.markdown(f"* :dart: Accuracy: {accuracy_str}")
                st.markdown(f"* :100: Points out of total possible: {possible_str}")
                st.markdown(f"* :fire: Current streak: {st.session_state.streak}")
                st.markdown(f"* :moneybag: Total points: {st.session_state.points}")
                if st.session_state.game_mode == "Survival (with 5 lives)":
                    st.markdown(f"* :space_invader: Lives: {st.session_state.lives}")