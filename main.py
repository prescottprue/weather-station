from dotenv import load_dotenv
load_dotenv()
import uvicorn
import os
from fastapi import FastAPI
from db import listMeasurements,getLatestMeasurement

app = FastAPI()

@app.get("/")
def read_root():
  return {"status": "active", "version": os.environ.get('VERSION') or "0.0.0" }

@app.get("/measurements")
def read_item():
  return listMeasurements()

@app.get("/latest")
def read_latest():
  return getLatestMeasurement()

if __name__ == "__main__":
  uvicorn.run("main:app", port=8080, host="0.0.0.0", log_level="info")
