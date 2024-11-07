import os
import json
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE

from bot import LOGGER


async def change_metadata(file, dirpath, key):
    LOGGER.info(f"Starting metadata modification for file: {file}")
    temp_file = f"{file}.temp.mkv"
    full_file_path = os.path.join(dirpath, file)
    temp_file_path = os.path.join(dirpath, temp_file)

    cmd = [
        "ffprobe",
        "-i", full_file_path,
        "-preset", "veryfast",
        "-c:v", "libx265",
        "-crf", "30",
        "-map", "0:v",
        "-c:a", "aac",
        "-b:a", "98k",
        "-map", "0:a",
        "-c:s", "copy",
        "-map", "0:s",
        "-metadata", "title=𝙏𝙂: 𝘼𝙣𝙞𝙢𝙚 𝙊𝙧𝙗𝙞𝙩𝙨",
        "-metadata", "author=𝘼𝙣𝙞𝙢𝙚 𝙊𝙧𝙗𝙞𝙩𝙨",
        "-metadata:s:s", "title=𝘼𝙣𝙞𝙢𝙚 𝙊𝙧𝙗𝙞𝙩𝙨",
        "-metadata:s:a", "title=𝘼𝙣𝙞𝙢𝙚 𝙊𝙧𝙗𝙞𝙩𝙨",
        "-metadata:s:v", "title=𝘼𝙣𝙞𝙢𝙚 𝙊𝙧𝙗𝙞𝙩𝙨",
        "-vf", "scale=1280:720, drawtext=text='Anime Orbit':fontfile=sezz.otf:fontsize=20:fontcolor=white:x=10:y=h-th-10:enable='between(t, 1, 59)':alpha='if(between(t,1,59), 0.8, 0)'",
        temp_file_path
    ]
    process = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        LOGGER.error(f"Error getting stream info: {stderr.decode().strip()}")
        return file

    os.replace(temp_file_path, full_file_path)
    LOGGER.info(f"Metadata modified successfully for file: {file}")
    return file


async def add_attachment(file, dirpath, attachment_path):
    LOGGER.info(f"Adding photo attachment to file: {file}")

    temp_file = f"{file}.temp.mkv"
    full_file_path = os.path.join(dirpath, file)
    temp_file_path = os.path.join(dirpath, temp_file)

    attachment_ext = attachment_path.split(".")[-1].lower()
    if attachment_ext in ["jpg", "jpeg"]:
        mime_type = "image/jpeg"
    elif attachment_ext == "png":
        mime_type = "image/png"
    else:
        mime_type = "application/octet-stream"

    cmd = [
        "xtra",
        "-y",
        "-i",
        full_file_path,
        "-attach",
        attachment_path,
        "-metadata:s:t",
        f"mimetype={mime_type}",
        "-c",
        "copy",
        "-map",
        "0",
        temp_file_path,
    ]

    process = await create_subprocess_exec(*cmd, stderr=PIPE, stdout=PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        err = stderr.decode().strip()
        LOGGER.error(err)
        LOGGER.error(f"Error adding photo attachment to file: {file}")
        return file

    os.replace(temp_file_path, full_file_path)
    LOGGER.info(f"Photo attachment added successfully to file: {file}")
    return file
