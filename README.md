# chatbot

This project intends to use Telegram platform to build a chatbot.
The contorl of chatbot is in bot_telegram.py. Run python bot.py for starting the chatbot server.

The log is stored in mongoDB. db is chatbot and collections are user and user_history.
user stores user_id 
user_history stores all interaction between user and chatbot in a json format

current_id is the id shows the index of chatbot(with bot_id)'s question.



Setting up
	1. Set up the python environment (anaconda) using "environment.yml"
	2. Install MongoDB 
		https://docs.mongodb.com/manual/installation/
	3. Ask for/create the file containing the Telegram bot token (token.txt).
		If you are developping the bot on your own, it is recommended to create your own bot
		and use your own token. https://core.telegram.org/bots


To run the project 
local computer
	1. Run "mongod" (mongo daemon)
	2. Open another shell window. Run "bot_telegram.py".

non-Stanford servers
	1. Copy the repository to the server.
	2. ssh into the server.
	3. Run "screen"
	4. Run "mongod" (mongo daemon) inside the screen
	5. Open another screen.
	3. Run "bot_telegram.py".

Stanford servers

non-Stanford servers
	1. Copy the repository to the server.
	2. ssh into the server.
	3. Run "krbscreen" and 
	4. Run "reauth", and then "mongod" (mongo daemon) inside the screen
	5. Open another "krbscreen"
	3. Run "reauth", and then "bot_telegram.py".

	(if you use screen or do not use reauth, the program will terminate after you log out)

