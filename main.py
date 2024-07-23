import threading
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from vessels import Vessel, vessels, start_ais_stream, POINT

app = FastAPI()

class VesselModel(BaseModel):
	mmsi: int
	lat: float
	long: float
	course: float
	speed: float
	name: str	

@app.get("/")
def read_root():
	return {"Hello": "World"}

@app.get("/vessels", response_model=List[VesselModel])
def get_vessels():
	return vessels

@app.get("/vessels_within_distance", response_model=List[VesselModel])
def vessels_within_distance(threshold: float = Query(..., description="Distance threshold in nautical miles")):
	nearby_vessels = [vessel for vessel in vessels if vessel.will_be_within_distance(POINT, threshold)]
	return nearby_vessels

def start_stream():
	thread = threading.Thread(target=start_ais_stream)
	thread.start()

if __name__ == "__main__":
	start_stream()
	import uvicorn
	uvicorn.run(app, host="127.0.0.1", port=8000)