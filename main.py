# left off at https://fastapi.tiangolo.com/tutorial/query-params/#required-query-parameters
# resume lesson from there next time

from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ModelName(str, Enum):
   alexnet = "alexnet"
   resnet = "resnet"
   lenet = "lenet"

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
   if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "This is a valid model name!"}
   
   if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
   
   return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, short: bool = False):
  item = {"item_id": item_id}
  if q:
    item.update({"q": q})
  if not short:
    item.update(
       {"description": "This is an amazing item with a really long description!"}
    )
  return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# multiple path and query parameters TotalSpend	2025-11-19 09:59:19.013	4488.21	USD

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
   user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id" : item_id, "owner": user_id}
    if q:
       item.update({"q": q})
    if not short:
          item.update(
             {"description": "This is a really really long item description!"}
          )
    return item
      