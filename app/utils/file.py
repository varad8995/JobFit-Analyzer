import os 
import aiofiles
import asyncio
from rq.job import Job

async def save_to_disc(file:bytes,path:str)-> bool:
    os.makedirs(os.path.dirname(path),exist_ok=True)
    async with aiofiles.open(path,"wb") as out_files:
        await out_files.write(file)

    return True    



async def wait_for_job(job: Job, interval: float = 0.5):
    """Async wait for an RQ job to finish"""
    while not job.is_finished:
        await asyncio.sleep(interval)
        job.refresh()
    return job.result
