# Arizona Copper Mine Remediation ETL

## Project Overview
Automated ETL pipeline to process groundwater telemetry and laboratory EDDs for legacy copper mine remediation in Pinal County, AZ. 

## Regulatory Drivers
* ADEQ Aquifer Protection Permit (APP) Quarterly Reporting
* CERCLA Compliance Tracking

## Architecture
* **Database:** Dockerized PostgreSQL + PostGIS
* **Pipeline:** Python (Pandas/GeoPandas/SQLAlchemy)
* **Visualization:** Tableau (External)