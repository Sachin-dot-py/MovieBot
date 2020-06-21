from credentials import TELEGRAM_TOKEN, CHAT_ID
from einthusan import downloadMovie, einthusanDetails
from omxplayer import OMX
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler

os.chdir(os.path.expanduser("~"))
logging.basicConfig(filename='moviebot.log', format='%(asctime)s ~ %(levelname)s : %(message)s', datefmt='%d-%m-%Y %H:%M:%S',level=logging.INFO)
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def player(update, context):
    chat_id = update.effective_chat.id
    query = update.message.text
    if chat_id != CHAT_ID: return
    if query == '⏪':
        mplayer.rewind()
    if query == '⏩':
        mplayer.forward()
    if query == '⏯':
        mplayer.playpause()
    if query == '➕':
        mplayer.volumeup()
    if query == '➖':
        mplayer.volumedown()
    if query == '🛑':
        mplayer.stop()
        ReplyKeyboardRemove()

def play(update, context):
    try:
        message = update.callback_query.data
    except:
        message = update.message.text
    if '<DELETE>' in message:
        os.remove(f'Movies/{message.replace("<DELETE>","")}.mp4')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Deleted {message.replace('<DELETE>','')} succesfully!")
    elif message == "":
        return
    else:
        global mplayer
        if 'youtu' in message:
            mplayer = OMX(message)
        else:
            mplayer = OMX(f'Movies/{message}.mp4')
        keyboard = ReplyKeyboardMarkup([[KeyboardButton('⏪'), KeyboardButton('⏯'), KeyboardButton('⏩')],
                                        [KeyboardButton('➕'), KeyboardButton('➖')],
                                        [KeyboardButton('🛑')]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Playing {message} right away!", reply_markup=keyboard)

def movies(update, context):
    if update.message.chat.id != CHAT_ID: return
    movies = [movie.replace('.mp4','') for movie in os.listdir('Movies') if '.mp4' in movie]
    if len(movies) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have no movies yet. Send the name of any movie to download it!")
    else:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(movie, callback_data=movie), InlineKeyboardButton('▶️', callback_data=movie), InlineKeyboardButton('🗑️', callback_data='<DELETE>' + movie)] for movie in movies])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here are your downloaded movies!\nClick ▶️ to play it and 🗑️ to delete any of them", reply_markup=keyboard)

def download(update, context):
    chat_id = update.effective_chat.id
    query = update.message.text
    if chat_id != CHAT_ID: return
    if query in ['⏪', '⏯', '⏩', '➕', '➖', '🛑']: 
        player(update, context)
        return
    if 'youtu' in query: 
        play(update, context)
    else:
        movie_name,einthusan_link = einthusanDetails(query)
        context.bot.send_message(chat_id=chat_id, text=f"Downloading {movie_name}...")
        downloadMovie(movie_name, einthusan_link)
        keyboard =  InlineKeyboardMarkup([[InlineKeyboardButton('✅', callback_data=movie_name), InlineKeyboardButton('❌', callback_data='')]])
        context.bot.send_message(chat_id=chat_id, text=f"{movie_name} has been downloaded!\nWould you like to play it?", reply_markup=keyboard)

movie_handler = CommandHandler('movies', movies)
dispatcher.add_handler(movie_handler)
download_handler = MessageHandler(Filters.text, download)
dispatcher.add_handler(download_handler)
callback_handler = CallbackQueryHandler(play)
dispatcher.add_handler(callback_handler)

updater.start_polling()
updater.idle()