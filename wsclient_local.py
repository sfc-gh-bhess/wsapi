import asyncio
import websockets
import json
import argparse

async def wsapi_local(url, data):
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        return response

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
parser.add_argument('--start_date', help='Starting of date range')
parser.add_argument('--end_date', help='Ending of date range')
parser.add_argument('--topn', help='Number of results to return')
args = vars(parser.parse_args())

url = args['url']
del args['url']

res = json.loads(asyncio.run(wsapi_local(url, args)))

if res['status'] == 'Error':
    print(f"ERROR: {res['message']}")
if res['status'] == 'Success':
    for x in res['data']:
        print(x)
