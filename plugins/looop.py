
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import json
import math
import os
import shutil
import subprocess
import time
from types import SimpleNamespace

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


myData = NestedNamespace({"from_user": {"_": "User","id":680601089,},"message":{"message_id": 824449,"chat": {"id":-559454773,},"reply_to_message":{"message_id": 1915,"text": "https://bboxlinks.herokuapp.com/704/Rango.2009.720p.BRRip.x264.mp4","entities": [{"_": "MessageEntity","type": "mention","offset": 0,"length": 10},{"_": "MessageEntity","type": "url","offset": 11,"length": 66}]}},"data":"file=mp4=mp4"})

@pyrogram.Client.on_message(pyrogram.filters.command(["work","ignite"]))
async def button(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=update.message.message_id,
            revoke=True
        )
        return
    # logger.info(update)
    cb_data = myData.data
    await bot.send_message(chat_id=68060108,text="kigannye")
    if "|" in cb_data:
        #await youtube_dl_call_back(bot, update)
        await bot.send_message(chat_id=myData.message.chat.id, text='jsj', parse_mode="html" )
        await youtube_dl_call_back(bot,myData)
    elif "=" in cb_data:     
  	  s=await bot.send_message(chat_id=-559454773,text=bot)
  	  myData.message.message_id = s.message_id
  	  await youtube_dl_call_back(bot, myData)
