import os
import random
import discord
import requests

import kaizen85modules

emojiDict = {"a": "🇦", "b": "🇧", "c": "🇨", "d": "🇩", "e": "🇪", "f": "🇫", "g": "🇬", "h": "🇭", "i": "🇮",
             "j": "🇯", "k": "🇰", "l": "🇱", "m": "🇲", "n": "🇳", "o": "🇴", "p": "🇵", "q": "🇶", "r": "🇷",
             "s": "🇸", "t": "🇹", "u": "🇺", "v": "🇻", "w": "🇼", "x": "🇽", "y": "🇾", "z": "🇿", "0": "0⃣",
             "1": "1⃣ ",
             "2": "2⃣ ", "3": "3⃣ ", "4": "4⃣ ", "5": "5⃣ ", "6": "6⃣ ", "7": "7⃣ ", "8": "8⃣ ", "9": "9⃣ ", "?": "❔",
             "!": "❕", " ": "    ", "-": "➖"}

gay_react_words = ["галя", "гей", "gay", "galya", "cleveron", "клеверон"]


class Module(kaizen85modules.ModuleHandler.Module):
    name = "FunStuff"
    desc = "Модуль, который добавляет бесполезные, но интересные вещи."
    
    async def run(self, bot: kaizen85modules.KaizenBot):
        if not os.path.isdir("./tts"):
            os.mkdir("./tts")
        
        class CommandTTE(bot.module_handler.Command):
            name = "tte"
            desc = "TextToEmoji - преобразовать буквы из текста в буквы-эмлдзи"
            args = "<text>"
            
            async def run(self, message: discord.Message, args, keys):
                if len(args) < 1:
                    return False
                
                string = ""
                for char in " ".join(args).strip().lower():
                    string += emojiDict[char] + " " if char in emojiDict else char + " "
                
                await message.channel.send(string)
                
                return True
        
        class CommandChoice(bot.module_handler.Command):
            name = "choice"
            desc = "Выбрать рандомный вариант из предоставленных"
            args = "<1, 2, 3...>"
            
            async def run(self, message: discord.Message, args, keys):
                choices = " ".join(message.clean_content.split()[1:]).split(", ")
                if len(choices) < 2:
                    return False
                
                await bot.send_info_embed(message.channel, "Я выбираю `\"%s\"`" % random.choice(choices))
                return True
        
        class CommandTTS(bot.module_handler.Command):
            name = "tts"
            desc = "Text To Speech"
            args = "<text>"
            
            async def run(self, message: discord.Message, args, keys):
                if len(args) < 1:
                    return False
                
                request = requests.get(
                    "http://tts.voicetech.yandex.net/tts?format=mp3&quality=hi&text=%s" % " ".join(args))
                
                if request.status_code != 200:
                    await bot.send_error_embed(message.channel, "Не удалось выполнить запрос.")
                    return True
                
                with open("./tts/%s.mp3" % message.id, "wb") as f:
                    f.write(request.content)
                
                with open("./tts/%s.mp3" % message.id, "rb") as f:
                    await message.channel.send("TTS (запросил: %s)" % message.author.mention,
                                         file=discord.File(f, filename="TTS.mp3"))
                
                return True
        
        bot.module_handler.add_command(CommandTTE(), self)
        bot.module_handler.add_command(CommandChoice(), self)
        bot.module_handler.add_command(CommandTTS(), self)
    
    async def on_message(self, message: discord.Message, bot):
        for word in gay_react_words:
            if word in message.content.lower():
                await message.add_reaction("🏳️‍🌈")
