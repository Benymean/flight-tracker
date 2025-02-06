# Flight Deals CSV Generator

A Python script that retrieves the cheapest flight deals for specified destinations using the Amadeus API and writes the results to a local CSV file.

## Features

- Retrieves flight offers from the Amadeus API
- Dynamically calculates departure and return dates
- Searches for the cheapest flight for each destination
- Writes flight deal details to a local CSV file (`flight_deals.csv`)
- Simple error handling for API calls and file operations

## Prerequisites

- Python 3.x
- `requests` library (install with `pip install requests`)
- Amadeus API key
  
## Usage
The script will:
- Use a predefined list of destinations (with city names and IATA codes).
- Dynamically calculate travel dates (departure 7 days from today and return 10 days after departure).
- Fetch the cheapest flight offers for each destination from the Amadeus API.
- Save the results, including flight price and travel dates, to a CSV file named flight_deals.csv.

## Sample Output
Searching for flights from 2025-02-13 to 2025-02-23.
- Found flight for Paris: $550.00
- Found flight for London: $670.00
- Found flight for New York: $900.00
- CSV file 'flight_deals.csv' created successfully with the destination flight details.

## Limitations
- The origin airport is currently hardcoded as "SYD". Modify the script if you need a different origin.
- The script is configured to search for one adult in ECONOMY class and returns prices in AUD.
- Only a predefined list of destinations is supported. Update the destinations list in the script as needed.




