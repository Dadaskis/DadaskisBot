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
	#chain.open("custom.txt", 100)
	#chain.open("kodeks rf.txt", 5)
	#chain.open("warhammer.txt", 1)
	#chain.open("first stalker.txt", 1)
	#chain.open("metro 2035 embrion.txt", 1)
	#chain.open("rock stalker.txt", 1)
	#chain.open("stalker half life.txt", 1)
	#chain.open("stalker winner.txt", 1)
	chain.open("sex shit.txt", 3)
	chain.open("Toxic.txt", 1)
	#chain.open("kamasutra.txt", 3)
	
	chain.open("ChainDefault.txt", 0.2)
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
        
        '''if (self.ChatTimer[chatName] + 0.2 > time.process_time()) and not skipTimer:
            return False, ""'''
        
        if info.platform == "Telegram":
            if self.ChatCounter[chatName] > 200:
                self.ChatCounter[chatName] = 0
                self.ChatTimer[chatName] = time.process_time()
                resultString = ""
                counter = 0
                while len(resultString.split(" ")) > 10 or len(resultString.split(" ")) < 50:
                    counter += 1
                    if counter > 100:
                        break
                    if len(resultString.split(" ")) > 10 and len(resultString.split(" ")) < 50:
                    	break
                    resultString = chain.getString(string)
                return True, resultString
        
        if info.botReply == True:
            #self.ChatTimer[chatName] = time.process_time()
            resultString = ""
            counter = 0
            while len(resultString.split(" ")) > 10 or len(resultString.split(" ")) < 50:
                counter += 1
                if counter > 100:
                    break
                if len(resultString.split(" ")) > 10 and len(resultString.split(" ")) < 50:
                	break
                resultString = chain.getString(string)
            return True, resultString
        
        for name in self.Names:
            name = name.lower()
            if string.find(name) > -1:
                #self.ChatTimer[chatName] = time.process_time()
                #return True, chain.getString(string)
            	resultString = ""
            	counter = 0
            	while len(resultString.split(" ")) > 10 or len(resultString.split(" ")) < 50:
                	counter += 1
                	if counter > 100:
                		break
                	if len(resultString.split(" ")) > 10 and len(resultString.split(" ")) < 50:
                		break
                	resultString = chain.getString(string)
            	return True, resultString
        return False, ""
