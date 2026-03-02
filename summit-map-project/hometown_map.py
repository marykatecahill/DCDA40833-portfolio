import pandas as pd
import folium
import requests

# Mapbox access token
access_token = "pk.eyJ1IjoibWFyeWthdGVjYWhpbGwiLCJhIjoiY21sdHI0YmFuMDM0NTNlb3E4cW9kbWd5MiJ9.I0G5MOaIsxYDNcHNH48Bag"

# Load CSV file
data = pd.read_csv("hometown_locations.csv")

# Mapbox style URL
tiles = "https://api.mapbox.com/styles/v1/marykatecahill/cmm3s8lth00m601s34t8xf3xy/tiles/{z}/{x}/{y}?access_token=" + access_token

# Create map with Mapbox style
m = folium.Map(
    location=[40.7167, -74.3572],  # Summit, NJ
    zoom_start=13,
    tiles=tiles,
    attr="Mapbox"
)
def geocode(address):
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={access_token}"
    response = requests.get(url)
    result = response.json()
    
    if result["features"]:
        coords = result["features"][0]["geometry"]["coordinates"]
        # Mapbox returns [longitude, latitude], so we return [lat, lon]
        return coords[1], coords[0]
    else:
        return None, None

# Geocode and add markers for each location
for index, row in data.iterrows():
    lat, lon = geocode(row["Address"])
    
    if lat and lon:
        
        # Choose marker color based on Type
        if row["Type"] == "Restaurant":
            color = "red"
        elif row["Type"] == "Park":
            color = "green"
        elif row["Type"] == "School":
            color = "blue"
        else:
            color = "purple"
        
        popup_html = f"""
        <h4>{row['Name']}</h4>
        <p>{row['Description']}</p>
        <img src="{row['Image_URL']}" width="200">
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=popup_html,
            icon=folium.Icon(color=color)
        ).add_to(m)

# Save map to HTML file
m.save("summit_map.html")
print("Map saved successfully as summit_map.html")
