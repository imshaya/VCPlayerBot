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
from pyrogram import Client
from contextlib import suppress
from config import Config
from asyncio import sleep
import datetime
import pytz
import calendar
from utils import (
    cancel_all_schedules,
    delete_messages,
    get_admins, 
    get_buttons, 
    get_playlist_str,
    leave_call, 
    mute, 
    pause,
    recorder_settings, 
    restart, 
    restart_playout, 
    resume,
    schedule_a_play, 
    seek_file, 
    set_config, 
    settings_panel, 
    shuffle_playlist, 
    skip,
    start_record_stream,
    stop_recording,
    sync_to_db, 
    unmute,
    volume,
    volume_buttons
    )
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery
)
from pyrogram.errors import (
    MessageNotModified,
    MessageIdInvalid,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

IST = pytz.timezone(Config.TIME_ZONE)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    with suppress(MessageIdInvalid, MessageNotModified, QueryIdInvalid):
        admins = await get_admins(Config.CHAT)
        if query.data.startswith("info"):
            me, you = query.data.split("_")
            text="El-enLiL"
            if you == "volume":
                await query.answer()
                await query.message.edit_reply_markup(reply_markup=await volume_buttons())
                return
            if you == "player":
                if not Config.CALL_STATUS:
                    return await query.answer("چیزی پلی نیس", show_alert=True)
                await query.message.edit_reply_markup(reply_markup=await get_buttons())
                await query.answer()
                return
            if you == "video":
                text="تغییر وضعیت ربات ب ویدیو/موزیک پلیر"
            elif you == "shuffle":
                text="فعال یا غیر فعال کردن پخش در هم"
            elif you == "admin":
                text="فعال کردن استفاده از قابلیت ها محدود به ادمین"
            elif you == "mode":
                text="فعال کردن نان استاپ، باعث میشه ک ۲۴ ساعته پلیر ورودی هاتونو پلی کنه "
            elif you == "title":
                text="با فعال کردن این گزینه، عنوان وویس چت خودمار تبدیل ب عنوان فایلتون میشه"
            elif you == "reply":
                text="فعال کردن پیامی ک ربات یوزرتون درجوابه پی وی ها قراره بده رو انتخاب کنید "
            elif you == "videorecord":
                text = "فعال کردن ضبط همزمان فیلم و صدا، اگ این گزینه غیر فعال باشه، فق صدا ظبط میشه"
            elif you == "videodimension":
                text = "انتخاب ابعاد ویدیو"
            elif you == "rectitle":
                text = "عنوان دستی، برای ویدیو چت برای همیشه"
            elif you == "recdumb":
                text = "چنلی ک دوس دارید هرچی ضبط شد، بره توش"
            await query.answer(text=text, show_alert=True)
            return


        elif query.data.startswith("help"):
            if query.message.chat.type != "private" and query.message.reply_to_message.from_user is None:
                return await query.answer("از وقتی ادمین مخفی شدی، اینجا کاری نمیتونم برات بکنم، بصیک پی", show_alert=True)
            elif query.message.chat.type != "private" and query.from_user.id != query.message.reply_to_message.from_user.id:
                return await query.answer("Okda", show_alert=True)
            me, nyav = query.data.split("_")
            back=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Back", callback_data="help_main"),
                        InlineKeyboardButton("Close", callback_data="close"),
                    ],
                ]
                )
            if nyav == 'main':
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"Play", callback_data='help_play'),
                            InlineKeyboardButton(f"Settings", callback_data=f"help_settings"),
                            InlineKeyboardButton(f"Recording", callback_data='help_record'),
                        ],
                        [
                            InlineKeyboardButton("Scheduling", callback_data="help_schedule"),
                            InlineKeyboardButton("Controling", callback_data='help_control'),
                            InlineKeyboardButton("Admins", callback_data="help_admin"),
                        ],
                        [
                            InlineKeyboardButton(f"Misc", callback_data='help_misc'),
                            InlineKeyboardButton("Config Vars", callback_data='help_env'),
                            InlineKeyboardButton("Close", callback_data="close"),
                        ],
                    ]
                    )
                await query.message.edit("Showing help menu, Choose from the below options.", reply_markup=reply_markup, disable_web_page_preview=True)
            elif nyav == 'play':
                await query.message.edit(Config.PLAY_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'settings':
                await query.message.edit(Config.SETTINGS_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'schedule':
                await query.message.edit(Config.SCHEDULER_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'control':
                await query.message.edit(Config.CONTROL_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'admin':
                await query.message.edit(Config.ADMIN_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'misc':
                await query.message.edit(Config.MISC_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'record':
                await query.message.edit(Config.RECORDER_HELP, reply_markup=back, disable_web_page_preview=True)
            elif nyav == 'env':
                await query.message.edit(Config.ENV_HELP, reply_markup=back, disable_web_page_preview=True)
            return
            
        if not query.from_user.id in admins:
            await query.answer(
                "ببند😒",
                show_alert=True
                )
            return
        #scheduler stuffs
        if query.data.startswith("sch"):
            if query.message.chat.type != "private" and query.message.reply_to_message.from_user is None:
                return await query.answer("ع وقتی ادمین مخفی شدی، اینجا کاری نمیتونم برات بکنم، بصیک پی", show_alert=True)
            if query.message.chat.type != "private" and query.from_user.id != query.message.reply_to_message.from_user.id:
                return await query.answer("Okda", show_alert=True)
            data = query.data
            today = datetime.datetime.now(IST)
            smonth=today.strftime("%B")
            obj = calendar.Calendar()
            thisday = today.day
            year = today.year
            month = today.month
            if data.startswith("sch_month"):
                none, none , yea_r, month_, day = data.split("_")
                if yea_r == "choose":
                    year=int(year)
                    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    button=[]
                    button_=[]
                    k=0
                    for month in months:
                        k+=1
                        year_ = year
                        if k < int(today.month):
                            year_ += 1
                            button_.append([InlineKeyboardButton(text=f"{str(month)}  {str(year_)}",callback_data=f"sch_showdate_{year_}_{k}")])
                        else:
                            button.append([InlineKeyboardButton(text=f"{str(month)}  {str(year_)}",callback_data=f"sch_showdate_{year_}_{k}")])
                    button = button + button_
                    button.append([InlineKeyboardButton("Close", callback_data="schclose")])
                    await query.message.edit("ماه رو انتخاب کنㅤ ㅤㅤ", reply_markup=InlineKeyboardMarkup(button))
                elif day == "none":
                    return
                else:
                    year = int(yea_r)
                    month = int(month_)
                    date = int(day)
                    datetime_object = datetime.datetime.strptime(str(month), "%m")
                    smonth = datetime_object.strftime("%B")
                    button=[]
                    if year == today.year and month == today.month and date == today.day:
                        now = today.hour
                    else:
                        now=0
                    l = list()
                    for i in range(now, 24):
                        l.append(i)
                    splited=[l[i:i + 6] for i in range(0, len(l), 6)]
                    for i in splited:
                        k=[]
                        for d in i:
                            k.append(InlineKeyboardButton(text=f"{d}",callback_data=f"sch_day_{year}_{month}_{date}_{d}"))
                        button.append(k)
                    if month == today.month and date < today.day and year==today.year+1:
                        pyear=year-1
                    else:
                        pyear=year
                    button.append([InlineKeyboardButton("Back", callback_data=f"sch_showdate_{pyear}_{month}"), InlineKeyboardButton("Close", callback_data="schclose")])
                    await query.message.edit(f"حالا ساعته {date} {smonth} {year} برای زمانبندی وویس چت انتخاب کن", reply_markup=InlineKeyboardMarkup(button))

            elif data.startswith("sch_day"):
                none, none, year, month, day, hour = data.split("_")
                year = int(year)
                month = int(month)
                day = int(day)
                hour = int(hour)
                datetime_object = datetime.datetime.strptime(str(month), "%m")
                smonth = datetime_object.strftime("%B")
                if year == today.year and month == today.month and day == today.day and hour == today.hour:
                    now=today.minute
                else:
                    now=0
                button=[]
                l = list()
                for i in range(now, 60):
                    l.append(i)
                for i in range(0, len(l), 6):
                    chunk = l[i:i + 6]
                    k=[]
                    for d in chunk:
                        k.append(InlineKeyboardButton(text=f"{d}",callback_data=f"sch_minute_{year}_{month}_{day}_{hour}_{d}"))
                    button.append(k)
                button.append([InlineKeyboardButton("Back", callback_data=f"sch_month_{year}_{month}_{day}"), InlineKeyboardButton("Close", callback_data="schclose")])
                await query.message.edit(f"حالا دقایقه {hour}th ساعات {day} {smonth} {year} برای زمانبندی وویس چت انتخاب کن", reply_markup=InlineKeyboardMarkup(button))

            elif data.startswith("sch_minute"):
                none, none, year, month, day, hour, minute = data.split("_")
                year = int(year)
                month = int(month)
                day = int(day)
                hour = int(hour)
                minute = int(minute)
                datetime_object = datetime.datetime.strptime(str(month), "%m")
                smonth = datetime_object.strftime("%B")
                if year == today.year and month == today.month and day == today.day and hour == today.hour and minute <= today.minute:
                    await query.answer("ماشین زمان نیستم ک برا گذشته زمانبندی کنم!!!")
                    return 
                final=f"{day}th {smonth} {year} at {hour}:{minute}"
                button=[
                    [
                        InlineKeyboardButton("Confirm", callback_data=f"schconfirm_{year}-{month}-{day} {hour}:{minute}"),
                        InlineKeyboardButton("Back", callback_data=f"sch_day_{year}_{month}_{day}_{hour}")
                    ],
                    [
                        InlineKeyboardButton("Close", callback_data="schclose")
                    ]
                ]
                data=Config.SCHEDULED_STREAM.get(f"{query.message.chat.id}_{query.message.message_id}")
                if not data:
                    await query.answer("این زمانبندی منقضی شده", show_alert=True)
                if data['3'] == "telegram":
                    title=data['1']
                else:
                    title=f"[{data['1']}]({data['2']})"
                await query.message.edit(f"این استریمت {title} برنامه ریزی شد برای شروع ب وقته {final}\n\nرو تایید بزن ک تایید شه", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)                

            elif data.startswith("sch_showdate"):
                tyear=year
                none, none, year, month = data.split("_")
                datetime_object = datetime.datetime.strptime(month, "%m")
                thissmonth = datetime_object.strftime("%B")
                obj = calendar.Calendar()
                thisday = today.day
                year = int(year)
                month = int(month)
                m=obj.monthdayscalendar(year, month)
                button=[]
                button.append([InlineKeyboardButton(text=f"{str(thissmonth)}  {str(year)}",callback_data=f"sch_month_choose_none_none")])
                days=["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
                f=[]
                for day in days:
                    f.append(InlineKeyboardButton(text=f"{day}",callback_data=f"day_info_none"))
                button.append(f)
                for one in m:
                    f=[]
                    for d in one:
                        year_=year
                        if year==today.year and month == today.month and d < int(today.day):
                            year_ += 1
                        if d == 0:
                            k="\u2063"
                            d="none"
                        else:
                            k=d
                        f.append(InlineKeyboardButton(text=f"{k}",callback_data=f"sch_month_{year_}_{month}_{d}"))
                    button.append(f)
                button.append([InlineKeyboardButton("Close", callback_data="schclose")])
                await query.message.edit(f"روز رو انتخاب کن\nToday هستش {thisday} {smonth} {tyear}. انتخابه امروز یا همون تودی میشه امروز خلاصه دیگ... {year+1}", reply_markup=InlineKeyboardMarkup(button))

            elif data.startswith("schconfirm"):
                none, date = data.split("_")
                date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
                local_dt = IST.localize(date, is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc).replace(tzinfo=None)
                job_id=f"{query.message.chat.id}_{query.message.message_id}"
                Config.SCHEDULE_LIST.append({"job_id":job_id, "date":utc_dt})
                Config.SCHEDULE_LIST = sorted(Config.SCHEDULE_LIST, key=lambda k: k['date'])
                await schedule_a_play(job_id, utc_dt)
                await query.message.edit(f"زمانبندی استریم تو وویس چت با موفقیت تنظیم شد در <code> {date.strftime('%b %d %Y, %I:%M %p')} </code>")
                await delete_messages([query.message, query.message.reply_to_message])
                
            elif query.data == 'schcancelall':
                await cancel_all_schedules()
                await query.message.edit("همه استریم های زمانبندی شده با موفقیت حذف شدن")

            elif query.data == "schcancel":
                buttons = [
                    [
                        InlineKeyboardButton('ر، قطعن.!.', callback_data='schcancelall'),
                        InlineKeyboardButton('ن', callback_data='schclose'),
                    ]
                ]
                await query.message.edit("مطمئنی میخای کل استریم های زمانبندی شده رو لغو کنی؟", reply_markup=InlineKeyboardMarkup(buttons))
            elif data == "schclose":
                await query.answer("منو بسته شد")
                await query.message.delete()
                await query.message.reply_to_message.delete()

        elif query.data == "shuffle":
            if not Config.playlist:
                await query.answer("پلی لیست خالیه", show_alert=True)
                return
            await shuffle_playlist()
            await query.answer("پلی لیست در هم شد")
            await sleep(1)        
            await query.message.edit_reply_markup(reply_markup=await get_buttons())
    

        elif query.data.lower() == "pause":
            if Config.PAUSE:
                await query.answer("در حال حاظر استوپ هس", show_alert=True)
            else:
                await pause()
                await query.answer("استوپ شد")
                await sleep(1)

            await query.message.edit_reply_markup(reply_markup=await get_buttons())
 
        
        elif query.data.lower() == "resume":   
            if not Config.PAUSE:
                await query.answer("چیزی استوپ نبود ک از سر گرفته شه", show_alert=True)
            else:
                await resume()
                await query.answer("از سر گرفتن استریم")
                await sleep(1)
            await query.message.edit_reply_markup(reply_markup=await get_buttons())
          
        elif query.data=="skip": 
            if not Config.playlist:
                await query.answer("پلی لیست خالیه", show_alert=True)
            else:
                await query.answer("درحال حذف از پلی لیست")
                await skip()
                await sleep(1)
            if Config.playlist:
                title=f"<b>{Config.playlist[0][1]}</b>\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
            elif Config.STREAM_LINK:
                title=f"<b>استفاده از استریم [Url]({Config.DATA['FILE_DATA']['file']})</b>ㅤ  ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
            else:
                title=f"<b>استریم راه اندازی [stream]({Config.STREAM_URL})</b> ㅤ ㅤ  ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
            await query.message.edit(f"<b>{title}</b>",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )

        elif query.data=="replay":
            if not Config.playlist:
                await query.answer("پلی لیست خالیه", show_alert=True)
            else:
                await query.answer("درحال ریستارت کردن پلیر")
                await restart_playout()
                await sleep(1)
            await query.message.edit_reply_markup(reply_markup=await get_buttons())


        elif query.data.lower() == "mute":
            if Config.MUTED:
                await unmute()
                await query.answer("استریم عان میوت شد")
            else:
                await mute()
                await query.answer("استریم میوت شد")
            await sleep(1)
            await query.message.edit_reply_markup(reply_markup=await volume_buttons())

        elif query.data.lower() == 'seek':
            if not Config.CALL_STATUS:
                return await query.answer("چیزی پلی نیس", show_alert=True)
            #if not (Config.playlist or Config.STREAM_LINK):
                #return await query.answer("استریم راه اندازی رو نمیشه جلو زد", show_alert=True)
            await query.answer("درحال جلو زدن")
            data=Config.DATA.get('FILE_DATA')
            if not data.get('dur', 0) or \
                data.get('dur') == 0:
                return await query.answer("این یه استریم زندس، و نمیتونی جلو بزنیش", show_alert=True)
            k, reply = await seek_file(10)
            if k == False:
                return await query.answer(reply, show_alert=True)
            await query.message.edit_reply_markup(reply_markup=await get_buttons())

        elif query.data.lower() == 'rewind':
            if not Config.CALL_STATUS:
                return await query.answer("چیزی پلی نیس", show_alert=True)
            #if not (Config.playlist or Config.STREAM_LINK):
                #return await query.answer("استریم راه اندازی رو نمیشه جلو زد", show_alert=True)
            await query.answer("درحال عقب بردن")
            data=Config.DATA.get('FILE_DATA')
            if not data.get('dur', 0) or \
                data.get('dur') == 0:
                return await query.answer("این ی استریم زندس و نمیشه جلو زدش", show_alert=True)
            k, reply = await seek_file(-10)
            if k == False:
                return await query.answer(reply, show_alert=True)
            await query.message.edit_reply_markup(reply_markup=await get_buttons())

    
        elif query.data == 'restart':
            if not Config.CALL_STATUS:
                if not Config.playlist:
                    await query.answer("پلیر خالیه، شروعه STARTUP_STREAM.")
                else:
                    await query.answer('از سرگیریه پلی لیست')
            await query.answer("ریستارت کردن پلیر")
            await restart()
            await query.message.edit(text=await get_playlist_str(), reply_markup=await get_buttons(), disable_web_page_preview=True)

        elif query.data.startswith("volume"):
            me, you = query.data.split("_")  
            if you == "main":
                await query.message.edit_reply_markup(reply_markup=await volume_buttons())
            if you == "add":
                if 190 <= Config.VOLUME <=200:
                    vol=200 
                else:
                    vol=Config.VOLUME+10
                if not (1 <= vol <= 200):
                    return await query.answer("فق میتونی ع ۱ تا ۲۰۰ انتخاب کنی")
                await volume(vol)
                Config.VOLUME=vol
                await query.message.edit_reply_markup(reply_markup=await volume_buttons())
            elif you == "less":
                if 1 <= Config.VOLUME <=10:
                    vol=1
                else:
                    vol=Config.VOLUME-10
                if not (1 <= vol <= 200):
                    return await query.answer("فق میتونی ع ۱ تا ۲۰۰ انتخاب کنی")
                await volume(vol)
                Config.VOLUME=vol
                await query.message.edit_reply_markup(reply_markup=await volume_buttons())
            elif you == "back":
                await query.message.edit_reply_markup(reply_markup=await get_buttons())


        elif query.data in ["is_loop", "is_video", "admin_only", "edit_title", "set_shuffle", "reply_msg", "set_new_chat", "record", "record_video", "record_dim"]:
            if query.data == "is_loop":
                Config.IS_LOOP = set_config(Config.IS_LOOP)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
  
            elif query.data == "is_video":
                Config.IS_VIDEO = set_config(Config.IS_VIDEO)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
                data=Config.DATA.get('FILE_DATA')
                if not data \
                    or data.get('dur', 0) == 0:
                    await restart_playout()
                    return
                k, reply = await seek_file(0)
                if k == False:
                    await restart_playout()

            elif query.data == "admin_only":
                Config.ADMIN_ONLY = set_config(Config.ADMIN_ONLY)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
        
            elif query.data == "edit_title":
                Config.EDIT_TITLE = set_config(Config.EDIT_TITLE)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
        
            elif query.data == "set_shuffle":
                Config.SHUFFLE = set_config(Config.SHUFFLE)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
        
            elif query.data == "reply_msg":
                Config.REPLY_PM = set_config(Config.REPLY_PM)
                await query.message.edit_reply_markup(reply_markup=await settings_panel())
        
            elif query.data == "record_dim":
                if not Config.IS_VIDEO_RECORD:
                    return await query.answer("این برای ضبط صدا استفاده نمیشه")
                Config.PORTRAIT=set_config(Config.PORTRAIT)
                await query.message.edit_reply_markup(reply_markup=(await recorder_settings()))
            elif query.data == 'record_video':
                Config.IS_VIDEO_RECORD=set_config(Config.IS_VIDEO_RECORD)
                await query.message.edit_reply_markup(reply_markup=(await recorder_settings()))

            elif query.data == 'record':
                if Config.IS_RECORDING:
                    k, msg = await stop_recording()
                    if k == False:
                        await query.answer(msg, show_alert=True)
                    else:
                        await query.answer("ضبط استوپ شد")
                else:
                    k, msg = await start_record_stream()
                    if k == False:
                        await query.answer(msg, show_alert=True)
                    else:
                        await query.answer("ضبط شروع شد")
                await query.message.edit_reply_markup(reply_markup=(await recorder_settings()))

            elif query.data == "set_new_chat":
                if query.from_user is None:
                    return await query.answer("ع وقتی ادمین مخفی شدی، اینجا کاری ازم برنمیاد، بصیک پی", show_alert=True)
                if query.from_user.id in Config.SUDO:
                    await query.answer("تنظیمه گپه جدید")
                    chat=query.message.chat.id
                    if Config.IS_RECORDING:
                        await stop_recording()
                    await cancel_all_schedules()
                    await leave_call()
                    Config.CHAT=chat
                    Config.ADMIN_CACHE=False
                    await restart()
                    await query.message.edit("گپه جدید اعمال شد")
                    await sync_to_db()
                else:
                    await query.answer("این فقط توسط مدیر کل انجام میشه", show_alert=True)
            if not Config.DATABASE_URI:
                await query.answer("دیتابیس یافت نشد، ی دیتابیش اضافه کن وگرنه با هربار ری استارت شدن ربات، همه چیش تنظیمات کارخونه میشه")
        elif query.data.startswith("close"):
            if "sudo" in query.data:
                if query.from_user.id in Config.SUDO:
                    await query.message.delete()
                else:
                    await query.answer("فقط توسط مدیر کل امکان پذیره", show_alert=True)  
            else:
                if query.message.chat.type != "private" and query.message.reply_to_message:
                    if query.message.reply_to_message.from_user is None:
                        pass
                    elif query.from_user.id != query.message.reply_to_message.from_user.id:
                        return await query.answer("Okda", show_alert=True)
                elif query.from_user.id in Config.ADMINS:
                    pass
                else:
                    return await query.answer("Okda", show_alert=True)
                await query.answer("منو بسته شد")
                await query.message.delete()
        await query.answer()
