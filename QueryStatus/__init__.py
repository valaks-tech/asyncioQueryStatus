"""
Tool to query ~1000 hosts and parse the status respomse
Write the aggregated results to report
"""
import asyncio
import time
import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper as AsyncIOFile
from aiohttp import ClientSession
from config import BASE_DIR, HOSTS_COUNT, REPORT_FILEPATH, HTTP_HEADERS
from .async_tasks import create_tasks  # Creates one task per URL
from .async_fetch_parse import fetch_parse_report_data

async def init_myscript():
    """
    Prepare the report file and start task creation/execution
    """
    # By using aiofiles, we can write to same file from multiple
    # resources at the same time
    async with aiofiles.open(REPORT_FILEPATH, mode="w+") as outfile:
        # Core logic for the tool
        await run_queryStatus(outfile)
        await outfile.close()

async def run_queryStatus(outfile: AsyncIOFile):
    """
    Open async HTTP session & execute created tasks.

    :param AsyncIOFile outfile: Path of local file to write to.
    """
    async with ClientSession(headers=HTTP_HEADERS) as session:
        # (function) create_tasks: (session: ClientSession,
        # outfile: AsyncTextIOWrapper) -> Coroutine[Any, Any, List[Task]]
        task_list = await create_tasks(session, outfile)
        await asyncio.gather(*task_list)
