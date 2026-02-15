# DadaskisBot - A Markov Chain Chat Bot with RPG Elements

A multi-platform chat bot that learns from conversations and features RPG-style progression systems. Originally created for Telegram and Discord. This entire thing was programmed on a smartphone.

## Features

### **Markov Chain Learning**
- Learns from messages in channels where it's present
- Generates context-aware responses based on conversation history
- Multiple text corpora included for training (Warhammer, Stalker, Metro 2035, and more...)

### **Leveling System**
- Users gain XP by participating in conversations
- Level up system with progress tracking
- `/lvl` command to check your current level and progress

### **Quest System**
- Dynamic quests assigned to users
- Quests are completed when other users trigger specific responses
- Quest types include: making someone curse, apologize, agree/disagree, etc.
- Commands: `/myquest`, `/changequest`, `/questhelp`

### **RPG Command System**
Customizable RPG mechanics with persistent variables:
- `/bind [name]` - Bind to a variable set
- `/add [amount] [variable]` - Add to a variable
- `/set [amount] [variable]` - Set variable value
- `/varinfo` - View your variables
- `/case [variable]` - Random outcome based on variable
- `/shoot [times] [damage] [chance] [target]` - Combat simulation

### **Item Pack System**
Create and manage loot tables:
- `/ipbind [pack_name]` - Bind to an item pack
- `/ipset [chance] [item_name]` - Add items with drop chances
- `/ipget [count]` - Get random items from your current pack
- `/iplist` - List items in current pack

## Project Structure

```
DadaskisBot-master/
├── start.py                 # Main bot launcher (Telegram + Discord)
├── commandHandler.py        # Command routing system
├── chain.py                 # Markov chain core logic
├── chainCommandHandler.py   # Chat learning & response generation
├── lvlUpHandler.py          # Leveling system
├── questsHandler.py         # Quest system
├── rpCommands.py            # RPG command system
├── everyoneHandler.py       # (WIP) Everyone tag handler
├── tree.py                  # Directory tree utility
├── show_code.py             # Code analysis tool
└── *.txt                    # Training corpora (ChainDefault, custom, etc.)
```

## Training Corpora

The bot comes pre-loaded with various text files for training:
- `warhammer.txt` - Warhammer 40K lore
- `stalker half life.txt` - S.T.A.L.K.E.R. content
- `metro 2035 embrion.txt` - Metro 2035
- `sex shit.txt` - NSFW content <3
- `Toxic.txt` - Toxic phrase patterns
- `ChainDefault.txt` - Default training data

## Setup

1. Install dependencies:
```bash
pip install python-telegram-bot discord.py
```

2. Configure bot tokens in `start.py`:
   - Telegram: Update the token in `StartTelegram()` function
   - Discord: Update the token in `DStart()` function

3. Run the bot:
```bash
python start.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/lvl` | Check your level and XP progress |
| `/myquest` | View your current quest |
| `/changequest` | Get a new quest |
| `/questhelp` | See quest details |
| `/bind [name]` | Bind to an RPG variable set |
| `/add [amount] [var]` | Add to a variable |
| `/set [amount] [var]` | Set variable value |
| `/varinfo` | View all your variables |
| `/case [var]` | Random outcome based on karma |
| `/shoot [t] [dmg] [chance] [target]` | Simulate combat |
| `/ipbind [pack]` | Bind to item pack |
| `/ipset [chance] [item]` | Add item to pack |
| `/ipget [count]` | Get random items |
| `/iplist` | List items in pack |

## How It Works

The bot uses a simple Markov chain algorithm to learn from messages and generate responses. It builds probability tables of word sequences and can generate new text based on learned patterns.

The RPG systems use persistent storage (`*.obj` files) to maintain user progress, quest states, and custom variables across bot restarts.

## Notes

- The bot was originally created for personal use in Russian-language communities
- Some training data is in Russian/Cyrillic
- NSFW content can be disabled by removing/commenting out certain training files in `chainCommandHandler.py`, but why would you need this anyways?

## License

MIT License. Happiness to everyone!
