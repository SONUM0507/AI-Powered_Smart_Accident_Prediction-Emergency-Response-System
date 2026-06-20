import folium
from geopy.distance import geodesic

def find_nearest_hospital(user_location, hospitals_df):
    """Finds the nearest hospital to the given coordinates."""
    if hospitals_df.empty:
        return None, 0.0

    nearest_hospital = None
    nearest_distance = float("inf")

    for index, row in hospitals_df.iterrows():
        hospital_location = (row["Latitude"], row["Longitude"])
        distance = geodesic(user_location, hospital_location).km

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_hospital = row
            
    return nearest_hospital, nearest_distance

def create_emergency_map(latitude, longitude, nearest_hospital):
    """Creates a folium map showing the accident location and the nearest hospital."""
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Accident marker
    folium.Marker(
        [latitude, longitude],
        popup="Accident Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Hospital marker and path
    if nearest_hospital is not None:
        folium.Marker(
            [nearest_hospital["Latitude"], nearest_hospital["Longitude"]],
            popup=nearest_hospital["Hospital"],
            icon=folium.Icon(color="green", icon="plus")
        ).add_to(m)

        # Draw a line connecting them
        folium.PolyLine(
            [
                [latitude, longitude],
                [nearest_hospital["Latitude"], nearest_hospital["Longitude"]]
            ],
            color="blue",
            weight=5,
            opacity=0.7
        ).add_to(m)

    return m
