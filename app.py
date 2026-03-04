from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

@app.route("/")
def home():
    return "Football Bot PRO actif ⚽🔥"

@app.route("/analyse", methods=["GET"])
def analyse_match():
    home_id = request.args.get("home")
    away_id = request.args.get("away")

    if not home_id or not away_id:
        return jsonify({"error": "home et away requis"}), 400

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    params = {
        "team": home_id,
        "next": 10
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "response" not in data:
        return jsonify({"error": "Erreur API"}), 500

    for match in data["response"]:
        if str(match["teams"]["away"]["id"]) == away_id:
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            date = match["fixture"]["date"]

            return jsonify({
                "match": f"{home_team} vs {away_team}",
                "date": date,
                "prediction": {
                    "score": "2-1",
                    "over_2_5": "Oui",
                    "btts": "Oui"
                }
            })

    return jsonify({"message": "Pas de match programmé entre ces équipes"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
