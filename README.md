# CSV-to-XLSX

This Python script converts **LOG CSV files** into an **Excel file**, sets column widths, and automatically generates charts for **windspeed** and **RPM**. It is interactive, allowing you to choose which file to use if multiple files are present.

---

## Features

1. **CSV File Detection**
   - Automatically searches for files starting with `LOG` and ending with `.CSV` or `.csv`.
   - Sorts files by modification date (most recent first).

2. **File Selection**
   - Prompts to use the most recent file.
   - Alternatively, allows manual file selection via a file dialog.

3. **CSV to Excel Conversion**
   - Reads the CSV file using **pandas**.
   - Creates an Excel file with the same name as the CSV file but with `.xlsx` extension.

4. **Column Formatting**
   - Sets specific column widths for important columns like `TIMESTAMP`, `WINDSPEED`, and `RPM`.
   - Extra columns are automatically sized to fit the column name.

5. **Automatic Charts**
   - **Windspeed**: blue line chart (x-axis = time since start, y-axis = windspeed in m/s)
   - **RPM**: red line chart (x-axis = time since start, y-axis = RPM)
   - Charts are added to the Excel sheet automatically.

---

## Requirements

- Python 3.x
- Packages:
  ```bash
  pip install pandas xlsxwriter
