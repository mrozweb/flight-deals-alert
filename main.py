import requests_cache
from dotenv import load_dotenv
from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
# from pprint import pprint
from datetime import datetime, timedelta

load_dotenv(dotenv_path=".env")

# ========== CACHE =======================================
requests_cache.install_cache("serp_fly_cache", expire_after=None)

# ========== OBJECTS =======================================
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# ========== HEADER =======================================
print("=" * 70)
print("✈️ FLIGHT DEAL FINDER")
print("=" * 70)

# ========== FETCH DATA =======================================
print("\nFetching data from spreadsheet...")
sheet_data = data_manager.get_data()

if not sheet_data:
    print("No data found in spreadsheet. Exiting.")
    exit(1)

# ========== SET THE DATES =======================================
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
two_weeks_later = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

print(f"Searching: {tomorrow} to {two_weeks_later}")

# ========== PRINT DATA =======================================
# pprint(sheet_data[2])

# ========== SEARCH EACH CITY =======================================
ORIGIN_CITY_IATA = "LHR"

for row in sheet_data:
    row_id = row.get("id")
    iata_code = row.get("iataCode")
    city = row.get("city")

    # Skip origin_city_code in loop
    if iata_code == ORIGIN_CITY_IATA:
        print("\n" + "=" * 70)
        print(f"Skipping: {iata_code} {city}")
        print("=" * 70 + "\n")
        continue

    if not iata_code:
        print(f"Skipping: {city} - no IATA code")
        continue

    try:
        current_price = float(row.get("lowestPrice", 0))
    except (TypeError, ValueError):
        print(f"Skipping: {city} invalid price")
        continue

    # Get the cheapest flight
    data = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=iata_code,
        from_time=tomorrow,
        to_time=two_weeks_later,
    )
    # pprint(data)

    # Convert dict → FlightData object
    cheapest_flight = find_cheapest_flight(data, return_date=two_weeks_later)

    if cheapest_flight and cheapest_flight.price != "N/A":
        new_price = float(cheapest_flight.price)

        print(f"Cheapest: {new_price:.0f} {flight_search.currency}")
        print(f"Route: {cheapest_flight.origin_airport} → {cheapest_flight.destination_airport}")
        print(f"Outbound: {cheapest_flight.out_date} - {cheapest_flight.out_time}")
        # print(f"Return: {cheapest_flight.return_date}")

        # Only update if the new price is cheaper
        if new_price < current_price:
            saving = current_price - new_price
            print(f"Deal! Save: {saving:.0f} {flight_search.currency}")

            data_manager.update_lowest_price(row_id=row_id, new_price=new_price)

            notification_manager.send_deal_email(
                origin_city_iata=ORIGIN_CITY_IATA,
                city=city,
                iata_code=iata_code,
                old_price=current_price,
                new_price=new_price,
                out_date=cheapest_flight.out_date,
                out_time=cheapest_flight.out_time,
            )
        else:
            print("No deal - current price is better.")
    else:
        print(f"No cheapest flight found")
    print("\n" + "=" * 70)