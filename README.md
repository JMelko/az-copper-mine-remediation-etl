# Arizona Copper Mine Remediation ETL

## Project Overview
Automated ETL pipeline to process groundwater telemetry and laboratory EDDs for legacy copper mine remediation in Pinal County, AZ. 

## Regulatory Drivers
* ADEQ Aquifer Protection Permit (APP) Quarterly Reporting 
* CERCLA Compliance Tracking 

## Architecture
* **Database:** Dockerized PostgreSQL 15 + PostGIS 3.3 
* **Pipeline:** Python (Pandas/GeoPandas/SQLAlchemy) 
* **Visualization:** Tableau (External) 

---

## Infrastructure Deployment

### Spatial Database
The spatial relational database serves as the immutable destination for cleaned telemetry data. 
To ensure complete reproducibility, the database is containerized using Docker.

To initialize the PostGIS database instance, execute the following command from the repository root using PowerShell:

```powershell
docker-compose -f docker/docker-compose.yml up -d

## Data Pipeline Operations

### 1. Extraction, Transformation, and Loading (`scripts/01_etl_pipeline.py`)
The initial ETL script processes the raw laboratory Electronic Data Deliverables (EDDs). Its primary functions include:
* **Ingestion:** Reads raw, immutable CSV files from the `data/raw/` directory.
* **Hygiene and Normalization:** Programmatically standardizes inconsistent column headers by stripping trailing spaces, converting text to lowercase, and removing special characters to ensure SQL compatibility.
* **Deduplication:** Enforces tabular integrity by dropping duplicate records based on the `well_id` and `sample_date` subset, preventing false compliance exceedances in the final analytical dataset.
* **Spatialization:** Converts tabular coordinates into distinct spatial geometries formatted to the EPSG:32612 (UTM Zone 12N) Coordinate Reference System.
* **Database Loading:** Connects to the local PostGIS container via SQLAlchemy and appends the normalized spatial dataset into the `groundwater_monitoring` table for downstream analysis.