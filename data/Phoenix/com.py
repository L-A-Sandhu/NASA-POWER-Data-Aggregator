import pandas as pd
import os

# File paths for all the city files
city_files = {
    "Center": "Center_nasa_power_data.csv",
    "N": "N_nasa_power_data.csv",
    "NE": "NE_nasa_power_data.csv",
    "E": "E_nasa_power_data.csv",
    "SE": "SE_nasa_power_data.csv",
    "S": "S_nasa_power_data.csv",
    "SW": "SW_nasa_power_data.csv",
    "W": "W_nasa_power_data.csv",
    "NW": "NW_nasa_power_data.csv"
}

# Define a function to clean up each CSV and read it into a DataFrame
def read_and_clean_csv(file_path):
    # Open the CSV file and search for the row that contains the header
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line with the correct header (YEAR, MO, DY, HR, WS50M, etc.)
    header_row = None
    for i, line in enumerate(lines):
        if "YEAR" in line and "MO" in line and "DY" in line and "HR" in line:
            header_row = i
            break
    
    # If we found the header, read the file from that row onward
    if header_row is not None:
        df = pd.read_csv(file_path, skiprows=header_row)
    else:
        print(f"Header row not found in {file_path}.")
        return pd.DataFrame()  # Return an empty DataFrame if header is not found
    
    return df

# Dictionary to hold dataframes for each city
city_data = {}

# Read data for each city and store in city_data
for city, file_path in city_files.items():
    city_data[city] = read_and_clean_csv(file_path)

# Initialize the final DataFrame with the 'Center' city data (including weather variables with C_ prefix)
center_df = city_data["Center"]
final_df = center_df[["YEAR", "MO", "DY", "HR"]].copy()
final_df["C_WS50M"] = center_df["WS50M"]
final_df["C_WD50M"] = center_df["WD50M"]
final_df["C_PS"] = center_df["PS"]
final_df["C_QV2M"] = center_df["QV2M"]
final_df["C_T2M"] = center_df["T2M"]

# Function to add the corresponding city data with proper prefixes
def add_city_data_to_final_df(df, city_name, prefix):
    city_df = city_data[city_name][["YEAR", "MO", "DY", "HR", "WS50M", "WD50M", "PS", "QV2M", "T2M"]].copy()
    city_df = city_df.rename(columns={
        "WS50M": f"{prefix}_WS50M",
        "WD50M": f"{prefix}_WD50M",
        "PS": f"{prefix}_PS",
        "QV2M": f"{prefix}_QV2M",
        "T2M": f"{prefix}_T2M"
    })
    df = df.merge(city_df, on=["YEAR", "MO", "DY", "HR"], how="left")
    return df

# Define prefixes for all cities (Center uses 'C', others use their keys)
city_prefix_mapping = {
    "Center": "C",
    "N": "N",
    "NE": "NE",
    "E": "E",
    "SE": "SE",
    "S": "S",
    "SW": "SW",
    "W": "W",
    "NW": "NW"
}

# Add data for all cities (including Center, but skip since we already have it)
for city in city_files.keys():
    if city == "Center":
        continue  # Skip Center since we already added it above
    prefix = city_prefix_mapping[city]
    final_df = add_city_data_to_final_df(final_df, city, prefix)

# Save the combined data to a new CSV file
final_df.to_csv("combined.csv", index=False)
print("combined.csv file has been created.")