import uvicorn
from fastapi import FastAPI
from db import listMeasurements

app = FastAPI()

@app.get("/")
def read_root():
  return {"status": "healthy"}

# TODO: Add auth header
@app.get("/measurements")
def read_item():
  return listMeasurements()

if __name__ == "__main__":
  uvicorn.run("main:app", port=8080, host="0.0.0.0", log_level="info")
