from sqlalchemy import create_engine, text

# 1. Database Connection
DB_URI = 'postgresql://admin:secure_password_123@localhost:5432/remediation_db'
engine = create_engine(DB_URI)

# 2. Define the Compliance View Logic
# Using CREATE OR REPLACE ensures this script is idempotent (can be run multiple times safely).
view_sql = text("""
CREATE OR REPLACE VIEW compliance_exceedances AS 
SELECT 
    well_id, 
    sample_date, 
    arsenic_mgl, 
    CASE 
        WHEN arsenic_mgl > 0.010 THEN 'EXCEEDANCE' 
        ELSE 'COMPLIANT' 
    END AS arsenic_status, 
    ST_AsText(geometry) as geometry_wkt 
FROM groundwater_monitoring;
""")

# 3. Execute the Transaction
try:
    with engine.connect() as connection:
        connection.execute(view_sql)
        # SQLAlchemy 2.0+ requires explicit commits for DDL statements
        connection.commit() 
    print("Successfully formalized 'compliance_exceedances' view in PostGIS.")
except Exception as e:
    print(f"Database execution error: {e}")