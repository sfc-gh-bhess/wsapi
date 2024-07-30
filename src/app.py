from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import datetime
import snowflake.snowpark.functions as f
import spcs_helpers

session = spcs_helpers.session()
app = FastAPI()

dateformat = '%Y-%m-%d'
html = """
<html>
    <head>
        <title>Hello There</title>
    </head>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        args = await websocket.receive_json()
        response = None

        # Validate arguments
        sdt_str = args.get('start_range') or '1995-01-01'
        edt_str = args.get('end_range') or '1995-03-31'
        topn_str = args.get('topn') or '10'
        try:
            sdt = datetime.datetime.strptime(sdt_str, dateformat)
            edt = datetime.datetime.strptime(edt_str, dateformat)
            topn = int(topn_str)
        except:
            response = {"status": "Error", "message": "Invalid arguments."}

        # Query Snowflake
        try:
            df = session.table('snowflake_sample_data.tpch_sf10.orders') \
                    .filter(f.col('O_ORDERDATE') >= sdt) \
                    .filter(f.col('O_ORDERDATE') <= edt) \
                    .group_by(f.col('O_CLERK')) \
                    .agg(f.sum(f.col('O_TOTALPRICE')).as_('CLERK_TOTAL')) \
                    .order_by(f.col('CLERK_TOTAL').desc()) \
                    .limit(topn)
            response = {
                    "status": "Success",
                    "data": [x.as_dict() for x in df.to_local_iterator()]
                }
        except:
            response = {"status": "Error", "message": "Error reading from Snowflake. Check the logs for details."}

        await websocket.send_json(jsonable_encoder(response))
