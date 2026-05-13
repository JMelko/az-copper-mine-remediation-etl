# =====================================================================
# Script: run_pipeline.ps1
# Purpose: Orchestrates the ADEQ/CERCLA groundwater ETL pipeline.
# =====================================================================

# 1. Define the absolute path to the project repository
$ProjectPath = "C:\Users\melko\Documents\Environmental_Portfolio\az-copper-mine-remediation-etl"

# 2. Navigate to the project directory
Set-Location -Path $ProjectPath

# 3. Activate the isolated Python virtual environment
& "$ProjectPath\venv\Scripts\Activate.ps1"

# 4. Execute the pipeline sequentially
Write-Output "Starting Pipeline Execution: $(Get-Date)"

Write-Output "Running ETL Pipeline..."
python scripts/01_etl_pipeline.py

Write-Output "Refreshing Compliance Views..."
python scripts/02_create_compliance_view.py

Write-Output "Pipeline Execution Complete: $(Get-Date)"