import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "8254455597:AAGoKJ74A5IlnHa31nVO_MWv-fM2x_Q-WfI"
API_KEY = "c777b294355a4fadb9110ced12646899"

def start(update, context):
    update.message.reply_text(
        "⚽ Football Bot PRO actif\n\nCommande:\n/match equipe1 equipe2"
    )

def match(update, context):

    if len(context.args) < 2:
        update.message.reply_text("Utilise: /match equipe1 equipe2")
        return

    team1 = context.args[0]
    team2 = context.args[1]

    url = "https://v3.football.api-sports.io/teams"
    headers = {
        "x-apisports-key": API_KEY
    }

    r1 = requests.get(url, headers=headers, params={"search": team1})
    r2 = requests.get(url, headers=headers, params={"search": team2})

    data1 = r1.json()
    data2 = r2.json()

    if not data1["response"] or not data2["response"]:
        update.message.reply_text("Équipe introuvable")
        return

    team1_id = data1["response"][0]["team"]["id"]
    team2_id = data2["response"][0]["team"]["id"]

    update.message.reply_text(f"🔎 Analyse de {team1} vs {team2}...")

    stats_url = "https://v3.football.api-sports.io/teams/statistics"

    s1 = requests.get(stats_url, headers=headers, params={"team": team1_id, "league": 39, "season": 2023}).json()
    s2 = requests.get(stats_url, headers=headers, params={"team": team2_id, "league": 39, "season": 2023}).json()

    goals1 = s1["response"]["goals"]["for"]["total"]["total"]
    goals2 = s2["response"]["goals"]["for"]["total"]["total"]

    if goals1 > goals2:
    pronostic = f"{team1} favori"
    score = "2-1"
    over = "Oui"
elif goals2 > goals1:
    pronostic = f"{team2} favori"
    score = "1-2"
    over = "Oui"
else:
    pronostic = "Match équilibré"
    score = "1-1"
    over = "Non"

    message = f"""
⚽ Analyse IA

{team1} vs {team2}

Pronostic :
🏆 {pronostic}
📊 Over 2.5 : {over}
🎯 Score probable : {score}
"""
    
    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("match", match))

    updater.start_polling()
    updater.idle()

main()
