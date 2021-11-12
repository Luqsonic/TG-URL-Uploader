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

b = {
    "_": "Message",
    "message_id": 1915,
    "from_user": {
        "_": "User",
        "id":680601089
         ,
        "is_self": False,
        "is_contact": False,
        "is_mutual_contact": False,
        "is_deleted": False,
        "is_bot": False,
        "is_verified": False,
        "is_restricted": False,
        "is_scam": False,
        "is_fake": False,
        "is_support": False,
        "first_name": "ℓυqмαи",
        "last_name": "σffι¢ιαℓ",
        "status": "recently",
        "username": "L_u_Q_m_a_n",
        "language_code": "en",
        "dc_id": 4,
        "photo": {
            "_": "ChatPhoto",
            "small_file_id": "AQADBAAD46cxGwEmkSgACOt7yzBdAAMCAAMBJpEoAAR-FQqRPh8yvbrzAAIeBA",
            "small_photo_unique_id": "AQAD63vLMF0AA7rzAAI",
            "big_file_id": "AQADBAAD46cxGwEmkSgACOt7yzBdAAMDAAMBJpEoAAR-FQqRPh8yvbzzAAIeBA",
            "big_photo_unique_id": "AQAD63vLMF0AA7zzAAI"
        }
    },
    "date": "2021-11-07 00:35:04",
    "chat": {
        "_": "Chat",
        "id":-559454773
        ,
        "type": "group",
        "is_creator": False,
        "title": "Noxleech",
        "members_count": 4,
        "permissions": {
            "_": "ChatPermissions",
            "can_send_messages": True,
            "can_send_media_messages": True,
            "can_send_stickers": True,
            "can_send_animations": True,
            "can_send_games": True,
            "can_use_inline_bots": True,
            "can_add_web_page_previews": True,
            "can_send_polls": True,
            "can_change_info": True,
            "can_invite_users": True,
            "can_pin_messages": True
        }
    },
    "mentioned": True,
    "scheduled": False,
    "from_scheduled": False,
    "text": "@sobbi_bot\nhttps://bboxlinks.herokuapp.com/704/Rango.2009.720p.BRRip.x264.mp4",
    "entities": [
        {
            "_": "MessageEntity",
            "type": "mention",
            "offset": 0,
            "length": 10
        },
        {
            "_": "MessageEntity",
            "type": "url",
            "offset": 11,
            "length": 66
        }
    ],
    "outgoing": False,
    "matches": [
        "<re.Match object; span=(11, 77), match='https://bboxlinks.herokuapp.com/704/Rango.2009.72>"
    ]
}

@pyrogram.Client.on_callback_query()
async def button(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=update.message.message_id,
            revoke=True
        )
        return
    # logger.info(update)
    cb_data = update.data
    if ":" in cb_data:
        # unzip formats
        extract_dir_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(update.from_user.id) + "zipped" + "/"
        if not os.path.isdir(extract_dir_path):
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.message_id,
                revoke=True
            )
            return False
        zip_file_contents = os.listdir(extract_dir_path)
        type_of_extract, index_extractor, undefined_tcartxe = cb_data.split(":")
        if index_extractor == "NONE":
            try:
                shutil.rmtree(extract_dir_path)
            except:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.CANCEL_STR,
                message_id=update.message.message_id
            )
        elif index_extractor == "ALL":
            i = 0
            for file_content in zip_file_contents:
                current_file_name = os.path.join(extract_dir_path, file_content)
                start_time = time.time()
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=current_file_name,
                    # thumb=thumb_image_path,
                    caption=file_content,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time
                    )
                )
                i = i + 1
                os.remove(current_file_name)
            try:
                shutil.rmtree(extract_dir_path)
            except:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format(i, "0"),
                message_id=update.message.message_id
            )
        else:
            file_content = zip_file_contents[int(index_extractor)]
            current_file_name = os.path.join(extract_dir_path, file_content)
            start_time = time.time()
            await bot.send_document(
                chat_id=update.message.chat.id,
                document=current_file_name,
                # thumb=thumb_image_path,
                caption=file_content,
                # reply_markup=reply_markup,
                reply_to_message_id=update.message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time
                )
            )
            try:
                shutil.rmtree(extract_dir_path)
            except:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format("1", "0"),
                message_id=update.message.message_id
            )
    elif "|" in cb_data:
        #await youtube_dl_call_back(bot, update)
        await bot.send_message( chat_id=b.chat.id, text='jsj', parse_mode="html" )
        await youtube_dl_call_back(bot,update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
