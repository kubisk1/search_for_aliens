import asyncio

async def stop_probes():
    global probe_tasks
    for task in probe_tasks:
        task.cancel()
    await asyncio.gather(*probe_tasks, return_exceptions=True)
    probe_tasks = []
