import os, time
import requests
from datetime import datetime as dt, timedelta
from data_manager import DataManager as dm

class FlightSearch:
    #Initiation class variables
    CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
    CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
    TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
    IATA_ENDPOINT = os.getenv("IATA_ENDPOINT")
    FLIGHT_ENDPOINT = os.getenv("FLIGHT_ENDPOINT")

    #determines variables for token needed for security header Amadeus protocol
    access_token = None
    token_expiry = 0

    @staticmethod
    def save_json_to_file(data, filename="flight_data.txt"): #Optional use, if you need to debug JSON response
        with open(filename, mode="w", newline="") as file:
            file.write(repr(data))
            print(f"JSON data saved to {filename}")

    @classmethod
    def get_access_token(cls):
        """Fetches a new access token if expired or not available."""
        current_time = time.time()

        # If token is valid, reuse it, if not, request another one
        if cls.access_token and current_time < cls.token_expiry:
            return cls.access_token

        print("Fetching new Amadeus access token...")

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": cls.CLIENT_ID,
            "client_secret": cls.CLIENT_SECRET
        }

        try:
            response = dm.perform_http_request(url=cls.TOKEN_URL, headers=headers, method="POST", data=data)
            token_data = response.json()

            cls.access_token = token_data.get("access_token")
            cls.token_expiry = current_time + token_data.get("expires_in", 1800) - 10 #expiration time of token with 10s buffer

            print(f"New token obtained. Expires in {token_data['expires_in']} seconds.")
            return cls.access_token

        except requests.exceptions.RequestException as e:
            print(f"Failed to get access token: {e}")
            return None

    @classmethod
    def make_request(cls, endpoint, params=None):
        """Makes a request to the Amadeus API with a valid token."""
        header = cls.get_header()
        response = dm.perform_http_request(method="GET", url=endpoint, params=params, headers=header)
        return response #No response.json() because for GET method, we get already json with perform_http_request

    @classmethod
    def get_header(cls):
        token = cls.get_access_token()
        header = {"Authorization": f"Bearer {token}"}
        return header

    @classmethod
    def get_iata_code(cls,city_name:str) -> str:
        """Gets code for specific city, our current airport or destination"""
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        data = cls.make_request(endpoint=FlightSearch.IATA_ENDPOINT, params=query)

        try:
            iata_code = data["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        return iata_code

    @classmethod
    def get_flights(cls, my_destination:str, desired_destination:str):
        """Finds flights according to destinations and search query"""

        start_date = dt.now() + timedelta(days=10)
        # future_end_date = start_date + timedelta(days=165) IMPORTANT Should be used inside other method for getting historical data...
        # past_end_date = start_date - timedelta(days=165)

        home = cls.get_iata_code(my_destination)
        desired_city = cls.get_iata_code(desired_destination)

        header = cls.get_header()
        headers = {
            "Authorization": header["Authorization"],
            "Content-Type": "application/json",
            "X-HTTP-Method-Override": "POST"
        }

        data = {
            "currencyCode": "EUR",
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": home,
                    "destinationLocationCode": desired_city,
                    "departureDateTimeRange": {
                        "date": start_date.strftime('%Y-%m-%d'),
                        "dateWindow": "P3D"
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT"
                }
            ],
            "sources": [
                "GDS"
            ],
            "searchCriteria": {
                "maxFlightOffers": 20
            }
        }

        data_returned = dm.perform_http_request(url=cls.FLIGHT_ENDPOINT, data=data, headers=headers, method="POST")
        flight_data = data_returned.json()

        #Optional - write JSON to txt just for better handling of huge file by using static method
        return flight_data

    def __str__(self):
        return "FlightSearch Amadeus API Service"

    # IMPORTANT Following function suppose to return historical data for a given params but
    # standard Amadeus plans does not provide historical data prices for desired flights.
    # The idea was with those data to populate excel like file, column with the lowest prices
    # and use it as a reference for the cheapest flight. Instead, we should populate column manually.
    # Prices for those flight are sourced from chatGPT and are estimated lowest prices.

    # Before actual usage, method bellow should be checked carefully
    # @classmethod
    # def get_lowest_flight_prices(cls, my_destination:str, desired_destination:str):
    #     """For a given destination string, returns the cheapest price from 6 months back
    #     Destination is updated dinamically from sheet data"""
    #     home = FlightSearch.get_iata_code(my_destination)
    #     desired_city = FlightSearch.get_iata_code(desired_destination)
    #     query = {
    #         "origin": home,
    #         "destination": desired_city,
    #         "departureDate":f"{cls.start_time.strftime('%Y-%m-%d')}, {cls.start_date.strftime('%Y-%m-%d')}",
    #         "oneWay": True,
    #         "nonStop": True,
    #     }
    #
    #     headers = cls.get_header()
    #     data = DataManager.fetch_data(url=cls.CHEAPEST_FLIGHT_ENDPOINT, params=query, header=headers)
    #     try:
    #         price = data["data"][0]['price']['total']
    #     except IndexError:
    #         print(f"IndexError: No recorded price found for {desired_city}.")
    #         return "Not found"
    #     except KeyError:
    #         print(f"KeyError: No such data for {desired_city}.")
    #         return "Not Found"
    #     return price