import pandas as pd
import openpyxl, pyarrow, fastparquet

# Load the data for anamlysis and visualization
df = pd.read_excel('data/data.xlsx', sheet_name="meta" ,engine='openpyxl')
coord = pd.read_excel('data/coord.xlsx', engine='openpyxl')

# Clean and transform the data
coord.columns = ['location', 'latitude', 'longitude']
df.loc[df['crop_rotation_factor'] == "Single-crop", 'crop_rotation_factor'] = '1 crop'
df.loc[df['crop_rotation_factor'] == "2 crops ", 'crop_rotation_factor'] ='2 crops'
df_merged = pd.merge(df, coord, on='location', how='left')
df_merged.columns = [col.replace('-', '_') for col in df_merged.columns]
df_merged['POX_C'] = df_merged['POX_C'].astype("float")
df_merged['texture_class'] = df_merged['texture_class'].str.strip()

# List of practices to compare
practices = ['tillage_factor', 'crop_rotation_factor', 'drainage', 'cover_crop']
# List of indicators to compare
indicators = ['pH', 'OM_LOI', 'STP', 'STK', 'TOC',
       'TC', 'TN', 'POX_C', 'WAS', 'Min_C', 'WEOC', 'ACE_N']
# List of condition factors
conditions = ['soil_order', 'texture_class', 'state']

# Add a columns with the combination of practices for each data point
df_merged['practices'] = df_merged[practices].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

# Load data for the modal
df_readme = pd.read_excel('data/data.xlsx', sheet_name="readme" ,engine='openpyxl')
df_readme.Variables = [col.replace('-', '_') for col in df_readme.Variables]
df_info = df_readme.loc[df_readme['Variables'].isin(practices + conditions + indicators), ['Variables', 'Description', 'Unit']]

# Save data
df_merged.to_parquet("data/dataset.gzip", compression="gzip")
df_info.to_parquet("data/info.gzip", compression="gzip")

