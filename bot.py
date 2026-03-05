import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# TOKEN TELEGRAM
TOKEN = "8254455597:AAGoKJ74A5IlnHa31nVO_MWv-fM2x_Q-WfI"

# API FOOTBALL
API_KEY = "c777b294355a4fadb9110ced12646899"

headers = {
    "x-apisports-key": API_KEY
}

# ---------------- START ----------------

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "⚽ FOOTBALL BOT PRO V2 ACTIF\n\n"
        "Commandes :\n"
        "/analyse equipe1 equipe2\n"
        "/match equipe1 equipe2"
    )

# -------- TROUVER ID EQUIPE --------

def get_team_id(team_name):

    url = "https://v3.football.api-sports.io/teams"

    params = {
        "search": team_name
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data["results"] == 0:
        return None

    return data["response"][0]["team"]["id"]

# -------- STATISTIQUES --------

def get_stats(team_id):

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "team": team_id,
        "last": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    goals = 0

    for match in data["response"]:
        goals += match["goals"]["for"]["total"] if "for" in match["goals"] else 0

    return goals

# -------- ANALYSE --------

def analyse(update: Update, context: CallbackContext):

    try:
        team1 = context.args[0]
        team2 = context.args[1]

        id1 = get_team_id(team1)
        id2 = get_team_id(team2)

        if not id1 or not id2:
            update.message.reply_text("❌ Equipe introuvable")
            return

        goals1 = get_stats(id1)
        goals2 = get_stats(id2)

        total = goals1 + goals2

        if goals1 > goals2:
            favori = team1
        elif goals2 > goals1:
            favori = team2
        else:
            favori = "Match équilibré"

        if total >= 10:
            over = "Oui"
        else:
            over = "Non"

        score = "2-1"

        message = f"""
🤖 Analyse IA

{team1} vs {team2}

📊 Buts 5 derniers matchs
{team1} : {goals1}
{team2} : {goals2}

🏆 Favori : {favori}

📈 Over 2.5 : {over}

🎯 Score probable : {score}
"""

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /analyse equipe1 equipe2")

# -------- MATCH --------

def match(update: Update, context: CallbackContext):

    try:
        team1 = context.args[0]
        team2 = context.args[1]

        message = f"""
⚽ Analyse rapide

{team1} vs {team2}

📊 Pronostic IA

• Les deux équipes marquent
• Over 2.5 probable
• Score probable : 2-1
"""

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /match equipe1 equipe2")

# -------- MAIN --------

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analyse", analyse))
    dp.add_handler(CommandHandler("match", match))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
