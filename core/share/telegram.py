import telegram
import os


bot = telegram.Bot(token=os.environ.get("TG_BOT_TOKEN"))


async def send_message_on_telegram(content: str):
    try:
        _ = await bot.send_message(
            chat_id=os.environ.get("TG_CHANNEL_ID"),
            text=content,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
    except telegram.error.TelegramError:
        print("Failed to send message to Telegram")
