import asyncio , sys

async def async_print(str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: sys.stdout.write(str + '\n'))

# 计算任务
async def compute_task():
    await async_print("开始计算任务...")
    for i in range(4):
        await async_print(f"计算进度: {i + 1}/4")
    # await asyncio.sleep(2)  # 模拟耗时计算
    await async_print("计算任务完成！")
    return 42  # 返回计算结果

# 显示任务
async def display_task():
    await async_print("开始显示任务...")
    for i in range(10):
        await async_print(f"显示进度: {i + 1}/10")
        # await asyncio.sleep(0.5)  # 模拟显示任务的耗时
    await async_print("显示任务完成！")

# 主逻辑
async def main():
    # while True:  # 重复执行任务
    
    # 并发执行计算任务和显示任务
    display_future = asyncio.create_task(display_task())
    compute_future = asyncio.create_task(compute_task())
    
    # 等待两个任务完成
    await asyncio.gather(compute_future, display_future)
    
    # 获取计算结果
    result = compute_future.result()
    await async_print(f"计算结果: {result}")

# 运行主程序
if __name__ == "__main__":
    asyncio.run(main())