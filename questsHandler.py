import random
import copy

class Quest:
	def __init__(self):
		self.Name = ""
		self.Description = ""
		self.Words = []
		self.Count = 0
		self.UserName = ""

class QuestsHandler:
    def __init__(self, commands):
        self.Users = {}
        self.Quests = []
        self.CommandsHandler = commands
		
        fuckYouQuest = Quest()
        fuckYouQuest.Count = 5
        fuckYouQuest.Name = "Быть посланным нахуй 5 раз"
        fuckYouQuest.Description = "Тебе кто-то должен сделать реплай со словами \"Иди нахуй\""
        fuckYouQuest.Words = ["иди нахуй", "пошёл нахуй", "ди нахуй", "пшёл нах", "ди нах", "нах иди", "нах иди", "на хуй иди", "нахуй иди", "нах иди"]
        
        sorryQuest = Quest()
        sorryQuest.Count = 5
        sorryQuest.Name = "Заставить кого-то извиниться 5 раз"
        sorryQuest.Description = "Тебе кто-то должен сделать реплай со словами \"извини\""
        sorryQuest.Words = ["извини", "извиня", "сорри", "сорян"]
        
        gitQuest = Quest()
        gitQuest.Count = 5
        gitQuest.Name = "Заставить кого-то поставить git 5 раз"
        gitQuest.Description = "Тебе кто-то должен сделать реплай со словами \"поставлю git\""
        gitQuest.Words = ["поставлю", "поставил", "ставлю"]
        
        hateQuest = Quest()
        hateQuest.Count = 5
        hateQuest.Name = "Заставить кого-то материться 5 раз"
        hateQuest.Description = "Тебе кто-то должен сделать реплай с матами"
        hateQuest.Words = ["блять", "нахуй", "хули", "хуй", "хуи", "педик", "пидор"]
        
        yesQuest = Quest()
        yesQuest.Count = 5
        yesQuest.Name = "Заставить кого-то согласиться 5 раз"
        yesQuest.Description = "Тебе кто-то должен сделать реплай со словом \"да\", \"согласен\", \"+\""
        yesQuest.Words = ["+", "согл", "да"]
        
        noQuest = Quest()
        noQuest.Count = 5
        noQuest.Name = "Заставить кого-то не согласиться 5 раз"
        noQuest.Description = "Тебе кто-то должен сделать реплай со словом \"не\", \"-\""
        noQuest.Words = ["-", "не"]
        
        imperatorQuest = Quest()
        imperatorQuest.Count = 5
        imperatorQuest.Name = "Заставить кого-то что-то говорить об императоре 5 раз"
        imperatorQuest.Description = "Тебе кто-то должен сделать реплай со словом \"император\""
        imperatorQuest.Words = ["император"]
	
        self.Quests = [fuckYouQuest, sorryQuest, gitQuest, hateQuest, yesQuest, noQuest, imperatorQuest]
	
    def currentQuest(self, user):
        if self.Users[user].Count > 0:
            return self.Users[user].Name + "\n\n(осталось " + str(self.Users[user].Count) + " раз, для деталей /questhelp)"
        else:
            return "У тебя нет задания, " + self.Users[user].UserName
	
    def questHelp(self, user):
        if self.Users[user].Count > 0:
            return self.Users[user].Description
        else:
            return "У тебя нет задания, " + self.Users[user].UserName
	
    def handle(self, string, info):
        string = string.lower()
        user = info.platform + str(info.userID)
		
        if self.Users.get(user) == None:
            self.Users.update({user : copy.deepcopy(self.Quests[random.randint(0, len(self.Quests) - 1)])})
            self.Users[user].UserName = info.userName
        
        if string.find("/changequest") > -1:
        	self.Users[user] = copy.deepcopy(self.Quests[random.randint(0, len(self.Quests) - 1)])
        	self.Users[user].UserName = info.userName
        	return True, "Квест поменяли"
		
        if string.find("/myquest") > -1:
            return True, self.currentQuest(user)
        
        if string.find("/thishumanquest") > -1:
        	return True, self.currentQuest(info.platform + str(info.userIDReply))
		
        if string.find("/questhelp") > -1 or string.find("/questhelp@dadaskisbot") > -1:
            return True, self.questHelp(user)
		
        if info.reply and info.userID != info.userIDReply:
            replyUser = info.platform + str(info.userIDReply)
            if self.Users.get(replyUser) == None:
            	return False, ""
            quest = self.Users[replyUser]
            if quest.Count > 0:
                for word in quest.Words:
                    if string.find(word.lower()) > -1:
                        quest.Count -= 1
                        if quest.Count <= 0:
                        	self.Users[replyUser] = copy.deepcopy(self.Quests[random.randint(0, len(self.Quests) - 1)])
                        	self.Users[replyUser].UserName = quest.UserName
                        	lvlUpHandler = self.CommandsHandler.Handlers[1]
                        	lvlUpHandler.levelUp(str(info.userIDReply) + info.platform, info.userNameReply)
                        	return True, quest.UserName + " выполнил задание, повышен уровень"
                        break
        return False, ""