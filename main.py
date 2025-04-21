import time
import dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
#loads variables from .env file
dotenv.load_dotenv()

#Initiating classes and data from excel-like file
def main():
	data_manager = DataManager()
	flight_search = FlightSearch()
	sheet_data = data_manager.get_sheety_data(params=None)
	users_info = data_manager.get_user_credentials(params=None)
	#Looping through all the desired destination from Excel like file, getting codes for those cities,
	# and getting data from the FLIGHT_ENDPOINT (Amadeus API) for given params. As final, getting the cheapest flight
	#object from FlightData class
	for name, email, current_destination in users_info:
		for city in sheet_data:
			city_param = city['city']

			#Calling the get_iata_code API only once to make sure codes are updated in Excel
			iata_code_from_api_call = flight_search.get_iata_code(city_name=city_param)
			if not city['iataCode'] or city['iataCode'] != iata_code_from_api_call:
				code = iata_code_from_api_call
			else:
				code =city['iataCode']

			flight_search_results = flight_search.get_flights(my_destination=current_destination, desired_destination=city_param)
			cheapest_flight = FlightData.find_cheapest_flight(flight_search_results)

			if isinstance(cheapest_flight, str): #IMPORTANT in case that find_cheapest_flight returns string
				print(f"No valid flight found for {city_param}. Skipping...")
				continue

			#Populates entire table with the acquired data for each city
			current_price = cheapest_flight.price
			departure_date = cheapest_flight.departure_date
			arrival_date = cheapest_flight.arrival_date

			#If price passes the condition, then user get informed via email for great deal
			notificator = NotificationManager(city, cheapest_flight)
			if notificator.is_it_worth_it():
				notificator.inform_user(destination=city_param, username=name, email=email)

			updated_sheety_data = {
				"price": {
					"iataCode": code,
					"currentPrice" : current_price,
					"departureDate": departure_date,
					"arrivalDate" : arrival_date
				}
			}

			#Optional print for tracking the update, more likely to be deleted in final code version
			print(f"Updating ID {city['id']} with data: {updated_sheety_data}")
			time.sleep(1)
			data_manager.update_sheety_table(updated_data=updated_sheety_data, object_id=city["id"])

if __name__ == "__main__":
	main()