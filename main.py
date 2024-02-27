from pyrogram import Client, filters as ay
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
import os, wget
from pyrogram.types import (
   InlineKeyboardMarkup,
   InlineKeyboardButton,
   InlineQuery,
   InlineQueryResultArticle,
   InputTextMessageContent,
)

api_id = '10356241'
api_hash = 'fbea11b5323c324387089425cda209b9'
token = '5146899202:AAHCp3RoH9sD0BPyT_haQQxh_aAfinHGF3Y'

app = Client("yt", bot_token=token, api_id=api_id, api_hash=api_hash)

Sudo_id = '1909129025'
@app.on_message(ay.command("start"))
async def start(client, message):
   await message.reply_text(
      "👋 Welcome!\nWith this bot, you can download videos and audios from YouTube in various formats and listen to them anytime. Just type 'search' followed by your query to get started.",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("❕ How to use the bot", url="https://t.me/MuzXMusicc"),
               InlineKeyboardButton("", url="https://t.me/MuzXMusicc"),
            ]
         ]
      )
   )
   await client.send_message(chat_id=Sudo_id,text=f"User: {message.from_user.mention()}\nPressed start in your bot\nID: `{message.from_user.id}`")

@app.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"🎬  : {message.text}", disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("🎧 Audio", callback_data="audio"),
               InlineKeyboardButton("🎬 Video", callback_data="video"),
            ]
         ]
      )
   )

@app.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("*🎚 Measuring download size*")
   try:
      url = callback_query.message.text.split(' : ', 1)[1]
      with YoutubeDL() as ytdl:
         await callback_query.edit_message_text("*♻️ Downloading...*")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("*🚀 Uploading to Telegram servers*")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text("Done sending video 🚧")
   os.remove(video_file)

@app.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("*🎚 Measuring download size*")
   try:
      url = callback_query.message.text.split(' : ', 1)[1]
      with YoutubeDL() as ytdl:
         await callback_query.edit_message_text("*♻️ Downloading...*")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("*🚀 Uploading to Telegram servers*")
   await client.send_audio(
      callback_query.message.chat.id,
      audio=audio_file,
      duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})"
   )
   await callback_query.edit_message_text("Done sending audio 🚧")
   os.remove(audio_file)
   os.remove(thumb)

@app.on_message(ay.command("search", None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("Please use the command like this: search + keyword")
            return

        m = await message.reply_text("Searching, please wait...")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"👤 {results[i]['title']}\n"
            text += f"🕑 {results[i]['duration']}\n"
            text += f"👁 {results[i]['views']}\n"
            text += f"🌐 {results[i]['channel']}\n"
            text += f"🔗 https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Safety and security⁞Bot ownership", url="https://t.me/MuzXMusicc")]]), disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))

@app.on_inline_query()
async def inline(client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="type a youtube video name...",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        results = YoutubeSearch(search_query).to_dict()
        for result in results:
            answers.append(
               InlineQueryResultArticle(
                  title=result["title"],
                  description="{}, {} views.".format(
                     result["duration"], result["views"]
                  ),
                  input_message_content=InputTextMessageContent(
                     "🔗 https://www.youtube.com/watch?v={}".format(result["id"])
                  ),
                  thumb_url=result["thumbnails"][0],
               )
            )
        
        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: search timed out",
                switch_pm_parameter="",
            )

print("The Bot Was Already Started")
app.run()
