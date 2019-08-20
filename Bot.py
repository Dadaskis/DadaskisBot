import pickle

import random
import threading
import telegram.ext
import asyncio
import copy
import os
import sys

import logging
#Fucked up shit begins...
class Chain:
	def __init__(self):
		self.Words = {}
		self.BeginWords = {}
		self.Maximum = 0
		self.Name = "Default"

	def open(self, fileName):
		with open(fileName, "r", encoding = "utf-8") as file:
			self.parse(file.read(), False)
	
	def openSerialized(self, fileName):
		with open(fileName, "rb") as file:
			data = pickle.load(file)
			self.Words = data.Words
			self.BeginWords = data.BeginWords
			self.Maximum = data.Maximum
			self.Name = data.Name

	def parse(self, string, append = True):
		string = string.lower()
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
		for symbol in [",", ".", "!", "?", ";"]:
			lastMessage = lastMessage.replace(symbol, "")
		keys = lastMessage.split(" ")
		index = random.randint(0, len(keys) - 1)
		words = keys[index]
		if self.Words.get(words) == None:
			keys = list(self.BeginWords.keys())
			if len(keys) == 0:
				return ""
			index = random.randint(0, len(keys) - 1)
			words = keys[index]
		lastWord = words

		while True:
			if self.Words.get(lastWord) == None:
				break
			keys = list(self.Words[lastWord].keys())
			index = random.randint(0, len(keys) - 1)
			count = self.Words[lastWord][keys[index]]
			if random.randint(0, round((self.Maximum + 1) * 3)) >= count:
				lastWord = keys[index]
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




updater = telegram.ext.Updater(TThiIsShittiestTokenEver")
dispatcher = updater.dispatcher

def TCommand(update, string):
	if not update.message or not update.message.text:
		return False
	return update.message.text.lower().find(string.lower()) > -1

def TCommands(upd):
	return TCommand(upd, "дудка") or TCommand(upd, "дадасаки") or TCommand(upd, "дадаскис") or TCommand(upd, "dadaskis") or TCommand(upd, "dudka") or TCommand(upd, "dadasaki")

telegramChannelCounter = {}
def message(bot, update):
	if not update.message:
		return

	if update.message.from_user.name == "@DadaskisBot":
		return
		
	#print(update.message.chat_id)
	
	chain.parse(update.message.text)
	
	if telegramChannelCounter.get(str(update.message.chat_id)) == None:
		telegramChannelCounter.update({str(update.message.chat_id) : 0})
		print("new")
	replied = False
	if update.message.reply_to_message:
		if update.message.reply_to_message.from_user.name == "@DadaskisBot":
			replied = True
	try:
		telegramChannelCounter[str(update.message.chat_id)] += 1
		if TCommands(update) or replied:
			#print(update.message.from_user.name + ", " + update.message.chat.username + ": " + update.message.text)
			telegramChannelCounter[str(update.message.chat_id)] = 0
			#for counter in range(1, 50):
			lastText = update.message.text
			lastText = lastText.replace("Дудка", "")
			string = chain.getString(lastText)
			if len(string) > 4000:
				string = string[:4000 - len(string)]

			bot.send_message(chat_id = update.message.chat_id, text = string)
	except Exception as ex:
		print(ex)

start_handler = telegram.ext.MessageHandler(telegram.ext.Filters.group, message)
dispatcher.add_handler(start_handler)
updater.start_polling()
