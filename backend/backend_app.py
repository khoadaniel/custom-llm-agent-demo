from fastapi import FastAPI
import uvicorn
from pydantic_models import ListItems, PaymentMethod


app = FastAPI()


@app.post("/add")
async def add(request_json: ListItems):
    try:
        # Turn request_json into a Python dict
        request_json = request_json.dict()
        print("====> request_json:\n", request_json, "\n")

    except Exception as e:
        print(e)


@app.post("/remove")
async def add(request_json: ListItems):
    try:
        # Turn request_json into a Python dict
        request_json = request_json.dict()
        print("====> request_json:\n", request_json, "\n")

    except Exception as e:
        print(e)


@app.post("/pay")
async def add(request_json: PaymentMethod):
    try:
        # Turn request_json into a Python dict
        request_json = request_json.dict()
        print("====> request_json:\n", request_json, "\n")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run("backend_app:app", host="0.0.0.0", port=8881, reload=True)
