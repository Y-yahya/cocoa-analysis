import pandas as pd
import matplotlib.pyplot as plt

# Data Organization (Task 1)
try:
    df = pd.read_csv('cocoa_production_data.csv')
except FileNotFoundError:
    print("Error: The file 'cocoa_production_data.csv' was not found.")
    print("Please make sure the file is in the same directory as this script.")
    exit()

df_filtered = df[
    (df['Area'].isin(['Ghana', "Côte d'Ivoire"])) &
    (df['Item'] == 'Cocoa, beans')
].copy()

df_pivot = df_filtered.pivot_table(
    index=['Year', 'Area'],
    columns='Element',
    values='Value'
).reset_index()

df_pivot.rename(columns={'Area': 'Country'}, inplace=True)
df_pivot['Country'].replace({"Côte d'Ivoire": "Ivory Coast (Côte d'Ivoire)"}, inplace=True)

required_metrics = ['Year', 'Country', 'Area harvested', 'Yield', 'Production']
df_clean = df_pivot[required_metrics].dropna().copy()
for col in ['Area harvested', 'Yield', 'Production']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

df_ghana = df_clean[df_clean['Country'] == 'Ghana']
df_ivory_coast = df_clean[df_clean['Country'] == "Ivory Coast (Côte d'Ivoire)"]

# Combined Plot, Annotation, and Styling (Task 3 & 4)
COLOR_GHANA_YIELD = '#006400'
COLOR_IVORY_COAST_YIELD = '#FF8C00'
COLOR_GHANA_AREA = '#3CB371'
COLOR_IVORY_COAST_AREA = '#DC143C'

plt.style.use('seaborn-v0_8-whitegrid')

fig, axs = plt.subplots(2, 2, figsize=(16, 14))

fig.suptitle(
    "Comparative Cocoa Production Analysis: Ghana vs. Ivory Coast (1961 - 2020)",
    fontsize=22,
    fontweight='bold',
    y=1.01
)

# Ghana Yield Scatter Plot
axs[0, 0].scatter(df_ghana['Year'], df_ghana['Yield'], color=COLOR_GHANA_YIELD)
axs[0, 0].set_title("Ghana: Cocoa Yield (hg/ha) Over Time", fontsize=16)
axs[0, 0].set_xlabel("Year")
axs[0, 0].set_ylabel("Yield (hg/ha)")
axs[0, 0].grid(True)

# Ivory Coast Yield Scatter Plot
axs[0, 1].scatter(df_ivory_coast['Year'], df_ivory_coast['Yield'], color=COLOR_IVORY_COAST_YIELD)
axs[0, 1].set_title("Ivory Coast: Cocoa Yield (hg/ha) Over Time", fontsize=16)
axs[0, 1].set_xlabel("Year")
axs[0, 1].set_ylabel("Yield (hg/ha)")
axs[0, 1].grid(True)

# Ghana Area Harvested Bar Chart
axs[1, 0].bar(df_ghana['Year'], df_ghana['Area harvested'], color=COLOR_GHANA_AREA)
axs[1, 0].set_title("Ghana: Cocoa Area Harvested (ha) by Year", fontsize=16)
axs[1, 0].set_xlabel("Year")
axs[1, 0].set_ylabel("Area Harvested (ha)")
axs[1, 0].tick_params(axis='x', rotation=45)
axs[1, 0].grid(axis='y')

# Ivory Coast Area Harvested Bar Chart
axs[1, 1].bar(df_ivory_coast['Year'], df_ivory_coast['Area harvested'], color=COLOR_IVORY_COAST_AREA)
axs[1, 1].set_title("Ivory Coast: Cocoa Area Harvested (ha) by Year", fontsize=16)
axs[1, 1].set_xlabel("Year")
axs[1, 1].set_ylabel("Area Harvested (ha)")
axs[1, 1].tick_params(axis='x', rotation=45)
axs[1, 1].grid(axis='y')

fig.tight_layout(rect=[0, 0.03, 1, 0.98])

fig.savefig('final_annotated_cocoa_analysis.pdf')

plt.show()