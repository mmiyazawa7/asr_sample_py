# coding: utf-8
from flask import Flask, render_template, request, Response,session
import nexmo
import requests
import json
import datetime
from datetime import datetime
from base64 import urlsafe_b64encode
import os
import calendar
from jose import jwt
import coloredlogs, logging
import urllib.parse
from urllib.parse import unquote
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


app = Flask(__name__) 

webhookurl="https://nexmodemo.ap.ngrok.io"


@app.route("/answerURL", methods = ['GET', 'POST']) 
def answer():    
    
    arg_to = request.args['to']
    arg_from = request.args['from']
    arg_conversation_uuid = request.args['conversation_uuid']
    arg_uuid = request.args['uuid']
    
    ncco = [
        {
            "action": "talk",
            "text": "お電話ありがとうございます。何か言ってみてください。あるいはDTMFで１を押してみてください。",
            "voiceName": "Mizuki"
        },
        {
            "action": "input",
            "speech": {
                "context": [
                    "agent"],
                "language": "ja-JP",
                "uuid": [arg_uuid],
                "endOnSilence": "3"
            },
            "dtmf": {
                "submitOnHash": "true",
                "maxDigits": "1",
                "timeOut": "2"
            },
            "eventUrl": [webhookurl+'/dtmf_asr'],
            "eventMethod": "POST"
        }
        ]
    
    print(ncco)
    js = json.dumps(ncco)
    resp = Response(js, status=200, mimetype='application/json')
    print(resp)
    return resp

@app.route('/dtmf_asr',methods=['GET', 'POST'])
def dtmf_asr():
    
    # arg_uuid = request.args['uuid']
    webhookContent = request.json
    logger.debug(webhookContent)
    
#    try:
#        result = webhookContent['dtmf']
#    except:
#        pass
        

    digit_result = webhookContent['dtmf']['digits']
    print(digit_result)

    asr_results = webhookContent['speech']['results']
    asr_text = asr_results[0]['text']
    print (asr_text)

    # 
    # let's play with ASR input here
    # 
    
    if digit_result == '1' or asr_text.find("エージェント") >= 0 :
        
        ncco = [
            {
                # TTS and then, Connect to agent
            }
        ]
        
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        logger.debug('Connecting to Agent')
        print(resp)
        return resp
    else:
        ncco = [
            {
                "action": "talk",
                "text": "お電話ありがとうございました",
                "voiceName": "Mizuki"
                }
        ]
        
        js = json.dumps(ncco)
        resp = Response(js, status=200, mimetype='application/json')
        print(resp)
        return resp

    
@app.route('/event', methods=['GET', 'POST', 'OPTIONS'])
def event():
    r = request.json
    print(r)
    return "OK"

if __name__ == "__main__":
    app.run(port="3000")