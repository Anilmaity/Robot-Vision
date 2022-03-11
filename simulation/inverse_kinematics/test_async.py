import asyncio
from multiprocessing.connection import wait
from time import sleep


async def move_robot(positions):
    print(positions)
    await asyncio.sleep(5)
    print('process completed')


async def process_vision_image(k):
    print('image processed')
    await asyncio.sleep(1)
    return k


async def start_object_detection():
    k = 0
    while(True):
        print('image processed')
        await asyncio.sleep(1)
        print(k)
        if k == 10:
            task1 = asyncio.create_task(move_robot('move'))
        k = k+2
    return 0


asyncio.run(start_object_detection())
