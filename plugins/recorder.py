#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from utils import LOGGER
from config import Config
from pyrogram import (
    Client, 
    filters
)
from utils import (
    chat_filter, 
    is_admin, 
    is_admin, 
    delete_messages, 
    recorder_settings,
    sync_to_db
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

admin_filter=filters.create(is_admin) 


@Client.on_message(filters.command(["record", f"record@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def record_vc(bot, message):
    await message.reply("تنظیمه تنظیماته ضبطه ربات از اینجاㅤㅤ ㅤ", reply_markup=(await recorder_settings()))
    await delete_messages([message])

@Client.on_message(filters.command(["rtitle", f"rtitle@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def recording_title(bot, message):
    m=await message.reply("چک کردن..")
    if " " in message.text:
        cmd, title = message.text.split(" ", 1)
    else:
        await m.edit("بهم با این دشتور تایتل جدید بده، /rtitle")
        await delete_messages([message, m])
        return

    if Config.DATABASE_URI:
        await m.edit("دیتابیس پیدا شد، درحاله تنظیمه تایتله ضبط") 
        if title == "False":
            await m.edit(f"با موفقیت تایتله دستی حذف شد")
            Config.RECORDING_TITLE=False
            await sync_to_db()
            await delete_messages([message, m])           
            return
        else:
            Config.RECORDING_TITLE=title
            await sync_to_db()
            await m.edit(f"با موفقیت تایتله ضبط تغییر پیدا کرد به {title}")
            await delete_messages([message, m])
            return
    else:
        if not Config.HEROKU_APP:
            buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('🗑 بستن', callback_data='close'),]]
            await m.edit(
                text="هیچ اپه هیروکویی پیدا نشد\n\n1. <code>HEROKU_API_KEY</code>: کلید ای پی عای اکانته هیروکو.\n2. <code>HEROKU_APP_NAME</code>: نام برنامه ی هیروکو", 
                reply_markup=InlineKeyboardMarkup(buttons)) 
            await delete_messages([message])
            return     
        config = Config.HEROKU_APP.config()
        if title == "False":
            if "RECORDING_TITLE" in config:
                await m.edit(f"با موفقیت تایتله ضبط حذف شد، درحاله ریست..")
                await delete_messages([message])
                del config["RECORDING_TITLE"]                
                config["RECORDING_TITLE"] = None
            else:
                await m.edit(f"درحاله حاظر تایتل تنظیمه رو پیشفرض، چیزی تغییر نکرد!")
                Config.RECORDING_TITLE=False
                await delete_messages([message, m])
        else:
            await m.edit(f"با موفقیت تاتیل تغییر پیدا کرد به {title}, درحاله ریست..")
            await delete_messages([message])
            config["RECORDING_TITLE"] = title
