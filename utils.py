# -*- coding: UTF-8 -*-
"""
Contains methods for processing text, getting features,
and defining fixed parameters.

Created by Honghao Wei.
"""

import random
import string
import nltk
# import enchant
from rake_nltk import Rake
from enum import Enum
import re

#from fbchat import Client
#from fbchat.models import *
     
from collections import *
r = Rake()

class Params:
    def __init__(self, bot_num=9, sleeping_time=2, abtest_choice=-1, bot_choice=-1):
        """
        Initializes the bot that will be used in the system.

        Notes: 
        - All new bot information must be added here.
        - bot_name_list refers to the actual name of the bot.
        - bot_tech_name_list refers to the method that the bot employs.
            (bots are manually evoked using this name.)

        """

        self.BOT_NUM = bot_num
        self.SLEEPING_TIME = sleeping_time
        self.ABTEST_CHOICE = abtest_choice #   -1 random choice, > -1, the index of selected reply
        self.BOT_CHOICE = bot_choice # -1 random, 0 worse case bot, 1 problem solving bot, 2 positive thining bot
        self.MODE = Modes.TEXT
        assert self.BOT_CHOICE < self.BOT_NUM, 'Bot_num: {}, Bot_choice: {}'.format(self.BOT_NUM, self.BOT_CHOICE)
        
        ##########Bot list##########
        self.bot_name_list = ['Doom Bot', 'Sherlock Bot', 'Glass-half-full Bot', 'Sir Laughs Bot', 'Chill bot', 'Treat yourself Bot', 'Dunno Bot', 'Onboarding Bot', 'Checkin Bot']
        self.bot_tech_name_list = ['worst case', 'problem solving', 'positive thinking', 'humor', 'relaxation', 'self love', 'distraction', 'introduce', 'check']
        #self.bot_color_list = [ThreadColor.BILOBA_FLOWER, ThreadColor.BRILLIANT_ROSE, ThreadColor.CAMEO, ThreadColor.DEEP_SKY_BLUE, ThreadColor.FERN, ThreadColor.PUMPKIN, ThreadColor.RADICAL_RED, ThreadColor.SHOCKING, ThreadColor.VIKING]

    def set_sleeping_time(self, sleeping_time):
        self.SLEEPING_TIME = sleeping_time

    def set_bot_choice(self, bot_choice):
        self.BOT_CHOICE = bot_choice
        assert self.BOT_CHOICE < self.BOT_NUM, 'Bot_num: {}, Bot_choice: {}'.format(self.BOT_NUM, self.BOT_CHOICE)

    def set_mode(self, mode):
        if mode == 'text':
            self.MODE = Modes.TEXT
        elif mode == 'voice':
            self.MODE = Modes.VOICE


class Config:
    """
    Contains standard 
    """
    def __init__(self):
        self.OPENNING_INDEX = -1
        self.CLOSING_INDEX = -2
        self.START_INDEX = -3
        self.DK_INDEX = -4
        self.ARE_YOU_DONE_INDEX = -5
        self.CONTINUE_INDEX = -6
        self.ABRUPT_CLOSING_INDEX = -7
        self.QUESTION_INDEX = -8


        self.DEFAULT_YES = ['yes', 'ok', 'sure', 'right', 'yea', 'ye', 'yup', 'yeah', 'okay']
        self.DEFAULT_NO = ['no', 'not',  'neither', 'neg', 'don\'t', 'doesn\'', 'donnot', 'dont', '\'t', 'nothing', 'nah', 'na']
        self.DEFAULT_DK = ["dk", "dunno", "dno", "don't know", "idk"]
        self.GREETINGS = ['hi','hey', 'hello']
        # self.DEFAULT_YES = "__YES__"
        # self.DEFAULT_NO = "__NO__"
        # self.DEFAULT_DK = "__DK__"
        self.DEFAULT_OTHERS = "__OTHERS__"

# class Topics:
#     def __init__(self):
#         self.GENERAL = 'general'
#         # self.TRAFFIC = 'traffic'
#         # self.TIRED = 'tired'
#         # self.LATE = 'late'
#         # self.DRIVER = 'driver'
#         # self.VEHICLE = 'vehicle'
#         self.TEXT = 'text'
#         self.VOICE = 'voice'

class Modes(Enum):
    GENERAL = 'general'
    TEXT = 'text'
    VOICE = 'voice'



class Reply:
    """
    A class representing a bot 

    Parameters:
        bot_id (int) -- id of the bot
        response_id (int) -- id of a response within a bot
        texts (list) -- list of strings winthin a reply 
                        Format: [['Hi', 'How are you?'], ['Howdy']]
        next_id (int or list) -- integer of the next reply or a list of tuples
                                in the form (pattern, int) to do choices.
        image (path) -- path to image. (optional)
                        Note: images are displayed before text.
        commands(set) -- set of special commands (optional)
    """
    def __init__(self, bot_id, response_id, texts, next_id, image=None, commands={}):
        self.bot_id = bot_id
        self.response_id = response_id
        self.texts = texts
        self.next_id = next_id
        self.image = image
        self.commands = commands


