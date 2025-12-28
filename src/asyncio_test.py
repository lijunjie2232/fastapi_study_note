import asyncio
from loguru import logger


_LOOP = asyncio.get_event_loop()


async def my_function(id=0):
    logger.debug(f"id[{id}]: Hello from my_function")
    await asyncio.sleep(1)
    logger.debug(f"id[{id}]: Goodbye from my_function")
    return f"id:{id} is done"


async def main():

    # await my_function(2)

    # task = asyncio.create_task(my_function(3))  # python 3.7+

    # # await asyncio.sleep(2)

    # await task

    # task_list = [asyncio.create_task(my_function(i)) for i in range(4, 7)]
    # done, pedding = await asyncio.wait(task_list, timeout=10)
    # for task in done:
    #     logger.debug(task.result())

    # task_list = [asyncio.create_task(my_function(i)) for i in range(4, 7)]
    # results = await asyncio.gather(*task_list)
    # for result in results:
    #     logger.debug(result)

    loop = asyncio.get_running_loop()
    logger.debug(f"loop == _LOOP: {loop == _LOOP}")  # False

    fut = loop.create_future()
    fut.set_result("done")
    result = await fut
    logger.debug(result)

    import time

    fut = loop.run_in_executor(None, time.sleep, 1)
    logger.debug(f"fut: {fut}")
    result = await fut
    logger.debug(result)


if __name__ == "__main__":
    _LOOP.run_until_complete(my_function(1))
    asyncio.run(main())
