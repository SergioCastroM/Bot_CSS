import sqlite3
import requests
import json
import logging
import src.configIni
from models import articleModel
from telegram import ChatAction, ParseMode, ForceReply
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError, Unauthorized


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

global estadoComando 
estadoComando = 0    

DataLista =[]

dataListi=[]
dataListiIndex=[]
dataListArticles =[]

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

def validateInput(update):
    try:
        if int(update.message.text)-1 in dataListiIndex:
            return int(update.message.text)-1
        else:
            return -1
    except:
        update.message.reply_text("Error de sintaxis. Presiona /help para más información")

def validateInputD(update):
    try:
        if int(update.message.text)-1 in dataListiIndex:
            return int(update.message.text)-1
        else:
            return -1
    except:
        update.message.reply_text("Error de sintaxis. Presiona /help para más información")   

def addtolist(update, context):
    
    global estadoComando

    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    responseConect = ConexionSL()
    getPF(update, responseConect)   
   
    estadoComando = 1
                
def show_list(update, context):
   
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    # Imprimir lista de items
    if len(dataListArticles) > 0:
        update.message.reply_text("Estos son los Artículos Agregados a tu Lista:")
        for oData in dataListArticles:
            update.message.reply_text(str(oData.idArticle+1) + " - " + oData.itemName )          
    else:
        update.message.reply_text("No tienes Artículos en tu lista")

def clear_list(update, context):
        
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    dataListArticles.clear()
    update.message.reply_text("La lista de artículos fue eliminada")

def rmfromlist(update, context):

    global estadoComando    
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if len(dataListArticles) > 0:
        update.message.reply_text("Cual de los siguientes Artículos deseas eliminar de tu Lista:")
        for oData in dataListArticles:
            update.message.reply_text(str(oData.idArticle+1) + " - " + oData.itemName) 
        estadoComando = 2                
    else:
        update.message.reply_text("No tienes Artículos en tu lista")
    
def serializeArticles():
    print("entro serialize")
    x=json.dumps(dataListArticles)
    print(x)
        
def help(update, context):
    update.message.reply_text("⭕️ /about: Información de la compañía\n"
                              "\n📝 LISTA DE ARTICULOS 📝\n"
                              "/addtolist <items>: Adiciona un artículo a la lista\n"
                              "/rmfromlist <items>: Remueve un artículo de la lista\n"
                              "/show_list: Mira la Lista de artículos\n"
                              "/clear_list: Limpia la lista de artículos\n")

def manage_text(update, context):
    
    global estadoComando
    
    try:
                
        if estadoComando == 1 :

           index = validateInput(update)
           
           if int(index)>=0:
               dataListArticles.append(dataListi[index])
               update.message.reply_text("El artículo fue agregado a la lista")
               estadoComando = 0
           else:
               update.message.reply_text("Este numero de artículo no existe") 

        elif estadoComando == 2:

           index = validateInputD(update)
           
           if int(index)>=0:
               dataListArticles.pop(index)
               update.message.reply_text("El artículo fue eliminado a la lista")
               estadoComando = 0
           else:
               update.message.reply_text("Este numero de artículo no existe")
        else:
           update.message.reply_text("Disculpa, no puedo entenderte. Presiona /help para más información")
           estadoComando = 0

    except:

        update.message.reply_text("Exc Disculpa, no puedo entenderte. Presiona /help para más información")    
        estadoComando = 0 

def manage_command(update, context):
    update.message.reply_text("Comando desconocido. Presiona /help para más información")                             
    
def ConexionSL():
    response = requests.Session()
    #requests.packages.urllib3.disable_warnings()
    response.post(src.configIni.urlLogin, data=json.dumps(src.configIni.parametersLogin), headers=src.configIni.headers, verify=False) 
    return response 

def getPF (update, responseConect):
    count = 0
    response = responseConect
    r=response.get(src.configIni.urlGetItem, verify=False)
    data = r.json()
    dataListi.clear()

    for i in data['value']:
        articleInstance = articleModel.Article()
        articleInstance.idArticle = count
        articleInstance.itemCode = i['ItemCode']
        articleInstance.itemName = i['ItemName']
        articleInstance.price = 10000
        dataListi.append(articleInstance)
        dataListiIndex.append(count)
        count+=1
    
    for oData in dataListi:
        update.message.reply_text(str(oData.idArticle+1) + " - " + oData.itemName)

if __name__ == '__main__':

    updater = Updater(token= src.configIni.API_TOKEN , use_context=True)

    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CallbackQueryHandler(call_back))

    dp.add_handler(CommandHandler('addtolist', addtolist))
    dp.add_handler(CommandHandler('show_list', show_list))
    dp.add_handler(CommandHandler('clear_list', clear_list))

    # camptura de comandos y textos
    dp.add_handler(MessageHandler(Filters.text, manage_text))
    dp.add_handler(MessageHandler(Filters.command, manage_command))

    updater.start_polling()
    updater.idle()