def find_keyword(input_str, word_list):
    """
    Loops through each word in the input string.
    Returns true is there is a match.

    Parameters:
        input_str (string) -- input string by the user
        word_list (list/tuple) -- list of extract_keywords_from_text

    Returns:
        (boolean) -- if keyword is found.
    """
    if word_list[0] == Config().DEFAULT_OTHERS:
        return True
    input_str = input_str.lower()
    return any([str(each) in str(input_str) for each in word_list])

def find_name(input_str):
    """
    A simple algorithm to extract names.

    Parameters:
        input_str(str) -- string containing the name
    """

    for each in ['i am', 'i\'m', 'this is', 'name is']:
        _index = input_str.lower().find(each)
        if _index != -1:
            result = input_str.lower()[_index + len(each)+1:]
            result = result.split()[0]
            for each_punc in list(string.punctuation):
                result = result.replace(each_punc,"")
            if len(result) > 0 and len(result) < 20:
                return result.capitalize()
    return input_str.capitalize().split()[0]

def find_id(input_str):
    """
    Extracts participant id number, 

    This function uses regular expression to extract the first
    string of numbers that matches the id format.

    Parameters:
        input_str(str) -- string containing the id

    Returns
        string (if found), None (if not found)

    """
    ids = re.findall(r'[0-9]{5}', input_str)
    if not ids:
        return None
    else:
        return ids[0]




# def find_topic(problem):
#     topics = Topics()
#     topic_list = [topics.TIRED, topics.LATE, topics.DRIVER, topics.VEHICLE, topics.TRAFFIC]
#     for topic in topic_list:
#         if topic in problem:
#             return topic
#     return topics.GENERAL

# def find_problem(input_str):
#     topics = Topics()

#     nervous_words = ["stressed", "nervous", "stress out", "stressed out", "stressful"]
#     because_words = ['for the reason that', 'on the grounds that', 'in the interest of', 'for the sake of', 'as a result of', 'in as much as', 'as things go', 'by reason of', 'by virtue of', 'in behalf of', 'by cause of', 'considering', 'as long as', 'because of', 'in view of', 'thanks to', 'now that', 'owing to', 'because', 'in that', 'through', 'whereas', 'due to', 'seeing', 'being', 'since', 'over', 'for', 'as', 'about', 'at']
#     first_person_list = [('our', 'your'), ('I ', 'you '), ('we', 'you'), ("my", 'your')]


#     if any([each in input_str for each in ['tired', 'tiring', 'exhausted']]):
#         return 'feeling tired', topics.TIRED
#     elif any([each in input_str for each in ['late']]):
#         return 'being late', topics.LATE
#     elif any([each in input_str for each in ['traffic']]):
#         return 'traffic', topics.TRAFFIC
#     elif any([each in input_str for each in ['driver']]):
#         return 'other drivers', topics.DRIVER
#     elif any([each in input_str for each in ['vehicle']]):
#         return 'your vehicle', topics.VEHICLE

#     for nervous_word in nervous_words:
#         for because_word in because_words:
#             _target = nervous_word+" "+because_word
#             _index = input_str.find(_target)
#             if _index != -1:
#                 result = input_str[_index + len(_target)+1:]
#                 #print(result)
#                 tokens = nltk.word_tokenize(result)
#                 tagged = nltk.pos_tag(tokens)
#                 result = ""

#                 for word, tag in tagged:
#                     if tag.startswith('N') or tag.startswith('PRP'):
#                         result += word + " "
#                 for each in list(string.punctuation):
#                     result = result.replace(each,"")
#                     #print(result)
#                 for each in first_person_list:
#                     result = result.replace(each[0], each[1])

#                 if len(result) > 0:# and len(result) < 20:
#                     _kind = find_topic(result)
#                     return result, _kind
#     return None, None


def find_problem(input_str):
    """
    Extract a candidate problem from an input string.

    Parameter:
        input_str(string) -- user input string

    Return:
        cand (string) -- candidate problem
    """
    r.extract_keywords_from_text(input_str)
    result = r.get_ranked_phrases()
    result = [''.join(c for c in s if c not in string.punctuation) for s in result]
    result = [s for s in result if (s and not s.endswith('ful'))]
    cand = None
    for keyword in result:
        tagged_list = [(token, pos) for token, pos in nltk.pos_tag(keyword.split()) if pos.startswith('N') or pos.startswith('V') or pos.startswith('J')]
        if len(tagged_list) == 0:
            continue
        tokens, poses = map(list, zip(*tagged_list))
        if not any([pos for pos in poses if pos.startswith('N')]):
            continue
        cand = ' '.join(tokens)
        break
    return cand



# def chcek_rubbish_word(input_str):
#     english_vocab = set(w.lower() for w in nltk.corpus.words.words())
#     d = enchant.Dict("en_US")
#     num_success_0 = sum(map(d.check, [each for each in input_str.split()]))
#     num_success_1 = 0
#     for each in input_str.split():
#         if each in english_vocab:
#             num_success_1 += 1
#     return False if num_success_0 < 0.5 * len(input_str.split()) and num_success_1 < 0.5 * len(input_str.split()) else True
