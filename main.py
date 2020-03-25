import requests
from api import *
from db import *
from flask import Flask, request
from flask_cors import CORS
from pymessenger.bot import Bot

app = Flask(__name__)
db = open_db()
CORS(app)
ACCESS_TOKEN = 'EAAkEI4VDUocBAPf6Jb6QEf6avRms21yuDMFXW5XbSOcB08znK5JCOpDGHua3TeQbQANZASrMsJHaIFhmuK9OmFjjLMHUJSn8m93RjI4AoPu7WpcH8zoQfGRIVxsSoHF5d19DJfTgjbNtOrC0iIHtOB7phTivwXOEslUNEZAQxdMAsSTrMM9PLWvVkEjqoZD'
VERIFY_TOKEN = 'kWGeLL6QnSAjpN9M3txuZUoY8AnDkVRUvnu'
bot = Bot(ACCESS_TOKEN)

# Give the verify token and receive the messages from FB users
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        print(output)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                recipient_id = message['sender']['id']
                if message.get('postback'):
                    welcome_options(recipient_id)
                elif message.get('message'):
                    handle_replies(message, recipient_id)
    return "Message Processed"


def welcome_options(recipient_id):
    send_quick_replies(recipient_id, "Que souhaitez-vous faire ?", [
        {
            "content_type": "text",
                            "title": "Commander",
                            "payload": "order"
        }, {
            "content_type": "text",
                            "title": "Disponibilité",
                            "payload": "availability"
        }
    ])


def handle_replies(message, recipient_id):
    if message['message'].get('quick_reply'):
        payload = message['message']['quick_reply']['payload']
        if payload == 'order':
            bot.send_text_message(
                recipient_id, "Entre ta commande séparé par des +")
            return
        if payload == 'availability':
            stocks(recipient_id)
        if payload == 'sales':
            bot.send_text_message(
                recipient_id, "Les réductions arrivent bientôt.")
    elif message['message'].get('text'):
        orders(recipient_id, message['message']['text'])
    # Handle games invitations, gifs, pictures ... (and says no)
    else:
        bot.send_text_message(
            recipient_id, "Le ClickNCollect ne répond qu'aux messages textuels.")
    welcome_options(recipient_id)


def orders(recipient_id, msg):
    order_items = msg.split('+')
    order_items = list(map(str.strip, order_items))
    cursor = db.execute(
        f"SELECT rowid FROM drinks WHERE in_stock = 1 AND name IN ({', '.join('?' * len(order_items))}) UNION SELECT rowid FROM snacks WHERE in_stock = 1 AND name IN ({', '.join('?' * len(order_items))})", (*order_items, *order_items))
    db_items = cursor.fetchall()
    if (len(db_items) != len(order_items)):
        bot.send_text_message(
            recipient_id, "Un des items est malorthographié ou n'est plus en stock")
        return
    bot.send_text_message(recipient_id, "Commande passée")
    cursor = db.execute(f"INSERT INTO orders (items) VALUES (?)", (msg,))
    db.commit()


def stocks(recipient_id):
    cursor = db.execute(
        f"SELECT name FROM drinks WHERE in_stock = 1 UNION SELECT name FROM snacks WHERE in_stock = 1")
    in_stock = cursor.fetchall()
    s = ""
    for product in in_stock:
        s += product["name"] + ", "
    s = s[:-2]
    bot.send_text_message(
        recipient_id, "Les produits en stock sont " + s)


def set_get_started(gs_obj):
    request_endpoint = '{0}/me/messenger_profile'.format(bot.graph_url)
    response = requests.post(
        request_endpoint,
        params=bot.auth_args,
        json=gs_obj,
    )
    result = response.json()
    return result


def send_quick_replies(recipient_id, text, quick_replies):
    return bot.send_message(recipient_id, {
        "text": text,
        "quick_replies": quick_replies
    })


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


if __name__ == "__main__":
    set_get_started({
        "get_started": {
            "payload": "started"
        }
    })
    api(app, db)
    app.run(host='0.0.0.0', debug=True)
