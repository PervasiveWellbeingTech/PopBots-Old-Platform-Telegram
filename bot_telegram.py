#/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This file communicates between the database and the API (Telegram).

Created by Nick Tantivasadakarn.
"""

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
from gibberish_filter import isGibberish



TIMEOUT_SECONDS = 3600
DEBUG_MODE = True

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
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        #initialize bot responses and parameters
        self.reply_dict = get_response_dict()
        self.reply_dict_informal = get_response_dict_informal()
        self.params = Params()
        self.config = Config()

        #initialize database
        if self.params.MODE == Modes.TEXT:
            self.db = MongoClient().study_Informal_Nov_2019  #MongoClient().textbot_telegram
        else:
            self.db = MongoClient().voicebot_telegram

        #initialize user info 
        self.user_history = defaultdict(list)
        #self.user_name_dict = self.load_names(self.db.user_history)
        self.user_bot_state_dict = defaultdict(lambda:(None, None))
        self.user_problem_dict = {}


        self.condition = False#True 
        #self.user_parameters_dict = self.load_user_parameters(self.db.user_history)
        self.user_name_dict, self.user_parameters_dict, self.ids = self.load_parameters(self.db.user_history)

        keyboards =[telegram.InlineKeyboardButton("Choose for me")]+[
                                telegram.InlineKeyboardButton(name) for idx, name in enumerate(self.params.bot_name_list) if idx not in {4,7}]
        self.bots_keyboard = [ [x,y] for x,y in zip(keyboards[0::2], keyboards[1::2]) ]
        if len(keyboards)%2 ==1:
            self.bots_keyboard.append([keyboards[-1]])


    def load_parameters(self, collection):
        """
        Loads names and user parameter from database

        Parameter:
            collection (mongo collection)

        Returns:
            (dict) user_id to user_name dictionary
        """
        names = defaultdict(lambda: '')
        parameters = defaultdict(dict)
        ids = defaultdict(lambda: None)
        for hist in collection.find():
            names[hist['user_id']] = hist.get('user_name', '')
            parameters[hist['user_id']] = hist.get('user_parameters', {})
            ids[hist['user_id']] = hist.get('subject_id', None)
        return names, parameters, ids


    # def load_user_parameters(self, collection):
    #     """
    #     Loads user parameters from database

    #     Parameter:
    #         collection (mongo collection)

    #     Returns:
    #         (dict) user_id to user_parameter dictionary
    #     """
    #     parameters = {}
    #     for hist in collection.find():
    #         parameters[hist['user_id']] = hist['user_parameters']
    #     return parameters

    # def process_updates(self, bot_updates):
    #     """
    #     Handles interactions with the Telegram server.
    #     Receives all the user replies in the form of updates and tells
    #     Telegram what to reply

    #     Parameters:
    #          bot_updates (iterator) -- all updates from bot.get_updates function
    #     """
    #     # Request updates after the last update_id

    #     for update in bot_updates:
    #         self.update_id = update.update_id + 1
    #         if update.message and update.message.text: #ignores all non-text inputs
    #             user_id = update.message.chat_id
    #             query = update.message.text 
    #             self.process_message(user_id, query) 
                    
    #@run_async
    def process_message(self, user_id, query):
        ############ Special Cases #######################
        if re.match(r'/start', query): #restart
            self.log_action(user_id, None, None, "RESET", "")
            self.save_history_to_database(user_id)
            self.user_history.pop(user_id, None)
            self.user_bot_state_dict[user_id] = (7 , self.config.START_INDEX)
            subj_id = re.findall(' ([0-9]+)', query)
            if subj_id:
                if DEBUG_MODE:
                    self.set_parameter(user_id, 'choice', True)
                    self.user_parameters_dict[user_id]['choice'] = True
                    self.set_parameter(user_id, 'formal', False)
                    self.user_parameters_dict[user_id]['formal'] = False
                else:
                    self.set_toggle(user_id, 'formal')
                self.set_subj_id(user_id, int(subj_id[0]))
            self.user_problem_dict.pop(user_id, None)

        elif self.conversation_timeout(user_id): #Time out
            self.log_action(user_id, None, None, "<TIMEOUT>", "")
            self.save_history_to_database(user_id)
            self.user_history.pop(user_id, None)
            self.user_bot_state_dict.pop(user_id, None)
            self.user_problem_dict.pop(user_id, None)

        elif re.match(r'/switch', query): #switch
            self.log_action(user_id, None, None, "<SWITCH>", "")
            self.user_parameters_dict[user_id]['switch'] = True
            #self.save_history_to_database(user_id)
            #self.user_history.pop(user_id, None)
            self.user_bot_state_dict[user_id] = (7,7)

        ############ Normal Cases #######################
        bot_id, response_id = self.get_next(user_id, query)
        choice = self.user_parameters_dict[user_id].get('choice', False)
        formal = self.user_parameters_dict[user_id].get('formal', False)
        switch = self.user_parameters_dict[user_id].get('switch', False)

        if response_id == self.config.CLOSING_INDEX and not switch:
            self.log_action(user_id, bot_id, response_id, "<CONVERSATION_END>", query)
            self.save_history_to_database(user_id)

        if bot_id == 7 and response_id == 9:
            self.log_action(user_id, bot_id, response_id, "<CONVERSATION_END>", query)
            self.save_history_to_database(user_id)

        if response_id == None: #End of conversation"
            self.user_history.pop(user_id, None)
            self.user_parameters_dict[user_id]['last']=bot_id
            if find_keyword(query, self.config.GREETINGS): #the user activates another bot
                self.user_bot_state_dict[user_id] = (None, None)
                bot_id, response_id = self.get_next(user_id, query)
            else:
                self.user_bot_state_dict.pop(user_id, None)

        # if it begins a conversation, increment the counter
        if bot_id == 7 and (response_id == self.config.OPENNING_INDEX or response_id == 6):
            conv_id = self.user_parameters_dict[user_id].get('conv_id', 0)
            self.set_parameter(user_id, 'conv_id', conv_id+1)
            self.user_parameters_dict[user_id]['conv_id'] = conv_id+1
        #extract names
        if bot_id == 7 and response_id == 2:
            name = find_name(query)
            self.user_name_dict[user_id] = name
            self.db.user_history.update_one({'user_id':user_id}, {'$set':{'user_name': name}},
                             upsert=True)
        
        #Set custom keyboard (defaults to none)
        reply_markup = telegram.ReplyKeyboardRemove()
        
        
        #get problem
        if  ((bot_id == 7 and response_id == 4 and not choice) or (bot_id == 7 and response_id == 3 and choice))\
                and not self.user_parameters_dict[user_id].get('switch', False):
            problem = find_problem(query)
            if problem:
                self.user_problem_dict[user_id] = problem

        #show choices
        if  bot_id == 7 and response_id == 3 and choice:
            bots_keyboard = self.bots_keyboard
            reply_markup = telegram.ReplyKeyboardMarkup(bots_keyboard, resize_keyboard= True)               

        if response_id in {self.config.CLOSING_INDEX, self.config.ABRUPT_CLOSING_INDEX} or (bot_id == 7 and response_id == 9):
            reply_markup = telegram.ReplyKeyboardMarkup([[telegram.InlineKeyboardButton("Hi")]], resize_keyboard= True)
        
        #select bot
        if bot_id == 7 and (response_id == 4 or response_id == 10):
            self.post_and_log_text(bot_id, response_id, user_id, query, reply_markup)
            bot_choice = self.params.bot2id.get(query, None)
            #reply_markup = telegram.ReplyKeyboardRemove()
            if type(bot_choice) == int:
                bot_id  = bot_choice
            else:
                last = self.user_parameters_dict[user_id].get('last', None)
                bot_id = self.recommend_bot(last)
                self.user_parameters_dict[user_id]['last']=bot_id
            response_id = self.config.OPENNING_INDEX


        #handle images
        if self.params.MODE == Modes.TEXT and response_id == self.config.OPENNING_INDEX:
            img = open('img/{}.png'.format(bot_id), 'rb')
            self.bot.send_photo(chat_id=user_id, photo=img)

        if bot_id == 7 and response_id == 6:
            img = open('img/{}.png'.format(bot_id), 'rb')
            self.bot.send_photo(chat_id=user_id, photo=img)
        

        #handle text responses
        self.post_and_log_text(bot_id, response_id, user_id, query, reply_markup)
        #To skip 
        if bot_id == 7 and response_id == 4:
            self.process_message(user_id, "<SKIP>")

        if bot_id == 2 and (response_id == 3 or response_id == 4):
            self.process_message(user_id, "<SKIP>")


    def set_parameter(self, user_id:int, parameter:str, value):
        """
        Sets a parameter in the database

        Parameters:
            user_id(int) -- unique user identifyer
            parameter(int) -- subject id (MUST be a non-indentifiable number)
            value -- value of the parameter
        """
        self.db.user_history.update_one({'user_id':user_id}, {
                            '$set':{'user_parameters.'+parameter : value}},
                            upsert=True)


    def set_subj_id(self, user_id:int, subject_id:int):
        """
        Parameters:
            user_id(int) -- unique user identifyer
            subject_id(int) -- subject id (MUST be a non-indentifiable number)
        """
        self.db.user_history.update_one({'user_id':user_id}, {'$set':{'subject_id': subject_id}},
                     upsert=True)

        self.ids[user_id] = subject_id

    def set_toggle(self, user_id:int, parameter:str):
        """
        Set subjects to either one of 2 conditions.
        Parameters:
            user_id(int) -- unique user identifyer
            parameter(str) -- name of the condition
        """
        if parameter not in self.user_parameters_dict[user_id]:
            if self.condition:
                # self.db.user_history.update_one({'user_id':user_id}, {
                #             '$set':{'user_parameters': {parameter: True}}},
                #             upsert=True)
                self.set_parameter(user_id, parameter, True)
                self.user_parameters_dict[user_id][parameter] = True
                self.condition = False
            else:
                # self.db.user_history.update_one({'user_id':user_id}, {
                #             '$set':{'user_parameters': {parameter: False}}},
                #             upsert=True)
                self.set_parameter(user_id, parameter, False)
                self.user_parameters_dict[user_id][parameter] = False
                self.condition = True


    def post_and_log_text(self, bot_id, response_id, user_id, query, reply_markup = None):
        """
        Posts the appropriate text to Telegram, and logs the conversation

        Parameters:
            bot_id(int) -- bot id
            response_id(int) -- response within bot
            user_id(int) -- unique identifyer
            query(string) -- user input
        """
        if response_id != None:
            formal = self.user_parameters_dict[user_id].get('formal', False)
            text_response = self.get_text_response(bot_id, response_id, formal)
            text_response_format = list(self.replace_entities(text_response, user_id, bot_id))
            for res in text_response_format:
                self.bot.sendChatAction(chat_id=user_id, action = telegram.ChatAction.TYPING)
                sleep(min(len(res)/20,2.5))
                self.bot.send_message(chat_id=user_id, text=res, reply_markup = reply_markup)
            self.log_action(user_id, bot_id, response_id, text_response_format, query)
            self.user_bot_state_dict[user_id] = (bot_id, response_id)


    def get_text_response(self, bot_id, response_id, formal):
        """
        Processes the input text and returns the response.

        This function looks at the state  within the conversation,
        and outputs the appropriate response. 

        Parameters:
            bot_id(int) -- id of the bot
            response_id(int) -- id of the response within a bot
            formal(bool) -- toggle between formal or informal scripts

        Returns:
            (list) -- list of strings the responses 
        """
        if formal:
            response_dict =  self.reply_dict[bot_id][response_id].texts
        else:
            response_dict =  self.reply_dict_informal[bot_id][response_id].texts
        #get text of the selected mode
        response_choices = response_dict.get(self.params.MODE, response_dict[Modes.GENERAL])
        response = random.choice(response_choices)
        return response

    def replace_entities(self, responses, user_id, bot_id):
        """
        Replaces entity place holders such as {name} {bot_name} 
        with appropriate names

        Parameters:
            responses(list) -- list of text responses
            user_id(int) -- user unique identifyer
            bot_id(int) -- id of the bot 

        Returns:
            (list) -- list of strings the responses 
        """
        name = self.user_name_dict.get(user_id, '')
        problem = self.user_problem_dict.get(user_id, "that")
        bot_name = self.params.bot_name_list[bot_id]
        subject_id = self.ids[user_id]
        for res in responses:
            yield res.format(name=name, problem=problem, bot_name=bot_name, subject_id=subject_id)


    def get_next(self, user_id, query):
        """
        Determines the next state in the conversation.

        NOTE: If next_id is a list of branching paths, 
        it will select the first path that has a matching keyword in the query.
        (DEFAULT_OTHERS will always match, so put it at the end)

        Parameters:
            user_id (int) -- user unique identifyer
            query (string) -- user input string.
        """
        #get current id
        (bot_id, response_id) = self.user_bot_state_dict[user_id]
        if response_id == self.config.QUESTION_INDEX and self.user_parameters_dict[user_id].get('switch', False):
            self.user_parameters_dict[user_id].pop('switch', None)
            return 7, 8
        if bot_id == None and response_id == None:
            return 7, 6

        if bot_id == 7 and (response_id == 6 or response_id == 7):
            if self.user_parameters_dict[user_id].get('choice', False): #go to choice selection
                return 7, 3
            else:
                return 7, 10
        next = self.reply_dict[bot_id][response_id].next_id
        if not next:
            next_id = None
        elif type(next) == list: #handle branching paths
            next_id = None
            for keywords, value in next:
                if keywords == self.config.DEFAULT_OTHERS:
                    next_id = value
                    break
                elif find_keyword(query, keywords):
                    #prevent catching long answers containing the word 'no'
                    if keywords != self.config.DEFAULT_NO or (len(query.split(" ")) <= 5 and len(query) <= 25):
                        next_id = value
                        break
            assert next_id != None, "No dialog option match."
        elif type(next) == int: #handle single path
            next_id = next
        else: #if no patters match
            raise ValueError
        return bot_id, next_id

    def log_action(self, user_id, bot_id, response_id, replies, query):
        """
        Creates a log of the interaction and saves it to self.user_history

        Parameters:
            user_id(int) -- unique identifyer
            bot_id(int) -- id of the bot
            response_id(int) -- id of the response within a bot
            replies(list/iterator) -- list/iterator of text that the bot replies to the user
            query(string) -- user input

            Note: it also logs a time stamp 
        """
        conv_id = self.user_parameters_dict[user_id].get('conv_id', 0)
        new_entry = {
                        'conv_id':conv_id,
                        'bot_id':bot_id, 
                        'response_id':response_id,
                        'query':query,
                        'replies':list(replies),
                        'time':time.time()
                    }
        self.user_history[user_id].append(new_entry)

    def recommend_bot(self, last=None):
        """
        Recommends a random bot except bot id 7 (onboarding bot) 
        and bot id 4 (relaxation bot) and the last used bot.

        Return:
            bot id (int)

        Notes: Refer to get_resposne.py or utils.py (bot_name_list) to get the list.
        """
        return random.choice([i for i in range(self.params.BOT_NUM) if i not in {4,7,last}])

    def conversation_timeout(self, user_id):
        """
        Check if the conversation has timed out.

        Parameter:
            user_id(int) -- unique identifyer

        Return:
            (bool) -- True if the conversation has timed out
        """
        if self.user_history[user_id]:
            last_entry_time = self.user_history[user_id][0]['time']
            return time.time()-last_entry_time >= TIMEOUT_SECONDS
        else:
            return False

    def save_history_to_database(self, user_id):

        """
        This function sends the data from the user history (pulled from the class variable)
        to the database

        Parameter:
            user_id(int) -- unique identifyer
        """
        history = self.user_history[user_id]
        self.db.user_history.update_one({'user_id':user_id},
                                        {"$push":{'user_history': history}}
                                    )
    
    def callback_handler(self, bot, update):
        """
        Wrapper function to call the message handler
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
        updater = Updater(token)
        dp = updater.dispatcher # Get the dispatcher to register handlers
        handler = MessageHandler(Filters.text, self.callback_handler)
        dp.add_handler(handler)
        dp.add_handler(CommandHandler("start", self.callback_handler))
        dp.add_handler(CommandHandler("switch", self.callback_handler))

        #dp.add_error_handler(self.error_callback)
        print("Running Bot ... (Ctrl-C to exit)")
        updater.start_polling()
        #updater.idle()

        # while True:
        #     #Check if there are updates.
        #     try:
        #         bot_updates = self.bot.get_updates(offset=self.update_id, timeout=60)
        #     except NetworkError:
        #         sleep(1)
        #         continue
        #     except Unauthorized:
        #         # The user has removed or blocked the bot.
        #         self.update_id += 1           
        #         continue
        #     #If succesful
        #     self.process_updates(bot_updates)

if __name__ == '__main__':
    # Telegram Bot Authorization Token
    f = open('token.txt')
    token = f.read()
    bot = TelegramBot(token)
    bot.run()

