from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp
import os

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.reply("🔄 Yuklab olinmoqda, kuting...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video:
            await message.reply_video(video)
        os.remove(file_path)

    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
