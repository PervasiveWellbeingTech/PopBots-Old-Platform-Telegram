# chatbot

This project intends to use Telegram platform to build a chatbot.
The contorl of chatbot is in bot_telegram.py. Run python bot.py for starting the chatbot server.

The log is stored in mongoDB. db is chatbot and collections are user and user_history.
user stores user_id 
user_history stores all interaction between user and chatbot in a json format

current_id is the id shows the index of chatbot(with bot_id)'s question.
