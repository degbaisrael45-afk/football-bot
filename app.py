from flask import Flask, request
import requests
import os
import math

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("FOOTBALL_API_KEY")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

# ----------- TELEGRAM -----------

def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# ----------- FOOTBALL DATA -----------

def get_last_matches(team_name):
    headers = {"X-Auth-Token": API_KEY}
    teams_url = "https://api.football-data.org/v4/teams"
    r = requests.get(teams_url, headers=headers)
    teams = r.json()["teams"]

    team_id = None
    for team in teams:
        if team_name.lower() in team["name"].lower():
            team_id = team["id"]
            break

    if not team_id:
        return None

    matches_url = f"https://api.football-data.org/v4/teams/{team_id}/matches?limit=5"
    r = requests.get(matches_url, headers=headers)
    matches = r.json()["matches"]

    goals_scored = 0
    goals_conceded = 0

    for m in matches:
        if m["homeTeam"]["id"] == team_id:
            goals_scored += m["score"]["fullTime"]["home"] or 0
            goals_conceded += m["score"]["fullTime"]["away"] or 0
        else:
            goals_scored += m["score"]["fullTime"]["away"] or 0
            goals_conceded += m["score"]["fullTime"]["home"] or 0

    return goals_scored/5, goals_conceded/5

# ----------- CALCULS -----------

def implied_prob(odd):
    return 1 / odd

def poisson(lmbda, k):
    return (math.exp(-lmbda) * lmbda**k) / math.factorial(k)

# ----------- WEBHOOK -----------

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if "vs" in text:
            lines = text.split("\n")
            match_line = lines[0]
            home, away = match_line.split("vs")
            home = home.strip()
            away = away.strip()

            try:
                odd1 = float(lines[1].split(":")[1])
                oddX = float(lines[2].split(":")[1])
                odd2 = float(lines[3].split(":")[1])
                oddBTTS = float(lines[4].split(":")[1])
                oddOver = float(lines[6].split(":")[1])
            except:
                send_message(chat_id, "Format incorrect.")
                return "ok"

            home_avg = get_last_matches(home)
            away_avg = get_last_matches(away)

            if not home_avg or not away_avg:
                send_message(chat_id, "Équipe introuvable.")
                return "ok"

            home_attack = home_avg[0]
            away_attack = away_avg[0]

            # Probabilités Poisson
            p_home_2 = poisson(home_attack, 2)
            p_away_1 = poisson(away_attack, 1)

            score1 = "2-1"
            score2 = "1-1"

            value_home = (home_attack/ (home_attack+away_attack)) - implied_prob(odd1)

            reply = f"""
Analyse IA 🔥

{home} Moy buts: {round(home_attack,2)}
{away} Moy buts: {round(away_attack,2)}

Prob implicite 1: {round(implied_prob(odd1)*100,1)}%
Value Home: {round(value_home*100,1)}%

Scores probables:
1️⃣ {score1}
2️⃣ {score2}
"""

            send_message(chat_id, reply)

        elif text == "/start":
            send_message(chat_id, "Football Bot Intelligent ⚽🔥\nEnvoie match + cotes.")

    return "ok"

@app.route("/")
def home():
    return "Bot Intelligent Actif ⚽🔥"

if __name__ == "__main__":
    app.run()
