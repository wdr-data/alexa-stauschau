import logging
import json

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import requests


app = Flask(__name__)
ask = Ask(app, "/")
#logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


def get_traffic_messages():
    logging.info('Downloading traffic info JSON...')
    r = requests.get('http://exporte.wdr.de/WDRVerkehrWebsite/map/all?zoom=8&bbox=4.27%2C49.71%2C12.73%2C53.01',)
                     #params={'zoom': '8', 'bbox': '4.27 49.71 12.73 53.01'})

    logging.info('Parsing JSON...')
    response_dict = json.loads(r.text)

    return response_dict['messages']


@ask.launch
def launch():
    speech_text = 'Nennen Sie eine Strecke, zum Beispiel "A1"'
    return question(speech_text).reprompt(speech_text)


@ask.intent('QueryIntent')
def query(road_type, road_number):
    road = road_type + road_number
    road = road.replace('.', '').replace(',', '').replace(' ', '')

    messages_for_road = [message['description'].replace('<br />', '\n')
                         for message in messages
                         if message['road'].lower() == road]

    speech_text = '\n\n'.join(messages_for_road) or 'Keine Meldungen'

    return question(speech_text + '\n\nNennen Sie noch eine weitere Strecke oder sagen Sie "Stop"'
                    ).simple_card('WDR StauSchau', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Liefert aktuelle Verkehrsinformationen des WDR'
    return question(speech_text).reprompt(speech_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Gute Fahrt!")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Gute Fahrt!")


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    messages = get_traffic_messages()
    app.run(debug=True)
