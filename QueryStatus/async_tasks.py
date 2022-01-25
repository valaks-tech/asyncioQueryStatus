"""Prepare tasks to be executed."""
import asyncio
from asyncio import Task
from typing import List

from aiofiles.threadpool.text import AsyncTextIOWrapper as AsyncIOFile
from aiohttp import ClientSession
from .async_fetch_parse import fetch_parse_report_data
from config import HOSTS_COUNT, REPORT_FILEPATH, QUERY_URL

async def create_tasks(
    session: ClientSession, outfile: AsyncIOFile
) -> List[Task]:
    """
    Create asyncio tasks to parse HTTP request responses.

    : ClientSession session: Async HTTP requests session.
    : AsyncIOFile outfile: Path of local file to write to.

    :returns: List[Task]
    """
    task_list = []
    counter = 1
    for x in range(HOSTS_COUNT):
        task = asyncio.create_task(
            fetch_parse_report_data(session, QUERY_URL.format(x), outfile, HOSTS_COUNT, counter)
        )
        task_list.append(task)
        counter += 1
    return task_list