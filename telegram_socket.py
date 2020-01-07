#!popbotsenv/bin/python

import telegram
#from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.error import NetworkError, Unauthorized

import time
import random
import string
#import sys, getopt
#import os, nltk
import re

from collections import defaultdict
#from os import system
from utils import Params, Config, Modes, find_keyword, find_name, find_id, find_problem
from get_response import get_response_dict
from get_response_informal import get_response_dict_informal
from pymongo import MongoClient
import telegram
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.error import NetworkError, Unauthorized
from time import sleep
import sys
import traceback

from messenger import Message
TIMEOUT_SECONDS = 3600

class TelegramBot():
    """
    Implementation of the bot.

    Initialization parameter:
        token (string) -- Telegram bot token

    Class parameters:
        self.bot (telegram.bot) -- telegram bot object
        self.reply_dict (dict) -- dictionary containing all responses
        self.params (utils.Params) -- fixed parameters
        self.config (utils.Config) -- bot configuration

        self.user_history(defaultdict) -- temporary dictionary of user to user history
        self.user_name_dict(defaultdict) -- user_id to name dictionary
        self.user_bot_state_dict (defaultdict) -- user_id to bot state dict (defaults to a random bot)
        self.user_problem_dict(dict) -- user_id to problem dictionary
        self.user_parameters_dict(defaultdict) -- dictionary that stores all parameters used by the bots.
    """

    def __init__(self, token): #, reply_dict, **kwargs):
        print("Bot initialization.")
        #initialize telegram bot
        self.bot = telegram.Bot(token)
        self.msg_engine  = Message()
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        self.params = Params()
        self.config = Config()


        keyboards =[telegram.InlineKeyboardButton("Choose for me")]+[
                                telegram.InlineKeyboardButton(name) for idx, name in enumerate(self.params.bot_name_list) if idx not in {4,7}]
        self.bots_keyboard = [ [x,y] for x,y in zip(keyboards[0::2], keyboards[1::2]) ]
        if len(keyboards)%2 ==1:
            self.bots_keyboard.append([keyboards[-1]])


    def send_message(self,user_id,text_response,reply_markup):
        for res in text_response:
            self.bot.sendChatAction(chat_id=user_id, action = telegram.ChatAction.TYPING)
            sleep(min(len(res)/20,2.5))
            self.bot.send_message(chat_id=user_id, text=res, reply_markup = reply_markup)
    def process_message(self, user_id, query):

        response  = self.msg_engine.process_message(user_id, query)

        if not response['img']:
            self.send_message(user_id,response['response_list'],response['reply_markup'])
       
        elif response['img'] and response['response_list'][0]:
            self.bot.send_photo(chat_id=user_id, photo=response['img'])
            self.send_message(user_id,response['response_list'],response['reply_markup'])

            


    def callback_handler(self, update,context):
            """
            Wrapper function to call the message handler

            This function will also catch and print out errors in the console
            
            """
            try:
                self.process_message(update.message.chat_id, update.message.text)
            except:
                exc_info = sys.exc_info()
            finally:
                traceback.print_exception(*exc_info)
                del exc_info
            #print(sys.exc_info()[0])
            # traceback.print_stack()

            self.process_updates(update)

    def error_callback(bot, update, error):
        raise error

    def run(self):
        """
        Run the bot.
        """
        updater = Updater(token,use_context = True)
        dp = updater.dispatcher # Get the dispatcher to register handlers
        handler = MessageHandler(Filters.text, self.callback_handler)
        dp.add_handler(handler)
        dp.add_handler(CommandHandler("start", self.callback_handler))
        dp.add_handler(CommandHandler("switch", self.callback_handler))

        #dp.add_error_handler(self.error_callback)
        print("Running Bot ... (Ctrl-C to exit)")
        updater.start_polling()


if __name__ == '__main__':
    # Telegram Bot Authorization Token
    f = open('token.txt')
    token = f.read()
    print(token)
    bot = TelegramBot(token)
    bot.run()