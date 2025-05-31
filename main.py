from aiogram import Bot, Dispatcher, types, executor
import yt_dlp
import os

API_TOKEN = os.getenv("API_TOKEN")  # yoki bevosita token yozilgan bo‘lishi mumkin

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("👋 Salom! YouTube, TikTok yoki Instagram videoning linkini yuboring -- men uni yuklab beraman.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()

    # Bu yerda url'ni valid linkmi yo‘qmi tekshirish ham mumkin
    if not url.startswith("http"):
        await message.answer("❌ Bu linkga o‘xshamaydi. Iltimos, to‘g‘ri video manzilini yuboring.")
        return

    await message.answer("🔄 Yuklab olinmoqda, kuting...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        with open(video_file, 'rb') as video:
            await message.answer_video(video)

        os.remove(video_file)
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")
