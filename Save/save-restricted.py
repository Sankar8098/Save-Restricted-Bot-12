# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/Save-Restricted-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/Save-Restricted-Bot

from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied, FloodWait, RPCError
from pyrogram import Client, filters
import os
import threading
import json

@Client.on_message(filters.text)
def save(client, message):
    try:
        if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
            if acc is None:
                app.send_message(message.chat.id, "**String Session is not Set**", reply_to_message_id=message.id)
                return

            try:
                acc.join_chat(message.text)
                app.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
            except UserAlreadyParticipant:
                app.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
            except InviteHashExpired:
                app.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)
            except Exception as e:
                app.send_message(message.chat.id, f"**Error**: __{e}__", reply_to_message_id=message.id)

        elif "https://t.me/" in message.text:
            datas = message.text.split("/")
            temp = datas[-1].replace("?single", "").split("-")
            fromID = int(temp[0].strip())
            try:
                toID = int(temp[1].strip())
            except:
                toID = fromID

            for msgid in range(fromID, toID + 1):
                if "https://t.me/c/" in message.text:
                    chatid = int("-100" + datas[4])
                    if acc is None:
                        app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                        return
                    handle_private(message, chatid, msgid)

                elif "https://t.me/b/" in message.text:
                    username = datas[4]
                    if acc is None:
                        app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                        return
                    try:
                        handle_private(message, username, msgid)
                    except Exception as e:
                        app.send_message(message.chat.id, f"**Error**: __{e}__", reply_to_message_id=message.id)

                else:
                    username = datas[3]
                    try:
                        msg = app.get_messages(username, msgid)
                    except UsernameNotOccupied:
                        app.send_message(message.chat.id, f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
                        return
                    except Exception as e:
                        app.send_message(message.chat.id, f"**Error**: __{e}__", reply_to_message_id=message.id)
                        return
                    try:
                        if '?single' not in message.text:
                            app.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                        else:
                            app.copy_media_group(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                    except Exception as e:
                        if acc is None:
                            app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                            return
                        try:
                            handle_private(message, username, msgid)
                        except Exception as e:
                            app.send_message(message.chat.id, f"**Error**: __{e}__", reply_to_message_id=message.id)
                    time.sleep(3)
    except Exception as e:
        app.send_message(message.chat.id, f"**Unexpected Error**: __{e}__", reply_to_message_id=message.id)


# handle private
def handle_private(message, chatid, msgid):
    msg = acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)

    if "Text" == msg_type:
        app.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = app.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    if "Document" == msg_type:
        try:
            thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None

        app.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif "Video" == msg_type:
        try:
            thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None

        app.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif "Animation" == msg_type:
        app.send_animation(message.chat.id, file, reply_to_message_id=message.id)

    elif "Sticker" == msg_type:
        app.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

    elif "Voice" == msg_type:
        app.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

    elif "Audio" == msg_type:
        try:
            thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None

        app.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif "Photo" == msg_type:
        app.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

    elif "Poll" == msg_type:
        app.send_poll(message.chat.id, question=msg.poll.question, options=[option.text for option in msg.poll.options], is_anonymous=msg.poll.is_anonymous, type=msg.poll.type, allows_multiple_answers=msg.poll.allows_multiple_answers, correct_option_id=msg.poll.correct_option_id, explanation=msg.poll.explanation, explanation_entities=msg.poll.explanation_entities, reply_to_message_id=message.id)

    elif "Location" == msg_type:
        app.send_location(message.chat.id, latitude=msg.location.latitude, longitude=msg.location.longitude, reply_to_message_id=message.id)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    app.delete_messages(message.chat.id, [smsg.id])

# get the type of message
def get_message_type(msg):
    try:
        msg.document.file_id
        return "Document"
    except AttributeError:
        pass

    try:
        msg.video.file_id
        return "Video"
    except AttributeError:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except AttributeError:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except AttributeError:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except AttributeError:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except AttributeError:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except AttributeError:
        pass

    try:
        msg.poll.id
        return "Poll"
    except AttributeError:
        pass

    try:
        msg.location.latitude
        return "Location"
    except AttributeError:
        pass

    try:
        msg.text
        return "Text"
    except AttributeError:
        pass





###################
# download status
def downstatus(statusfile, message):
    while not os.path.exists(statusfile):
        time.sleep(1)

    time.sleep(1)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            app.edit_message_text(message.chat.id, message.id, f"__Downloaded__: **{txt}**")
            time.sleep(5)
        except FloodWait as e:
            time.sleep(e.x)
        except RPCError:
            pass

# upload status
def upstatus(statusfile, message):
    while not os.path.exists(statusfile):
        time.sleep(1)

    time.sleep(1)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            app.edit_message_text(message.chat.id, message.id, f"__Uploaded__: **{txt}**")
            time.sleep(5)
        except FloodWait as e:
            time.sleep(e.x)
        except RPCError:
            pass

# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")





