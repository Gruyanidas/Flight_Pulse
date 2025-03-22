import requests, json
import os, dotenv
dotenv.load_dotenv()

class DataManager:

    SHEETY_URL_ENDPOINT = os.getenv("SHEETY_URL_ENDPOINT")
    SHEETY_HEADERS = {
        "Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"
    }
    SHEETY_USERS_ENDPOINT = os.getenv("USERS_ENDPOINT")

    def __init__(self):
        self.destination_data = {}
        self.SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")

    @classmethod
    def get_sheety_data(cls, params=None):
        """Retrieves data from entire prices sheet from Excel like table"""
        data = cls.perform_http_request(url=cls.SHEETY_URL_ENDPOINT,method="GET", params=params, headers=None)
        return data["prices"]

    @classmethod
    def get_user_credentials(cls, params=None):
        """Retrieves user info from Excel like table in a tuple form (name, email)"""
        users = cls.perform_http_request(url=cls.SHEETY_USERS_ENDPOINT, method="GET", params=params, headers=None)
        if not users or "users" not in users or not users["users"]:
            print("There is no users data in data base!")
            return
        return [(user["name"],user["email"], user["my_city"]) for user in users["users"]]

    @classmethod
    def update_sheety_table(cls, updated_data:dict, object_id : int): #IMPORTANT Get sheety token headers work!
        """Updates data in sheety table"""
        response = cls.perform_http_request(url=f"{cls.SHEETY_URL_ENDPOINT}/{object_id}", method="PUT", data=updated_data)
        if response.status_code == 200 or response.status_code == 204:
            print("Update was successful!")
        print(response.status_code, response.text)

    @staticmethod
    def perform_http_request(url: str, method: str = "GET", params=None, data=None, headers=None):
        """Generic method to handle GET, POST, PUT"""
        try:
            method = method.upper()
            if method == "GET":
                response = requests.get(url=url, params=params, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url=url, json=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url=url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url=url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if method == "GET" else response

        except requests.exceptions.Timeout:
            raise RuntimeError("Request timed out. Try again later.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Network connection error. Check your internet.")
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(f"Request failed: {req_err}")
        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse JSON response.")


