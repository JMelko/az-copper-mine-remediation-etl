import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd

# 1. Database Connection
# Utilizing SQLAlchemy to map our Pandas DataFrame to the PostgreSQL instance.
# Credentials match the docker-compose.yml configuration.
DB_URI = 'postgresql://admin:secure_password_123@localhost:5432/remediation_db'
engine = create_engine(DB_URI)

# 2. Ingest Raw Data
# Treating the raw directory as an immutable chain of custody.
raw_data_path = 'data/raw/lab_report_2023_q1.csv'
df = pd.read_csv(raw_data_path)

# 3. Data Validation and Hygiene
# Environmental datasets must have normalized headers for SQL compatibility.
# We strip trailing spaces, convert to lowercase, and replace spaces with underscores.
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.columns = df.columns.str.replace('/', '') # Remove special characters from units

# Resolve duplicate registry IDs. A single well cannot be sampled twice at the exact same time 
# without being marked as a duplicate quality control (QC) sample.
df = df.drop_duplicates(subset=['well_id', 'sample_date'])

print("Data normalized and deduplicated.")
print(df.head())

# 4. Spatialization
# The Easting and Northing values represent projected coordinates. 
# Pinal County, AZ falls within UTM Zone 12N. The corresponding EPSG code is 32612.
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df['easting'], df['northing']),
    crs="EPSG:32612"
)

print("\nSpatialization complete. CRS set to:", gdf.crs)

# 5. Database Loading
# Push the GeoDataFrame to the PostGIS container.
# Using if_exists='append' ensures future monthly lab reports will add to this table rather than overwrite it.
try:
    gdf.to_postgis(
        name='groundwater_monitoring',
        con=engine,
        if_exists='append',
        index=False
    )
    print("Successfully loaded spatial data into PostGIS table: 'groundwater_monitoring'")
except Exception as e:
    print(f"Database insertion error: {e}")