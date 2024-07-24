import asyncio
import json
import websockets
from datetime import datetime, timezone
from haversine import haversine, inverse_haversine, Direction, Unit
from math import radians, cos, sin, asin, sqrt, pi

# Define area for AIS message bounding box (approximates to a RADIUS by RADIUS
# nautical mile square area centered on POINT)
POINT = (50.761001904299036 , -1.1063575744628908) # Decimal lat/long coordinates
RADIUS = 6
TOP_LEFT = inverse_haversine(POINT, RADIUS*sqrt(2), Direction.NORTHWEST, unit=Unit.NAUTICAL_MILES)
BOTTOM_RIGHT = inverse_haversine(POINT, RADIUS*sqrt(2), Direction.SOUTHEAST, unit=Unit.NAUTICAL_MILES)

class Vessel:
	"""
	A class used to represent a vessel transmitting on AIS

	Attributes
	----------
	mmsi : int
		the MMSI number of the vessel
	lat : float
		the decimal latitude of the vessel
	long : float
		the decimal longitude of the vessel
	course : float
		the course over ground in degrees of the vessel 
	speed : float
		the speed over ground in knots of the vessel
	name : str
		the broadcasted name of the vessel
	threat: str
		the threat level (blue, white or red) of the vessel
	
	Methods
	-------
	distance_to_point(point)
		computes haversine distance in nautical miles from the vessel to a point
	future_position(minutes)
		computes dead reckoned position in specified time in minutes
	will_be_within_distance(point, threshold)
		computes whether the vessel will be within a certain distance of specified point at any time in next hour
	"""

	def __init__(self, mmsi=0, lat=0, long=0, course=0, speed=0, name="NO_NAME", threat="white", range=0):
		"""
		Parameters
		----------
		mmsi : int
			the MMSI number of the vessel
		lat : float
			the decimal latitude of the vessel
		long : float
			the decimal longitude of the vessel
		course : float
			the course over ground in degrees of the vessel 
		speed : float
			the speed over ground in knots of the vessel
		name : str
			the broadcasted name of the vessel
		threat: str
			the threat level (blue, white or red) of the vessel
			
		"""
		
		self.mmsi = mmsi
		self.lat = lat
		self.long = long
		self.course = course
		self.speed = speed
		self.name = name
		self.threat = threat
		self.range = self.distance_to_point(POINT)
	
	def distance_to_point(self, point):
		return haversine((self.lat, self.long), point, unit=Unit.NAUTICAL_MILES)
	
	def future_position(self, minutes: float):
		distance = self.speed * (minutes / 60)
		return inverse_haversine((self.lat, self.long), distance, self.course * (pi / 180), unit=Unit.NAUTICAL_MILES)
	
	def will_be_within_distance(self, point, threshold):
		current_distance = self.distance_to_point(point)
		if current_distance <= threshold:
			return True
		
		for t in range(1,61):
			future_pos = self.future_position(t)
			if haversine(future_pos, point, unit=Unit.NAUTICAL_MILES) <= threshold:
				return True
		
		return False

vessels = []

async def connect_ais_stream():
	filename = 'apikey'
	try:
		with open(filename, 'r') as f:
			key = f.read().strip()
	except FileNotFoundError:
		print("'%s' file not found" % filename)

	async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:

		subscribe_message = {"APIKey": key, "BoundingBoxes": [[list(TOP_LEFT), list(BOTTOM_RIGHT)]]}

		subscribe_message_json = json.dumps(subscribe_message)
		await websocket.send(subscribe_message_json)

		async for message_json in websocket:
			message = json.loads(message_json)
			message_type = message["MessageType"]

			if message_type == "PositionReport":
 				# the message parameter contains a key of the message type which contains the message itself
				ais_message = message['Message']['PositionReport']
				# print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']} Speed: {ais_message['Sog']} COG: {ais_message['Cog']}")

				vessel_not_in_list = True
				for vessel in vessels:
					if vessel.mmsi == ais_message['UserID']:
						vessel.lat = ais_message['Latitude']
						vessel.long = ais_message['Longitude']
						vessel.course = ais_message['Cog']
						vessel.speed = ais_message['Sog']
						vessel.range = vessel.distance_to_point(POINT)
						vessel_not_in_list = False
				
				if vessel_not_in_list:
					vessels.append(Vessel(ais_message['UserID'], ais_message['Latitude'], ais_message['Longitude'], ais_message['Cog'], ais_message['Sog']))


			if message_type == "ShipStaticData":
				ais_message = message['Message']['ShipStaticData']
				# print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Name: {ais_message['Name']}")

				vessel_not_in_list = True
				for vessel in vessels:
					if vessel.mmsi == ais_message['UserID']:
						vessel.name = ais_message['Name']

def start_ais_stream():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(connect_ais_stream())

if __name__ == "__main__":
    start_ais_stream()