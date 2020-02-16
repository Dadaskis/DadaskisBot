import random
import pickle
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


class RPCommands:
	def load(self):
		try:
			input = open('RPCommandsData.obj', 'rb')
			obj = pickle.load(input)
			input.close()
			self.Variables = obj.Variables
		except Exception as ex:
			print(ex)

	def save(self):
		output = open("RPCommandsData.obj", "wb")
		pickle.dump(self, output)
		output.close()
	
	def __init__(self):
		self.Variables = {}
		self.load()
	
	def Add(self, string, amount):
		print("RP add")
		if self.Variables.get(string) == None:
			self.Variables.update({string : amount})
		else:
			self.Variables[string] += amount
		return True, string + ": " + str(self.Variables[string])
	
	def Set(self, string, amount):
		print("RP set")
		if self.Variables.get(string) == None:
			self.Variables.update({string : amount})
		else:
			self.Variables[string] = amount
		return True, string + ": " + str(self.Variables[string])
	
	def VarInfo(self):
		print("RP varinfo")
		info = "\n"
		for key in self.Variables:
			if self.Variables[key] == 0:
				continue
			info += "\n"
			info += str(key) + ": " + str(self.Variables[key])
		return True, info
	
	def Shoot(self, times, damage, chance, target):
		print("RP shoot")
		totalDamage = 0
		for counter in range(0, times):
			if random.randint(0, 100) >= chance:
				try:
					self.Variables[target] -= damage
					totalDamage -= damage
				except Exception:
					pass
		return True, target + " " + str(totalDamage)
	
	def Case(self, karma):
		case = random.randint(-200, 200)
		case += karma
		if case >= 50:
			return True, "Good case"
		elif case >= -50 and case <= 50:
			return True, "Neutral case"
		elif case <= -50:
			return True, "Bad case"
	
	def handle(self, string, info):
		try:
			string = string.lower()
			self.save()
			
			if string.find("/case") > -1:
				parts = string.split(" ")
				itemName = ""
				index = 0
				for part in parts:
					if index > 0:
						itemName += part + " "
					index += 1
				return self.Case(self.Variables[itemName])
			
			if string.find("/reset") > -1:
				self.Variables = {}
				return True, "RP reset"
			
			if string.find("/add") > -1:
				parts = string.split(" ")
				itemName = ""
				index = 0
				for part in parts:
					if index > 1:
						itemName += part + " "
					index += 1
				return self.Add(itemName, int(parts[1]))
			
			if string.find("/set") > -1:
				parts = string.split(" ")
				itemName = ""
				index = 0
				for part in parts:
					if index > 1:
						itemName += part + " "
					index += 1
				return self.Set(itemName, int(parts[1]))
			
			if string.find("/varinfo") > -1:
				return self.VarInfo()
			
			if string.find("/shoot") > -1:
				parts = string.split(" ")
				itemName = ""
				index = 0
				for part in parts:
					if index > 3:
						itemName += part + " "
					index += 1
				return self.Shoot(int(parts[1]), int(parts[2]), int(parts[3]), itemName)
		except Exception as ex:
			PrintException()
			return False, ""