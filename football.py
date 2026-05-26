import requests
import streamlit as st
import pandas as pd

API_KEY = st.secrets["API_FOOTBALL_KEY"]

headers = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="Premier League 2025/26", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #00d4aa; color: #0e1117; padding: 10px; text-align: left; }
        td { padding: 8px 10px; border-bottom: 1px solid #1e2530; color: #ffffff; }
        tr:hover { background-color: #1e2530; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background: linear-gradient(90deg, #00d4aa, #0e1117); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 2.5em;">⚽ Premier League 2025/26</h1>
        <p style="color: #00d4aa; margin: 0;">Live Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# Standings
response = requests.get(
    "https://api.football-data.org/v4/competitions/PL/standings",
    headers=headers
)

standings = response.json()["standings"][0]["table"]

data = []
for team in standings:
    data.append({
        "Rank": team["position"],
        "Club": f'<img src="{team["team"]["crest"]}" width="25"/> {team["team"]["name"]}',
        "Points": team["points"],
        "Played": team["playedGames"],
        "Won": team["won"],
        "Drawn": team["draw"],
        "Lost": team["lost"],
        "GD": team["goalDifference"],
    })

df = pd.DataFrame(data)
st.subheader("Current Standings")
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Team selector
st.write("---")
teams = [team["team"]["name"] for team in standings]
selected_team = st.selectbox("Select a team", teams)

for team in standings:
    if team["team"]["name"] == selected_team:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0;">
                <img src="{team["team"]["crest"]}" width="60"/>
                <h2 style="color: white; margin: 0;">{team["team"]["name"]}</h2>
                <span style="color: #00d4aa; font-size: 1.2em;">#{team["position"]} in Premier League</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="display: flex; gap: 15px; margin: 20px 0;">
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">POINTS</p>
                    <h2 style="color: white; margin: 0;">{team["points"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">WON</p>
                    <h2 style="color: white; margin: 0;">{team["won"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">DRAWN</p>
                    <h2 style="color: white; margin: 0;">{team["draw"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">LOST</p>
                    <h2 style="color: white; margin: 0;">{team["lost"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; flex: 1; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">GOAL DIFF</p>
                    <h2 style="color: white; margin: 0;">{team["goalDifference"]}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)