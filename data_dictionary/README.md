# Data Dictionary

This folder contains the **data dictionary** for the Domestic Homicide Reviews (DHR) dataset.

The data dictionary is the *authoritative reference* for what information is captured in the dataset, how it is structured, and what each field means.

## Contents
- `data_dictionary.xlsx` — master version of the dictionary, with one worksheet per table:
  - **DHR** (one row per report)
  - **Victim**
  - **Perpetrator**
  - **Incident**
  - **AgencyContact**
  - **Recommendation**

## How it is structured
Each worksheet in the Excel file corresponds to a dataset “table”.  
Each row within a worksheet describes a field/column, with the following information:
- **Field name** — the name used in the dataset
- **Data type** — e.g. Text, Number, Date
- **Description** — plain English definition of the field
- **Allowed values** — list of permitted values, or reference to an external standard (e.g. ONS ethnicity categories)
- **Nullable?** — whether blanks/unknown values are permitted
- **Notes** — any extra details (e.g. mapping rules, provenance)

## Updating the dictionary
1. Always edit the **Excel file** (`data_dictionary.xlsx`).  
2. If possible, export updated copies to CSV/Markdown so others can preview it in GitHub.  
3. Commit changes with a clear message, e.g. `update victim table with residence_local_authority field`.  
4. Increment the version number in this README (see below).

## Version
- Current version: **v0.1 (draft)**
- Change log:
  - v0.1 — initial draft tables created

---
