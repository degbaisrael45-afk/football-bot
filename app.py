import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

headers = {"X-Auth-Token": API_KEY}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "⚽ FOOTBALL BOT PRO 1000X\n\n"
        "Commandes :\n"
        "/analyse equipe1 equipe2 cote1 coteX cote2 btts over25\n\n"
        "Exemple :\n"
        "/analyse Arsenal Chelsea 1.90 3.40 3.80 1.70 1.65"
    )

    await update.message.reply_text(message)


# ANALYSE MATCH
async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        equipe1 = context.args[0]
        equipe2 = context.args[1]

        cote1 = float(context.args[2])
        coteX = float(context.args[3])
        cote2 = float(context.args[4])
        btts = float(context.args[5])
        over25 = float(context.args[6])

        message = f"⚽ Analyse IA\n\n{equipe1} vs {equipe2}\n\n"

        # FAVORI
        if cote1 < cote2:
            favori = equipe1
        else:
            favori = equipe2

        message += f"🏆 Favori : {favori}\n"

        # Probabilité victoire
        prob1 = round((1 / cote1) * 100, 1)
        prob2 = round((1 / cote2) * 100, 1)

        message += f"\n📊 Probabilité victoire\n"
        message += f"{equipe1} : {prob1}%\n"
        message += f"{equipe2} : {prob2}%\n"

        # OVER / UNDER
        if over25 < 1.80:
            message += "\n🔥 Over 2.5 très probable"
            score = "2-1 ou 3-1"
        else:
            message += "\n❄️ Under 2.5 probable"
            score = "1-0 ou 1-1"

        # BTTS
        if btts < 1.80:
            message += "\n⚽ BTTS : OUI"
        else:
            message += "\n⚽ BTTS : NON"

        message += f"\n\n🎯 Score probable : {score}"

        await update.message.reply_text(message)

    except:

        await update.message.reply_text(
            "❌ Mauvaise commande\n\n"
            "Exemple :\n"
            "/analyse Arsenal Chelsea 1.90 3.40 3.80 1.70 1.65"
        )


# MATCH DU JOUR
async def matchs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = "https://api.football-data.org/v4/matches"

    response = requests.get(url, headers=headers)
    data = response.json()

    message = "📅 Matchs du jour\n\n"

    for match in data["matches"][:10]:

        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        message += f"{home} vs {away}\n"

    await update.message.reply_text(message)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyse", analyse))
app.add_handler(CommandHandler("matchs", matchs))

print("Bot PRO 1000X lancé")

app.run_polling()
