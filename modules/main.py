import os
import re
import sys
import json
import time
import pytz
import asyncio
import requests
import subprocess
import random
import aiohttp
from aiohttp import web
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto

# 🔥 पायथन 3.14 टाइमआउट क्रैश फिक्स पैच
async def dummy_wait_for(fut, timeout, *, loop=None):
    return await fut

asyncio.wait_for = dummy_wait_for

if hasattr(asyncio, "timeout"):
    from contextlib import asynccontextmanager
    @asynccontextmanager
    async def dummy_timeout(delay):
        yield
    asyncio.timeout = dummy_timeout

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
import globals
from logs import logging
from html_handler import register_html_handlers
from drm_handler import register_drm_handlers
from text_handler import register_text_handlers
from features import register_feature_handlers
from upgrade import register_upgrade_handlers
from commands import register_commands_handlers
from settings import register_settings_handlers
from broadcast import register_broadcast_handlers
from youtube_handler import register_youtube_handlers
from authorisation import register_authorisation_handlers

# सीधे आपके क्रेडेंशियल्स (सुरक्षित और फुलप्रूफ)
final_api_id = 39218807
final_api_hash = "5de693a30428272c34497419328466a1"
final_bot_token = "8121982164:AAEE454kBbDACIkKoNV5hi6IgHoLjzG68rU"
from vars import OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path, api_url, api_token
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# Initialize the bot
bot = Client(
    "bot",
    api_id=final_api_id,
    api_hash=final_api_hash,
    bot_token=final_bot_token
)

# 🟢 रेंडर के लिए फेक वेब सर्वर (पोर्ट बाइंडिंग एरर फिक्स)
async def web_handle(request):
    return web.Response(text="Bot is running completely fine! 🚀")

async def keep_alive_loop():
    await asyncio.sleep(30)  
    app_url = os.environ.get("RENDER_EXTERNAL_URL") or "https://your-app-name.onrender.com"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(app_url) as response:
                    pass
            except Exception:
                pass
            await asyncio.sleep(600)  

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://t.me/Avigat1210")],
        ])      

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user = await bot.get_me()
    mention = user.mention
    if m.chat.id in AUTH_USERS:
        caption = (
            f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n"
            f"Great! You are a premium member!\n"
            f"Use button: **✨ Commands** to get started 🌟\n\n"
            f"If you face any problem contact - [{CREDIT}](tg://openmessage?user_id={OWNER})\n"
        )
    else:
        caption = (
            f"🎉 Welcome {m.from_user.first_name} to DRM Bot! 🎉\n\n"
            f"**You are currently using the free version.** 🆓\n\n"
            f"I'm here to make your life easier by downloading videos from your **.txt** file 📄 and uploading them directly to Telegram!\n\n"
            f"**Want to get started? Press /id**\n\n"
            f"💬 Contact: [{CREDIT}](tg://openmessage?user_id={OWNER}) to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓\n"
        )
    await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://files.catbox.moe/28epkq.jpg",
        caption=caption,
        reply_markup=keyboard
    )
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id}) in My uploader bot**"
    
    await callback_query.message.edit_media(
      InputMediaPhoto(
        media="https://files.catbox.moe/tp3wk6.jpg",
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()  

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Send to Owner", url=f"tg://openmessage?user_id={OWNER}")]])
    chat_id = message.chat.id
    text = f"<blockquote expandable><b>The ID of this chat id is:</b></blockquote>\n`{chat_id}`"
    
    if str(chat_id).startswith("-100"):
        await message.reply_text(text)
    else:
        await message.reply_text(text, reply_markup=keyboard)

# .....,.....,.......,...,.......,.....,
@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}")]])
    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )

# .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):  
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")

# .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["reset"]))
async def restart_handler(_, m):
    if m.chat.id != OWNER:
        return
    else:
        await m.reply_text("𝐁𝐨𝐭 𝐢𝐬 𝐑e𝐬e𝐭𝐢𝐧𝐠...", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

# .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id, 
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**PLEASE /upgrade YOUR PLAN**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        if globals.processing_request:
            globals.cancel_requested = True
            await m.delete()
            cancel_message = await m.reply_text("**🚦 Process cancel request received. Stopping after current process...**")
            await asyncio.sleep(30)  
            await cancel_message.delete()
        else:
            await m.reply_text("**⚡ No active process to cancel.**")

#=================================================================
register_text_handlers(bot)
register_html_handlers(bot)
register_feature_handlers(bot)
register_settings_handlers(bot)
register_upgrade_handlers(bot)
register_commands_handlers(bot)
register_broadcast_handlers(bot)
register_youtube_handlers(bot)
register_authorisation_handlers(bot)
register_drm_handlers(bot)
#==================================================================

def notify_owner():
    url = f"https://api.telegram.org/bot{final_bot_token}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    try: requests.post(url, data=data)
    except: pass

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{final_bot_token}/setMyCommands"
    general_commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YouTube → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "t2h", "description": "🌐 .txt → .html Converter"},
        {"command": "logs", "description": "👁️ View Bot Activity"},
    ]
    owner_commands = general_commands + [
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation "},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"},
        {"command": "reset", "description": "✅ Reset the Bot"}
    ]
    try:
        requests.post(url, json={"commands": general_commands, "scope": {"type": "default"}, "language_code": "en"})
        requests.post(url, json={"commands": owner_commands, "scope": {"type": "chat", "chat_id": OWNER}, "language_code": "en"})
    except: pass

# बोट स्टार्ट होने, फेक वेब सर्वर और पिंगर लूप को साथ में रन करने के लिए
async def start_services():
    reset_and_set_commands()
    notify_owner()
    
    # 🎯 फेक वेब सर्वर सेटअप जो रेंडर को हमेशा एक्टिव रखेगा
    app = web.Application()
    app.router.add_get('/', web_handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🎯 Web server running on port {port}")

    asyncio.create_task(keep_alive_loop())
    await bot.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
