from pyrogram import Client
from Save.config import Config



app = Client("mybot", bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH, plugins=dict(root="Save"))


if Config.STRING is not None:
    acc = Client("myacc", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING)
    acc.start()
else:
    acc = None



# Start the bot
print("🎊 I AM ALIVE 🎊")
app.run()
