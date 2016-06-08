import os
import logging
from logging import StreamHandler
from flask import Flask, request
import json
import requests
import apiai
from openrice import fetch_restro
from weather import fetch_weather
from latest_news import fetch_news
from hello import say_hello, say_goodbye
app = Flask(__name__)
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)


#TODO fill in the tokens
#app.config['SECRET_KEY'] = ''
#API_AI_CLIENT_ACCESS_TOKEN = ''
#FB_TOKEN = ""
#FB_VERIFICATION_TOKEN = ''
ai = apiai.ApiAI(API_AI_CLIENT_ACCESS_TOKEN)


@app.route('/facebook', methods=['GET'])
def verify():
    verify_token = None
    if 'hub.verify_token' in request.args:
      verify_token = request.args['hub.verify_token']
    if FB_VERIFICATION_TOKEN == verify_token:
        return request.args['hub.challenge']
    return "Unknown"

@app.route('/facebook', methods=['POST'])
def message_callback():
    app.logger.info(request.json)
    entries = request.json['entry']
    for entry in entries:
        messagings = entry['messaging']
        if messagings is None:
            continue
        for m in messagings:
            if 'message' in m:
                to = m['sender']['id']
                message_bodies = [{"text":"I don't understand your message. (%s)" % (m['message']['text'])}]
                post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=FB_TOKEN)
                ai_request = ai.text_request()
                ai_request.lang = 'en'  # optional, default value equal 'en'
                ai_request.query = m['message']['text']
                ai_response = json.loads(ai_request.getresponse().read())
                action = None
                parameters = None
                if "result" in ai_response:
                    action = ai_response["result"].get("action", None)
                    parameters = ai_response["result"].get("parameters", None)
                if action is not None:
                    app.logger.info("Action=%s" % (action))
                    app.logger.info("Parameters=%s" % (parameters))
                    if action == "show_weather":
                        message_bodies = fetch_weather()
                    if action == "show_news":
                        message_bodies = fetch_news(parameters['Media'])
                    if action == "show_restro":
                        message_bodies = fetch_restro(parameters['Places'])
                    if action == "say_hello":
                        message_bodies = say_hello()
                    if action == "say_goodbye":
                        message_bodies = say_goodbye()
                for message_body in message_bodies:
                    response_message = json.dumps({"recipient":{"id": to}, 
                                       "message":message_body})
                    app.logger.info(response_message)
                    req = requests.post(post_message_url, 
                                headers={"Content-Type": "application/json"}, 
                                data=response_message)
                    app.logger.info(req.text)
 
    return "Done"

@app.route('/')
def index():
    return "Hello world."

if __name__ == '__main__':
    app.run(debug=True)
