import pickle
import time

class LvlUpHandler:
    def __init__(self):
        self.UsersMessages = {}
        self.UsersLevels = {}
        self.UsersTimers = {}
        try:
            self.load()
        except Exception as ex:
            print(ex)
    
    def load(self):
        input = open('LvlUpHandlerData.obj', 'rb')
        obj = pickle.load(input)
        input.close()
        self.UsersMessages = obj.UsersMessages
        self.UsersLevels = obj.UsersLevels
        self.MessageCount = 20
    
    def save(self):
        output = open("LvlUpHandlerData.obj", "wb")
        pickle.dump(self, output)
        output.close()
     
    def levelUp(self, user, name):
        self.UsersLevels[user] += 1
        self.UsersMessages[user] = 0
        return name + " lvl up! (" + str(self.UsersLevels[user]) + " lvl)"
    
    def handle(self, string, info):
        user = str(info.userID) + info.platform
        
        if self.UsersMessages.get(user) == None:
            self.UsersMessages.update({user : 0})
        
        if self.UsersLevels.get(user) == None:
            self.UsersLevels.update({user : 1})
            
        if string.lower().find("/lvl") > -1:
            expMessage = info.userName + " " + str(self.UsersLevels[user]) + " lvl.\n"
            progress = self.UsersMessages[user] / (self.MessageCount * self.UsersLevels[user])
            progress *= 100
            progress = round(progress)
            expMessage += "Progress: " + str(progress) + "%"
            return True, expMessage
        
        if self.UsersTimers.get(user) == None:
            self.UsersTimers.update({user : -1000})
        
        #print(self.UsersTimers[user], time.process_time())
        if (self.UsersTimers[user] + 1.0) < time.process_time():     
	        self.UsersMessages[user] += 1
	        self.UsersTimers[user] = time.process_time()
	        
	        if self.UsersMessages[user] > self.MessageCount * self.UsersLevels[user]:
	            return True, self.levelUp(user, info.userName)
        self.save()
        
        return False, ""