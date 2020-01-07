# -*- coding: UTF-8 -*-

"""
This file contains the script for all bots of the informal variation.
Created by Nick Tantivasadakarn.
Bot Scripts by Morco Mora-Mendoza. 
Original Bot Scripts by Pablo Paredes, Honghao Wei, Hiroshi Mendoza, Jade Thronton, Nick Tantivasadakarn and others. 
"""




from collections import *
from utils import Params, Config, Modes, Reply

import random


def get_response_dict_informal():
    """
    Returns a dictionary containing all the scripts for the bots.
        Format: bot_texts[bot_id][response_id] = Reply(...)
    Note: 
        - All bots must have a bot name and a bot tech name, and must be added in the 
        bot_name_list and bot_tech_name_list in the Parameters class in utils.py
        - In the reply object, if next_id is a list always have a config.DEFAULT_OTHERS
        option and put it as the last entry 
    """


    params = Params()
    config = Config()
    modes = Modes

    openning = [["Hi {name}, I\'m {bot_name} 👋"]]
    closing = [["Thank you for sharing with me. I hope I\'ve been able to help", "Have a nice day!", "---The conversation has ended. Say \"Hi\" when you need us---"]]

    dk_check_at_begining = [["Do you want me to come back later?"]]

    questions_at_end = [["Do you think this conversation has helped you to reduce stress? Almost no help, neutral or very helpful?"]]

    bot_texts = defaultdict(dict)
    for i in range(params.BOT_NUM):
        bot_texts[i][config.START_INDEX] = Reply(bot_id=i, response_id=config.START_INDEX, texts={modes.GENERAL:[["START_OF_CONVERSATION"]]}, next_id=config.OPENNING_INDEX)
        # bot_texts[i][config.OPENNING_INDEX] = Reply(bot_id=i, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:openning}, next_id=[(config.DEFAULT_DK, config.ARE_YOU_DONE_INDEX), (config.DEFAULT_NO, config.ABRUPT_CLOSING_INDEX), (config.DEFAULT_OTHERS, config.ARE_YOU_DONE_INDEX)])
        #bot_texts[i][config.OPENNING_INDEX] = Reply(bot_id=i, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:openning}, next_id=[(config.DEFAULT_NO, config.ABRUPT_CLOSING_INDEX), (config.DEFAULT_OTHERS,0)])
        # bot_texts[i][config.ARE_YOU_DONE_INDEX] = Reply(bot_id=i, response_id=config.ARE_YOU_DONE_INDEX, texts={modes.GENERAL:[["Are you done?"]]}, next_id=[(config.DEFAULT_NO, config.CONTINUE_INDEX), (config.DEFAULT_OTHERS, 0)])
        # bot_texts[i][config.CONTINUE_INDEX] = Reply(bot_id=i, response_id=config.CONTINUE_INDEX, texts={modes.GENERAL:[["Please continue"]]}, next_id=config.ARE_YOU_DONE_INDEX)
        bot_texts[i][config.CLOSING_INDEX] = Reply(bot_id=i, response_id=config.CLOSING_INDEX, texts={modes.GENERAL:closing}, next_id=None)
        # bot_texts[i][config.DK_INDEX] = Reply(bot_id=i, response_id=config.DK_INDEX, texts={modes.GENERAL:dk_check_at_begining}, next_id=[(config.DEFAULT_DK, config.DK_INDEX), (config.DEFAULT_NO, config.CLOSING_INDEX), (config.DEFAULT_OTHERS, config.CLOSING_INDEX)])
        bot_texts[i][config.ABRUPT_CLOSING_INDEX] = Reply(bot_id=i, response_id=config.ABRUPT_CLOSING_INDEX, texts={modes.GENERAL:[["I understand if you don\'t feel like talking right now", "We bots are always here to help when ever you feel like chatting with us!", "We hope you have a great day!","---The conversation has ended. Say \"Hi\" when you need us.---"]]}, next_id=None)
        bot_texts[i][config.QUESTION_INDEX] = Reply(bot_id=i, response_id=config.QUESTION_INDEX, texts={modes.GENERAL:questions_at_end}, next_id=config.CLOSING_INDEX)
    
    
    #---------------------------------------------------------------------------------------------------------------------------------
    # Doom Bot (WORST CASE SCENARIO)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Hi {name}, I\'m {bot_name} 👋", "Tell with me more details about {problem}?"]]
    # tmp_text[topics.TRAFFIC] = [["Traffic can really suck", "How bad is it out there today?"]]
    # tmp_text[topics.TIRED] = [["I see that you seem tired", "Do you feel you got enough sleep last night?"]]
    # tmp_text[topics.LATE] = [["Sorry to hear that you are late", "How bad is it?"]]
    # tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road", "Can you give me more detail why it\'s stressing you out?"]]
    # tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn\'t responding?"]]
    bot_texts[0][config.OPENNING_INDEX] = Reply(bot_id=0, response_id=config.OPENNING_INDEX, texts=tmp_text, next_id=1)
    del tmp_text


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Hmm I see… 🤔", "What are you most worried about happening?"]]
    # tmp_text[topics.TRAFFIC] = [["That\'s unfortunate", "What do you think the worst possible outcome of this traffic is for you?"]]
    # tmp_text[topics.TIRED] = [["That could be a possible fix", "What\'s the worst possible outcome of you being tired?"]]
    # tmp_text[topics.LATE] = [["Sorry to hear that", "Let me ask you something, what is the worst possible outcome of your lateness?"]]
    # tmp_text[topics.DRIVER] = [["Hmm I see...", "What are most afraid might happen as a result of these other drivers?"]]
    # tmp_text[topics.VEHICLE] = [["That\'s unfortunate", "What\'s the worst possible outcome of this malfunction?"]]
    bot_texts[0][1] = Reply(bot_id=0, response_id=1, texts=tmp_text, next_id=[(config.DEFAULT_DK, 7), (config.DEFAULT_OTHERS, 2)])
    del tmp_text

    bot_texts[0][2] = Reply(bot_id=0, response_id=2, texts={modes.GENERAL:[["Thanks for sharing", "Ok, from 1 to 10 with 1 being almost impossible, how likely is the worst thing to happen"]]}, next_id= [(('5','6','7', 'five', 'six','seven', '8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('1','2','3','4','one','two','three','four', 'unlikely', 'impossible'), 4), ((config.DEFAULT_OTHERS, ), 10)])


    bot_texts[0][3] = Reply(bot_id=0, response_id=3, texts={modes.GENERAL:[["Alright, so if this happens what could you do to get back on track?"]]}, next_id=[(config.DEFAULT_DK, 6), (config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
    bot_texts[0][4] = Reply(bot_id=0, response_id=4, texts={modes.GENERAL:[["So you agree this is unlikely? 🤔"]]}, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 9)])
    #bot_texts[0][5] = Reply(bot_id=0, response_id=5, texts={modes.GENERAL:[["So would you agree that the worst case situation is unlikely?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 9)])

    bot_texts[0][6] = Reply(bot_id=0, response_id=6, texts={modes.GENERAL:[[""]]}, next_id= [(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])
    

    tmp_text = {}
    tmp_text[modes.GENERAL] = [["It\'s ok if you don’t know. What are you worried about?"]]
    # tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution"]]
    # tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep", "But if this doesn\'t work for you,", "spend some time thinking of ways to re-organize your schedule to accommodate a good night\'s rest"]]
    # tmp_text[topics.LATE] = [["Everyone\'s late once in awhile", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time"]]
    # tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem"]]
    # tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution"]]
    bot_texts[0][7] = Reply(bot_id=0, response_id=7, texts=tmp_text, next_id=2)
    del tmp_text



    bot_texts[0][8] = Reply(bot_id=0, response_id=8, texts={modes.GENERAL:[["Cool,😊 looks like you have a plan B", "Remember even if you can’t control everything you can still get back on your feet 🙌", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Great to hear", "Sometimes it\'s helpful to realize that the worst possible scenario isn\'t that likely to happen or wouldn\'t be the end of the world 🤷", "Do you agree?"]]
    # tmp_text[topics.TRAFFIC] = [["Glad to hear that", "Traffic is a nuisance but getting too stressed out by it is often more trouble than it\'s worth"]]
    # tmp_text[topics.TIRED] = [["Seems like you have things in perspective", "Often, we just need a good night\'s rest or even  a short nap to feel refreshed"]]
    # tmp_text[topics.LATE] = [["Even the best prepared are sometimes late", "It\'s usually more trouble than it\'s worth to get too worked up about it"]]
    # tmp_text[topics.DRIVER] = [["Sounds like you have things in perspective", "Aggressive drivers can often be scary to share the road with, but as long as you are driving safely it will usually work out"]]
    # tmp_text[topics.VEHICLE] = [["Glad to hear that", "Oftentimes, vehicle malfunctions are quick fixes and not worth stressing about"]]
    bot_texts[0][9] = Reply(bot_id=0, response_id=9, texts=tmp_text, next_id=config.QUESTION_INDEX)
    del tmp_text


    bot_texts[0][10] = Reply(bot_id=0, response_id=10, texts={modes.GENERAL:[["I\'m sorry, I didn\'t quite catch that, could you repeat? 😕"]]}, next_id= [(('5','6','7', 'five', 'six','seven', '8','9','10', 'eight', 'nine', 'ten', 'likely', 'certain'), 3), (('1','2','3','4','one','two','three','four', 'unlikely', 'impossible'), 4), ((config.DEFAULT_OTHERS, ), 10)])

    #---------------------------------------------------------------------------------------------------------------------------------
    # Sherlock (PROBLEM SOLVING BOT)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Hey {name}, I\'m {bot_name}. 👋","Tell me more about {problem}."]]
    # tmp_text[topics.TRAFFIC] = [["No one likes traffic", "How bad is it out there today?"]]
    # tmp_text[topics.TIRED] = [["I see that you seem tired", "Do you know why?"]]
    # tmp_text[topics.LATE] = [["Why are you late today?"]]
    # tmp_text[topics.DRIVER] = [["Why do these aggressive drivers have you stressed?"]]
    # tmp_text[topics.VEHICLE] = [["Can you give me more details on what you think is wrong with your vehicle?"]]
    bot_texts[1][config.OPENNING_INDEX] = Reply(bot_id=1, response_id=config.OPENNING_INDEX, texts=tmp_text, next_id=1)
    del tmp_text



    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Alright, let\'s think about this together 🤔", "Do you feel this is has affected your life?"]]
    # tmp_text[topics.TRAFFIC] = [["Do you feel traffic is significantly affecting your life?"]]
    # tmp_text[topics.TIRED] = [["Are you frequently tired during your normal working hours?", "Is tiredness negatively affecting important aspects of your life?"]]
    # tmp_text[topics.LATE] = [["I see", "Is lateness a problem that frequently affects your life or is this a one-time thing?"]]
    # tmp_text[topics.DRIVER] = [["Ok, is aggressive driving by others a problem that occurs often enough in your life to worry about it?"]]
    # tmp_text[topics.VEHICLE] = [["Ok, let\'s see how bad this problem is?", "Do you think it will be a quick fix?"]]
    bot_texts[1][1] = Reply(bot_id=1, response_id=1, texts=tmp_text, next_id=4)
    del tmp_text

    # bot_texts[1][2] = Reply(bot_id=1, response_id=2, texts={modes.GENERAL:[["If you could solve this problem, would your life improve?"]]}, next_id=4)
    # bot_texts[1][3] = Reply(bot_id=1, response_id=3, texts={modes.GENERAL:[["Seems like this is not a problem worth worrying about", " Do you still want to work on it?"], ["In that case, do you feel that you\'d still like to spend time working on it?"]]}, next_id=[(config.DEFAULT_NO, config.QUESTION_INDEX), (config.DEFAULT_OTHERS, 4)])
    

    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Have you\'ve dealt with something like this before?"]]
    # tmp_text[topics.TRAFFIC] = [["Was there an effective way you coped with traffic before?"]]
    # tmp_text[topics.TIRED] = [["How have you coped with being tired in the past?"]]
    # tmp_text[topics.LATE] = [["Have you ever found a way to avoid being late in the past that worked well?"]]
    # tmp_text[topics.DRIVER] = [["Have you ever dealt with this problem or something similar before?"]]
    # tmp_text[topics.VEHICLE] = [["Have you ever experienced this problem before?"]]
    bot_texts[1][4] = Reply(bot_id=1, response_id=4, texts=tmp_text, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_YES, 5), (config.DEFAULT_DK, 6), (config.DEFAULT_OTHERS, 6)])
    del tmp_text



    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Ok, what have you tried to do before to deal with a similar problem? 🤔"]]
    # tmp_text[topics.TRAFFIC] = [["Could this strategy help you deal with traffic now?"]]
    # tmp_text[topics.TIRED] = [["Could you use this method to deal with your current tiredness?"]]
    # tmp_text[topics.LATE] = [["Could a similar strategy work now?"]]
    # tmp_text[topics.DRIVER] = [["Was it effective in reducing your stress in dealing with these drivers?"]]
    # tmp_text[topics.VEHICLE] = [["Could a similar solution work here too?"]]
    bot_texts[1][5] = Reply(bot_id=1, response_id=5, texts=tmp_text, next_id=11)
    del tmp_text

    bot_texts[1][11] = Reply(bot_id=1, response_id=11, texts={modes.GENERAL:[["Could you do the same with the current problem?"]]}, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 12)])
    bot_texts[1][12] = Reply(bot_id=1, response_id=12, texts={modes.GENERAL:[["Great! Is there anything stopping you from doing this?"]]}, next_id=[(config.DEFAULT_YES, 6), (config.DEFAULT_OTHERS, 13)])
    bot_texts[1][13] = Reply(bot_id=1, response_id=13, texts={modes.GENERAL:[["Awesome! 🙂 When can you do this in the next couple of days? I find super useful to add my plans to my calendar", "Sounds good?🤷"]]}, next_id=config.QUESTION_INDEX)


    bot_texts[1][6] = Reply(bot_id=1, response_id=6, texts={modes.GENERAL:[["Maybe breaking it down would be helpful 🤷", "What\'s a small part of the problem and a simple solution?"]]}, next_id=[(config.DEFAULT_NO, 8), (config.DEFAULT_OTHERS, 9)])
    #bot_texts[1][7] = Reply(bot_id=1, response_id=7, texts={modes.GENERAL:[["That\'s alright. Can you "]]}, next_id=config.QUESTION_INDEX)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["That\'s alright", "Can you think of a super tiny step that will take you closer to solving the problem? 🤔"]]
    # tmp_text[topics.TRAFFIC] = [["That\'s ok", "Is there any small thing you could do that would reduce the amount of traffic you need to deal with?"]]
    # tmp_text[topics.TIRED] = [["That\'s ok", "Is there any small step you could take to increase the amount of rest you get?"]]
    # tmp_text[topics.LATE] = [["That\'s alright", "Is there a small step you could take in the future to avoid being late next time?"]]
    # tmp_text[topics.DRIVER] = [["Alright, do you feel there is anything you could do so that you could either avoid these drivers entirely or at least feel better about sharing the road with them?"]]
    # tmp_text[topics.VEHICLE] = [["Is there someone you could talk to that might help you find a fix for your vehicle?"]]
    bot_texts[1][8] = Reply(bot_id=1, response_id=8, texts=tmp_text, next_id=[(config.DEFAULT_NO, 10), (config.DEFAULT_OTHERS, 9)])
    del tmp_text


    bot_texts[1][9] = Reply(bot_id=1, response_id=9, texts={modes.GENERAL:[["There you go, you can do that", "Breaking down big problems helps tackle them one step at a time", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Sorry but it seems like I might not be the right bot for this", "If you\'d like to talk to one of my friends say \'/switch\'", "Otherwise, just type goodbye to end the conversation 🤷"]]
    # tmp_text[topics.TRAFFIC] = [["Maybe taking a different route or leaving earlier or later could solve your problem?", "Spending some time planning your travel may help you come up with a solution"]]
    # tmp_text[topics.TIRED] = [["The easiest solution would be to just go to sleep, but if this doesn\'t work for you spend some time thinking of ways to re-organize your schedule to accommodate a good night\'s rest"]]
    # tmp_text[topics.LATE] = [["Everyone\'s late once in awhile", "However, if it is a common occurence maybe think about leaving earlier or taking a quicker route to make your scheduled events on time"]]
    # tmp_text[topics.DRIVER] = [["If aggressive driving is a frequent issue, then perhaps taking a different route could solve your problem"]]
    # tmp_text[topics.VEHICLE] = [["Taking your vehicle to the dealership or mechanic is usually a good solution", "as they can pinpoint the exact problem with your vehicle and offer you a solution"]]
    bot_texts[1][10] = Reply(bot_id=1, response_id=10, texts=tmp_text, next_id=config.QUESTION_INDEX)
    del tmp_text


    #---------------------------------------------------------------------------------------------------------------------------------
    ## Glass-half-full (Positive thinking bot)

    tmp_text = {}
    tmp_text[modes.GENERAL] = [["Hey {name}, I\'m {bot_name}", "What\'s up?"]]
    # tmp_text[topics.TRAFFIC] = [["Could you give me more detail on the traffic is today?"]]
    # tmp_text[topics.TIRED] = [["How do you feel your tiredness is adding to your stress level?"]]
    # tmp_text[topics.LATE] = [["Can you give me more detail on the event you are late to"]]
    # tmp_text[topics.DRIVER] = [["Yeah, there are a lot of aggressive drivers on the road", "Can you give me more detail why it\'s stressing you out?"]]
    # tmp_text[topics.VEHICLE] = [["Can you give me more details on how your vehicle isn\'t responding?"]]
    bot_texts[2][config.OPENNING_INDEX] = Reply(bot_id=2, response_id=config.OPENNING_INDEX, texts=tmp_text, next_id=1)
    del tmp_text

    bot_texts[2][1] = Reply(bot_id=2, response_id=1, texts={modes.GENERAL:[["Hmm I see 🤔", "Ok let\'s do this. Why don\'t you take a couple minutes and think about at least one positive thing about the problem?", "What did you think of?"]]}, next_id=2)
    bot_texts[2][2] = Reply(bot_id=2, response_id=2, texts={modes.GENERAL:[["Great!", "Can you think of any other ones?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 3)])
    bot_texts[2][3] = Reply(bot_id=2, response_id=3, texts={modes.GENERAL:[["Haha that\'s cool! See, you can always find the good out of a bad situation <3"]]}, next_id=5)
    bot_texts[2][4] = Reply(bot_id=2, response_id=4, texts={modes.GENERAL:[["That\'s ok! 😊 At least you found something positive about it"]]}, next_id=5)
    bot_texts[2][5] = Reply(bot_id=2, response_id=5, texts={modes.GENERAL:[["When you're having a bad day looking at the bright side might make you feel better btw 🌞", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)


    tmp_text = {}
    tmp_text[modes.GENERAL] = [["That\'s ok"]]
    # tmp_text[topics.TRAFFIC] = [["That\'s ok traffic is a real nuisance", "Maybe finding something you can do in the car while being stuck in traffic can help pass the time", "listening to music, radio, or just thinking about life"]]
    # tmp_text[topics.TIRED] = [["That\'s ok, honestly being tired is draining", "Maybe finding some time to sleep or at least relax a little could help you feel better"]]
    # tmp_text[topics.LATE] = [["That\'s fair, it\'s tough to find positives in being late", "Maybe leaving a little earlier could help you avoid the situation entirely and solve your problem"]]
    # tmp_text[topics.DRIVER] = [["Yeah, honestly those drivers are real assholes sometimes", "Maybe thinking about how much better of a driver you are can add a positive spin to the situation"]]
    # tmp_text[topics.VEHICLE] = [["Having vehicle trouble is no fun", "Maybe you can use the time to run errands while you get it fixed"]]
    bot_texts[2][6] = Reply(bot_id=2, response_id=6, texts=tmp_text, next_id=5)
    del tmp_text
    
    # bot_texts[0][10] = Reply(bot_id=0, response_id=10, texts=[""], next_id=None)
    # bot_texts[0][11] = Reply(bot_id=0, response_id=11, texts=[""], next_id=None)
    #bot_texts[0][3] = Reply(bot_id=0, response_id=3, text=[""], next_id=4)


    #---------------------------------------------------------------------------------------------------------------------------------
    ## Sir laughts-a-bot (Humor bot)
    bot_texts[3][config.OPENNING_INDEX] = Reply(bot_id=3, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Heyo {name}, I\'m {bot_name}", "What\'s on your mind? "]]}, next_id=1)
    bot_texts[3][1] = Reply(bot_id=3, response_id=1, texts={modes.GENERAL:[["Thanks for sharing. That does sound stressful 🤔", "Have you thought about looking at this problem in a different way", "Maybe you could think of something funny about this whole situation", "¯\\_(ツ)_/¯", " Would you like an example?"]]}, next_id=[(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 2)])
    bot_texts[3][7] = Reply(bot_id=3, response_id=7, texts={modes.GENERAL:[["Great! What did you think of?"]]}, next_id=[(config.DEFAULT_NO, config.ABRUPT_CLOSING_INDEX), (config.DEFAULT_OTHERS, 3)])
    bot_texts[3][2] = Reply(bot_id=3, response_id=2, texts={modes.GENERAL:[["Like if you\'re hungry and stuck in traffic this can be a good one:", "\"why do French people eat snails?🐌\"", "because they don\'t like fast food!!! 😂😂😂", "Don\'t worry if the joke is lame, just try finding something funny", "What did you think of?"]]}, next_id=[(config.DEFAULT_NO, config.ABRUPT_CLOSING_INDEX), (config.DEFAULT_OTHERS, 3)])
    bot_texts[3][3] = Reply(bot_id=3, response_id=3, texts={modes.GENERAL:[["😂😂😂 hahah that\'s funny", "Humor can be found in many situations", "Okay?"]]}, next_id=4)
    bot_texts[3][4] = Reply(bot_id=3, response_id=4, texts={modes.GENERAL:[["Did that help you to find something good (or at least funny) about the situation?"]]}, next_id=[(config.DEFAULT_NO, 6), (config.DEFAULT_OTHERS, 5)])
    bot_texts[3][5] = Reply(bot_id=3, response_id=5, texts={modes.GENERAL:[["I\'m glad 🙂 Do you think this might be a good approach for problems in the future?"]]}, next_id=config.QUESTION_INDEX)
    bot_texts[3][6] = Reply(bot_id=3, response_id=6, texts={modes.GENERAL:[["That\'s ok, humor isn\'t always the answer", "Just remember that trying to find something funny about your situation can help lighten the mood when you\'re stressed", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)


    #---------------------------------------------------------------------------------------------------------------------------------
    ## Chill bot (relaxation bot)
    bot_texts[4][config.OPENNING_INDEX] = Reply(bot_id=4, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Hey {name}, I\'m {bot_name}", "Tell me more details about {problem}"]]}, next_id=1)
    bot_texts[4][1] = Reply(bot_id=4, response_id=1, texts={modes.GENERAL:[["I have a couple strategies to help you feel better", "Say yes if you would rather do a visualization", "Say no if you want to focus on your breathing",  "If you don\'t know which activity you want to do, you can also say no preference and I can decide for you"]]}, next_id=[(('no preference', 'both'), random.randint(2,3)), (('no', ), 3), (('yes', ), 2)])

    bot_texts[4][2] = Reply(bot_id=4, response_id=2, texts={modes.GENERAL:[["Ok, {name}, let\'s do a visualization activity", "I\'d like you to imagine of any place that makes you feel happy or calm", "Think of all the details, as vivid of a picture as you can imagine", "Think of your senses: the sights, the smells, the sounds"], ["Picture a time when you felt at peace. What was around you in this time?", "What did it feel like?", "What do you see, smell or hear?", "Let me know when you are done with your visualization"]]}, next_id=4)
    bot_texts[4][4] = Reply(bot_id=4, response_id=4, texts={modes.GENERAL:[["Could you walk me through your experience?", "What did you see? What did you hear?", "How did you feel?"]]}, next_id=5)
    bot_texts[4][5] = Reply(bot_id=4, response_id=5, texts={modes.GENERAL:[["That sounds lovely, thanks for sharing", "You can look at what you wrote here later to remind you of this place, and how good it makes you feel", "Visualization can be a great tool to destress", "Sounds good?"]]}, next_id=11)
    bot_texts[4][11] = Reply(bot_id=4, response_id=11, texts={modes.GENERAL:[["Would you like to repeat the exercise?"]]}, next_id=[(config.DEFAULT_NO, 13), (config.DEFAULT_OTHERS, 2)])
    


    bot_texts[4][3] = Reply(bot_id=4, response_id=3, texts={modes.GENERAL:[["Okay, let me guide you through a mindfulness exercise to help you {name}. Tell me when you are done after each instruction", "First sit up straight in your chair"]]}, next_id=7)
    bot_texts[4][7] = Reply(bot_id=4, response_id=7, texts={modes.GENERAL:[["Focus on the sensation of air moving through your nose"]]}, next_id=8)
    bot_texts[4][8] = Reply(bot_id=4, response_id=8, texts={modes.GENERAL:[["Slowly widen your focus to the room around you while still observing the sensation of air through your nose"]]}, next_id=9)
    bot_texts[4][9] = Reply(bot_id=4, response_id=9, texts={modes.GENERAL:[["Just think about being present in the moment, and if you feel your mind wandering, return to thinking about the original sensation of air flowing through your nose"]]}, next_id=10)
    bot_texts[4][10] = Reply(bot_id=4, response_id=10, texts={modes.GENERAL:[["Take 5 deep breaths while focusing on you surroundings"]]}, next_id=12)
    bot_texts[4][12] = Reply(bot_id=4, response_id=12, texts={modes.GENERAL:[["Would you like to repeat the exercise?"]]}, next_id=[(config.DEFAULT_NO, 13), (config.DEFAULT_OTHERS, 3)])

    bot_texts[4][13] = Reply(bot_id=4, response_id=13, texts={modes.GENERAL:[["Oftentimes, taking a moment to be mindful may help you in situations when you are feeling stressed", "Sounds good?"]]}, next_id=[(config.DEFAULT_NO, 14), (config.DEFAULT_OTHERS, config.QUESTION_INDEX)])
    bot_texts[4][14] = Reply(bot_id=4, response_id=14, texts={modes.GENERAL:[["That\'s ok. There are many other ways to deal with stress" , "Ok?"]]}, next_id=config.QUESTION_INDEX)
    #---------------------------------------------------------------------------------------------------------------------------------
    ## Treat Yourself Bot (self-love bot)

    bot_texts[5][config.OPENNING_INDEX] = Reply(bot_id=5, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Hi {name}, I\'m {bot_name} 👋", "Could you give me more information about {problem}?"]]}, next_id=2)
    bot_texts[5][2] = Reply(bot_id=5, response_id=2, texts={modes.GENERAL:[["Hmm… imagine a friend came to you and asked you for advice on the same thing", "What would you tell them?"]]}, next_id=[(config.DEFAULT_DK, 3), (config.DEFAULT_OTHERS, 5)])
    bot_texts[5][3] = Reply(bot_id=5, response_id=3, texts={modes.GENERAL:[["That\'s okay, sometimes it\'s hard to know how to support someone", "I’ll send you some things I might do when I\'m stressed", "Feel free to use this list for ideas 🙂", "You can also add your own if you feel like I missed something", "Is that good?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, config.QUESTION_INDEX)])
    bot_texts[5][5] = Reply(bot_id=5, response_id=5, texts={modes.GENERAL:[["What are the benefits of this advice?"]]}, next_id=6)
    bot_texts[5][6] = Reply(bot_id=5, response_id=6, texts={modes.GENERAL:[["Do you have a friend or somebody else to talk to that could give you this kind of support? 🤷"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 7)])
    bot_texts[5][7] = Reply(bot_id=5, response_id=7, texts={modes.GENERAL:[["Ok. Can you make a plan of when to talk to them?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 8)])
    bot_texts[5][8] = Reply(bot_id=5, response_id=8, texts={modes.GENERAL:[["Awesome, friends can often provide the best support", "It\'s great that you have made time to care about yourself 😄" , "Sounds good?"]]}, next_id=config.QUESTION_INDEX)

    bot_texts[5][4] = Reply(bot_id=5, response_id=4, texts={modes.GENERAL:[["I wish I could give you a hug right now to make you feel better! ", "I care about you!, and I\'m sure there are others that do too!, even if they are busy right now", "I hope I could help!, I\'m here whenever you need me 🙂", "If you ever want to talk about your problems just find me or one of my friends, ok? 👍"]]}, next_id=config.QUESTION_INDEX)
    

    #---------------------------------------------------------------------------------------------------------------------------------
    ## Dunno bot (distraction bot)
        #Distraction - dunno bot
    bot_texts[6][config.OPENNING_INDEX] = Reply(bot_id=6, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Heyo  {name}, I\'m {bot_name} 👋", "I\'ve heard you are stressed. Let\'s get your mind off it by distracting ourselves a little 🙌", "What\'s something you\'ve been looking forward to? It can be anything"]]}, next_id=1)
    bot_texts[6][1] = Reply(bot_id=6, response_id=1, texts={modes.GENERAL:[["Oooh tell me more 😮"]]}, next_id=2)
    bot_texts[6][2] = Reply(bot_id=6, response_id=2, texts={modes.GENERAL:[["Is that all? I want to hear all about it!"]]}, next_id=3)
    bot_texts[6][3] = Reply(bot_id=6, response_id=3, texts={modes.GENERAL:[["Cool. Anything else you\'re excited about?"]]}, next_id=[(config.DEFAULT_NO, 4), (config.DEFAULT_OTHERS, 2)])
    bot_texts[6][4] = Reply(bot_id=6, response_id=4, texts={modes.GENERAL:[["Alright. Remember that when you\'re stressed you can think of things you\'re looking forward to do ", "Sound good?"]]}, next_id=config.QUESTION_INDEX)

    #---------------------------------------------------------------------------------------------------------------------------------
    ## checkin bot

    # bot_texts[7][0] = Reply(bot_id=7, response_id=0, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])

    # bot_texts[7][1] = Reply(bot_id=7, response_id=1, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 4)])
    # bot_texts[7][2] = Reply(bot_id=7, response_id=2, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 5), (config.DEFAULT_OTHERS, 6)])



    # bot_texts[7][3] = Reply(bot_id=7, response_id=3, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 2)])
    # bot_texts[7][4] = Reply(bot_id=7, response_id=4, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])
    # bot_texts[7][5] = Reply(bot_id=7, response_id=5, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])
    # bot_texts[7][6] = Reply(bot_id=7, response_id=6, texts={modes.GENERAL:[[""]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])



    # bot_texts[7][7] = Reply(bot_id=7, response_id=7, texts={modes.GENERAL:[["Wonderful, it seems as though this problem isn\'t affecting these three major aspects of your life", "Great job staying on top of your sleeping and eating as well as reaching out to friends and family for support"]]}, next_id=config.QUESTION_INDEX)
    # bot_texts[7][8] = Reply(bot_id=7, response_id=8, texts={modes.GENERAL:[[""]]}, next_id=config.QUESTION_INDEX)
    # bot_texts[7][9] = Reply(bot_id=7, response_id=9, texts={modes.GENERAL:[[""]]}, next_id=config.QUESTION_INDEX)
    # bot_texts[7][10] = Reply(bot_id=7, response_id=10, texts={modes.GENERAL:[[""]]}, next_id=config.QUESTION_INDEX)

    # bot_texts[7][7] = Reply(bot_id=7, response_id=7, texts={modes.GENERAL:[[""]]}, next_id=)

    #---------------------------------------------------------------------------------------------------------------------------------
    ## onboarding bot

    #bot_texts[7][config.OPENNING_INDEX] = Reply(bot_id=7, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Hi! We\'re the Pop-Bots!", "We are here to help you with stress", "May we have your name, please?"]]}, next_id=config.CLOSING_INDEX)#next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 0)])
    bot_texts[7][config.OPENNING_INDEX] = Reply(bot_id=7, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Hi! ✋ We\'re the Pop-Bots!","We \"pop\" in to have simple and brief conversations and help you with your everyday stress", "Please keep each response in one line so we know that you are done 😊", "Sounds good?"]]}, next_id=1)#next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 0)])
    bot_texts[7][1] = Reply(bot_id=7, response_id=1, texts={modes.GENERAL:[["What should we call you?"]]}, next_id=2)
    bot_texts[7][2] = Reply(bot_id=7, response_id=2, texts={modes.GENERAL:[["Nice to meet you, {name}. We\'re all excited to get to know you. Please explore the app and get to know all 7 of us as well","As you interact with us, we will learn to choose the best PopBot for you", "Okay?"]]}, next_id=5)
    bot_texts[7][5] = Reply(bot_id=7, response_id=5, texts={modes.GENERAL:[["Remember that we are just bots and we are pretty limited", "Also, we are not made to handle serious mental problems. Please talk to a therapist for those situations or call 911 if it is an emergency", "Got it? 😉"]]}, next_id=config.CLOSING_INDEX)
    bot_texts[7][config.CLOSING_INDEX] = Reply(bot_id=7, response_id=config.CLOSING_INDEX, texts={modes.GENERAL:[["Let\'s get started! 🎉🎉🎉 Type \"Hi\" to start the conversation with one of us", "At any point, you can type \"/switch\" to have a conversation with a new bot"]]}, next_id=None)
    

    # tmp_text = [["I\'m here to give you a few pointers about how to interact with me and my friends",  "First, we are only bots. We strive to do our best to understand you, and you will get more from us if you are able to give more than a yes or no answer to our questions", 
    #             "We bots are also pretty new, which means that we are still learning", "Right now it\'s important for us that you respond to each question in one message block", "Feel free to hit return to add multiple paragraphs but only press send once you have expressed what you want to share. It\'s okay if you forget, we might just get a bit confused", 
    #             "We will also ask some questions about how helpful we are. We want you to answer as honestly as you can because it will help us to learn and improve",
    #             "Lastly, in emergencies, please stop and call 911 or 1-800-273-8255 (the suicide hotline).", "A human may never read what you are writing, so it\'s important that you get help apart from us if you feel you are in danger",
    #             "Sound good? "]]
    
    # bot_texts[7][0] = Reply(bot_id=7, response_id=0, texts={modes.GENERAL:tmp_text}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])
    #bot_texts[7][1] = Reply(bot_id=7, response_id=1, texts={modes.GENERAL:[["We are part of a research study by Stanford University. If you wish to participate, please register at the link below", "https://stanforduniversity.qualtrics.com/jfe/form/SV_cGZtiXUVLkXHjud?id={subject_id}", "If you do not wish to participate, your data will not be used in the study"]]}, next_id=2)
    #bot_texts[7][2] = Reply(bot_id=7, response_id=2, texts={modes.GENERAL:[["Awesome!", "May we have your name, please?"]]}, next_id=config.CLOSING_INDEX)
    #bot_texts[7][3] = Reply(bot_id=7, response_id=3, texts={modes.GENERAL:[["May I have your name, please?"]]}, next_id=config.CLOSING_INDEX)
    
    bot_texts[7][6] = Reply(bot_id=7, response_id=6, texts={modes.GENERAL:[
                ["Hi {name}. Thank\'s for texting us again","What\'s a recent situation that has been stressing you out?"],
                ["Hi {name}. Thank\'s for texting us again","What\'s stressing you out right now?"],
                ["Hi {name}. Thank\'s for texting us again","What\'s on your mind that is stressing you out?"],
                ["Hi {name}. Thank\'s for texting us again","What\'s something that\'s on your mind that is stressing you out?"]

                ]}, next_id=4)

    bot_texts[7][3] = Reply(bot_id=7, response_id=3, texts={modes.GENERAL:[["Which bot do you want to talk to?"]]}, next_id=4)
    bot_texts[7][4] = Reply(bot_id=7, response_id=4, texts={modes.GENERAL:[["Got it! Switching bots!"], ["Roger! Switching bots!"],["Roger! Switching bots! (You can always type /switch to change bots again.)"]]}, next_id=None)
    bot_texts[7][10] = Reply(bot_id=7, response_id=10, texts={modes.GENERAL:[["Hmm... What about this one?"], ["Hmm... How about this bot?"],["Hmm... What about this one? (You can always type /switch to change bots again.)"]]}, next_id=None)

    bot_texts[7][7] = Reply(bot_id=7, response_id=7, texts={modes.GENERAL:[[""]]}, next_id=8)
    bot_texts[7][8] = Reply(bot_id=7, response_id=8, texts={modes.GENERAL:[["You seem to have switched bots in the past conversation. Could you tell us why?"]]}, next_id=9)
    bot_texts[7][9] = Reply(bot_id=7, response_id=9, texts={modes.GENERAL:closing}, next_id=None)
    #bot_texts[7][11] = Reply(bot_id=7, response_id=11, texts={modes.GENERAL:[["I\'m sorry, I didn\'t quite catch that, could you repeat? 😕"]]}, next_id=None)


    #---------------------------------------------------------------------------------------------------------------------------------
    ## checkin bot

    bot_texts[8][config.OPENNING_INDEX] = Reply(bot_id=8, response_id=config.OPENNING_INDEX, texts={modes.GENERAL:[["Hi {name}, I\'m {bot_name} 👋", "Hmm, that sounds stressful", "Maybe we can think of how the problem is affecting other parts of your life 🤷","Sounds good?"]]}, next_id=[(config.DEFAULT_NO, 1), (config.DEFAULT_OTHERS, 2)])

    #can we pass off to a bot friend?
    bot_texts[8][1] =  Reply(bot_id=8, response_id=1, texts={modes.GENERAL:[["Okay, maybe I can introduce you to my other bot-friends?😊"]]}, next_id=[(config.DEFAULT_NO, config.ABRUPT_CLOSING_INDEX), (config.DEFAULT_OTHERS, config.QUESTION_INDEX)])

    bot_texts[8][2] = Reply(bot_id=8, response_id=2, texts={modes.GENERAL:[["Cool, let’s start. Have you had problems sleeping because of this?😴"]]}, next_id=[(config.DEFAULT_NO, 3), (config.DEFAULT_OTHERS, 4)])

    #{}
    #no - good sleep +1
    # {+1}
    bot_texts[8][3] = Reply(bot_id=8, response_id=3, texts={modes.GENERAL:[["Ok, rockin! Yay sleep!","What about your eating habits? Have you stopped eating because of this problem? 🤤"]]}, next_id=[(config.DEFAULT_NO, 5), (config.DEFAULT_OTHERS, 6)])
    #yes - bad sleep 0
    # {0}
    bot_texts[8][4] = Reply(bot_id=8, response_id=4, texts={modes.GENERAL:[["That\'s ok. Although sleeping is great sometimes we might miss out on it", "What about eating? Have you been eating regularly? 🤷"]]}, next_id=[(config.DEFAULT_NO, 7), (config.DEFAULT_OTHERS, 8)])


    #good sleep
    #no - good food =2
    #{1, 1}
    bot_texts[8][5] = Reply(bot_id=8, response_id=5, texts={modes.GENERAL:[["I\'m glad to hear that","One last thing. Have you\'ve talked about this with other people? Talking to your friends or family might help"]]}, next_id=[(config.DEFAULT_NO, 10), (config.DEFAULT_OTHERS, 9)])
    #yes - bad food =1
    #{1, 0}
    bot_texts[8][6] = Reply(bot_id=8, response_id=6, texts={modes.GENERAL:[["That can be tough, but I can tell that you are working hard and doing your best!","Have you tried talking to your friends or family? They\'re the ones who often can help in a time like this 😮"]]}, next_id=[(config.DEFAULT_NO, 12), (config.DEFAULT_OTHERS, 11)])
    
    #bad sleep
    #no - good food =1
    #{0, 1}
    bot_texts[8][7] = Reply(bot_id=8, response_id=7, texts={modes.GENERAL:[["I\'m glad to hear that","One last question. Have you tried talking to your friends or family? They\'re the ones who often can help in a time like this 😮"]]}, next_id=[(config.DEFAULT_NO, 14), (config.DEFAULT_OTHERS, 13)])
    #yes - bad food =0
    #{0, 0}
    bot_texts[8][8] = Reply(bot_id=8, response_id=8, texts={modes.GENERAL:[["That can be tough, but I can tell that you are working hard and doing your best!","Have you tried talking to your friends or family? They\'re the ones who often can help in a time like this 😮"]]}, next_id=[(config.DEFAULT_NO, 16), (config.DEFAULT_OTHERS, 15)])
    
    #Yes friends!
    #good sleep
    #good food = 3
    #{1, 1, 1}
    bot_texts[8][9] = Reply(bot_id=8, response_id=9, texts={modes.GENERAL:[["I\'m glad that you have been able to talk to others about this","Wonderful! It seems like this isn\'t affecting these areas of your life. Great job staying on top of your sleeping and eating as well as talking to others for support! 👍" , "Sounds good?"]]}, next_id=config.QUESTION_INDEX)

    #{sleep, eat, friends}
    #{1, 1, 0}
    bot_texts[8][10] = Reply(bot_id=8, response_id=10, texts={modes.GENERAL:[["I\'m sorry to hear that. 😕 Me and my bot-friends are always here to support you 🤗","Great! Seems like things are not that bad. It might be helpful to reach out to people you care about" , "Sounds good?"]]}, next_id=config.QUESTION_INDEX)
    
    #{1, 0, 1}
    bot_texts[8][11] = Reply(bot_id=8, response_id=11, texts={modes.GENERAL:[["I\'m glad that you have been able to talk to others about this", "Great! Seems like things are not that bad. Remember to set aside some time for eating so that you can feel better in general 🌞" , "Sounds good?"]]}, next_id=config.QUESTION_INDEX)
    
    #{1, 0, 0}
    bot_texts[8][12] = Reply(bot_id=8, response_id=12, texts={modes.GENERAL:[["I\'m sorry to hear that. 😕 Me and my bot-friends are always here to support you 🤗","Great job on sleeping regularly! It might be helpful to focus on eating regularly and reaching out to people you care about" , "Sounds good?"]]}, next_id=config.QUESTION_INDEX)
    
    #{0, 1, 1}
    bot_texts[8][13] = Reply(bot_id=8, response_id=13, texts={modes.GENERAL:[["I\'m glad that you have been able to talk to others about this","Great! Seems like things are not that bad. Remember to set aside some time for sleeping so that you can feel better in general 🌞", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)
    
    #{0, 1, 0}
    bot_texts[8][14] = Reply(bot_id=8, response_id=14, texts={modes.GENERAL:[["I\'m sorry to hear that. 😕 Me and my bot-friends are always here to support you 🤗","Great job on eating regularly! It might be helpful to focus on sleeping regularly and reaching out to people who care about you", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)

    #{0, 0, 1}
    bot_texts[8][15] = Reply(bot_id=8, response_id=15, texts={modes.GENERAL:[["I\'m glad that you have been able to talk to others about this","Great job on reaching out to people who care about you! Remember to set aside some time for eating and sleeping so that you can feel better in general 🌞", "Sounds good?"]]}, next_id=config.QUESTION_INDEX)

    #{0, 0, 0}
    bot_texts[8][16] = Reply(bot_id=8, response_id=16, texts={modes.GENERAL:[["I\'m sorry to hear that. 😕 Me and my bot-friends are always here to support you 🤗","Hey, I just want to say that things are going to get better. 🌞 Hang in there tiger! Eating and sleeping regularly as well as talking to loved ones can be great places to start if you are feeling stressed 🤷", "Sounds good?"]]}, next_id=config.CLOSING_INDEX)    


    return bot_texts