from tools.accommodations.apis import Accommodations
from tools.flights.apis import Flights
from tools.restaurants.apis import Restaurants
from tools.googleDistanceMatrix.apis import GoogleDistanceMatrix
import pandas as pd

hotel = Accommodations()
flight = Flights()
flight.load_db()
restaurant = Restaurants()
distanceMatrix = GoogleDistanceMatrix()

def estimate_budget(data, mode):
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
    multipliers = {3: {"flight": 2, "hotel": 3, "restaurant": 9}, 5: {"flight": 3, "hotel": 5, "restaurant": 15}, 7: {"flight": 4, "hotel": 7, "restaurant": 21}}
    return {"lowest": 0, "highest": 0, "average": 0}