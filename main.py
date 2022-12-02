import random as rnd
import asyncio
import time

from fastapi import FastAPI

from scraper import async_run_v1, indices


app = FastAPI(
    title="Scraper Runner",
    description="",
    redoc_url=None,
    docs_url="/ReDux"
)


@app.on_event("startup")
async def startup_event():
    """
        StartUp
    """
    # for index in range(1, 10):
    #     print(f"FastAPI #{str(index).zfill(2)}")
    #     await asyncio.sleep(20)
    print("Server Started....")

    stock_indices = indices()
    print(f"There Are {len(stock_indices)} Available Stocks")

    size = rnd.randint(20, 30)
    start = time.time()
    _data = await async_run_v1(stock_indices[:size])
    finish = time.time()
    takes = round(finish - start, 3)
    print(f"{size} Requests Takes {takes} Seconds!")


@app.on_event("shutdown")
async def startup_event2():
    """
        StartUp
    """
    for index in range(1, 10):
        print(f"FastAPI #{str(index).zfill(2)}")
        await asyncio.sleep(1)
    print("Server Started2....")


@app.get("/")
async def index():
    """
        docstring
    """
    return {}
