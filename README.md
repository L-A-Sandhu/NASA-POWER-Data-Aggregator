# NASA-POWER-Data-Aggregator
The NASA POWER Data Aggregator is a powerful Python-based tool designed to simplify the retrieval and processing of spatio-temporal weather data from NASA's POWER (Prediction Of Worldwide Energy Resources) API. 

This project includes two Python scripts to download and process spatio-temporal weather data from NASA's POWER (Prediction Of Worldwide Energy Resources) API using the Data Access Viewer (https://power.larc.nasa.gov/data-access-viewer/).

## Introduction

- **`download_nasa_power_data.py`**: Downloads hourly weather data for multiple cities (e.g., Karachi, Beijing, etc.), including the city center and eight points 100 km away in directions (N, NE, E, SE, S, SW, W, NW). Data is sourced from the NASA POWER API.
- **`combine_nasa_power_data.py`**: Combines the downloaded data for a single city from its center and directional points into one CSV file, with columns prefixed by direction (e.g., `C_WS50M` for center wind speed, `N_WS50M` for north wind speed).

## Prerequisites

- Python 3.x
- Required libraries: `requests`, `pandas`, `os`, `math`
- An active internet connection to access the NASA POWER API

## Usage

### Downloading Data

1. Place `download_nasa_power_data.py` in a directory where you want to store the data.
2. Run the script:
   ```bash
   python download_nasa_power_data.py
   ```
3. The script creates a `data` directory (if it doesn’t exist) with subdirectories for each city (e.g., `./data/Karachi`). It downloads hourly weather data for the center and eight directional points, saving them as CSV files (e.g., `Center_nasa_power_data.csv`, `N_nasa_power_data.csv`) in the respective city directories.

### Combining Data

1. Navigate to a city’s directory containing the downloaded CSV files (e.g., `cd ./data/Karachi`).
2. Place `combine_nasa_power_data.py` in this directory.
3. Run the script:
   ```bash
   python combine_nasa_power_data.py
   ```
4. The script combines the data from all points into a single `combined.csv` file in the same directory.
5. Repeat steps 1–4 for each city directory.

**Note**: The combine script must be run separately for each city from within its directory.

## Output

- **Download Script**:
  - Directory structure: `data/<city_name>/<direction>_nasa_power_data.csv`
  - Example files: `data/Karachi/Center_nasa_power_data.csv`, `data/Karachi/N_nasa_power_data.csv`
  - Each CSV contains hourly weather data (2015-01-01 to 2024-12-31) with columns: `YEAR`, `MO`, `DY`, `HR`, `WS50M` (wind speed at 50m), `WD50M` (wind direction at 50m), `PS` (surface pressure), `QV2M` (specific humidity at 2m), `T2M` (temperature at 2m).

- **Combine Script**:
  - File: `<city_directory>/combined.csv`
  - Contains merged data with columns like `YEAR`, `MO`, `DY`, `HR`, `C_WS50M`, `C_WD50M`, ..., `N_WS50M`, `N_WD50M`, ..., up to `NW_T2M`, combining all points’ weather variables with directional prefixes (C for center, N for north, etc.).

