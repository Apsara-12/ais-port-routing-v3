
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

def create_route_map(df, start, goal, routes):

    m = folium.Map(
        location=start,
        zoom_start=6
    )

    folium.Marker(
        start,
        tooltip="Start Port",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        goal,
        tooltip="Destination Port",
        icon=folium.Icon(color="red")
    ).add_to(m)

    colors = [
        "blue",
        "purple",
        "orange",
        "darkred"
    ]

    for idx, route in enumerate(routes):

        color = colors[idx % len(colors)]

        folium.PolyLine(
            route["baseline_route"],
            color="red",
            weight=3,
            opacity=0.7,
            tooltip=f'Baseline Route ({route["ship_type"]})'
        ).add_to(m)

        folium.PolyLine(
            route["optimized_route"],
            color=color,
            weight=5,
            opacity=0.9,
            tooltip=f'Optimized Route ({route["ship_type"]})'
        ).add_to(m)

    m.save("optimized_routes.html")

def create_heatmap(df):

    heat_data = list(zip(
        df["latitude"],
        df["longitude"]
    ))

    m = folium.Map(
        location=[
            df["latitude"].mean(),
            df["longitude"].mean()
        ],
        zoom_start=4
    )

    HeatMap(heat_data).add_to(m)

    m.save("traffic_heatmap.html")

def plot_comparison_graphs(routes):

    ship_names = []
    optimized = []
    baseline = []
    distances = []

    for r in routes:

        ship_names.append(r["ship_type"])

        optimized.append(r["optimized_fuel"])

        baseline.append(r["baseline_fuel"])

        distances.append(r["distance"])

    plt.figure(figsize=(8, 5))

    x = range(len(ship_names))

    plt.bar(
        x,
        baseline,
        width=0.4,
        label="Baseline Fuel"
    )

    plt.bar(
        [i + 0.4 for i in x],
        optimized,
        width=0.4,
        label="Optimized Fuel"
    )

    plt.xticks(
        [i + 0.2 for i in x],
        ship_names
    )

    plt.ylabel("Fuel Consumption")
    plt.title("Optimized vs Baseline Fuel Usage")
    plt.legend()

    plt.savefig("fuel_comparison.png")

    plt.figure(figsize=(8, 5))

    plt.bar(ship_names, distances)

    plt.ylabel("Distance (km)")
    plt.title("Route Distance Comparison")

    plt.savefig("distance_comparison.png")
