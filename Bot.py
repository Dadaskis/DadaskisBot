#Беги отсюда мужик
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

"""
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    """

class Chain:
	def __init__(self):
		self.Words = {}
		self.BeginWords = {}
		self.Maximum = 0
		self.Name = "Default"

	def open(self, fileName):
		with open(fileName, "r", encoding = "utf-8") as file:
			self.parse(file.read(), False, True)
	
	def openSerialized(self, fileName):
		with open(fileName, "rb") as file:
			data = pickle.load(file)
			self.Words = data.Words
			self.BeginWords = data.BeginWords
			self.Maximum = data.Maximum
			self.Name = data.Name

	def parse(self, string, append = True, onLoad = False):
		string = string.lower()
		if not onLoad:
			for symbol in ["\"", "\'", "\\", "/", "[", "]", "(", ")", "-", "_", "«", "»", "*", "—"]:
				if string.find(symbol) > -1:
					print("hui")
					return
		string = string.replace(".", ". %END")
		string = string.replace("%end", "%END ")
		string += " %END "
		format = "a"
		if not append:
			format = "w"
		with open("Chain" + self.Name + ".txt", format, encoding = "utf-8") as file:
			file.write(" " + string + " ")
		'''with open("Chain" + self.Name + ".obj", "wb") as file:
			pickle.dump(self, file)'''

		strings = string.split("%END")
		for string in strings:
			words = string.split()
			if len(words) == 0:
				continue
			if self.BeginWords.get(words[0]) == None:
				self.BeginWords.update({words[0] : 0})
			self.BeginWords[words[0]] = self.BeginWords[words[0]] + 1
			self.Maximum = max(self.Maximum, self.BeginWords[words[0]])

			for index in range(0, len(words) - 1):
				if self.Words.get(words[index]) == None:
				    self.Words.update({words[index] : {}})
				if self.Words.get(words[index]).get(words[index + 1]) == None:
					self.Words[words[index]].update({words[index + 1] : 0})
				self.Words[words[index]][words[index + 1]] = self.Words[words[index]][words[index + 1]] + 1
				self.Maximum = max(self.Maximum, self.Words[words[index]][words[index + 1]])

	def getString(self, lastMessage):
		lastMessage = lastMessage.lower()
		#for symbol in [",", ".", "!", "?", ";"]:
			#lastMessage = lastMessage.replace(symbol, "")
		keys = lastMessage.split(" ")
		keys = list(set(keys))
		index = random.randint(0, len(keys) - 1)
		words = ""
		founded = False
		for index in range(0, len(keys)):
			words = keys[index]
			if self.Words.get(words) == None:
				continue
				"""keys = list(self.BeginWords.keys())
				if len(keys) == 0:
					return ""
				index = random.randint(0, len(keys) - 1)
				words = keys[index]"""
			else:
				founded = True
				break
		if not founded:
			return ""
		lastWord = words
		lastMessageSplit = keys

		while True:
			if self.Words.get(lastWord) == None:
				break
			keys = list(self.Words[lastWord].keys())
			index = random.randint(0, len(keys) - 1)
			count = self.Words[lastWord][keys[index]]
			newWord = keys[index]
			foundKnown = False
			for word in lastMessageSplit:
				if word in keys and random.randint(0, 100) > 200 / len(lastMessageSplit) and word != lastWord:
					foundKnown = True
					newWord = word
			if random.randint(0, round((self.Maximum + 1) * 2)) >= count or foundKnown:
				lastWord = newWord
				if lastWord.lower().find("%end") > -1:
					break
				words += " " + lastWord
		with open("Chain" + self.Name + "Output.txt", "a", encoding = "utf-8") as file:
			file.write(" " + words + " %END")
		
		return words

chain = Chain()
try:
	#chain.openSerialized("ChainDefault.obj")
	chain.open("ChainDefault.txt")
except Exception as ex:
	print(ex)

'''
for index in range(0, 1):
	print(index)
	with open("newtext" + str(index) + ".txt", "r") as file:
		text = file.read()
		text = text.replace(".", ". %END")
		text = text.replace("- ", "")
		for counter in range(0, 1):
			chain.parse(text)'''
#for counter in range(0, chain.Maximum):
#	chain.parse("Свободная касса")

for counter in range(0, 30):
	print(chain.getString("А ты"))
	print()

