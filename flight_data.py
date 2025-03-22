
class FlightData:
	"""Handles data received from flight APIs"""
	NO_DATA = "No data!"

	def __init__(self, price:float, departure_date:str, arrival_date:str):
		self.price = price
		self.departure_date = departure_date
		self.arrival_date = arrival_date

	@classmethod
	def find_cheapest_flight(cls, data:dict):
		"""Returns the cheapest flight out of all parsed json data as an object of this class"""
		if not data or 'data' not in data or not data['data']:
			print("There is no data from API endpoint!")
			return cls.NO_DATA

		try:
			cheapest_price = float(data['data'][0]['price']['total'])
			departure_time = data['data'][0]["itineraries"][0]['segments'][0]["departure"]['at'].replace("T"," at ")
			arrival_time = data['data'][0]["itineraries"][0]['segments'][-1]["arrival"]['at'].replace("T", " at ")

			cheapest_flight = cls(cheapest_price, departure_time, arrival_time)

			for flight in data['data'][1:]:
				price = float(flight['price']['total'])
				if price < cheapest_price:
					cheapest_price = price
					departure_time = flight["itineraries"][0]['segments'][0]["departure"]['at']
					arrival_time = flight["itineraries"][0]['segments'][-1]["arrival"]['at']
					cheapest_flight = cls(cheapest_price, departure_time, arrival_time)
			return cheapest_flight
		except (NameError, ValueError, KeyError) as e:
			print(f"Error while processing data:{e} ")
			return cls.NO_DATA

	def __repr__(self):
		return f"Flight(price={self.price}, departure='{self.departure_date}', arrival='{self.arrival_date}')"

	def __str__(self):
		return f"{self.price} EUR | Departure: {self.departure_date} | Arrival: {self.arrival_date}"

