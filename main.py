from telethon import events,TelegramClient
from telethon.utils import get_attributes
from dotenv import load_dotenv
from os import getenv,path
from utils import ocr_doc
from telethon.tl.types import InputMediaUploadedDocument
load_dotenv()


api_id=getenv("API_ID")
api_hash=getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")

bot = TelegramClient("question_extractor",api_id=api_id,api_hash=api_hash)
@bot.on(events.NewMessage)
async def newMessage(event):
    message = event.message
    if(event.message.reply_to):
        message = await event.message.get_reply_message()
    if(message.media and message.file.ext==".pdf"):
        reply = await event.message.reply("Downloading pdf...")
        if not path.isfile('./in/'+message.file.name):
            await bot.download_media(message,"./in/"+message.file.name)
        await reply.edit("Pdf is Downloaded, Now converting...")
        convertedFile =  ocr_doc.qExtractor(message.file.name)
        attr, mime_type = get_attributes(
                    convertedFile
                )
        await reply.edit("Successfully converted. Uploading... ")
        file = await bot.upload_file(convertedFile)
        sendDoc = InputMediaUploadedDocument(file=file,mime_type=mime_type,attributes=attr)
        await message.reply(file=sendDoc,message="OCR_"+file.name)
        await reply.delete()
    
bot.start(bot_token=bot_token)
bot.run_until_disconnected()