lastTimer = -60
def StartTelegram():
	updater = telegram.ext.Updater("81265ИсусТыСлышышМеняИсусVt0MapdIto0x5dbU")
	dispatcher = updater.dispatcher
	
	interestingCat = "🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n🌕🌕🌘🌑🌓🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n🌕🌕🌑🌕🌕🌕🌗🌑🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌑🌕🌕🌖🌑👁🌑👁🌔🌗🌑🌕🌕\n🌕🌕🌘🌓🌕🌑🌑🌑🌑🌑🌔🌕🌘🌔🌕\n🌕🌕🌗🌑🌘🌑🌑🌑🌑🌑🌕🌖🌑🌕🌕\n🌕🌕🌕🌘🌑🌑🌑🌑🌑🌕🌖🌑🌔🌕🌕\n🌕🌕🌕🌖🌑🌑🌑🌑🌑🌑🌑🌔🌕🌕🌕\n🌕🌕🌕🌗🌑🌑🌑🌑🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌕🌘🌑🌕🌕🌘🌑🌔🌕🌕🌕🌕🌕\n🌕🌕🌕🌑🌓🌕🌕🌗🌑🌕🌕🌕🌕🌕🌕\n🌕🌕🌖🌑🌔🌕🌕🌖🌑🌔🌕🌕🌕🌕🌕\n🌕🌕🌗🌑🌕🌕🌕🌕🌑🌑🌕🌕🌕🌕🌕\n🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n"
	
	def SendInterestingCat(bot, update):
		bot.send_message(chat_id = update.message.chat_id, text = interestingCat)
	
	def TCustomCommands(bot, update):
		message = update.message.text
		
		if message.find("/ъуъ") > -1:
			SendInterestingCat(bot, update)
			return True
		
		return False
	
	def TCommand(update, string):
		if not update.message or not update.message.text:
			return False
		return update.message.text.lower().find(string.lower()) > -1

	def TCommands(upd):
		return TCommand(upd, "дудка") or TCommand(upd, "дадасаки") or TCommand(upd, "дадаскис") or TCommand(upd, "dadaskis") or TCommand(upd, "dudka") or TCommand(upd, "dadasaki")
	
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

	def message(bot, update):
		if not update.message:
			return
	
		if update.message.from_user.name == "@DadaskisBot":
			return
			
		if TCustomCommands(bot, update):
			return
			
		#print(update.message.chat_id)
		
		#if random.randint(0, 100) <= 12:
		chain.parse(update.message.text)
		
		if telegramChannelCounter.get(str(update.message.chat_id)) == None:
			telegramChannelCounter.update({str(update.message.chat_id) : 0})
			print("new " + update.message.chat)
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
			if (timers[update.message.chat_id] + 0.5) > time.process_time():
				#print("asd", lastTime, time.process_time())
				return
		
		try:
			telegramChannelCounter[str(update.message.chat_id)] += 1
			if TCommands(update) or replied:
				#print(update.message.from_user.name + ", " + update.message.chat.username + ": " + update.message.text)
				telegramChannelCounter[str(update.message.chat_id)] = 0
				#for counter in range(1, 50):
				lastText = update.message.text.lower()
				lastText = lastText.replace("дудка", "")
				string = chain.getString(lastText)
				for counter in range(1, 3):
					newString = chain.getString(lastText)
					if len(newString) < len(string):
						string = newString
				if len(string) > 4000:
					string = string[:4000 - len(string)]
				print("### Telegram msg: " + string)
				bot.send_message(chat_id = update.message.chat_id, text = string)
				timers[update.message.chat_id] = time.process_time()
		except Exception as ex:
			print(ex)
	
	start_handler = telegram.ext.MessageHandler(telegram.ext.Filters.chat, message)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(telegram.ext.InlineQueryHandler(TInlineCallback))
	updater.start_polling()

TThread = threading.Thread(target = StartTelegram)
TThread.start()

class DiscordDudka(discord.Client):
	async def on_ready(self):
		print("Logged on as {0}!".format(self.user))
	
	async def on_message(self, message):
		if message.author == self.user:
			return
		chain.parse(message.content)
		await message.channel.send(chain.getString(message.content))
		
def DStart():
	try:
		client = DiscordDudka()
		client.run('NTIwODg0ODI4NDQzNTAahahahanulltoken12Fsw9jB7kMIDXcfzEM')
	except Exception:
		DStart()

DStart()
