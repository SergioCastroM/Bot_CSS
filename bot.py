import sqlite3
import requests
import resources
import json
import logging
#import resources
from resources import config
from telegram import ChatAction, ParseMode, ForceReply
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
from random import randint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DataLista =[]

dataListi=[]

cookies=''

def start(update, context):
    update.message.reply_text('Hola, bienvenido, qué deseas hacer?')    
    #ConexionSL(update,context)  

def about(update, context):
    keyboard = [[InlineKeyboardButton("Facebook", callback_data='Facebook'),
                 InlineKeyboardButton("Web", callback_data='WWW'),
                 InlineKeyboardButton("Youtube", callback_data='youtube')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('📌 CONSENSUS S.A.S.\n', reply_markup=reply_markup)

def call_back(update, context):
    query = update.callback_query

    if format(query.data) == 'Facebook':
        context.bot.edit_message_text(text="https://www.facebook.com/consensussap/",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    if format(query.data) == 'WWW':
        context.bot.edit_message_text(text="https://consensussap.co/",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    if format(query.data) == 'youtube':
        context.bot.edit_message_text(text="https://www.youtube.com/user/Consensussa",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

def addtolist(update, context):
    
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    strings = update.message.text.lower().split()

    if len(strings) >= 2:
        strings.remove('/addtolist')
        
        chat_id = update.message.chat_id
        chat_id = str(chat_id)
        #username = update.message.from_user.username

        for s in strings:
            
            DataLista.append({'ItemCode':s,'Price':10000 })
            print(DataLista)

        update.message.reply_text("Todos los art fueron agregados a la lista")
    else:
        update.message.reply_text("Error de sintaxis. Presiona /help para más información")

def addtolist1(update, context):
    responseConect = ConexionSL()
    getPF(update, responseConect)
    
def help(update, context):
    update.message.reply_text("⭕️ /about: Información de la compañía\n"
                              "\n📝 LISTA DE ARTICULOS 📝\n"
                              "/addtolist <items>: Adiciona un artículo a la lista\n"
                              "/rmfromlist <items>: Remueve un artículo de la lista\n"
                              "/show_list: Mira la Lista de artículos\n"
                              "/clear_list: Limpia la lista de artículos\n")

def manage_text(update, context):
        
    update.message.reply_text("Disculpa, no puedo entenderte. Presiona /help para más información")

def manage_command(update, context):
    update.message.reply_text("Comando desconocido. Presiona /help para más información")                             
    
def ConexionSL():
    response = requests.Session()
    url = 'https://192.168.1.143:50000/b1s/v1/Login'
    parameters = { "UserName": "manager", "Password": "manager","CompanyDB": "VISDECOL_PRD", "Language": "23"}
    headers = {'content-type': 'application/json'}
    response.post(url, data=json.dumps(parameters), headers=headers, verify=False) 
    return response 

def getPF (update, responseConect):
    count = 0
    response = responseConect
    url = 'http://192.168.1.143:50001/b1s/v1/Items?$filter=SalesItem eq \'tYES\''
    r=response.get(url, verify=False)
    data = r.json()
    
    for i in data['value']:
        class Data:
            idData=count
            ItemCode = i['ItemCode']
            ItemName = i['ItemName']
            Price = i['ItemName']
        dataListi.append(Data)
        count+=1
    
    for oData in dataListi:
        update.message.reply_text(str(oData.idData+1) + " - " + oData.ItemName)

if __name__ == '__main__':

    updater = Updater(token= config.API_TOKEN , use_context=True)

    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CallbackQueryHandler(call_back))

    dp.add_handler(CommandHandler('addtolist1', addtolist1))
    dp.add_handler(CommandHandler('addtolist', addtolist))
    
    # On noncommand i.e message
    dp.add_handler(MessageHandler(Filters.text, manage_text))
    dp.add_handler(MessageHandler(Filters.command, manage_command))

    updater.start_polling()
    updater.idle()
