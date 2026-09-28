
import pandas as pd
from routing import AISMarineRouter
from visualize import (
    create_route_map,
    create_heatmap,
    plot_comparison_graphs
)

# ============================================
# USER CONFIGURATION
# ============================================

START_PORT = "Los Angeles"
END_PORT = "Long Beach"

NUMBER_OF_SHIPS = 3

SHIP_TYPES = [
    "Cargo",
    "Tanker",
    "Passenger"
]

DATASET = "ais_sample.parquet"

# ============================================
# PORT DATABASE
# ============================================

PORTS = {
    "Los Angeles": (33.7361, -118.2631),
    "Long Beach": (33.7542, -118.2167),
    "Singapore": (1.2644, 103.8200),
    "Chennai": (13.0827, 80.2707),
    "Dubai": (25.2697, 55.3095)
}

# ============================================

def main():

    print("Loading AIS Dataset...")
    df = pd.read_parquet(DATASET)

    print("Dataset Loaded.")

    start = PORTS[START_PORT]
    goal = PORTS[END_PORT]

    router = AISMarineRouter(df)

    all_routes = []

    for i in range(NUMBER_OF_SHIPS):

        ship_type = SHIP_TYPES[i % len(SHIP_TYPES)]

        print(f"Optimizing route for Ship {i+1} ({ship_type})")

        result = router.optimize_route(
            start=start,
            goal=goal,
            ship_type=ship_type
        )

        all_routes.append(result)

    print("Generating Visualizations...")

    create_route_map(
        df,
        start,
        goal,
        all_routes
    )

    create_heatmap(df)

    plot_comparison_graphs(all_routes)

    print("Done.")
    print("Generated:")
    print("- optimized_routes.html")
    print("- traffic_heatmap.html")
    print("- fuel_comparison.png")
    print("- distance_comparison.png")


if __name__ == "__main__":
    main()
