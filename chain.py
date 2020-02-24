import random
import math
import copy
import time

class Chain:
	def __init__(self):
		self.Words = {}
		self.BeginWords = {}
		self.Maximum = 0
		self.Name = "Default"

	def open(self, fileName, multiplier = 1):
		print("Chain: open " + fileName)
		with open(fileName, "r", encoding = "utf-8") as file:
			self.parse(file.read(), False, True, multiplier)
	
	def openSerialized(self, fileName):
		with open(fileName, "rb") as file:
			data = pickle.load(file)
			self.Words = data.Words
			self.BeginWords = data.BeginWords
			self.Maximum = data.Maximum
			self.Name = data.Name

	def parse(self, string, append = True, onLoad = False, multiplier = 1):
		string = string.lower()
		for symbol in ["“", "”", "\"", "\'", "\\", "/", "[", "]", "(", ")", "-", "_", "«", "»", "»"]:
			string = string.replace(symbol, " ")
				#if string.find(symbol) > -1:
					#print("hui")
					#return
		#string = string.replace(".", ". %END")
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
				addUnits = multiplier
				self.Words[words[index]][words[index + 1]] = self.Words[words[index]][words[index + 1]] + addUnits
				self.Maximum = max(self.Maximum, self.Words[words[index]][words[index + 1]])

	def getString(self, lastMessage, depth = 0):
		if depth > 3:
			return lastMessage
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
		
		loopCounter = 0
		while True:
			loopCounter += 1
			if self.Words.get(lastWord) == None:
				break
			keys = list(self.Words[lastWord].keys())
			index = random.randint(0, len(keys) - 1)
			count = self.Words[lastWord][keys[index]]
			newWord = keys[index]
			foundKnown = False
			for word in lastMessageSplit:
				if word in keys and random.randint(0, 100) < 40 / len(lastMessageSplit) and word != lastWord:
					foundKnown = True
					newWord = word
			if random.randint(0, round(self.Maximum * 1.2)) >= count or foundKnown:
				oldWord = lastWord
				lastWord = newWord
				skip = False
				if lastWord.lower().find("%end") > -1:
					if random.randint(0, 100) > 50:
						lastWord = oldWord
						skip = True
					else:
						break
				#for symbol in ["\"", "\'", "\\", "/", "[", "]", "(", ")", "-", "_", "«", "»", "*", "—", "хуй", "бля", "пиз", "еб", "ёб", "хер"]:
					#if lastWord.find(symbol) > -1:
						#continue
				if not skip:
					words += " " + lastWord
				else:
					continue
			if loopCounter > 1000:
				return self.getString(lastMessage, depth + 1)
				break
		with open("Chain" + self.Name + "Output.txt", "a", encoding = "utf-8") as file:
			pass#file.write(" " + words + " %END")
		
		wordsSet = set(words)
		wordsCount = {}
		for word in words.split(" "):
			if wordsCount.get(word) == None:
				wordsCount.update({ word : 0 })
			wordsCount[word] += 1
			if wordsCount[word] > 10:
				words = word
				break
		return words
