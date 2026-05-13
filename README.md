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

### 2. View Generation (`scripts/02_create_compliance_view.py`)
This script abstracts complex regulatory logic into the database layer by generating SQL `VIEW`s. 
* **Idempotency:** Utilizes `CREATE OR REPLACE` logic to securely establish or update the `compliance_exceedances` view.
* **Regulatory Abstraction:** Evaluates raw chemical concentrations against ADEQ/CERCLA Maximum Contaminant Levels (MCLs) to programmatically flag exceedances, providing a Single Source of Truth for downstream GIS and Tableau visualization.

## Analytical Deliverables

### Compliance Exceedance View
To support downstream visualization and ensure strict regulatory adherence, compliance logic is enforced at the database level via a SQL `VIEW` (`compliance_exceedances`). 

* **Logic:** Evaluates raw heavy metal concentrations against regulatory Maximum Contaminant Levels (MCLs). For example, Arsenic concentrations strictly greater than 0.010 mg/L are flagged as `EXCEEDANCE`.
* **Output:** A spatial dataset containing well IDs, sample dates, categorized compliance statuses, and Well-Known Text (WKT) geometries.
* **Integration:** This view serves as the direct, read-only data source for the client's Tableau dashboard, ensuring all mapping and reporting rely on a centralized, immutable source of truth.