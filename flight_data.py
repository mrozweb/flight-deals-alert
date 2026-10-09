class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, out_time, return_date):
        # This class is responsible for structuring the flight data.
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.out_time = out_time
        self.return_date = return_date

def find_cheapest_flight(data, return_date):
    # Parse the JSON data and find the cheapest flight.
    # Helper return placeholder object instead of None
    def _empty_flight():
        return FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            out_time="N/A",
            return_date=return_date,
        )

    # ========== Handle empty data =======================================
    if data is None:
        print("data is None")
        return _empty_flight()

    if "error" in data:
        print(f"API error - {data['error']}")
        return _empty_flight()

    # ========== Get data for flights =======================================
    best_flights = data.get("best_flights", [])
    other_flights = data.get("other_flights", [])

    print(f"best_flights = {len(best_flights)} items")
    print(f"other_flights = {len(other_flights)} items")

    # ========== Combine all flights =======================================
    all_flights = best_flights + other_flights

    if not all_flights:
        print("No flights found in response")
        return _empty_flight()

    # ========== Find the cheapest flight =======================================
    cheapest_flight_data = None
    cheapest_price = float("inf")

    for i, flight in enumerate(all_flights, 1):
        price = flight.get("price")
        print(f"Flight {i} price = {price}")

        if price is None:
            continue
        if price < cheapest_price:
            cheapest_price = price
            cheapest_flight_data = flight

    if cheapest_flight_data is None:
        print("No valid flights with prices found")
        return _empty_flight()

    print(f"Cheapest price = {cheapest_price}")

    # ========== Extract flight details =======================================
    try:
        price = cheapest_flight_data["price"]
        origin_airport = cheapest_flight_data["flights"][0]["departure_airport"]["id"]
        destination_airport = cheapest_flight_data["flights"][-1]["arrival_airport"]["id"]

        #  Get the full datetime string: "2026-10-04 07:20"
        departure_datetime = cheapest_flight_data["flights"][0]["departure_airport"]["time"]

        # Split into date and time
        parts = departure_datetime.split(" ")
        out_date = parts[0]
        out_time = parts[1] if len(parts) > 1 else "N/A"

        print(
            f"Extracted - price={price}, origin={origin_airport}, "
            f"destination={destination_airport}, out_date={out_date}, out_time={out_time}"
        )

        return FlightData(
            price=price,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            out_date=out_date,
            out_time=out_time,
            return_date=return_date
        )

    except (KeyError, IndexError) as e:
        print(f"Error extracting flight data: {e}")
        return _empty_flight()