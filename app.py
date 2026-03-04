from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

@app.route("/")
def home():
    return "Football Bot PRO actif ⚽🔥"

@app.route("/match", methods=["GET"])
def get_match():
    team = request.args.get("team")

    if not team:
        return jsonify({"error": "Nom d'équipe requis"}), 400

    params = {
        "team": team,
        "next": 1
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    data = response.json()

    if "response" not in data or len(data["response"]) == 0:
        return jsonify({"error": "Équipe introuvable"}), 404

    match = data["response"][0]
    home_team = match["teams"]["home"]["name"]
    away_team = match["teams"]["away"]["name"]
    date = match["fixture"]["date"]

    # 🎯 2 scores exacts proposés
    score1 = "1-0"
    score2 = "2-1"

    return jsonify({
        "match": f"{home_team} vs {away_team}",
        "date": date,
        "prediction_scores": [score1, score2]
    })

# ⚠️ IMPORTANT POUR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
