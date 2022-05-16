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
    get_admins, 
    sync_to_db, 
    delete_messages,
    sudo_filter
)


@Client.on_message(filters.command(['vcpromote', f"vcpromote@{Config.BOT_USERNAME}"]) & sudo_filter)
async def add_admin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id is None:
            k = await message.reply("ت ی ادمین مخفی ای، نمیتونی این کارو کنی")
            await delete_messages([message, k])
            return
        user_id=message.reply_to_message.from_user.id
        user=message.reply_to_message.from_user

    elif ' ' in message.text:
        c, user = message.text.split(" ", 1)
        if user.startswith("@"):
            user=user.replace("@", "")
            try:
                user=await client.get_users(user)
            except Exception as e:
                k=await message.reply(f"من نمیتونم این یوزرو پیدا کنم.\nError: {e}")
                LOGGER.error(f"نمیشه یوزرو پیدا کرد - {e}", exc_info=True)
                await delete_messages([message, k])
                return
            user_id=user.id
        else:
            try:
                user_id=int(user)
                user=await client.get_users(user_id)
            except:
                k=await message.reply(f"یا باید عای دی عددیشو بدی، یا عای دی ادساینیش.")
                await delete_messages([message, k])
                return
    else:
        k=await message.reply("یوزری تعیین نشده، ریپلای کن روش با این دستور /vcpromote یا از ای دیش استفاده کن")
        await delete_messages([message, k])
        return
    if user_id in Config.ADMINS:
        k = await message.reply("ع قبل ادمینه") 
        await delete_messages([message, k])
        return
    Config.ADMINS.append(user_id)
    k=await message.reply(f"ارتقا پیدا کرد {user.mention} بعنوان ادمین وویس چت")
    await sync_to_db()
    await delete_messages([message, k])


@Client.on_message(filters.command(['vcdemote', f"vcdemote@{Config.BOT_USERNAME}"]) & sudo_filter)
async def remove_admin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id is None:
            k = await message.reply("ت ی ادمین مخفی ای، نمیتونی همچین گوهی بخوری")
            await delete_messages([message, k])
            return
        user_id=message.reply_to_message.from_user.id
        user=message.reply_to_message.from_user
    elif ' ' in message.text:
        c, user = message.text.split(" ", 1)
        if user.startswith("@"):
            user=user.replace("@", "")
            try:
                user=await client.get_users(user)
            except Exception as e:
                k = await message.reply(f"من نمیتونم این یزرو پیدا کنم.\nError: {e}")
                LOGGER.error(f"ناتوان در پیدا کردن یوزر, {e}", exc_info=True)
                await delete_messages([message, k])
                return
            user_id=user.id
        else:
            try:
                user_id=int(user)
                user=await client.get_users(user_id)
            except:
                k = await message.reply(f"یا باید بهم ای دی عددی بدی یا عای دی ادساینیش")
                await delete_messages([message, k])
                return
    else:
        k = await message.reply("هیچ یوزری تعیین نشده، ریپلای کن روش با این دستور /vcdemote یا عای دیشو بهم بده")
        await delete_messages([message, k])
        return
    if not user_id in Config.ADMINS:
        k = await message.reply("ع قبل ادمین نبود")
        await delete_messages([message, k])
        return
    Config.ADMINS.remove(user_id)
    k = await message.reply(f"عزل شد {user.mention}")
    await sync_to_db()
    await delete_messages([message, k])


@Client.on_message(filters.command(['refresh', f"refresh@{Config.BOT_USERNAME}"]) & filters.user(Config.SUDO))
async def refresh_admins(client, message):
    Config.ADMIN_CACHE=False
    await get_admins(Config.CHAT)
    k = await message.reply("لیست ادمین ها پیکربندی شد")
    await sync_to_db()
    await delete_messages([message, k])
