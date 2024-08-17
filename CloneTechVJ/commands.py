# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db
from CloneTechVJ.database.clone_bot_userdb import clonedb
from info import *
from shortzy import Shortzy
from utils import get_size, temp, get_seconds, get_clone_shortlink
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    me = await client.get_me()
    cd = await db.get_bot(me.id)
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
            InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{me.username}?startgroup=true')
        ]]
        if cd["update_channel_link"] != None:
            up = cd["update_channel_link"]
            buttons.append([InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=up)])
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.CLONE_START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, me.username, me.first_name), reply_markup=reply_markup)
        return 
    if not await clonedb.is_user_exist(me.id, message.from_user.id):
        await clonedb.add_user(me.id, message.from_user.id)
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{me.username}?startgroup=true')
        ],[
            InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about')
        ]]
        if cd["update_channel_link"] != None:
            up = cd["update_channel_link"]
            buttons.append([InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=up)])
        reply_markup = InlineKeyboardMarkup(buttons)
        m=await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_text(
            text=script.CLONE_START_TXT.format(message.from_user.mention, me.username, me.first_name),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.startswith("sendfiles"):
        chat_id = int("-" + file_id.split("-")[1])
        userid = message.from_user.id if message.from_user else None
        g = await get_clone_shortlink(f"https://telegram.me/{me.username}?start=allfiles_{file_id}", cd["url"], cd["api"])
        t = cd["tutorial"]
        btn = [[
            InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
        ],[
            InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=t)
        ]]
        k = await client.send_message(chat_id=message.from_user.id,text=f"<b>Get All Files in a Single Click!!!\n\n📂 ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 5 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(300)
        await k.edit("<b>Your message is successfully deleted!!!</b>")
        return
        
    
    elif data.startswith("short"):
        user = message.from_user.id
        files_ = await get_file_details(file_id)
        files = files_[0]
        g = await get_clone_shortlink(f"https://telegram.me/{me.username}?start=file_{file_id}", cd["url"], cd["api"]) 
        t = cd["tutorial"]
        btn = [[
            InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
        ],[
            InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=t)
        ]]
        k = await client.send_message(chat_id=user,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(1200)
        await k.edit("<b>Your message is successfully deleted!!!</b>")
        return
        
    elif data.startswith("all"):
        files = temp.GETALL.get(file_id)
        if not files:
            return await message.reply('<b><i>No such file exist.</b></i>')
        filesarr = []
        for file in files:
            vj_file_id = file.file_id
            k = await temp.BOT.send_cached_media(chat_id=PUBLIC_FILE_CHANNEL, file_id=vj_file_id)
            vj = await client.get_messages(PUBLIC_FILE_CHANNEL, k.id)
            mg = getattr(vj, vj.media.value)
            file_id = mg.file_id
            files_ = await get_file_details(vj_file_id)
            files1 = files_[0]
            title = '' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))
            size=get_size(files1.file_size)
            f_caption=files1.caption
            if f_caption is None:
                f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))}"
            if cd["update_channel_link"] != None:
                up = cd["update_channel_link"]
                button = [[
                    InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=up)
                ]]
                reply_markup=InlineKeyboardMarkup(button)
            else:
                reply_markup=None
       
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=False,
                reply_markup=reply_markup
            )
            filesarr.append(msg)
        k = await client.send_message(chat_id = message.from_user.id, text=f"𝗙𝗶𝗹𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗗𝗲𝗹𝗲𝘁𝗲𝗱 𝗶𝗻 𝟭𝟬 𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗕𝗲𝗰𝗮𝘂𝘀𝗲 𝗼𝗳 𝗰𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 𝗶𝘀𝘀𝘂𝗲..✍🏻\n\n𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲, 𝗞𝗶𝗻𝗱𝗹𝘆 𝗳𝗼𝗿𝘄𝗼𝗿𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲 𝘁𝗼 𝗮𝗻𝘆 𝗼𝘁𝗵𝗲𝗿 𝗰𝗵𝗮𝘁 𝗼𝗿 𝗶𝗻 𝘆𝗼𝘂𝗿 [𝘀𝗮𝘃𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀] 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲𝗿𝗲...")
        await asyncio.sleep(600)
        for x in filesarr:
            await x.delete()
        await k.edit_text("<b>Your All Files/Videos is successfully deleted!!!</b>")
        return    
    elif data.startswith("files"):
        if cd['url']:
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_clone_shortlink(f"https://telegram.me/{me.username}?start=file_{file_id}", cd["url"], cd["api"])
            t = cd["tutorial"]
            btn = [[
                InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
            ],[
                InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=t)
            ]]
            k = await client.send_message(chat_id=message.from_user.id,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(1200)
            await k.edit("<b>Your message is successfully deleted!!!</b>")
            return
    user = message.from_user.id
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            k = await temp.BOT.send_cached_media(chat_id=PUBLIC_FILE_CHANNEL, file_id=file_id)
            vj = await client.get_messages(PUBLIC_FILE_CHANNEL, k.id)
            mg = getattr(vj, vj.media.value)
            file_id = mg.file_id
            if cd["update_channel_link"] != None:
                up = cd["update_channel_link"]
                button = [[
                    InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=up)
                ]]
                reply_markup=InlineKeyboardMarkup(button)
            else:
                reply_markup=None
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                reply_markup=reply_markup
            )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = '' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            await msg.edit_caption(
                caption=f_caption,
                reply_markup=reply_markup
            )
            k = await msg.reply("𝗙𝗶𝗹𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗗𝗲𝗹𝗲𝘁𝗲𝗱 𝗶𝗻 𝟭𝟬 𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗕𝗲𝗰𝗮𝘂𝘀𝗲 𝗼𝗳 𝗰𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 𝗶𝘀𝘀𝘂𝗲..✍🏻\n\n𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲, 𝗞𝗶𝗻𝗱𝗹𝘆 𝗳𝗼𝗿𝘄𝗼𝗿𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲 𝘁𝗼 𝗮𝗻𝘆 𝗼𝘁𝗵𝗲𝗿 𝗰𝗵𝗮𝘁 𝗼𝗿 𝗶𝗻 𝘆𝗼𝘂𝗿 [𝘀𝗮𝘃𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀] 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲𝗿𝗲...",quote=True)
            await asyncio.sleep(600)
            await msg.delete()
            await k.edit_text("<b>Your File/Video is successfully deleted!!!</b>")
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = '' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))
    size=get_size(files.file_size)
    f_caption=files.caption
    if f_caption is None:
        f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))}"
    if cd["update_channel_link"] != None:
        up = cd["update_channel_link"]
        button = [[
            InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url=up)
        ]]
        reply_markup=InlineKeyboardMarkup(button)
    else:
        reply_markup=None
    k = await temp.BOT.send_cached_media(chat_id=PUBLIC_FILE_CHANNEL, file_id=file_id)
    vj = await client.get_messages(PUBLIC_FILE_CHANNEL, k.id)
    m = getattr(vj, vj.media.value)
    file_id = m.file_id
    msg = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        reply_markup=reply_markup
    )
    k = await msg.reply("𝗙𝗶𝗹𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗗𝗲𝗹𝗲𝘁𝗲𝗱 𝗶𝗻 𝟭𝟬 𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗕𝗲𝗰𝗮𝘂𝘀𝗲 𝗼𝗳 𝗰𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 𝗶𝘀𝘀𝘂𝗲..✍🏻.\n\n𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲, 𝗞𝗶𝗻𝗱𝗹𝘆 𝗳𝗼𝗿𝘄𝗼𝗿𝗱 𝘁𝗵𝗶𝘀 𝗳𝗶𝗹𝗲 𝘁𝗼 𝗮𝗻𝘆 𝗼𝘁𝗵𝗲𝗿 𝗰𝗵𝗮𝘁 𝗼𝗿 𝗶𝗻 𝘆𝗼𝘂𝗿 [𝘀𝗮𝘃𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀] 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲𝗿𝗲...",quote=True)
    await asyncio.sleep(600)
    await msg.delete()
    await k.edit_text("<b>Your File/Video is successfully deleted!!!</b>")
    return   
  
