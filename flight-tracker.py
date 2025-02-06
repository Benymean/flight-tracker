import requests
import csv
from datetime import datetime, timedelta


class FlightSearch:
    def __init__(self):
        self.OAUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.AMADEUS_API_KEY = "JOh1CBYaZXMIv26wjVNwH9PDDs56mLV8"
        self.AMADEUS_API_SECRET = "TUVmBGtr0pG8gULM"
        self.ACCESS_TOKEN = None
        self.get_token()

    def get_token(self):
        header_data = {
            "grant_type": "client_credentials",
            "client_id": self.AMADEUS_API_KEY,
            "client_secret": self.AMADEUS_API_SECRET
        }
        response = requests.post(self.OAUTH_URL, data=header_data)
        if response.status_code == 200:
            self.ACCESS_TOKEN = response.json()["access_token"]
        else:
            print("Error retrieving access token:", response.text)

    def get_cheap_flight(self, destination, departure, return_date):
        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
        }
        AMADEUS_EP = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "originLocationCode": "SYD",  # Hardcoded origin airport code.
            "destinationLocationCode": destination,
            "departureDate": departure,
            "returnDate": return_date,
            "adults": 1,
            "travelClass": "ECONOMY",
            "currencyCode": "AUD"
        }
        response = requests.get(url=AMADEUS_EP, params=params, headers=headers)
        if response.status_code == 200:
            flights = response.json().get("data", [])
            if flights:
                try:
                    # Extract the cheapest flight
                    cheapest = min(
                        float(flight["price"]["grandTotal"])
                        for flight in flights
                        if "price" in flight and "grandTotal" in flight["price"]
                    )
                    return cheapest
                except ValueError:
                    print(f"Price conversion error for destination {destination}.")
                    return None
            else:
                print(f"No flights found for {destination}.")
                return None
        else:
            print(f"Failed to fetch flight offers for {destination}: {response.status_code}, {response.text}")
            return None


def main():
    # Define destination data as parameters
    destinations = [
        {"id": 1, "city": "Paris", "iataCode": "PAR"},
        {"id": 2, "city": "London", "iataCode": "LON"},
        {"id": 3, "city": "New York", "iataCode": "NYC"},
        # You can add more destinations as needed.
    ]

    # Initialize the FlightSearch class and generate dynamic travel dates
    flight_searcher = FlightSearch()
    today = datetime.today()
    departure_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")   # Departure 7 days from today.
    return_date = (today + timedelta(days=17)).strftime("%Y-%m-%d")     # Return 10 days after departure.

    print(f"Searching for flights from {departure_date} to {return_date}.")

    # Process each destination to search for the cheapest flight.
    updated_destinations = []

    for destination in destinations:
        city = destination.get("city", "Unknown City")
        iata = destination.get("iataCode", "").strip()
        row_id = destination.get("id")

        if not row_id:
            print(f"Skipping {city} due to missing 'id' field.")
            continue

        if not iata:
            print(f"Skipping {city} due to missing IATA code.")
            continue

        cheapest_price = flight_searcher.get_cheap_flight(
            destination=iata,
            departure=departure_date,
            return_date=return_date
        )

        if cheapest_price is None:
            print(f"No cheap flight found for {city} ({iata}). Recording as N/A.")
            destination.update({
                "cheapestPrice": "N/A",
                "Departure Date": departure_date,
                "Return Date": return_date
            })
        else:
            destination.update({
                "cheapestPrice": cheapest_price,
                "Departure Date": departure_date,
                "Return Date": return_date
            })
            print(f"Found flight for {city}: ${cheapest_price}")

        updated_destinations.append(destination)

    # Write the updated destination data to a local CSV file.
    csv_file = "flight_deals.csv"
    fieldnames = ["id", "city", "iataCode", "cheapestPrice", "Departure Date", "Return Date"]

    try:
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in updated_destinations:
                writer.writerow(data)
        print(f"CSV file '{csv_file}' created successfully with the destination flight details.")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")


if __name__ == "__main__":
    main()
