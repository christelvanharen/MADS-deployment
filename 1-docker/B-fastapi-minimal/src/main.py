from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{username}")
def read_user(username: str, q: Union[str, None] = None):
    return {"username": username, "q": q}


@app.get("/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)