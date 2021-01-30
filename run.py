from moviebot.credentials import TELEGRAM_TOKEN as mbtoken
from moviebot.loggingconfig import logging, handle_unhandled_exception
import telegram
import time
import os
import sys
import json
import requests
import moviebot.app as apy
from bs4 import BeautifulSoup
from flask import Flask, request

bot = telegram.Bot(token=mbtoken)
app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/{}'.format(mbtoken), methods=['POST'])
def moviebot_respond():
    """ Parses telegram update """
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text.encode('utf-8').decode()
    logging.info(f"MOVIEBOT: Recieved message {text}")
    if str(chat_id) not in ['855910557', '1207015683']: return
    try:
        apy.dispatcher.process_update(update)
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        handle_unhandled_exception(exc_type, exc_value, exc_tb)
    return 'ok'


def setWebhook(url):
    """ Sets telegram webhook """
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=url, HOOK=mbtoken))
    if s:
        logging.info("Webhook succesfully set up!")
    else:
        logging.error("Webhook setup failed.")


def ngrok():
    """ Starts ngrok and returns url """
    try:
        req = requests.get('http://127.0.0.1:4040/api/tunnels')
        soup = BeautifulSoup(req.text, 'lxml')
        tunnelsjson = json.loads(soup.find('p').text)
        url = tunnelsjson['tunnels'][0]['public_url'].replace(
            'http://', 'https://')
    except:
        os.system('ngrok http 4000 > /dev/null &')
        time.sleep(10)
        try:
            req = requests.get('http://127.0.0.1:4040/api/tunnels')
            soup = BeautifulSoup(req.text, 'lxml')
            tunnelsjson = json.loads(soup.find('p').text)
            url = tunnelsjson['tunnels'][0]['public_url'].replace(
                'http://', 'https://')
        except:
            logging.critical("Failure in obtaining ngrok url")
            exit()
    return url


url = ngrok()
logging.info(f"Ngrok url obtained - {url}")
setWebhook(url)
logging.info("Web app starting")

if __name__ == '__main__':
    app.run(port=4000, threaded=True)
