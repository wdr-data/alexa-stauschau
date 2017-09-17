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

logging.getLogger('flask_ask').setLevel(logging.INFO)
logging.root.setLevel(logging.INFO)

INTRO_MSG = '<speak><say-as interpret-as="interjection">Hallo</say-as>. Nenne eine Strecke, zum Beispiel "A 1", oder sag "Hilfe".</speak>'
INTRO_MSG_2 = '''Frage nach einer Autobahn, zum Beispiel "A 3",
oder einer Bundesstraße wie "B 7". Zum Beenden, sage "Stop". 
Um die Hilfe anzuhören, sage "Hilfe"'''
NO_MESSAGES_MSG = 'Keine Meldungen für die %s'
REPEAT_MSG = 'Kannst du das noch einmal wiederholen?'
ANOTHER_MSG = 'Nenne noch eine weitere Strecke oder sage "Stop"'
HELP_MSG = '''<speak>Dieser Skill liefert aktuelle <say-as interpret-as="spell-out">WDR</say-as> Verkehrsinformationen für Nordrhein Westfalen. 
Frage nach Autobahnen zum Beispiel mit "A 1" oder "A 7", nach Bundesstraßen mit "B 224" 
oder nach Kreisstraßen mit "K siebzehn". 
Du kannst den Skill auch direkt aufrufen, indem du sagst: 
"Alexa, frage <say-as interpret-as="spell-out">WDR</say-as> Verkehr nach A drei".
Mehr Informationen und Karten findest Du auf <say-as interpret-as="spell-out">wdr.de/</say-as>verkehrslage.
Wenn Du den Skill beenden möchtest, sage "Stop".</speak>
'''
STOP_MESSAGES = [
    'Gute Fahrt!',
    '<speak><say-as interpret-as="interjection">Gute Reise</say-as></speak>',
    '<speak><say-as interpret-as="interjection">Mach\'s gut</say-as></speak>',
    '<speak><say-as interpret-as="interjection">Bis dann.</say-as></speak>',
    'Fahr vorsichtig.',
    '<speak><say-as interpret-as="interjection">Tschüss.</say-as></speak>',
]
CARD_TITLE = 'WDR Verkehr'

messages = list()


def get_traffic_messages():
    logging.debug('Downloading traffic info JSON...')
    r = requests.get('http://exporte.wdr.de/WDRVerkehrWebsite/map/all?zoom=8&bbox=4.27%2C49.71%2C12.73%2C53.01',)
                     #params={'zoom': '8', 'bbox': '4.27 49.71 12.73 53.01'})

    logging.debug('Parsing JSON...')
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

    if road_type.lower() in ('d', 'p', 'e'):
        road_type = 'b'

    road = road_type + road_number
    road = road.replace('.', '').replace(',', '').replace(' ', '')

    messages_for_road = [message['description'].replace('<br />', '\n')
                         for message in messages
                         if message['road'].lower() == road.lower() 
                         and (not message['closure'] or message['warning'])]

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


# TODO research why this is needed
@ask.intent('StopIntent')
def stop():
    return statement(random.choice(STOP_MESSAGES))


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement(random.choice(STOP_MESSAGES))


# TODO research why this is needed
@ask.intent('CancelIntent')
def stop():
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
