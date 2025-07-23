import sys, asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from utils.Playerxstream import playerxstream_updater
from utils.other import reset_directory
from utils.Client import app, start_clients, logger_bot
from utils.Queue import get_active_task, queue_handler, ACTIVE_USERS
from config import OWNER_ID
from utils.Logger import Logger, log_updater
from utils.CmdHandler import check_file, convert_playerx, remote_url_upload

logger = Logger(__name__)


@app.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client: Client, message: Message):
    await message.reply_text(
        """💠 <b>Enhance Your Streaming with Better TG Streamer Bot</b>

Transform MP4 and MKV files into smooth M3U8 HLS streams! Remote URL uploading is supported from various hosts, including FTP, Direct Links, Google Drive, OneDrive, and more. Enjoy unlimited file uploads and permanent file links.

👉 Click /help for quick commands.

🆘 Need help? Join our support group: <b>@BillaCore</b>

<b>Made with ❤️ by @BillaSpace</b>
""",
        parse_mode="html"
    )


@app.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(client: Client, message: Message):
    await message.reply_text(
        """🤖 <b>Streamer Bot Help & Commands</b>

Here are the commands you can use to unleash the full potential of Better TG Streamer Bot:

1. <b>/convert</b> – Convert Video To M3u8
   • Speed: Fast
   • Quality: Original
   • Features: Supports Multiple Audio Tracks

2. <b>/encode</b> – Encode Video To M3u8
   • Speed: Slow
   • Quality: Multiple Options
   • Features: Supports Audio + Subtitles (H.264/AAC)

3. <b>/remote</b> – Upload Remote File For Encoding
   • Supported Hosts: Google Drive, FTP, etc.

4. <b>/queue</b> – Check Queue Status

Enjoy seamless streaming with Better TG Streamer Bot!
""",
        parse_mode="html"
    )


@app.on_message(filters.command("convert") & filters.private & filters.incoming)
async def _convert(client: Client, message: Message):
    await convert_playerx(client, message)

    await message.reply_text(
        "<b>⪼ 𝐑𝐄𝐒𝐔𝐋𝐓</b>\n\n<code>ʏᴏᴜʀ ᴠɪᴅᴇᴏ ʜᴀꜱ ʙᴇᴇɴ ᴄᴏɴᴠᴇʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪɴᴛᴏ ᴍ𝟹ᴜ𝟾.</code>",
        parse_mode="html"
    )


@app.on_message(filters.command("encode") & filters.private & filters.incoming)
async def _encode(client: Client, message: Message):
    return await check_file(client, message, "encode")


@app.on_message(filters.command("remote") & filters.private & filters.incoming)
async def _remote(client: Client, message: Message):
    return await remote_url_upload(client, message)


@app.on_message(filters.command("queue") & filters.private & filters.incoming)
async def queue(client: Client, message: Message):
    global ACTIVE_USERS
    x = get_active_task()
    y = ACTIVE_USERS.count(message.from_user.id)

    text = (
        "<b>⪼ 𝐐𝐔𝐄𝐔𝐄 𝐒𝐓𝐀𝐓𝐔𝐒</b>\n\n"
        f"<code>🔵 ᴛᴏᴛᴀʟ ǫᴜᴇᴜᴇᴅ ᴛᴀꜱᴋꜱ: {len(ACTIVE_USERS) - x}\n"
        f"🟢 ᴀᴄᴛɪᴠᴇ ᴛᴀꜱᴋꜱ: {x}\n"
        f"👤 ʏᴏᴜʀ ᴛᴀꜱᴋꜱ: {y}</code>"
    )
    await message.reply_text(text, parse_mode="html")


# Owner Commands

@app.on_message(
    filters.command("restart")
    & filters.private
    & filters.incoming
    & filters.user(OWNER_ID)
)
async def restart(client: Client, message: Message):
    global ACTIVE_USERS
    for user_id in ACTIVE_USERS:
        try:
            await client.send_message(
                user_id,
                "<b>⪼ 𝐍𝐎𝐓𝐈𝐂𝐄</b>\n\n<code>♻️ ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛɪɴɢ ᴅᴜᴇ ᴛᴏ ᴀ ᴄᴏᴅᴇ ᴜᴘᴅᴀᴛᴇ. ꜱᴇɴᴅ /convert ᴀɢᴀɪɴ ᴛᴏ ꜱᴛᴀʀᴛ.</code>",
                parse_mode="html"
            )
        except Exception as e:
            print(e)

    await message.reply_text(
        f"<b>⪼ 𝐍𝐎𝐓𝐈𝐂𝐄</b>\n\n<code>♻️ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇɴᴛ ᴛᴏ {len(ACTIVE_USERS)} ᴜꜱᴇʀꜱ.</code>",
        parse_mode="html"
    )


@app.on_message(
    filters.command("logs")
    & filters.private
    & filters.incoming
    & filters.user(OWNER_ID)
)
async def logs(client: Client, message: Message):
    await message.reply_document("logs.txt")


async def main():
    logger.info("Cleaning File Cache")
    reset_directory()

    logger.info("Starting Queue Handler")
    asyncio.create_task(queue_handler())

    logger.info("Starting Log Updater")
    asyncio.create_task(log_updater(logger_bot))

    logger.info("Starting PlayerX Stream Updater")
    asyncio.create_task(playerxstream_updater())

    await start_clients()
    await idle()


loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)
    finally:
        loop.stop()
        print("Bot Stopped!")