import asyncio
import re
import time

from telethon import Button, events
from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep

from . import *


@ultroid_cmd(
    pattern="wupload",
)
async def _(event):
    xx = await eor(event, "`Processing...`")
    vv = event.text.split(" ", maxsplit=1)
    try:
        file_name = vv[1]
    except IndexError:
        pass
    if event.reply_to_msg_id:
        bb = await event.get_reply_message()
        if bb.media:
            ccc = time.time()
            file_name = await event.client.download_media(
                bb,
                "./resources/downloads/",
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        xx,
                        ccc,
                        "Downloading...",
                    )
                ),
            )
        else:
            return await eod(xx, "`Reply to media file`", time=5)
    try:
        results = await ultroid_bot.inline_query(
            Var.BOT_USERNAME, f"fl2lnk {file_name}"
        )
    except rep:
        return await eor(
            xx,
            "`The bot did not respond to the inline query.\nConsider using {}restart`".format(
                HNDLR
            ),
        )
    except dis:
        return await eor(
            xx, "`Please turn on inline mode for your bot from` @Botfather."
        )
    await results[0].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
    await xx.delete()
    await event.delete()


@in_pattern("fl2lnk ?(.*)")
@in_owner
async def _(e):
    file_path = e.pattern_match.group(1)
    file_name = file_path.split("/")[-1]
    bitton = [
        [
            Button.inline("anonfiles", data=f"ful-anonfiles//{file_path}"),
            Button.inline("transfer", data=f"ful-transfer//{file_path}"),
        ],
        [
            Button.inline("bayfiles", data=f"ful-bayfiles//{file_path}"),
            Button.inline("x0", data=f"x0//{file_path}"),
        ],
        [
            Button.inline("file.io", data=f"ful-file.io//{file_path}"),
            Button.inline("siasky", data=f"ful-siasky//{file_path}"),
        ],
    ]
    try:
        lnk = e.builder.article(
            title="fl2lnk",
            text=f"**File:**\n{file_name}",
            buttons=bitton,
        )
    except:
        lnk = e.builder.article(
            title="fl2lnk",
            text="File not found",
        )
    await e.answer([lnk])


@callback(
    re.compile(
        "ful-(.*)",
    ),
)
@owner
async def _(e):
    t = (e.data).decode("UTF-8")
    data = t.split("-")[1]
    host = data.split("//")[0]
    file = data.split("//")[1]
    file_name = file.split("/")[-1]
    await e.edit(f"Uploading `{file_name}` on {host}")
    await dloader(e, host, file)
