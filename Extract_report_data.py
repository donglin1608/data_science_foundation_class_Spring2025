import os
import requests
from bs4 import BeautifulSoup

# Base URL for state reports
BASE_URL = "https://traffickinginstitute.org/state-reports/"

# List of state abbreviations (50 states + DC)
STATE_ABBREVIATIONS = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga",
    "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md",
    "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj",
    "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc",
    "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy", "dc"
]

# Define the root save path
ROOT_SAVE_PATH = "/Users/donglinxiong/Downloads/Detecting labor trafficking/all_states_reports"

# Ensure the root directory exists
os.makedirs(ROOT_SAVE_PATH, exist_ok=True)

# Loop through all states
for state in STATE_ABBREVIATIONS:
    state_url = f"{BASE_URL}{state}/"
    state_folder = os.path.join(ROOT_SAVE_PATH, state.upper())  # Create state folder
    os.makedirs(state_folder, exist_ok=True)

    # Request the state report page
    response = requests.get(state_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all report links
        report_links = soup.find_all("a", string=lambda t: t and "State Report" in t)
        report_urls = [link.get('href') for link in report_links]

        print(f"\n📌 Found reports for {state.upper()}: {report_urls}")

        # Download each PDF
        for url in report_urls:
            file_name = os.path.join(state_folder, url.split("/")[-1])  # Extract filename from URL
            pdf_data = requests.get(url)  # Fetch PDF content

            if pdf_data.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(pdf_data.content)
                print(f"✅ Downloaded: {file_name}")
            else:
                print(f"❌ Failed to download {url}, status: {pdf_data.status_code}")

    else:
        print(f"❌ Failed to access {state_url}, status code: {response.status_code}")
