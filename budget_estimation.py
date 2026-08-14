from tools.accommodations.apis import Accommodations
from tools.flights.apis import Flights
from tools.restaurants.apis import Restaurants
from tools.googleDistanceMatrix.apis import GoogleDistanceMatrix
import pandas as pd

# Initialize API clients
hotel = Accommodations()
flight = Flights()
flight.load_db()
restaurant = Restaurants()
distanceMatrix = GoogleDistanceMatrix()


def estimate_budget(data, mode):
    """
    Estimate the budget based on the mode (lowest, highest, average) for flight, hotel, or restaurant data.
    """
    if mode == "lowest":
        return min(data)
    elif mode == "highest":
        return max(data)
    elif mode == "average":
        data = [x for x in data if str(x) != nan]
        return sum(data) / len(data)

def budget_calc(org, dest, days, date, people_number=None, local_constraint=None):
    if days == 3:
        grain = "city"
    elif days in [5,7]:
        grain = "state"
    if grain not in ["city", "state"]:
        raise ValueError("grain must be one of city, state")
    multipliers = {3: {"flight": 2, "hotel": 3, "restaurant": 9}, 5: {"flight": 3, "hotel": 5, "restaurant": 15}, 7: {"flight": 4, "hotel": 7, "restaurant": 21}}
    if grain == "city":
        hotel_data = hotel.run(dest)
        restaurant_data = restaurant.run(dest)
        flight_data = flight.data[(flight.data["DestCityName"] == dest) & (flight.data["OriginCityName"] == org)]
    elif grain == "state":
        city_set = open(../database/background/citySet_with_states.txt).read().strip().split(\n)
        all_hotel_data = []
        all_restaurant_data = []
        all_flight_data = []
        for city in city_set:
            if dest == city.split(\t)[1]:
                candidate_city = city.split(\t)[0]
                current_hotel_data = hotel.run(candidate_city)
                current_restaurant_data = restaurant.run(candidate_city)
                current_flight_data = flight.data[(flight.data["DestCityName"] == candidate_city) & (flight.data["OriginCityName"] == org)]
                all_hotel_data.append(current_hotel_data)
                all_restaurant_data.append(current_restaurant_data)
                all_flight_data.append(current_flight_data)
        hotel_data = pd.concat(all_hotel_data, axis=0)
        restaurant_data = pd.concat(all_restaurant_data, axis=0)
        flight_data = pd.concat(all_flight_data, axis=0)
        flight_data = flight_data[flight_data[FlightDate].isin(date)]
    if people_number:
        hotel_data = hotel_data[hotel_data[maximum occupancy] >= people_number]
    if local_constraint:
        if local_constraint.get(transportation) == no self-driving:
            if grain == "city" and len(flight_data[flight_data[FlightDate] == date[0]]) < 2:
                raise ValueError("No flight data")
            elif grain == "state" and len(flight_data[flight_data[FlightDate] == date[0]]) < 10:
                raise ValueError("No flight data")
        elif local_constraint.get(transportation) == no flight:
            if len(flight_data[flight_data[FlightDate] == date[0]]) < 2:
                raise ValueError("Impossible")
        if local_constraint.get(room type):
            rt = local_constraint[room type]
            if rt == shared room:
                hotel_data = hotel_data[hotel_data[room type] == Shared room]
            elif rt == private room:
                hotel_data = hotel_data[hotel_data[room type] == Private room]
    budgets = {}
    for mode in ["lowest", "highest", "average"]:
        flight_budget = estimate_budget(flight_data["Price"].tolist(), mode) * multipliers[days]["flight"]
        hotel_budget = estimate_budget(hotel_data["price"].tolist(), mode) * multipliers[days]["hotel"]
        restaurant_budget = estimate_budget(restaurant_data["Average Cost"].tolist(), mode) * multipliers[days]["restaurant"]
        budgets[mode] = flight_budget + hotel_budget + restaurant_budget
    return budgets
