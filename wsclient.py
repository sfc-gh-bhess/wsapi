import asyncio
import websockets
import json
import os
import argparse

def get_auth_headers():
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
    import snowflake.connector
    conn = snowflake.connector.connect(account=SNOWFLAKE_ACCOUNT, user=SNOWFLAKE_USER, password=SNOWFLAKE_PASSWORD, session_parameters={'PYTHON_CONNECTOR_QUERY_RESULT_FORMAT': 'json'})
    token_data = conn._rest._token_request('ISSUE')
    bearer_token = token_data["data"]["sessionToken"]
    token = f'"{bearer_token}"'
    headers = {"Authorization": f"Snowflake Token={token}"}
    return headers

async def wsapi(url, headers, data):
    async with websockets.connect(url, extra_headers=headers) as websocket:
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
headers = get_auth_headers()

res = json.loads(asyncio.run(wsapi(url, headers, args)))

if res['status'] == 'Error':
    print(f"ERROR: {res['message']}")
if res['status'] == 'Success':
    for x in res['data']:
        print(x)
