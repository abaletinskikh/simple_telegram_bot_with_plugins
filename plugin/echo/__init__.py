# coding: utf-8
from telegram.ext import MessageHandler, Filters

def init(updater):
    def echo(bot, update):
        update.message.reply_text(update.message.text)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))


