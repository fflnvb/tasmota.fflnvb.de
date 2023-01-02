#!/usr/bin/python

import json
import aiohttp
import asyncio
import websockets
from datetime import datetime 

import modules.setup as setup
import modules.helpers as helpers

jsonOut = {}
devices = []

async def singleRequest(block):
    ip = setup.BASE_IP + '.' + str(block)
    url = 'http://' + ip + setup.REQUEST_URL
    async with aiohttp.ClientSession(timeout=setup.CLIENT_TIMEOUT) as session:
        try:
            url = 'http://' + ip + setup.REQUEST_URL
            async with session.get(url) as response:
                if response.status == 200 and helpers.isJson(await response.text()):
                    dictionary = await response.json()
                    devices.append(dictionary)
                    print('Found ' + dictionary['Status']['DeviceName'] + ' at ' + ip )
        except aiohttp.ClientConnectorError as e:
            pass
        except Exception as e:
            pass

async def performRequests():
    print('Starting scan')

    tasks = [singleRequest(i) for i in range(setup.RANGE_FROM, setup.RANGE_TO) ]
    await asyncio.gather(*tasks)

    print('Scan complete!')

async def webserver():
    async with websockets.serve(webRequest, "0.0.0.0", 8081):
        await asyncio.Future()  # run forever

async def webRequest(websocket):
    while True:
        message = await websocket.recv()
        if message == "getDevices":
            devices.clear()
            await performRequests()
            created = datetime.now()
            jsonOut['created'] = created.strftime("%Y-%m-%dT%H:%M:%SZ")
            jsonOut['devices'] = devices

            jsonString = json.dumps(jsonOut)
            await websocket.send(jsonString)

if __name__ == '__main__':
    asyncio.run(webserver())