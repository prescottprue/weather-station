import uvicorn
from fastapi import FastAPI
from db import readWeather

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

# TODO: Add auth header
@app.get("/measurements")
def read_item():
  return readWeather()

if __name__ == "__main__":
  uvicorn.run("main:app", port=8080, log_level="info")
