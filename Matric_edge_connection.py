import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = '/Users/donglinxiong/Downloads/Detecting labor trafficking/all_states_reports/Master_Fact_Table-copy1.xlsx'
df = pd.read_excel(file_path, sheet_name='Master_Fact_Table-copy1')

# Standardize column names by stripping whitespace
columns = [col.strip() for col in df.columns]
df.columns = columns

# Ensure 'Year' is numeric to avoid comparison issues
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Try to identify the closest matching column names
print("Available columns:", df.columns.tolist())

# Filter the most recent year (e.g., 2021)
latest_year = df['Year'].max()
df_latest = df[df['Year'] == latest_year].copy()

# Convert trafficking columns to float
sex_col = [col for col in df.columns if 'Sex' in col][0]
labor_col = [col for col in df.columns if 'Labor' in col][0]
df_latest[sex_col] = pd.to_numeric(df_latest[sex_col], errors='coerce')
df_latest[labor_col] = pd.to_numeric(df_latest[labor_col], errors='coerce')

# Drop rows with missing data
df_latest = df_latest.dropna(subset=[sex_col, labor_col])

# Sort states alphabetically for a clean radial layout
df_latest = df_latest.sort_values('State')

# Radial chart setup
states = df_latest['State'].tolist()
num_states = len(states)
angles = np.linspace(0, 2 * np.pi, num_states, endpoint=False)

# Normalize values to be plotted as bars
sex = df_latest[sex_col].values
labor = df_latest[labor_col].values

# Plot
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))

# Outer ring - Labor
bars1 = ax.bar(angles, labor, width=0.3, color='tomato', label='Labor Trafficking')
# Inner ring - Sex
bars2 = ax.bar(angles, sex, width=0.2, color='royalblue', label='Sex Trafficking')

# Label each bar with the state
ax.set_xticks(angles)
ax.set_xticklabels(states, fontsize=9, rotation=90)

# Remove radial labels
ax.set_yticklabels([])
ax.set_title(f"Human Trafficking Types by State ({int(latest_year)})", va='bottom', fontsize=16)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))

plt.tight_layout()
plt.show()
