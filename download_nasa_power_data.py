# import os
# import math
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Helper function to calculate points 100 km away at a given bearing
# def calculate_point(lat0, lon0, angle_deg, distance_km=100.0):
#     R = 6371.0  # Earth radius in km
#     angle_rad = math.radians(angle_deg)
    
#     # Calculate displacement components
#     dNorth = distance_km * math.cos(angle_rad)
#     dEast = distance_km * math.sin(angle_rad)
    
#     # Calculate latitude change (constant)
#     delta_lat = (dNorth / R) * (180.0 / math.pi)
#     new_lat = lat0 + delta_lat
    
#     # Calculate longitude change (depends on latitude)
#     delta_lon = (dEast / (R * math.cos(math.radians(lat0)))) * (180.0 / math.pi)
#     new_lon = lon0 + delta_lon
    
#     return new_lat, new_lon

# # Define parameters for API requests
# parameters = "WS50M,WD50M,PS,QV2M,T2M"
# start_date = "20200101"
# end_date = "20241231"
# community = "re"
# format_type = "csv"
# header = "true"

# # Define centers for all cities
# city_centers = {
#     "Karachi": (24.860, 67.001),
#     "Faisalabad": (31.450, 73.135),
#     "Milan": (45.464, 9.190),
#     "Dhaka": (23.810, 90.412)
# }

# # Directions and their corresponding angles (in degrees)
# directions = {
#     "N": 0,
#     "NE": 45,
#     "E": 90,
#     "SE": 135,
#     "S": 180,
#     "SW": 225,
#     "W": 270,
#     "NW": 315
# }

# # Generate points for all cities (center + 8 directions)
# cities = {}
# for city, center in city_centers.items():
#     points = [("Center", center[0], center[1])]
#     for direction, angle in directions.items():
#         new_lat, new_lon = calculate_point(center[0], center[1], angle)
#         points.append((direction, new_lat, new_lon))
#     cities[city] = points

# # Base directory for saving files
# base_dir = "./data"

# # NASA POWER API base URL
# base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

# # Set up session with retry strategy
# session = requests.Session()
# retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
# session.mount('https://', HTTPAdapter(max_retries=retries))

# # Iterate through each city and its points
# for city, points in cities.items():
#     # Create city directory if it doesn't exist
#     city_dir = os.path.join(base_dir, city)
#     os.makedirs(city_dir, exist_ok=True)
    
#     for direction, lat, lon in points:
#         # Define output filename with direction prefix
#         filename = f"{direction}_nasa_power_data.csv"
#         filepath = os.path.join(city_dir, filename)
        
#         # Check if the file already exists
#         if os.path.exists(filepath):
#             print(f"Data for {city} ({direction}) already exists, skipping download.")
#             continue
        
#         # Construct the query URL
#         url = f"{base_url}?start={start_date}&end={end_date}&latitude={lat:.3f}&longitude={lon:.3f}&community={community}&parameters={parameters}&format={format_type}&header={header}"
        
#         # Make API request with retries
#         try:
#             response = session.get(url, timeout=30)
#             response.raise_for_status()
#             data = response.text
            
#             # Validate response content
#             if not data.strip():
#                 print(f"Empty response for {city} ({direction})")
#                 continue
                
#             # Save to CSV
#             with open(filepath, "w") as f:
#                 f.write(data)
            
#             print(f"Saved data for {city} ({direction}) to {filepath}")
            
#         except requests.RequestException as e:
#             print(f"Failed to download data for {city} ({direction}) after retries: {e}")
#             continue





import os
import math
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Helper function to calculate points 100 km away at a given bearing
def calculate_point(lat0, lon0, angle_deg, distance_km=100.0):
    R = 6371.0  # Earth radius in km
    angle_rad = math.radians(angle_deg)
    
    # Calculate displacement components
    dNorth = distance_km * math.cos(angle_rad)
    dEast = distance_km * math.sin(angle_rad)
    
    # Calculate latitude change (constant)
    delta_lat = (dNorth / R) * (180.0 / math.pi)
    new_lat = lat0 + delta_lat
    
    # Calculate longitude change (depends on latitude)
    delta_lon = (dEast / (R * math.cos(math.radians(lat0)))) * (180.0 / math.pi)
    new_lon = lon0 + delta_lon
    
    return new_lat, new_lon

# Define parameters for API requests
parameters = "WS50M,WD50M,PS,QV2M,T2M"
start_date = "20150101"
end_date = "20241231"
community = "re"
format_type = "csv"
header = "true"

# Define centers for all cities including Beijing
city_centers = {
    "Karachi": (24.860, 67.001),
    "Faisalabad": (31.450, 73.135),
    "Milan": (45.464, 9.190),
    "Dhaka": (23.810, 90.412),
    "Beijing": (39.9042, 116.4074),  # Beijing center added
    "California":(37.5, -119.5), #  California Central Valley
    "Denver" :(39.7392, -104.9903),
    "Tucumán":(-26.8245, -65.2221),
    "Zabol": (31.03, 61.49),
    "Phoenix":(33.4484, -112.0740)

}

# Directions and their corresponding angles (in degrees)
directions = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
    "SW": 225,
    "W": 270,
    "NW": 315
}

# Generate points for all cities (center + 8 directions)
cities = {}
for city, center in city_centers.items():
    points = [("Center", center[0], center[1])]
    for direction, angle in directions.items():
        new_lat, new_lon = calculate_point(center[0], center[1], angle)
        points.append((direction, new_lat, new_lon))
    cities[city] = points

# Base directory for saving files
base_dir = "./data"

# NASA POWER API base URL
base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

# Set up session with retry strategy
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Iterate through each city and its points
for city, points in cities.items():
    # Create city directory if it doesn't exist
    city_dir = os.path.join(base_dir, city)
    os.makedirs(city_dir, exist_ok=True)
    
    for direction, lat, lon in points:
        # Define output filename with direction prefix
        filename = f"{direction}_nasa_power_data.csv"
        filepath = os.path.join(city_dir, filename)
        
        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"Data for {city} ({direction}) already exists, skipping download.")
            continue
        
        # Construct the query URL
        url = f"{base_url}?start={start_date}&end={end_date}&latitude={lat:.3f}&longitude={lon:.3f}&community={community}&parameters={parameters}&format={format_type}&header={header}"
        
        # Make API request with retries
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            data = response.text
            
            # Validate response content
            if not data.strip():
                print(f"Empty response for {city} ({direction})")
                continue
                
            # Save to CSV
            with open(filepath, "w") as f:
                f.write(data)
            
            print(f"Saved data for {city} ({direction}) to {filepath}")
            
        except requests.RequestException as e:
            print(f"Failed to download data for {city} ({direction}) after retries: {e}")
            continue
