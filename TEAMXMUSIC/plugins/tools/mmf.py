import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pyrogram import filters
from pyrogram.types import Message
from TEAMXMUSIC import app

@app.on_message(filters.command("mmf"))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if len(message.text.split()) < 2:
        await message.reply_text("**Give me text after /mmf to memify.**")
        return

    msg = await message.reply_text("❄️")
    text = message.text.split(None, 1)[1]
    file = await app.download_media(reply_message)

    meme = await drawText(file, text)
    await app.send_document(chat_id, document=meme)

    await msg.delete()

    os.remove(meme)


async def drawText(image_path, text):
    # Open the image
    img = Image.open(image_path)

    # Check if the image is an animated webp
    if img.is_animated:
        # Handle animated sticker by processing each frame
        frames = []
        for frame in ImageSequence.Iterator(img):
            # Copy the frame so it doesn't modify the original
            frame_copy = frame.convert("RGBA")
            frame_copy = apply_text_to_frame(frame_copy, text)
            frames.append(frame_copy)

        # Save the frames back as an animated webp
        webp_file = "memify_animated.webp"
        frames[0].save(
            webp_file,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=img.info['duration'],
        )

    else:
        # Handle static image case
        webp_file = "memify_static.webp"
        img = img.convert("RGBA")
        img = apply_text_to_frame(img, text)
        img.save(webp_file, "webp")

    return webp_file


def apply_text_to_frame(frame, text):
    # Get the frame dimensions
    i_width, i_height = frame.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./TEAMXMUSIC/assets/default.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(frame)

    # Apply the text to the upper part
    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            uwl, uht, uwr, uhb = m_font.getbbox(u_text)
            u_width, u_height = uwr - uwl, uhb - uht

            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    # Apply the text to the lower part
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            uwl, uht, uwr, uhb = m_font.getbbox(l_text)
            u_width, u_height = uwr - uwl, uhb - uht

            draw.text(
                xy=(((i_width - u_width) / 2) - 2, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 2, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640) * i_width)) - 2),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640) * i_width)) + 2),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    return frame
