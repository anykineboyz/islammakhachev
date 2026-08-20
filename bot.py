from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

niko_message_count = 0

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

    except Exception as error:
        print("Error sending GroupMe message:", error)

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global niko_message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO
    # -----------------------------

    if "niko" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT NIKO'S MESSAGES
    # -----------------------------

    niko_message_count += 1

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                "Brotha Niko, watch your language."
            )

            break

    # -----------------------------
    # EVERY 3RD MESSAGE
    # -----------------------------

    if niko_message_count % 3 == 0:

        islam_style_messages = [

            "Brotha Niko, you no have wrestling.",

            "Come 2-3 years Dagestan, brotha. We fix this problem.",

            "2-3 years Dagestan and forget, brotha.",

            "Niko, you need wrestling. Come Dagestan.",

            "Brotha, your wrestling is no good. 2-3 years Dagestan.",

            "You talk too much, brotha. Need more wrestling.",

            "Niko, stop talking and start wrestling, brotha.",

            "Come Dagestan, brotha. We train. No more excuses.",

            "Brotha Niko, you have no cardio and no wrestling.",

            "2-3 years with us, brotha. Then you can talk.",

            "Niko, first wrestling. Then talking. This is rule.",

            "Brotha, you cannot escape wrestling forever.",

            "Niko, why you talking? You should be wrestling, brotha.",

            "Come Dagestan, brotha. We make you strong.",

            "2-3 years Dagestan. After that, maybe you ready.",

            "Brotha Niko, you need to work on takedown defense.",

            "Niko, your wrestling defense is sleeping, brotha.",

            "No wrestling, no problem. Come Dagestan and we fix it.",

            "Brotha, I see your messages. I see no wrestling.",

            "Niko, you need dagestan, wrestling, and less talking."

        ]

        send_message(
            random.choice(
                islam_style_messages
            )
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
