import asyncio


async def start_strongman(name, power):
    print(f"The strongman {name} has begun the competition.")
    for i in range(1, 6):
        print(f"The strongman {name} has lifted up the ball # {i}.")
        await asyncio.sleep(1 / power)
    print(f"The strongman {name} has completed the competition.")


async def start_tournament():
    task_1 = asyncio.create_task(start_strongman('Pack', 0.3))
    task_2 = asyncio.create_task(start_strongman('Shack', 0.2))
    task_3 = asyncio.create_task(start_strongman('Crack', 0.5))
    await task_1
    await task_2
    await task_3


asyncio.run(start_tournament())
