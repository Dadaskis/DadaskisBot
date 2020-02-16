from chainCommandHandler import ChainCommandHandler
from lvlUpHandler import LvlUpHandler
from questsHandler import QuestsHandler
from rpCommands import RPCommands

class ChatUserInfo:
	def __init__(self):
		self.chatName = ""
		self.chatID = 0
		self.userName = ""
		self.userID = 0
		self.platform = ""
		self.reply = False
		self.botReply = False
		self.userIDReply = 0
		self.userNameReply = ""
		self.telegramUpdate = None
		self.telegramBot = None

class CommandHandler:
	def __init__(self):
		self.Handlers = [ChainCommandHandler(), LvlUpHandler(), QuestsHandler(self), RPCommands()]
	
	def handle(self, stringMessage, info):
		for handler in self.Handlers:
			try:
				skip, string = handler.handle(stringMessage, info)
				if skip == True:
					if len(string) == 0:
						string = " "
					return string
			except Exception as ex:
				print(ex)
		return " "