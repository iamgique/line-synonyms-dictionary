from flask import Flask, request
import json
import requests

global LINE_API_KEY
global APP_OXFORD_ID
global APP_OXFORD_KEY
global OXFORD_LANGUAGE
global OXFORD_URL

LINE_API_KEY = 'Bearer LINE_API_KEY'
APP_OXFORD_ID = 'APP_OXFORD_ID'
APP_OXFORD_KEY = 'APP_OXFORD_KEY'
OXFORD_LANGUAGE = 'en'
OXFORD_URL = 'https://od-api.oxforddictionaries.com:443/api/v1/entries'

app = Flask(__name__) 
@app.route('/')
def index():
    return 'This is Synonyms Dictionary.'

@app.route('/webhook', methods=['POST'])
def webhook():
    replyQueue = list()
    msg = request.get_json()
    replyToken = msg["events"][0]['replyToken']
    msgType =  msg["events"][0]['message']['type']
    
    if msgType != 'text':
        reply(replyToken, ['Only text is allowed. \nSynonyms dictionary return "definitions and synonyms" of word that user input to chat. \nIf sentence contain many words then analyze only the first word.'])
        return 'OK',200
    
    text = msg["events"][0]['message']['text'].lower().strip()
    
    print(text)
    print(splitAndRemoveSpecialCharacter(text))
    msgToReply = splitAndRemoveSpecialCharacter(text)

    if not msgToReply:
        replyQueue.append('Something went wrong.\nPlease try again.')
    else:
        definitionMsg = definitions(msgToReply)
        synonymMsg = synonym(msgToReply)
        replyQueue.append(definitionMsg)
        replyQueue.append(synonymMsg)

    reply(replyToken, replyQueue[:5])
    return 'OK', 200

def reply(replyToken, textList):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })

    requests.post(LINE_API, headers=headers, data=data)
    return

def splitAndRemoveSpecialCharacter(txt):
    splitTxt = txt.split(" ")
    return ''.join(e for e in splitTxt[0] if e.isalnum())

def definitions(textInput):
    definitionsPath = OXFORD_URL + '/' + OXFORD_LANGUAGE + '/' + textInput.lower()
    r = requests.get(definitionsPath, headers = {'app_id': APP_OXFORD_ID, 'app_key': APP_OXFORD_KEY})
    print("Call Oxford get definitions response code: {}".format(r.status_code))

    if r.status_code == 200:
        resp = r.json()
        respSet = resp['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    else:
        respSet = 'Cannot find definitions in word: ' + textInput
    return respSet

def synonym(textInput):
    synonymsPath = OXFORD_URL + '/' + OXFORD_LANGUAGE + '/' + textInput.lower() + '/synonyms;antonyms'
    r = requests.get(synonymsPath, headers = {'app_id': APP_OXFORD_ID, 'app_key': APP_OXFORD_KEY})
    print("Call Oxford get synonym response code: {}".format(r.status_code))

    comma = ''
    returnSynonyms = ''

    if r.status_code == 200:
        resp = r.json()
        print(resp)
        respSet = ''
        
        respCheckSet = resp['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        for z in range(len(respCheckSet)):
            if 'subsenses' in respCheckSet[z]:
                respSet = respCheckSet[z]['subsenses'][0]['synonyms']
                break
            else:
                respSet = 'Cannot find synonym in word: ' + textInput
            
        for y in range(0, len(respSet) > 5 and 5 or len(respSet)):
            if y == 4:
                returnSynonyms += ' and ' + respSet[y]['text']
            else:
                comma = y != 0 and ', ' or comma
                returnSynonyms += comma + respSet[y]['text']
        
    else:
        returnSynonyms = 'Cannot find synonym in word: ' + textInput

    return returnSynonyms

if __name__ == '__main__':
    app.run()