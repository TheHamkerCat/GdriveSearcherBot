from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageNotModified
from config import BOT_TOKEN, RESULTS_COUNT, SUDO_CHATS_ID
from drive import drive
from requests import get as g

app = Client(":memory:", bot_token=BOT_TOKEN, api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

i = 0
ii = 0
m = None
keyboard = None
data = None


@app.on_message(filters.command("start") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def start_command(_, message):
    await message.reply_text("What did you expect to happen? Try /help")


@app.on_message(filters.command("help") & ~filters.edited)
async def help_command(_, message):
    await message.reply_text("/search [Query]")


@app.on_message(filters.command("search") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def search(_, message):
    global i, m, data
    try:
        query = message.text.split(' ',maxsplit=1)[1]
    except:
        await message.reply_text('/seach Filename')
        return
    m = await message.reply_text("**Searching....**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="Found Literally Nothing.")
        return

    text = f"**Total Results:** __{results}__\n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""
    if len(data) > RESULTS_COUNT:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="<<   Previous",
                        callback_data="previous"
                    ),
                    InlineKeyboardButton(
                        text="Next   >>",
                        callback_data="next"
                    )
                ]
            ]
        )
        try:
            await m.edit(text=text, reply_markup=keyboard)
        except (MessageEmpty, MessageNotModified):
            pass
        return
    try:
        await m.edit(text=text)
    except (MessageEmpty, MessageNotModified):
        pass


@app.on_callback_query(filters.regex("previous"))
async def previous_callbacc(_, CallbackQuery):
    global i, ii, m, data
    if i < RESULTS_COUNT:
        await CallbackQuery.answer(
            "Already at 1st page, Can't go back.",
            show_alert=True
        )
        return
    ii -= RESULTS_COUNT
    i -= RESULTS_COUNT
    text = ""

    for count in range(ii, i):
        try:
            if data[count]['type'] == "file":
                text += f"""
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<<   Previous",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="Next   >>",
                    callback_data="next"
                )
            ]
        ]
    )
    try:
        await m.edit(text=text, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass


@app.on_callback_query(filters.regex("next"))
async def next_callbacc(_, CallbackQuery):
    global i, ii, m, data
    ii = i
    i += RESULTS_COUNT
    text = ""

    for count in range(ii, i):
        try:
            if data[count]['type'] == "file":
                text += f"""
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
**[Drive Link]({data[count]['drive_url']})** | **[Index Link]({data[count]['url']})**\n"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<<   Previous",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="Next   >>",
                    callback_data="next"
                )
            ]
        ]
    )
    try:
        await m.edit(text=text, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass


app.run()
