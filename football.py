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
        .stRadio label { color: #00d4aa; }
        div[data-testid="stMarkdownContainer"] > div { overflow-x: auto; }
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

# Get selected team ID and stats
team_id = None
for team in standings:
    if team["team"]["name"] == selected_team:
        team_id = team["team"]["id"]
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0;">
                <img src="{team["team"]["crest"]}" width="60"/>
                <h2 style="color: white; margin: 0;">{team["team"]["name"]}</h2>
                <span style="color: #00d4aa; font-size: 1.2em;">#{team["position"]} in Premier League</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 10px; margin: 20px 0;">
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">POINTS</p>
                    <h2 style="color: white; margin: 0;">{team["points"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">WON</p>
                    <h2 style="color: white; margin: 0;">{team["won"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">DRAWN</p>
                    <h2 style="color: white; margin: 0;">{team["draw"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">LOST</p>
                    <h2 style="color: white; margin: 0;">{team["lost"]}</h2>
                </div>
                <div style="background: #1e2530; border-radius: 10px; padding: 15px; text-align: center; border-top: 3px solid #00d4aa;">
                    <p style="color: #00d4aa; margin: 0; font-size: 0.8em;">GOAL DIFF</p>
                    <h2 style="color: white; margin: 0;">{team["goalDifference"]}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Squad View
st.write("---")
st.subheader(f"🏃 {selected_team} Squad")

squad_response = requests.get(
    f"https://api.football-data.org/v4/teams/{team_id}",
    headers=headers
)

squad = squad_response.json().get("squad", [])

squad_data = []
for player in squad:
    squad_data.append({
        "Player": player["name"],
        "Position": player["position"],
        "Nationality": player["nationality"],
        "Date of Birth": player["dateOfBirth"][:4] if player["dateOfBirth"] else "N/A",
    })

df_squad = pd.DataFrame(squad_data)

search = st.text_input("Search player by name or position", key="squad_search")

if search:
    df_squad = df_squad[
        df_squad["Player"].str.contains(search, case=False) |
        df_squad["Position"].str.contains(search, case=False)
    ]

st.write(df_squad.to_html(escape=False, index=False), unsafe_allow_html=True)


# Top Scorers
st.write("---")
st.subheader("⚽ Top Scorers")
sort_by = st.radio("Sort by", ["Goals", "Assists"], horizontal=True)

scorers_response = requests.get(
    "https://api.football-data.org/v4/competitions/PL/scorers",
    headers=headers
)

scorers = scorers_response.json()["scorers"]

scorers_data = []
for player in scorers:
    scorers_data.append({
        "Player": f'<img src="{player["player"]["photo"] if "photo" in player["player"] else ""}" width="25"/> {player["player"]["name"]}',
        "Club": player["team"]["name"],
        "Goals": player["goals"],
        "Assists": player["assists"] if player["assists"] else 0,
        "Played": player["playedMatches"],
    })

df_scorers = pd.DataFrame(scorers_data)
df_scorers = df_scorers.sort_values(by=sort_by, ascending=False).reset_index(drop=True)
st.write(df_scorers.to_html(escape=False, index=False), unsafe_allow_html=True)

# Squad View
st.write("---")
st.subheader(f"🏃 {selected_team} Squad")

team_id = None
for team in standings:
    if team["team"]["name"] == selected_team:
        team_id = team["team"]["id"]

squad_response = requests.get(
    f"https://api.football-data.org/v4/teams/{team_id}",
    headers=headers
)

squad = squad_response.json().get("squad", [])

squad_data = []
for player in squad:
    squad_data.append({
        "Player": player["name"],
        "Position": player["position"],
        "Nationality": player["nationality"],
        "Date of Birth": player["dateOfBirth"][:4] if player["dateOfBirth"] else "N/A",
    })

df_squad = pd.DataFrame(squad_data)


if search:
    df_squad = df_squad[
        df_squad["Player"].str.contains(search, case=False) |
        df_squad["Position"].str.contains(search, case=False)
    ]

st.write(df_squad.to_html(escape=False, index=False), unsafe_allow_html=True)

# Recent Matches
st.write("---")
st.subheader(f"📅 Last 5 Matches — {selected_team}")

matches_response = requests.get(
    f"https://api.football-data.org/v4/teams/{team_id}/matches",
    headers=headers,
    params={"status": "FINISHED", "limit": 5}
)

matches = matches_response.json().get("matches", [])

for match in matches:
    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]
    home_score = match["score"]["fullTime"]["home"]
    away_score = match["score"]["fullTime"]["away"]
    date = match["utcDate"][:10]
    
    st.markdown(f"""
        <div style="background: #1e2530; border-radius: 8px; padding: 12px; margin: 8px 0; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #ffffff;">{home}</span>
            <span style="color: #00d4aa; font-size: 1.2em; font-weight: bold;">{home_score} - {away_score}</span>
            <span style="color: #ffffff;">{away}</span>
            <span style="color: #888; font-size: 0.8em;">{date}</span>
        </div>
    """, unsafe_allow_html=True)