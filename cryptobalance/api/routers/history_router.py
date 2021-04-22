from fastapi import APIRouter, Request
from typing import Optional

History_Router = APIRouter()

@History_Router.get("/total")
async def get_totals(request: Request, datapoints: int):
   """
   Endpoint that returns a list of portfolio (total) values for a specified number of datapoints in the past
   """
   history_handler = request.app.state.dependencies["history_handler"]
   result = await history_handler.get_historic_total(amount=datapoints)
   retlist = []
   for a in result:
      item = {
         'x': a['datetime_time'],
         'y': a['total']
      }
      retlist.append(item)
   return retlist

@History_Router.get("/invidivual")
async def get_invidivuals(request: Request, datapoints: int):
   """
   Endpoint that returns a list of values of assets in the portfolio for a specified number of datapoints in the past
   """
   history_handler = request.app.state.dependencies["history_handler"]
   result = await history_handler.get_historic_individual(amount=datapoints)
   return result