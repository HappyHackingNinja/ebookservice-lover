# -*- coding: utf-8 -*-
"""This module provides utility functions.
"""
import aiohttp
import asyncio
import requests

CHUNK_SIZE = 1024


def simple_download_file(file_url: str, file_name: str):
    r = requests.get(file_url)
    with open(file_name, 'wb') as f:
        f.write(r.content)


async def download_file(
        file_url: str,
        semaphore: asyncio.Semaphore,
        session: aiohttp.ClientSession,
        path: str) -> bool:
    """Download content from URL and save it to target path

    :param file_url: URL of content.
    :param semaphore:
    :param session:
    :param path: Target path for saving file.
    :return: bool
    """
    with await semaphore:
        with open(path, 'wb') as file:
            async with session.get(file_url) as response:
                while True:
                    chunk = await response.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    file.write(chunk)
                    file.flush()
    return True
