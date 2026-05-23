import requests
import streamlit as st
import pandas as pd

API_KEY = st.secrets["75b372c45c4019ee79142ca0e3718132"]

headers = {"x-apisports-key": API_KEY}
params = {"league": 103, "season": 2024}

st.set_page_config(page_title="Eliteserien 2024", page_icon="⚽", layout="wide")
st.markdown("""
    <div style="background: linear-gradient(90deg, #00d4aa, #0e1117); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 2.5em;">⚽ Eliteserien 2024</h1>
        <p style="color: #00d4aa; margin: 0;">Live Dashboard</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        h1 { color: #00d4aa; font-family: 'Arial Black'; letter-spacing: 2px; }
        h2, h3 { color: #ffffff; }
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #00d4aa; color: #0e1117; padding: 10px; text-align: left; }
        td { padding: 8px 10px; border-bottom: 1px solid #1e2530; color: #ffffff; }
        tr:hover { background-color: #1e2530; }
        .stSelectbox label { color: #00d4aa; font-weight: bold; }
        .stMetric { background-color: #1e2530; border-radius: 8px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# Standings
response = requests.get("https://v3.football.api-sports.io/standings", headers=headers, params=params)
data_json = response.json()

if not data_json["response"]:
    st.error(f"API error: {data_json.get('errors')}")
    st.stop()

standings = data_json["response"][0]["league"]["standings"][0]

teams = [team["team"]["name"] for team in standings]
selected_team = st.selectbox("Select a team", teams)
for team in standings:
    if team["team"]["name"] == selected_team:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0;">
                <img src="{team["team"]["logo"]}" width="60"/>
                <h2 style="color: white; margin: 0;">{team["team"]["name"]}</h2>
                <span style="color: #00d4aa; font-size: 1.2em;">#{team["rank"]} in Eliteserien</span>
            </div>
        """, unsafe_allow_html=True)

# Show selected team stats
for team in standings:
    if team["team"]["name"] == selected_team:
        st.write("---")
        st.markdown(f"""
    <div style="display: flex; gap: 15px; margin: 20px 0;">
        <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
            <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">POINTS</p>
            <h2 style="color: white; margin: 0;">{team["points"]}</h2>
        </div>
        <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
            <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">WON</p>
            <h2 style="color: white; margin: 0;">{team["all"]["win"]}</h2>
        </div>
        <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
            <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">DRAWN</p>
            <h2 style="color: white; margin: 0;">{team["all"]["draw"]}</h2>
        </div>
        <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
            <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">LOST</p>
            <h2 style="color: white; margin: 0;">{team["all"]["lose"]}</h2>
        </div>
        <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
            <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">GOAL DIFF</p>
            <h2 style="color: white; margin: 0;">{team["goalsDiff"]}</h2>
        </div>
    </div>
""", unsafe_allow_html=True)
        st.write("---")
st.subheader(f"Top Players — {selected_team}")

players_response = requests.get(
    "https://v3.football.api-sports.io/players",
    headers=headers,
    params={"league": 103, "season": 2024, "team": team["team"]["id"]}
)

players = players_response.json()["response"]

players_data = []
for p in players:
    players_data.append({
        "Player": f'<img src="{p["player"]["photo"]}" width="25"/> {p["player"]["name"]}',
        "Age": p["player"]["age"],
        "Goals": p["statistics"][0]["goals"]["total"],
        "Assists": p["statistics"][0]["goals"]["assists"],
        "Appearances": p["statistics"][0]["games"]["appearences"],
    })

df_players = pd.DataFrame(players_data)
st.write(df_players.to_html(escape=False, index=False), unsafe_allow_html=True)

data = []
for team in standings:
    data.append({
        "Rank": team["rank"],
        "Club": f'<img src="{team["team"]["logo"]}" width="25"/> {team["team"]["name"]}',
        "Points": team["points"],
        "Played": team["all"]["played"],
        "Won": team["all"]["win"],
        "Drawn": team["all"]["draw"],
        "Lost": team["all"]["lose"],
        "GD": team["goalsDiff"],
    })

df = pd.DataFrame(data)
st.subheader("Final Standings")
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Top Scorers
st.write("---")
st.subheader("⚽ Top Scorers")

scorers_response = requests.get(
    "https://v3.football.api-sports.io/players/topscorers",
    headers=headers,
    params={"league": 103, "season": 2024}
)

scorers = scorers_response.json()["response"]

scorers_data = []
for player in scorers:
    scorers_data.append({
        "Player": f'<img src="{player["player"]["photo"]}" width="25"/> {player["player"]["name"]}',
        "Club": player["statistics"][0]["team"]["name"],
        "Goals": player["statistics"][0]["goals"]["total"],
        "Assists": player["statistics"][0]["goals"]["assists"],
        "Appearances": player["statistics"][0]["games"]["appearences"],
    })

df_scorers = pd.DataFrame(scorers_data)
st.write(df_scorers.to_html(escape=False, index=False), unsafe_allow_html=True)