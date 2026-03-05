import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "8254455597:AAGoKJ74A5IlnHa31nVO_MWv-fM2x_Q-WfI"
API_KEY = "c777b294355a4fadb9110ced12646899"

url = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 FOOTBALL BOT PRO V3\n\n"
        "Commande :\n"
        "/analyse equipe1 equipe2\n\n"
        "Exemple :\n"
        "/analyse lyon lens"
    )

def get_team_id(team):

    r = requests.get(
        url + "/teams",
        headers=headers,
        params={"search": team}
    )

    data = r.json()

    if data["results"] == 0:
        return None

    return data["response"][0]["team"]["id"]


def get_stats(team_id):

    r = requests.get(
        url + "/teams/statistics",
        headers=headers,
        params={
            "team": team_id,
            "league": 61,
            "season": 2023
        }
    )

    data = r.json()

    return data["response"]


def analyse(update: Update, context: CallbackContext):

    try:

        team1 = context.args[0]
        team2 = context.args[1]

        id1 = get_team_id(team1)
        id2 = get_team_id(team2)

        if id1 is None or id2 is None:
            update.message.reply_text("❌ Équipe introuvable")
            return

        stats1 = get_stats(id1)
        stats2 = get_stats(id2)

        goals1 = stats1["goals"]["for"]["average"]["total"]
        goals2 = stats2["goals"]["for"]["average"]["total"]

        conceded1 = stats1["goals"]["against"]["average"]["total"]
        conceded2 = stats2["goals"]["against"]["average"]["total"]

        avg_total = float(goals1) + float(goals2)

        if avg_total > 2.5:
            over = "Oui"
        else:
            over = "Non"

        if float(goals1) > float(goals2):
            favori = team1
        elif float(goals2) > float(goals1):
            favori = team2
        else:
            favori = "Match équilibré"

        score1 = round((float(goals1)+float(conceded2))/2)
        score2 = round((float(goals2)+float(conceded1))/2)

        message = f"""
🤖 Analyse IA réelle

⚽ {team1} vs {team2}

📊 Moyenne buts {team1} : {goals1}
📊 Moyenne buts {team2} : {goals2}

📉 Défense {team1} : {conceded1}
📉 Défense {team2} : {conceded2}

🏆 Favori : {favori}

📈 Over 2.5 : {over}

🎯 Score probable :
{score1} - {score2}
"""

        update.message.reply_text(message)

    except:
        update.message.reply_text("Utilisation : /analyse equipe1 equipe2")


def main():

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analyse", analyse))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
