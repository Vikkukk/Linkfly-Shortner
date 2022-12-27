#!/usr/bin/env python3
# Copyright (C) @ZauteKm
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
import os
import aiohttp 
from .admin import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener

KINKFLY_API = os.environ.get("LINKFLY_API", None)

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='🗣️ Join Updates Channel 📢', url='https://t.me/movierequestbackup1')
        ]]
    )

@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(update.from_user.id, link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = await short(update.id, link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(chat_id, link):
    shorten_urls = "**--Shorted URLs--**\n"
    
    # Linkfly shorten
    if LINKFLY_API and await db.allow_domain(chat_id, "linkfly.me"):
        try:
            api_url = "https://linkfly.me/member/tools/api"
            params = {'api': LINKFLY_API, 'url': link}
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params, raise_for_status=True) as response:
                    data = await response.json()
                    url = data["shortenedUrl"]
                    shorten_urls += f"\n**linkfly.me :-** {url}"
        except Exception as error:
            print(f"Linkfly error :- {error}")
    
   
    # Send the text
    try:
        shorten_urls += "\n\nMade with by ❤️ @victorlctt"
        return shorten_urls
    except Exception as error:
        return error
