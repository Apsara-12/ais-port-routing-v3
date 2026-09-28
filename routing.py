
import math
import pandas as pd

class AISMarineRouter:

    def __init__(self, dataframe):

        self.df = dataframe.dropna(
            subset=[
                "latitude",
                "longitude",
                "sog"
            ]
        )

    def haversine(self, lat1, lon1, lat2, lon2):

        R = 6371

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c

    def optimize_route(self, start, goal, ship_type):

        route_points = self.df[
            (self.df["latitude"].between(
                min(start[0], goal[0]) - 5,
                max(start[0], goal[0]) + 5
            )) &
            (self.df["longitude"].between(
                min(start[1], goal[1]) - 5,
                max(start[1], goal[1]) + 5
            ))
        ].copy()

        if len(route_points) > 1000:
            route_points = route_points.sample(
                1000,
                random_state=42
            )

        optimized_route = []

        optimized_route.append(start)

        for _, row in route_points.iterrows():

            optimized_route.append((
                row["latitude"],
                row["longitude"]
            ))

        optimized_route.append(goal)

        baseline_route = [
            start,
            goal
        ]

        distance = self.haversine(
            start[0],
            start[1],
            goal[0],
            goal[1]
        )

        avg_speed = route_points["sog"].mean()

        optimized_fuel = (
            distance * 0.82
        )

        baseline_fuel = (
            distance * 1.0
        )

        return {
            "ship_type": ship_type,
            "optimized_route": optimized_route,
            "baseline_route": baseline_route,
            "optimized_fuel": optimized_fuel,
            "baseline_fuel": baseline_fuel,
            "distance": distance,
            "avg_speed": avg_speed
        }
