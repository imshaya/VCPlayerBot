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
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "VCPlayerBot")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)


    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "False"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'True'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'True'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))
    PTN=is_enabled(os.environ.get("PTN", "False"))

    #Quality vars
    E_BITRATE=os.environ.get("BITRATE", False)
    E_FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "100")

    #Search filters for cplay
    FILTERS =  [filter.lower() for filter in (os.environ.get("FILTERS", "video document")).split(" ")]


    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]
    CONFIG_LIST = ["ADMINS", "IS_VIDEO", "IS_LOOP", "REPLY_PM", "ADMIN_ONLY", "SHUFFLE", "EDIT_TITLE", "CHAT", 
    "SUDO", "REPLY_MESSAGE", "STREAM_URL", "DELAY", "LOG_GROUP", "SCHEDULED_STREAM", "SCHEDULE_LIST", 
    "IS_VIDEO_RECORD", "IS_RECORDING", "WAS_RECORDING", "RECORDING_TITLE", "PORTRAIT", "RECORDING_DUMP", "HAS_SCHEDULE", 
    "CUSTOM_QUALITY"]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    CPLAY=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=100
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=True
        LOGGER.info("Reply Message Found, Enabled PM MSG")
    else:
        REPLY_MESSAGE=False
        REPLY_PM=False

    if E_BITRATE:
       try:
          BITRATE=int(E_BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          E_BITRATE=False
          BITRATE=48000
       if not BITRATE >= 48000:
          BITRATE=48000
    else:
       BITRATE=48000
    
    if E_FPS:
       try:
          FPS=int(E_FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          E_FPS=False
       if not FPS >= 30:
          FPS=30
    else:
       FPS=30
    try:
       CUSTOM_QUALITY=int(CUSTOM_QUALITY)
       if CUSTOM_QUALITY > 100:
          CUSTOM_QUALITY = 100
          LOGGER.warning("maximum quality allowed is 100, invalid quality specified. Quality set to 100")
       elif CUSTOM_QUALITY < 10:
          LOGGER.warning("Minimum Quality allowed is 10., Qulaity set to 10")
          CUSTOM_QUALITY = 10
       if  66.9  < CUSTOM_QUALITY < 100:
          if not E_BITRATE:
             BITRATE=48000
       elif 50 < CUSTOM_QUALITY < 66.9:
          if not E_BITRATE:
             BITRATE=36000
       else:
          if not E_BITRATE:
             BITRATE=24000
    except:
       if CUSTOM_QUALITY.lower() == 'high':
          CUSTOM_QUALITY=100
       elif CUSTOM_QUALITY.lower() == 'medium':
          CUSTOM_QUALITY=66.9
       elif CUSTOM_QUALITY.lower() == 'low':
          CUSTOM_QUALITY=50
       else:
          LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
          CUSTOM_QUALITY=100



    #help strings 
    PLAY_HELP="""
__با هرکودوم از این موارد میتونید پلی کنید__

1. پلی کردنه ویدیو از لینکه یوتوب
دستور: **/play**
__همین کار رو با ریپلای کردن روی لینکه یوتوب هم میتونید انجام بدید__

2. پلی کردن از فایله تلگرام
دستور: **/play**
__روی مدیای خودتون ریپلای کنید و دستور رو بنویسید.__
نکته: __در هر دو مورد میتونید با این دستور: /fplay همه ی پلی ها رو خودکار کنسل کرده و چیزی ک میخاید رو سریعن پخش کنید__

3. پلی کردنه پلی لیسته یوتوب
دستور: **/yplay**
__اول از همه از طریقه این ربات پلی لیسته مورد نظرتون رو تبدیل ب فایل کنید @GetPlaylistBot این ربات هم خوبه @DumpPlaylist و سپس ریپلای کنید روی فایله پلی لیست و دستور بدید__

4. لایو استریم
دستور: **/stream**
__هر لینکه مستقیمی یا لینکه پخش زنده ای رو با این دستور میتونید استریم کنید__

5. استفاده از پلی لیسته قدیمیه خودتون از همین ربات
دستور: **/import**
__ریپلای کنید روی فایل پلی لیستتون __

6. پلی از چنل
دستور: **/cplay**
__با استفاده از `/cplay عای عددی یا عدساینی چنل` میتونید تمام فایل های چنل موردنظرتون رو پلی کنید
بطور پیشفرض همه ی چیز های چنل رو پلی میکنه ولی شما میتونی از طریقه این دستور شخصی سازی کنید: /env FILTERS=audio, video, documents و همچین شمام میتونید از چنل مورد نظرتون بعنوان استارتاپ استریم هم استفاده کنید`
"""
    SETTINGS_HELP="""
**میتونی رباتتو با این دستورا ب راحتی شخصی سازی کنی**

🔹دستور: **/settings**

🔹موارده در دسترس:

**مود پلیر** -  __این بهت این امکان رو میده ک بصورت ۲۴ ساعته رباتت کار کنه یا فقط موقعی ک چیزی پلی میکنی__

**ویدیو فعال** -  __این بهت این امکان رو میده ک رباتو از حالته ویدیویی به موزیکی سوییچ کنی__

**فقط ادمین** - __با فعال کردنه این مورد کسی جز ادمینا نمیتونه ب ربات دستور بده__

**تغییر تایتل** - __با فعال کردنه این مورد، ربات اتوماتیک تایتل وویس چت رو عوض میکنه__

**مود دَرهم** - __با فعال کردنه این مورد، ربات پلی لیست رو دَرهم پخش میکنه __

**ریپلای اتوماتیک** - __با فعال کردنه این مورد، یوزر باتتون اتوماتیک جوابه پی ویاش رو میده__

"""
    SCHEDULER_HELP="""
__این ربات، امکان برنامه ریزی زمانبندی برای پخش خودکار هم داره __

دستور: **/schedule**

__چیزی ک میخاید برنامه ریزی شده پخش بشه رو از طریقه این دستور با ریپلای یا لینک اجرا کنید__

دستور: **/slist**
__این دستور، لیسته زمان بندی هایی ک از قبل کردید رو نشون میده__

دستور: **/cancel**
__با این دستور و نوشتن عای دیه برنامه ریزی جلوش، اون برنامه ریزی رو میتونید کنسل کنید__

دستور: **/cancelall**
__با این دستور همه ی برنامه ریزی هارو میتونید کنسل کنید__
"""
    RECORDER_HELP="""
__با این ربات شما میتونید هم ویدیو هم صدا رو ب مدت ۴ ساعت ضبط کنید__

دستور: **/record**

مقادیر در دسترس:
1. ضبط ویدیو: __اگ فعال باشه، هم ویدیو هم صدا ضبط میشن__

2. ابعاد ویدیو: __میتونید از این طریق ویدیو خودتون رو انتخاب کنید ک پرتره ضبط بشه یا افقی__

3. تایتل دستیه ضبط: __با این گزینه میتونید تایتل وویس چت رو برای ضبط دستی تغییر بدید__

4. چنل بخصوص برای ضبط: __از طریقه این قابلیت میتونید چنلی رو تنظیم کنید ک همه ی ضبط ها خودکار اونجا منتقل شن__

⚠️نکته: وقتی ضبطی با ربات شروع میکنید، باید با ربات هم تمومش کنید

"""

    CONTROL_HELP="""
__این ربات حتی کنترلی داره مثه کنترل تلویزیون__
1. رد کردن
دستور: **/skip**

2. استوپ کردن
دستور: **/pause**

3. از سرگرفتن
دستور: **/resume**

4. تغییر ولوم
دستور: **/volume**

5. خروج از وویس چت
دستور: **/leave**

6. دَرهم کردن پلی لیست
دستور: **/shuffle**

7. خالی کردنه پلی لیست
دستور: **/clearplaylist**

8. جلو زدن
دستور: **/seek**

9. سکوت کردن
دستور: **/vcmute**

10. لغو سکوت کردن
دستور : **/vcunmute**

11. نشان دادنه پلی لیست
دستور: **/playlist** 
__با استفاده از این دستور: /player اگه پلیر حذف شده باشه یا زیاد رفته باشه بالا، دوباره میتونید بیاریدش__
"""

    ADMIN_HELP="""
__این ربات حتی بهتون امکانه مدیریت ادمین ها رو هم میده__

دستور: **/vcpromote**
__میتونید یک ادمین ب ربات اضاقه کنید__

دستور: **/vcdemote**
__میتونید یک ادمین رباتو عزل کنید__

دستور: **/refresh**
__تطبیق ادمین های گپ با ربات__
"""

    MISC_HELP="""
دستور: **/export**
__تبدیل پلی لیست ب فایل__

دستور : **/logs**
__اگ مشکلی برای ربات پیش اومد با این دستور میتونی اخر اوضاع کدنویسیشو مشاهده کنی /logs__
 
دستور : **/env**
__با این دستور میتونی تنظیماته کدنویسیه ربات رو تغییر بدی__

دستور: **/config**
__همون کاراییه دستوره قبلیو داره /env**

دستور: **/update**
__عاپدیت کردنه ربات با اخرین تغییرات__

"""
    ENV_HELP="""
**تنظیمه کانفیگه کدنویسیه ربات**


**کانفیگ های سیستمی**

1. `API_ID` 

2. `API_HASH` 

3. `BOT_TOKEN`

4. `SESSION_STRING`

5. `CHAT`

6. `STARTUP_STREAM`

**کانفیگ های پیشنهاد شده**

1. `DATABASE_URI`

2. `HEROKU_API_KEY`

3. `HEROKU_APP_NAME`

4. `FILTERS`

**کانفیگ های اختیاری**

1. `LOG_GROUP`

2. `ADMINS`

3. `REPLY_MESSAGE`

4. `ADMIN_ONLY`

5. `DATABASE_NAME`

6. `SHUFFLE`

7. `EDIT_TITLE`

8. `RECORDING_DUMP`

9. `RECORDING_TITLE`

10. `TIME_ZONE`

11. `IS_VIDEO_RECORD`

12. `IS_LOOP`

13. `IS_VIDEO`

14. `PORTRAIT`

15. `DELAY`

16. `QUALITY`

17. `BITRATE`

18. `FPS`

"""