@Client.on_message(filters.command("settings") & filters.private)
async def settings(client, message):
    me = await client.get_me()
    owner = await db.get_bot(me.id)
    if owner["user_id"] != message.from_user.id:
        return
    url = await client.ask(message.chat.id, "<b>Now Send Me Your Shortlink Site Domain Or Url Without https://</b>")
    api = await client.ask(message.chat.id, "<b>Now Send Your Api</b>")
    try:
        shortzy = Shortzy(api_key=api.text, base_site=url.text)
        link = 'https://t.me/VJ_Botz'
        await shortzy.convert(link)
    except Exception as e:
        await message.reply(f"**Error In Converting Link**\n\n<code>{e}</code>\n\n**Start The Process Again By - /settings**", reply_markup=InlineKeyboardMarkup(btn))
        return
    tutorial = await client.ask(message.chat.id, "<b>Now Send Me Your How To Open Link means Tutorial Link.</b>")
    if not tutorial.text.startswith(('https://', 'http://')):
        await message.reply("**Invalid Link. Start The Process Again By - /settings**")
        return 
    link = await client.ask(message.chat.id, "<b>Now Send Me Your Update Channel Link Which Is Shown In Your Start Button And Below File Button.</b>")
    if not link.text.startswith(('https://', 'http://')):
        await message.reply("**Invalid Link. Start The Process Again By - /settings**")
        return 
    data = {
        'url': url.text,
        'api': api.text,
        'tutorial': tutorial.text,
        'update_channel_link': link.text
    }
    await db.update_bot(me.id, data)
    await message.reply("**Successfully Added All Settings**")

@Client.on_message(filters.command("reset") & filters.private)
async def reset_settings(client, message):
    me = await client.get_me()
    owner = await db.get_bot(me.id)
    if owner["user_id"] != message.from_user.id:
        return
    if owner["url"] == None:
        await message.reply("**No Settings Found.**")
    else:
        data = {
            'url': None,
            'api': None,
            'tutorial': None,
            'update_channel_link': None
        }
        await db.update_bot(me.id, data)
        await message.reply("**Successfully Reset All Settings To Default.**")

@Client.on_message(filters.command("stats") & filters.private)
async def stats(client, message):
    me = await client.get_me()
    total_users = await clonedb.total_users_count(me.id)
    total = await Media.count_documents()
    await message.reply(f"**Total Files : {total}\n\nTotal Users : {total_users}**")
