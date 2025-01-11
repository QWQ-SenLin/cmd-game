import asyncio , time

async def say_after(delay):
    num = 0
    for i in range(100000 * delay):
        num += i
        await asyncio.sleep(0)
    print(num)

async def main():
    task1 = asyncio.create_task(say_after(2))
    task2 = asyncio.create_task(say_after(5))

    st = time.time()

    # 等待协程完成
    await task1
    await task2

    print(f"finished at {time.time() - st}")

# Python 3.7+
asyncio.run(main())