import logging
import json
import random
from threading import Thread
from time import sleep

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import requests


app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger('flask_ask').setLevel(logging.DEBUG)
logging.root.setLevel(logging.INFO)

INTRO_MSG = 'Nennen Sie eine Strecke, zum Beispiel "A 1", oder sagen Sie "Hilfe".'
INTRO_MSG_2 = '''Fragen sie nach einer Autobahn, zum Beispiel "A 3",
oder einer Bundesstraße wie "B 7". Zum Beenden, sagen Sie "Stop". 
Um die Hilfe anzuhören, sagen Sie "Hilfe"'''
NO_MESSAGES_MSG = 'Keine Meldungen für die %s'
REPEAT_MSG = 'Kannst du das noch einmal wiederholen?'
ANOTHER_MSG = 'Nennen Sie noch eine weitere Strecke oder sagen Sie "Stop"'
HELP_MSG = '''Dieser Skill liefert aktuelle WDR Verkehrsinformationen für Nordrhein Westfalen. 
Fragen sie nach Autobahnen zum Beispiel mit "A 1" oder "A 7", nach Bundesstraßen mit "B 224" 
oder nach Kreisstraßen mit "K 17"
Sie können den Skill auch direkt aufrufen, indem Sie sagen: 
"Alexa frage WDR Verkehr nach A 3"
Wenn Sie den Skill beenden möchten, sagen Sie "Stop".
'''
STOP_MESSAGES = ["Gute Fahrt!", "Bis dann.", "Fahren Sie vorsichtig.", "Tschüss."]
CARD_TITLE = 'WDR Verkehr'

messages = list()


def get_traffic_messages():
    logging.info('Downloading traffic info JSON...')
    r = requests.get('http://exporte.wdr.de/WDRVerkehrWebsite/map/all?zoom=8&bbox=4.27%2C49.71%2C12.73%2C53.01',)
                     #params={'zoom': '8', 'bbox': '4.27 49.71 12.73 53.01'})

    logging.info('Parsing JSON...')
    response_dict = json.loads(r.text)

    return response_dict['messages']


@ask.launch
def launch():
    return question(INTRO_MSG).reprompt(INTRO_MSG_2)


@ask.intent('QueryIntent')
def query(road_type, road_number):
    if road_type is None or road_number is None:
        return question(REPEAT_MSG)

    if road_type.lower() == 'r':
        road_type = 'a'
        
    road = road_type + road_number
    road = road.replace('.', '').replace(',', '').replace(' ', '')

    messages_for_road = [message['description'].replace('<br />', '\n')
                         for message in messages
                         if message['road'].lower() == road.lower() 
                         and not message['closure'] 
                         or message['warning']]

    speech_text = '\n\n'.join(messages_for_road) or NO_MESSAGES_MSG % road.upper()

    speech_text = speech_text.replace('-', ' ').replace('/', ' ')

    return question(speech_text + '\n\n' + ANOTHER_MSG
                    ).reprompt(ANOTHER_MSG
                    ).simple_card(CARD_TITLE, speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    return question(HELP_MSG).reprompt(INTRO_MSG_2)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement(random.choice(STOP_MESSAGES))


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement(random.choice(STOP_MESSAGES))

@ask.session_ended
def session_ended():
    return "", 200

def update_traffic_messages():
    global messages
    while True:
        try:
            messages = get_traffic_messages()
        except:
            logging.warning("Parsing JSON failed!")

        sleep(60)


Thread(target=update_traffic_messages, daemon=True).start()

if __name__ == '__main__':    
    app.run(host='127.0.0.1', port='5000', debug=False)
