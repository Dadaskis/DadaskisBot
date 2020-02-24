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
        self.Binds = {}
        self.load()
	
    def Add(self, variables, string, amount):
        print("RP add")
        if variables.get(string) == None:
            variables.update({string : amount})
        else:
            variables[string] += amount
        return True, string + ": " + str(variables[string])
	
    def Set(self, variables, string, amount):
        print("RP set")
        if variables.get(string) == None:
            variables.update({string : amount})
        else:
            variables[string] = amount
        return True, string + ": " + str(variables[string])
	
    def VarInfo(self, variables):
        print("RP varinfo")
        info = "\n"
        for key in variables:
            if variables[key] == 0:
                continue
            info += "\n"
            info += str(key) + ": " + str(variables[key])
        return True, info
	
    def Shoot(self, variables, times, damage, chance, target):
        totalDamage = 0
        for counter in range(0, times):
            if random.randint(0, 100) >= chance:
                try:
                    variables[target] -= damage
                    totalDamage -= damage
                except Exception:
                    pass
        return True, target + " " + str(totalDamage)
	
    def Case(self, karma):
        case = random.randint(-200, 200)
        case += karma
        if case >= 50:
            return True, "Good case " + str(case)
        elif case >= -50 and case <= 50:
            return True, "Neutral case " + str(case)
        elif case <= -50:
            return True, "Bad case " + str(case)
        
    def GetVariables(self, info, itemName):
        target = info.platform + str(info.userID) + itemName
        if self.Variables.get(target) == None:
            self.Variables.update({target : {}})
        return self.Variables[target]
        
    def GetBind(self, info):
        target = info.platform + str(info.userID)
        if self.Binds.get(target) == None:
            self.Binds.update({target : ""})
        bind = self.Binds[target]
        return self.GetVariables(info, bind)

    def Bind(self, info, itemName):
        target = info.platform + str(info.userID)
        if self.Binds.get(target) == None:
            self.Binds.update({target : ""})
        self.Binds[target] = itemName
        return True, "Bind: " + itemName

	
    def handle(self, string, info):
        try:
            string = string.lower()
            self.save()
            if string.find("/bind") > -1:
                parts = string.split(" ")
                itemName = ""
                index = 0
                for part in parts:
                    if index > 0:
                        itemName += part + " "
                    index += 1
                return self.Bind(info, itemName)
			
            if string.find("/case") > -1:
                parts = string.split(" ")
                itemName = ""
                index = 0
                for part in parts:
                    if index > 0:
                        itemName += part + " "
                    index += 1
                variables = GetBind(info)
                return self.Case(variables[itemName])
			
            if string.find("/reset") > -1:
                target = str(info.userID) + info.platform
                target += self.Binds[target]
                self.Variables[target] = {}
                return True, "RP reset"
			
            if string.find("/add") > -1:
                parts = string.split(" ")
                itemName = ""
                index = 0
                for part in parts:
                    if index > 1:
                        itemName += part + " "
                    index += 1
                return self.Add(self.GetBind(info), itemName, int(parts[1]))
			
            if string.find("/set") > -1:
                parts = string.split(" ")
                itemName = ""
                index = 0
                for part in parts:
                    if index > 1:
                        itemName += part + " "
                    index += 1
                return self.Set(self.GetBind(info), itemName, int(parts[1]))
	    	
            if string.find("/varinfo") > -1:
                return self.VarInfo(self.GetBind(info))
			
            if string.find("/shoot") > -1:
                parts = string.split(" ")
                itemName = ""
                index = 0
                for part in parts:
                    if index > 3:
                        itemName += part + " "
                    index += 1
                return self.Shoot(self.GetBind(info), int(parts[1]), int(parts[2]), int(parts[3]), itemName)
        except Exception as ex:
            PrintException()
        return False, ""
