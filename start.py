import pickle
import discord
import random
import threading
import telegram.ext
import asyncio
import copy
import os
import sys
import time
import uuid
import math
import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


#our shit
from commandHandler import CommandHandler, ChatUserInfo


import logging
#logging.basicConfig(level=logging.ERROR,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



'''
for index in range(0, 1):
	print(index)
	with open("newtext" + str(index) + ".txt", "r") as file:
		text = file.read()
		text = text.replace(".", ". %END")
		text = text.replace("- ", "")
		for counter in range(0, 1):
			chain.parse(text)'''

command = CommandHandler()

lastTimer = -606
def StartTelegram():
	updater = telegram.ext.Updater("812651832:AAFyITJP_a0bn--9sfISeKiJMLf3rk8YnQ4", use_context = True)
	dispatcher = updater.dispatcher
	
	interestingCat = "🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n🌕🌕🌘🌑🌓🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n🌕🌕🌑🌕🌕🌕🌗🌑🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌑🌕🌕🌖🌑👁🌑👁🌔🌗🌑🌕🌕\n🌕🌕🌘🌓🌕🌑🌑🌑🌑🌑🌔🌕🌘🌔🌕\n🌕🌕🌗🌑🌘🌑🌑🌑🌑🌑🌕🌖🌑🌕🌕\n🌕🌕🌕🌘🌑🌑🌑🌑🌑🌕🌖🌑🌔🌕🌕\n🌕🌕🌕🌖🌑🌑🌑🌑🌑🌑🌑🌔🌕🌕🌕\n🌕🌕🌕🌗🌑🌑🌑🌑🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌕🌘🌑🌕🌕🌘🌑🌔🌕🌕🌕🌕🌕\n🌕🌕🌕🌑🌓🌕🌕🌗🌑🌕🌕🌕🌕🌕🌕\n🌕🌕🌖🌑🌔🌕🌕🌖🌑🌔🌕🌕🌕🌕🌕\n🌕🌕🌗🌑🌕🌕🌕🌕🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n"
	
	def TInlineCallback(bot, update):
		query = update.inline_query.query
		results = [
			telegram.InlineQueryResultArticle(
				id = uuid.uuid4(),
				title = "ъуъ",
				input_message_content = telegram.InputTextMessageContent(interestingCat))]
		update.inline_query.answer(results)
	
	telegramChannelCounter = {}
	timers = {}

	def message(update : telegram.Update, context : telegram.ext.CallbackContext):
		 
		if not update.message:
			return
	
		if update.message.from_user.name == "@DadaskisBot":
			return

		info = ChatUserInfo()
		info.userName = update.message.from_user.first_name
		info.userID = update.message.from_user.id
		info.platform = "Telegram"
		info.chatID = update.effective_chat.id
		info.telegramBot = context.bot
		info.telegramUpdate = update
		
		if update.message.reply_to_message:
			if update.message.reply_to_message.from_user.username == "DadaskisBot":
				info.botReply = True
			info.reply = True
			info.userIDReply = update.message.reply_to_message.from_user.id
			info.userNameReply = update.message.reply_to_message.from_user.name
		print("send")
		context.bot.send_message(chat_id = update.effective_chat.id, text = command.handle(update.message.text, info))
		
	start_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, message)
	dispatcher.add_handler(start_handler)
	#dispatcher.add_handler(telegram.ext.InlineQueryHandler(TInlineCallback))
	updater.start_polling()

TThread = threading.Thread(target = StartTelegram)
TThread.start()

class DiscordDudka(discord.Client):
	async def on_ready(self):
		print("Logged on as {0}!".format(self.user))
	
	async def on_message(self, message):
		#try:
		if message.author == self.user:
			return
		if message.guild == None:
			return
				
		info = ChatUserInfo()
		info.userName = message.author.nick
		info.userID = message.author.id
		info.platform = "Discord"
		info.chatID = message.guild.id
		#info.telegramBot = bot
		#info.telegramUpdate = update
		info.discordBot = self
		info.discordMessage = message
		messageString = command.handle(message.content, info)
		if len(messageString) > 1:
			await message.channel.send(messageString)
		#except Exception as ex:
		#	PrintException()
		#	await self.logout()
		#	DStart()
			
def DStart():
	try:
		client = DiscordDudka()
		client.run('NTIwODg0ODI4NDQzNTA4NzM2.XknWMg.Jgl-QHbzJJAKt2tPQU6vx3I9Gq8')
	except Exception:
		pass#DStart()

DStart()






'''
		#print(update.message.chat_id)
		
		#if random.randint(0, 100) <= 12:
		chain.parse(update.message.text)
		
		if telegramChannelCounter.get(str(update.message.chat_id)) == None:
			telegramChannelCounter.update({str(update.message.chat_id) : 0})
		#	print("new " + update.message.chat)
		replied = False
		if update.message.reply_to_message:
			if update.message.reply_to_message.from_user.name == "@DadaskisBot":
				replied = True
		
		global lastTimer	
		#global timers
		#print(lastTimer, time.process_time())
		#print(update.message.chat.description)
		if (bot.get_chat(update.message.chat_id).description or "").find("DudkaNonStop") == -1:
			if(timers.get(update.message.chat_id) == None):
				timers[update.message.chat_id] = 0
			if (timers[update.message.chat_id] + 0.1) > time.process_time():
				#print("asd", lastTime, time.process_time())
				return
		
		try:
			telegramChannelCounter[str(update.message.chat_id)] += 1
			if TCommands(update) or replied or telegramChannelCounter[str(update.message.chat_id)] > 200:
				#print(update.message.from_user.name + ", " + update.message.chat.username + ": " + update.message.text)
				telegramChannelCounter[str(update.message.chat_id)] = 0
				#for counter in range(1, 50):
				lastText = update.message.text.lower()
				lastText = lastText.replace("дудка, ", "")
				lastText = lastText.replace("дудка,", "")
				lastText = lastText.replace("дудка", "")
				string = chain.getString(lastText)
				for counter in range(1, 40):
					newString = chain.getString(lastText)
					newStringSet = newString.split(" ")
					if len(newStringSet) > 30 and len(newStringSet) < 80:
						if len(newString) < len(string):
							string = newString
				if len(string) > 4000:
					string = string[:4000 - len(string)]
				print("### Telegram msg: " + string)
				bot.send_message(chat_id = update.message.chat_id, text = string)
				timers[update.message.chat_id] = time.process_time()
		except Exception as ex:
			print(ex)
'''
