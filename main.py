import requests_cache
from dotenv import load_dotenv
from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
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
users = data_manager.get_customer_emails()

if not sheet_data:
    print("No data found in spreadsheet. Exiting.")
    exit(1)

# Extract emails
user_emails = [
    user["whatIsYourEmail?"]
    for user in users
    if user.get("whatIsYourEmail?")
]

# Remove duplication if someone signed twice
user_emails = list(dict.fromkeys(user_emails))

if not user_emails:
    print("No subscribers - emails will be skipped")

# ========== SET THE DATES =======================================
tomorrow        = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
two_weeks_later = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

print(f"Searching: {tomorrow} to {two_weeks_later}")

# ========== SEARCH EACH CITY =======================================
ORIGIN_CITY_IATA = "LHR"

for row in sheet_data:
    row_id    = row.get("id")
    iata_code = row.get("iataCode")
    city      = row.get("city")

    # Skip origin city
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

    print("\n" + "=" * 70)
    print(f" Route: {ORIGIN_CITY_IATA} → {iata_code} ({city})")
    print("=" * 70)

    # ============ 1) DIRECT (NONSTOP) FLIGHTS ============
    direct_data = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=iata_code,
        from_time=tomorrow,
        to_time=two_weeks_later,
        is_direct=True,
    )

    # Inline filter: keep only flights with 0 stops
    raw_direct = direct_data.get("best_flights", []) + direct_data.get("other_flights", [])
    direct_only = [
        f for f in raw_direct
        if f.get("price") is not None and len(f.get("flights", [])) - 1 == 0
    ]

    if direct_only:
        cheapest_direct = find_cheapest_flight(
            {"best_flights": direct_only, "other_flights": []},
            return_date=two_weeks_later,
        )
    else:
        cheapest_direct = find_cheapest_flight(None, return_date=two_weeks_later)

    if cheapest_direct.price != "N/A":
        direct_price = float(cheapest_direct.price)
        print(f" Cheapest DIRECT:   {direct_price:.0f} {flight_search.currency} | "
              f"{cheapest_direct.out_date} {cheapest_direct.out_time} | "
              f"{cheapest_direct.stops} stop(s)")

        if direct_price < current_price:
            saving = current_price - direct_price
            print(f" DIRECT deal! Save: {saving:.0f} {flight_search.currency}")

            data_manager.update_lowest_price(row_id=row_id, new_price=direct_price)

            notification_manager.send_deal_email(
                emails_to=user_emails,
                origin_city_iata=ORIGIN_CITY_IATA,
                city=city,
                iata_code=iata_code,
                old_price=current_price,
                new_price=direct_price,
                out_date=cheapest_direct.out_date,
                out_time=cheapest_direct.out_time,
                stops=cheapest_direct.stops,
            )
            current_price = direct_price
        else:
            print(f" No direct deal — sheet {current_price:.0f} "
                  f"{flight_search.currency} is cheaper.")
    else:
        print(" No direct (nonstop) flights found")

    # ============ 2) INDIRECT (1+ STOPS) FLIGHTS ============
    indirect_data = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=iata_code,
        from_time=tomorrow,
        to_time=two_weeks_later,
        is_direct=False,
    )

    # Inline filter: keep only flights with 1+ stops
    raw_list = indirect_data.get("best_flights", []) + indirect_data.get("other_flights", [])
    indirect_only = [
        f for f in raw_list
        if f.get("price") is not None and len(f.get("flights", [])) - 1 >= 1
    ]

    if indirect_only:
        cheapest_indirect = find_cheapest_flight(
            {"best_flights": indirect_only, "other_flights": []},
            return_date=two_weeks_later,
        )
    else:
        cheapest_indirect = find_cheapest_flight(None, return_date=two_weeks_later)

    if cheapest_indirect.price != "N/A":
        indirect_price = float(cheapest_indirect.price)
        print(f" Cheapest INDIRECT: {indirect_price:.0f} {flight_search.currency} | "
              f"{cheapest_indirect.out_date} {cheapest_indirect.out_time} | "
              f"{cheapest_indirect.stops} stop(s)")

        if indirect_price < current_price:
            saving = current_price - indirect_price
            print(f" INDIRECT deal! Save: {saving:.0f} {flight_search.currency}")

            data_manager.update_lowest_price(row_id=row_id, new_price=indirect_price)

            notification_manager.send_deal_email(
                emails_to=user_emails,
                origin_city_iata=ORIGIN_CITY_IATA,
                city=city,
                iata_code=iata_code,
                old_price=current_price,
                new_price=indirect_price,
                out_date=cheapest_indirect.out_date,
                out_time=cheapest_indirect.out_time,
                stops=cheapest_indirect.stops,
            )
        else:
            print(f" No indirect deal — sheet {current_price:.0f} "
                  f"{flight_search.currency} is cheaper.")
    else:
        print(" No indirect flights found")

    print("\n" + "=" * 70)