import xml.etree.ElementTree as ET
from typing import List, Tuple
import datetime as dt
import asyncio
import json
import time

import aiohttp

from utils import indices, xml_parser


TSE = "http://www.tsetmc.com"


async def get_res(session: aiohttp.ClientSession, url: str):
    async with session.get(url, ssl=False) as response:
        pokemon = await response.json()
        return pokemon["name"]


async def async_run_v0():
    tasks = []
    result = []
    async with aiohttp.ClientSession() as session:
        for number in range(1, 30):
            url = f"https://pokeapi.co/api/v2/pokemon/{number}"
            tasks.append(asyncio.ensure_future(get_res(session, url)))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            result.append(response)
            # print(response)
    return result


# ----------- [ Ensure Future ] -----------
async def get_response(session: aiohttp.ClientSession, stock_id: str) -> Tuple[int, bytes]:
    """
        Retrieve Response
    """
    url = f"{TSE}/tsev2/data/TradeDetail.aspx?i={stock_id}"
    async with session.get(url, ssl=False) as response:
        content = b""
        async for data in response.content.iter_chunked(768):
            content += data
        return stock_id, content


async def async_run_v1(stock_ids: List[int]) -> List[dict]:
    tasks = []
    result = []
    async with aiohttp.ClientSession() as session:
        # session.headers.update({"User-Agent": "Mozilla/5.0"})
        for stock_id in stock_ids:
            # url = f"{TSE}/tsev2/data/TradeDetail.aspx?i={stock_id}"
            tasks.append(
                asyncio.ensure_future(get_response(session, stock_id))
            )

        responses = await asyncio.gather(*tasks)
        for stock_id, content in responses:
            result.append(xml_parser(content, stock_id))
    return result


# ----------- [ Create Tasks ] -----------
def latest_trades_queue(session, stock_ids: List[int]) -> List[dict]:
    """
        Create Request Task Queue
    """
    tasks = []
    for stock_id in stock_ids:
        url = f"{TSE}/tsev2/data/TradeDetail.aspx?i={stock_id}"
        tasks.append(
            asyncio.create_task(session.get(url, ssl=False))
        )
    return tasks


async def async_run_v2(stock_ids: List[int]) -> List[dict]:
    """
        Get List of Latest Trades
    """
    result = []

    async with aiohttp.ClientSession() as session:
        # session.headers.update({"User-Agent": "Mozilla/5.0"})
        tasks = latest_trades_queue(session, stock_ids)

        responses = await asyncio.gather(*tasks)
        for response in responses:
            stock_id = str(response.url).split("=")[-1]
            # print(stock_id)

            content = b""
            async for data in response.content.iter_chunked(768):
                content += data
            # print(stock_id, len(content) // 1024)
            result.append(xml_parser(content, stock_id))
    return result


def test1(counter: int = 15) -> None:
    """
        docstring
    """
    for size in range(10, 51):
        print("-" * 11, size, "-" * 11)
        timez = 0
        _max, _min = 0, 0
        for _ in range(counter):
            start = time.time()
            _data = asyncio.run(async_run_v1(stock_indices[:size]))
            finish = time.time()
            takes = round(finish - start, 3)
            timez += takes
            print(takes, end=", ")
            if not _max and not _min:
                _max, _min = takes, takes
            elif takes > _max:
                _max = takes
            elif takes < _min:
                _min = takes
            time.sleep(0.2)
        # print(f"{size} Requests Takes {takes} Seconds")
        avg = round(timez / counter, 3)
        print(f"Average => {avg} | ({_min} - {_max})")
        time.sleep(3)


if __name__ == "__main__":
    stock_indices = indices()
    print(f"There Are {len(stock_indices)} Available Stocks")

    start = time.time()
    # _data = asyncio.run(async_run_v0())

    # _data = asyncio.run(async_run_v1(stock_indices[:25]))

    # _data = asyncio.run(async_run_v2(stock_indices[:25]))

    finish = time.time()
    takes = round(finish - start, 3)
    # print(takes)
    # print(_data)
    test1(20)
