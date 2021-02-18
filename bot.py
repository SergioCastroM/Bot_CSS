import requests
import json
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton

cookies=''

def start(update, context):
    update.message.reply_text('Hola, bienvenido, qué deseas hacer?')    
    ConexionSL(update,context)  
    
def ConexionSL(update,context):
    response = requests.Session()
    url = 'https://servicesunit2.abilitysap.com.co:50000/b1s/v1/Login'
    parameters = {"CompanyDB":"GIMNASIO_LOS_PINOS","UserName":"ABILITYSAP\\glp-jrestrepo","Password":"2o18P1n0s"}
    headers = {'content-type': 'application/json'}
    response.post(url, data=json.dumps(parameters), headers=headers, verify=False) 
    #if(response.cookies.get)
    #cookies = response.cookies     
    update.message.reply_text(requests.utils.dict_from_cookiejar(response.cookies))  

if __name__ == '__main__':

    updater = Updater(token='1618570620:AAHa-yq9RYRoZ-FndRjZ_FLCNBQlFzFfRTE', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
   
    updater.start_polling()
    updater.idle()