from chain import Chain
import time

chain = Chain()
try:
	#chain.openSerialized("ChainDefault.obj")
	#chain.open("quran.txt", 4)
	#chain.open("Marks Karl  _KAPITAL.txt", 10)
	#chain.open("n3690.txt", 10)
	#chain.open("Bible.txt", 1)
	#chain.open("C++.txt", 10)
	chain.open("custom.txt", 10)
	#chain.open("kodeks rf.txt", 5)
	#chain.open("warhammer.txt", 10)
	#chain.open("first stalker.txt", 1)
	#chain.open("metro 2035 embrion.txt", 1)
	#chain.open("rock stalker.txt", 1)
	#chain.open("stalker half life.txt", 1)
	#chain.open("stalker winner.txt", 1)
	chain.open("sex shit.txt", 10)
	#chain.open("Toxic.txt", 1)
	#chain.open("kamasutra.txt", 3)
	
	chain.open("ChainDefault.txt", 1)
except Exception as ex:
	print(ex)
	
class ChainCommandHandler:
    def __init__(self):
        self.Names = ["Дудк", "Дадаскис", "Дадасаки", "Dudk", "Dadaskis", "Dadasaki"]
        self.ChatCounter = {}
        self.ChatTimer = {}
    
    def handle(self, string, info):
        string = string.lower()
        
        for name in self.Names:
        	string = string.replace(name, "")
        
        chain.parse(string)
        
        chatName = info.platform + str(info.chatID)
        if self.ChatCounter.get(chatName) == None:
            self.ChatCounter.update({chatName : 0})
        self.ChatCounter[chatName] += 1
        if self.ChatTimer.get(chatName) == None:
            self.ChatTimer.update({chatName : 0})
        
        skipTimer = False
        
        if info.platform == "Telegram":
        	if (info.telegramBot.get_chat(info.telegramUpdate.message.chat_id).description or "").find("DudkaNonStop") == -1:
        		skipTimer = True
        
        if (self.ChatTimer[chatName] + 0.2 > time.process_time()) and not skipTimer:
            return False, ""
        
        if self.ChatCounter[chatName] > 50:
            self.ChatCounter[chatName] = 0
            self.ChatTimer[chatName] = time.process_time()
            return True, chain.getString(string)
        
        if info.botReply == True:
            self.ChatTimer[chatName] = time.process_time()
            return True, chain.getString(string)
        
        for name in self.Names:
            name = name.lower()
            if string.find(name) > -1:
                self.ChatTimer[chatName] = time.process_time()
                return True, chain.getString(string)
        return False, ""