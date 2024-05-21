# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/Save-Restricted-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/Save-Restricted-Bot


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Callback query handler
@Client.on_callback_query(filters.regex("cancel"))
async def cancel(client, callback_query):
    await callback_query.message.delete()

# start command
@Client.on_message(filters.command(["start"]))
def send_start(client, message):
    app.send_message(
        message.chat.id,
        f"👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot! 🤖\n\n"
        "I can help you retrieve and forward restricted content from Telegram posts.\n\n"
        "__For more details on usage, click the Help button below.__\n\n",
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('📍 Update Channel', url='https://t.me/NT_BOT_CHANNEL'),
                InlineKeyboardButton('👥 Support Group', url='https://t.me/NT_BOTS_SUPPORT'),
            ],
            [
                InlineKeyboardButton('👩‍💻 Developer', url='https://t.me/LISA_FAN_LK'),
                InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            ],
            [
                InlineKeyboardButton('⛔️ Close', callback_data='cancel')
            ]
        ]
    ))


# help command
@Client.on_message(filters.command(["help"]))
def send_help(client, message):
    app.send_message(
        message.chat.id,
        HELP_TEXT,
    )

# callback query handler for help button
@Client.on_callback_query(filters.regex("help"))
def show_help(client, callback_query):
    callback_query.message.edit_text(
        HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('⛔️ Close', callback_data='cancel')]
        ])
    )

HELP_TEXT = """
**HOW TO USE ME**

- Send private channel or group post link.
- Example: `https://t.me/123456789`

**SUPPORTED CONTENT TYPES**

- Text
- Photos
- Videos
- Documents
- Polls
- Locations
- Animations
- Stickers
- Voice Messages
- Audio Messages

©️ Channel : @NT_BOT_CHANNEL
"""


