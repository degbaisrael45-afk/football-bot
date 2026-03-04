from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("FOOTBALL_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

headers = {
    "x-apisports-key": API_KEY
}

@app.route("/")
def home():
    return "Bot Telegram Actif ⚽🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.lower() == "/start":
            reply = "Bienvenue sur Football Bot Pro ⚽🔥\n\nEnvoie :\nAston Villa vs Chelsea"
        else:
            reply = analyse_match(text)

        send_message(chat_id, reply)

    return "ok"


def analyse_match(text):
    try:
        teams = text.split("vs")
        team1 = teams[0].strip()
        team2 = teams[1].strip()

        id1 = get_team_id(team1)
        id2 = get_team_id(team2)

        if not id1 or not id2:
            return "❌ Équipe introuvable."

        stats1 = get_last_matches(id1)
        stats2 = get_last_matches(id2)

        prediction = generate_prediction(stats1, stats2, team1, team2)

        return prediction

    except:
        return "❌ Format invalide. Utilise : Equipe1 vs Equipe2"


def get_team_id(team_name):
    url = f"https://v3.football.api-sports.io/teams?search={team_name}"
    response = requests.get(url, headers=headers).json()

    if response["results"] == 0:
        return None

    return response["response"][0]["team"]["id"]


def get_last_matches(team_id):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    response = requests.get(url, headers=headers).json()

    matches = response["response"]

    total_goals = 0

    for match in matches:
        goals = match["goals"]["for"]
        total_goals += goals

    avg_goals = total_goals / 5

    return avg_goals


def generate_prediction(avg1, avg2, team1, team2):

    score1 = round(avg1)
    score2 = round(avg2)

    alt1 = max(score1, score2)
    alt2 = min(score1, score2)

    result = f"""
📊 Analyse des 5 derniers matchs :

{team1} ➜ Moyenne buts : {avg1:.2f}
{team2} ➜ Moyenne buts : {avg2:.2f}

🎯 2 Scores exacts probables :
1️⃣ {team1} {score1} - {score2} {team2}
2️⃣ {team1} {alt1} - {alt2} {team2}
"""

    return result


def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)


if __name__ == "__main__":
    app.run()
