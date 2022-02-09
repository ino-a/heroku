from flask import Flask
from flask import request

from janome.tokenizer import Tokenizer

import requests
import json
import re

import settings

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':settings.CHANNEL_ID,
    'X-Line-ChannelSecret':settings.CHANNEL_SECRET,
    'X-Line-Trusted-User-With-ACL':settings.MID
}

def post_event(to, content):
    msg = {
        'to': [to],
        'toChannel': 1383378250,
        'eventType': "138311608800106203",
        'content': content
    }
    r = requests.post(LINEBOT_API_EVENT, headers = LINE_HEADERS, data = json.dumps(msg))

def post_text(to, text):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)


commands = (
    (re.compile('作者', 0), lambda x: 'https://nnsnodnb.moe'),
)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    messages = request.json['result']

    for message in messages:
        text = message['content']['text']
        for matcher, action in commands:
            if matcher.search(text):
                response = action(text)
                break
        else:
            post_text(message['content']['from'], '解析中...')
            # 形態素解析
            response = ''
            t = Tokenizer()
            for token in t.tokenize(message['content']['text']):
                response += str(token) + '\n'
        post_text(message['content']['from'], response)
    return ''

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8001, threaded = True, debug = True)