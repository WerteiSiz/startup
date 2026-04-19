import aiohttp
from fastapi import HTTPException

async def send_notification(data):
    notify_url = 'http://127.0.0.1:8001/notify'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(notify_url, json=data, headers={"Content-Type": "application/json"}) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else: 
                    raise HTTPException(status_code=400, detail=f"Bad request: {resp.json()}")
        
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
    






