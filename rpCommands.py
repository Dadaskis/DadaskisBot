import random
import pickle
import linecache
import sys
import ast

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
            self.Binds = obj.Binds
            self.BindsList = obj.BindsList
            self.UserScripts = obj.UserScripts
            self.ItemPacks = obj.ItemPacks
            self.ItemPackBinds = obj.ItemPackBinds
        except Exception as ex:
            print(ex)

    def save(self):
        output = open("RPCommandsData.obj", "wb")
        pickle.dump(self, output)
        output.close()
	
    def __init__(self):
        self.Variables = {}
        self.Binds = {}
        self.BindsList = {}
        self.UserScripts = {}
        self.ItemPacks = {}
        self.ItemPackBinds = {}
        self.load()
    
    def SetItemInItemPack(self, info, chance, name):
        bind = self.GetBindItemPack(info)
        if bind != None:
            if bind.get(name) == None:
                bind.update({name : 0})
            bind[name] = chance
            return "Set item. " + name + ": " + str(chance)
        return "Cant set item"
    
    def BindItemPack(self, info, name):
        target = info.platform + str(info.userID)
        if self.ItemPacks.get(target) == None:
            self.ItemPacks.update({target : {}})
        userPacks = self.ItemPacks[target]
        if userPacks.get(name) == None:
            userPacks.update({name : {}})
        self.ItemPackBinds[target] = name
        return "Bind item pack " + name

    def GetBindItemPack(self, info):
        target = info.platform + str(info.userID)
        if self.ItemPacks.get(target) != None:
            if self.ItemPackBinds.get(target) != None:
                return self.ItemPacks[target][self.ItemPackBinds[target]]

    def ItemPacksList(self, info):
        target = info.platform + str(info.userID)
        result = ""
        for key in list(self.ItemPacks.get(target).keys()):
            result += key + "\n"
        return result

    def GetItemsFromItemPack(self, info, count):
        bind = self.GetBindItemPack(info)
        if bind != None:
            result = ""
            items = []
            for counter in range(0, count):
                for counter1 in range(1, 100):
                    name, chance = random.choice(list(bind.items()))
                    if random.randint(0, 100) > chance:
                        #result += name + "\n"
                        items.append(name)
                        break
            items.sort()
            for item in items:
                result += item + "\n"
            return result

    def GetItemsFromItemPackFast(self, info, count, name):
        target = info.platform + str(info.userID)
        bind = self.ItemPacks.get(target)[name]
        if bind != None:
            result = ""
            items = []
            for counter in range(0, count):
                for counter1 in range(1, 100):
                    name, chance = random.choice(list(bind.items()))
                    if random.randint(0, 100) > chance:
                        #result += name + "\n"
                        items.append(name)
                        break
            items.sort()
            for item in items:
                result += item + "\n"
            return result

    def SetUserScript(self, info, name, script):
#        target = info.platform + str(info.userID)
#        if self.UserScripts.get(target) == None:
#            self.UserScripts.update({target : {}})
#        userTable = self.UserScripts[target]
#        if userTable.get(name) == None:
#            userTable.update({name : """"""})
#        userTable[name] = script
        return "Set user script " + name

    def RunUserScript(self, info, name, arguments, variables):
#        target = info.platform + str(info.userID)
#        if self.UserScripts.get(target) != None:
#            userTable = self.UserScripts[target]
#            if userTable.get(name) != None:
#                try:
#                    textResult = ast.literal_eval(userTable[name])
#                    return "Script result: \n" + str(textResult)
#                except Exception as ex:
#                    return "Script error:\n" + str(ex)
        return "Script error."
	
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

        if self.BindsList.get(target) == None:
            self.BindsList.update({target : []})
        if not (itemName in self.BindsList[target]):
            self.BindsList[target].append(itemName)

        self.Binds[target] = itemName
        return True, "Bind: " + itemName

	
    def handle(self, string, info):
        try:
            string = string.lower()
            self.save()
            
            if string.find("/itempackbind") > -1 or string.find("/ipbind") > -1:
                words = string.split(" ")
                name = ""
                for index in range(1, len(words)):
                    name += words[index] + " "
                return True, self.BindItemPack(info, name)

            if string.find("/itempacklist") > -1 or string.find("/iplist") > -1:
                bind = self.GetBindItemPack(info)
                result = ""
                for key in list(bind.keys()):
                    result += "\n" + key + ": " + str(bind[key])
                return True, result
            
            if string.find("/itempackslist") > -1 or string.find("/ipslist") > -1:
                return True, self.ItemPacksList(info)

            if string.find("/itempackset") > -1 or string.find("/ipset") > -1:
                words = string.split(" ")
                chance = int(words[1])
                name = ""
                for index in range(2, len(words)):
                    name += words[index] + " "
                return True, self.SetItemInItemPack(info, chance, name)
            
            if string.find("/itempackget") > -1 or string.find("/ipget") > -1:
                words = string.split(" ")
                count = int(words[1])
                return True, self.GetItemsFromItemPack(info, count)
            
            if string.find("/itempackfastget") > -1 or string.find("/ipfget") > -1:
                words = string.split(" ")
                count = int(words[1])
                name = ""
                for index in range(2, len(words)):
                    name += words[index] + " "
                return True, self.GetItemsFromItemPackFast(info, count, name)

            if string.find("/setscript") > -1:
                words = string.split(" ")
                name = words[1].split("\n")[0]
                script = """""" + words[1].split("\n")[1] + " "
                for index in range(2, len(words)):
                    script += words[index] + " "
                return True, self.SetUserScript(info, name, script)

            if string.find("/scriptlist") > -1:
                target = info.platform + str(info.userID)
                return True, str(self.UserScripts[target])

            if string.find("/getscript") > -1:
                words = string.split(" ")
                target = info.platform + str(info.userID)
                if self.UserScripts.get(target) != None:
                    return True, self.UserScripts[target][words[1]]

            if string.find("/runscript") > -1:
                words = string.split(" ")
                name = words[1]
                arguments = ""
                for index in range(2, len(words)):
                    arguments += words[index]
                return True, self.RunUserScript(info, name, arguments, self.GetBind(info))

            if string.find("/bindslist") > -1:
                target = info.platform + str(info.userID)
                result = "Binds list: "
                if self.BindsList.get(target) != None:
                    result += str(self.BindsList[target])
                return True, result

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
                variables = self.GetBind(info)
                return self.Case(variables[itemName])
			
            if string.find("/reset") > -1:
                target = info.platform + str(info.userID)
                target += self.Binds.get(target)
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
