
class EveryoneHandler:
	def Handle(string, info):
		if info.platform == "Telegram":
			update = info.telegramUpdate
			