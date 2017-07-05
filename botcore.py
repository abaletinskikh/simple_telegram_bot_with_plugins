# coding: utf-8

from telegram.ext import    (Updater, 
                            CommandHandler, 
                            CallbackQueryHandler)
from telegram import        (ChatAction,
                            InlineKeyboardButton,
                            InlineKeyboardMarkup)
import os,os.path
import inspect
import importlib

PLUGIN_DIR='plugin'

class Bot(Updater):
    def __init__(self,**kwargs):
        super(Bot,self).__init__(**kwargs)
        #add /start comman to bot
        def start(bot, update):
            bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
            update.message.reply_text('Привет')
            try:
                dirs=[file for file in os.listdir(PLUGIN_DIR)
                        if os.path.isdir(os.path.join(PLUGIN_DIR,file)) ]
                if not dirs:
                    update.message.reply_text('Нет доступных плагинов')
                else:
                    keyboard = [[InlineKeyboardButton(dir,callback_data=dir) for dir in dirs]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_text('Выбирите модуль',reply_markup = reply_markup)
            except Exception as e:
                update.message.reply_text(str(e))
        self.dispatcher.add_handler(CommandHandler('start', start))
        #add handler for button
        def select_plugin(bot, update):
            query = update.callback_query
            try:
                plugin=importlib.import_module('plugin.%s'%query.data)
                importlib.reload(plugin)
                init_func=[val for name,val in inspect.getmembers(plugin,inspect.isfunction) if name == 'init']
                if not init_func:
                    query.answer(text='ошибка инициализации плагина')
                    return                
                #remove standart handler and add /exit handler exit
                _closure=self.dispatcher.handlers[0]
                self.dispatcher.handlers[0]=[]
                def exit(bot, update):
                    #restore standart handlers
                    self.dispatcher.handlers[0]=_closure
                    update.message.reply_text('Выход из плагина %s'%query.data)
                self.dispatcher.add_handler(CommandHandler('exit', exit))
                init_func[0](self)
                query.answer(text='выбран плагин %s'%query.data)
            except Exception as e:
                query.answer(text='ошибка загрузки плагина: %s'%str(e))
        self.dispatcher.add_handler(CallbackQueryHandler(select_plugin))
        def error(bot, update, error):
            print('Update "%s" caused error "%s"' % (update, error))
        self.dispatcher.add_error_handler(error)
        self.start_polling()
                            
if __name__ == "__main__":
    app=Bot(token='YOUR TOKEN HERE')
    app.idle()


