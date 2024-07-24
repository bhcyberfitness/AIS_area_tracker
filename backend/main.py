import threading
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from vessels import Vessel, vessels, start_ais_stream, POINT

app = FastAPI()

origins = [
	"http://localhost:3000",
	"localhost:3000"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

class VesselModel(BaseModel):
	mmsi: int
	lat: float
	long: float
	course: float
	speed: float
	name: str
	threat: str
	range: float	

class ThreatUpdateModel(BaseModel):
	threat: str

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

@app.put("/vessels/{mmsi}", tags=["vessels"])
def update_vessel(mmsi: int, threat_update: ThreatUpdateModel):
	for vessel in vessels:
		if vessel.mmsi == mmsi:
			vessel.threat = threat_update.threat
			return {
				"data": f"Vessel {mmsi} threat has been updated."
			}
	return {
		"data": f"Vessel {mmsi} not found."
	}


def start_stream():
	thread = threading.Thread(target=start_ais_stream)
	thread.start()

if __name__ == "__main__":
	start_stream()
	uvicorn.run(app, host="127.0.0.1", port=8000)