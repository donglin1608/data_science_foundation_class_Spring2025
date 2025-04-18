import os
import fitz  # PyMuPDF
import pandas as pd
import re

# Root directory containing all state folders
ROOT_DIR = "/Users/donglinxiong/Downloads/Detecting labor trafficking/all_states_reports"

# Define output CSV file structure
FACT_TABLE_COLUMNS = [
    "State", "Year", "New Cases", "Active Cases", "Convictions",
    "Labor Trafficking %", "Sex Trafficking %", "Restitution Orders", "Avg. Prison Sentence (Months)"
]

# Initialize an empty list to store all data
all_fact_table_data = []

# Function to extract state name and year from the first few lines of the document
def extract_state_year(text):
    first_300_chars = text[:300]  # Extract the first few lines of the report

    # Regex pattern to match "State Name YEAR Federal Human Trafficking Report"
    match = re.search(r"(\b[A-Z]{2,}\b)\s+(\d{4})\s+Federal Human Trafficking Report", first_300_chars, re.IGNORECASE)

    if match:
        state_name = match.group(1).title()  # Extract state name
        year = int(match.group(2))  # Extract year
        return state_name, year
    else:
        print(f"⚠️ Warning: Could not find state/year in:\n{first_300_chars[:100]}...")
        return None, None

# Function to extract numeric values from text
def extract_number(text, pattern):
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None

# Function to extract data from a PDF
def extract_data_from_pdf(pdf_path, default_state):
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")

        # Extract state name and year using the new regex-based method
        state, year = extract_state_year(text)

        # If no state is found, use folder name as fallback
        if not state:
            state = default_state

        # Extract other key values
        new_cases = extract_number(text, r"NEW CRIMINAL CASES\s+(\d+)")
        active_cases = extract_number(text, r"ACTIVE CRIMINAL CASES\s+(\d+)")
        convictions = extract_number(text, r"CONVICTIONS\s+(\d+)")
        restitution_orders = extract_number(text, r"RESTITUTION.*?(\d+)%")
        avg_prison_sentence = extract_number(text, r"(\d{2,3})\s+MONTHS PRISON SENTENCE")

        # Extract Trafficking Percentages
        labor_traffic_match = re.search(r"(\d+\.\d+)% LABOR TRAFFICKING", text)
        sex_traffic_match = re.search(r"(\d+\.\d+)% SEX TRAFFICKING", text)
        labor_traffic = float(labor_traffic_match.group(1)) if labor_traffic_match else 0
        sex_traffic = float(sex_traffic_match.group(1)) if sex_traffic_match else 100 - labor_traffic

        return [state, year, new_cases, active_cases, convictions, labor_traffic, sex_traffic, restitution_orders, avg_prison_sentence]

    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
        return None

# Loop through all state folders and process PDFs
for state_folder in os.listdir(ROOT_DIR):
    state_path = os.path.join(ROOT_DIR, state_folder)

    if os.path.isdir(state_path):  # Ensure it's a folder
        for pdf_file in os.listdir(state_path):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(state_path, pdf_file)
                extracted_data = extract_data_from_pdf(pdf_path, state_folder)

                if extracted_data:
                    all_fact_table_data.append(extracted_data)

# Create a single DataFrame for all states and save as a master CSV
if all_fact_table_data:
    master_df = pd.DataFrame(all_fact_table_data, columns=FACT_TABLE_COLUMNS)
    master_csv_path = os.path.join(ROOT_DIR, "Master_Fact_Table.csv")
    master_df.to_csv(master_csv_path, index=False)
    print(f"✅ Master fact table saved: {master_csv_path}")
