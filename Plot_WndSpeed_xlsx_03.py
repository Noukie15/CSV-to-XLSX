# pip install pandas xlsxwriter

import pandas as pd
import os
import glob
import tkinter as tk
from tkinter import filedialog

# Zoek alle LOG-bestanden in de map
log_files = glob.glob("LOG*.CSV") + glob.glob("LOG*.csv")

if log_files:
    # Sorteer op modificatietijd (meest recent eerst)
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    # Vraag de gebruiker of ze het recentste bestand willen gebruiken
    root = tk.Tk()
    root.withdraw()  # Verberg het hoofdvenster
    
    choice = tk.messagebox.askyesno(
        "Bestand keuze", 
        f"Meest recente bestand: {os.path.basename(log_files[0])}\n\nWilt u dit bestand gebruiken?",
        icon='question'
    )
    
    if choice:
        csv_bestand = log_files[0]
    else:
        # Laat gebruiker handmatig een bestand kiezen
        csv_bestand = filedialog.askopenfilename(
            title="Selecteer een LOG bestand",
            filetypes=[("CSV files", "*.CSV;*.csv"), ("All files", "*.*")]
        )
        
        if not csv_bestand:
            print("Geen bestand geselecteerd. Script afgebroken.")
            exit()
else:
    # Geen LOG-bestanden gevonden, laat gebruiker handmatig selecteren
    root = tk.Tk()
    root.withdraw()
    
    csv_bestand = filedialog.askopenfilename(
        title="Selecteer een LOG bestand",
        filetypes=[("CSV files", "*.CSV;*.csv"), ("All files", "*.*")]
    )
    
    if not csv_bestand:
        print("Geen bestand geselecteerd. Script afgebroken.")
        exit()

# Genereer Excel bestandsnaam op basis van CSV bestandsnaam
excel_bestand = os.path.splitext(csv_bestand)[0] + ".xlsx"

# Kolombreedtes aanpassbaar maken
kolom_breedtes = {
    'A': 16,  # TIMESTAMP
    'B': 33,  # TIME_SINCE_START_MEASUREMENT
    'C': 15,  # WINDSPEED
    'D': 15   # RPM
    # Voeg meer kolommen toe indien nodig
}

# CSV inladen met timestamp als string
df = pd.read_csv(csv_bestand, dtype={'TIMESTAMP': str})

# Data wegschrijven naar Excel met grafieken
with pd.ExcelWriter(excel_bestand, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    
    # Workbook en worksheet ophalen
    workbook  = writer.book
    worksheet = writer.sheets["Data"]
    
    # --- Kolombreedtes aanpassen ---
    # Kolom A = TIMESTAMP (tekstformaat)
    text_format = workbook.add_format({'num_format': '@'})  # Tekstformaat
    worksheet.set_column(0, 0, kolom_breedtes['A'], text_format)
    
    # Overige kolommen met aangepaste breedtes
    for col_idx, (col_letter, width) in enumerate(kolom_breedtes.items(), start=0):
        if col_letter != 'A':  # Kolom A is al ingesteld
            worksheet.set_column(col_idx, col_idx, width)
    
    # Automatische breedte voor eventuele extra kolommen
    if len(df.columns) > len(kolom_breedtes):
        for i in range(len(kolom_breedtes), len(df.columns)):
            col_name = df.columns[i]
            worksheet.set_column(i, i, len(col_name) + 2)
    
    # --- Grafiek 1: Windsnelheid ---
    chart_wind = workbook.add_chart({"type": "line"})
    chart_wind.add_series({
        "name":       "Windspeed",
        "categories": ["Data", 1, 1, len(df), 1],  # TIME_SINCE_START_MEASUREMENT
        "values":     ["Data", 1, 2, len(df), 2],  # WINDSPEED
        "line":       {"color": "blue"},
    })
    chart_wind.set_title({"name": "Windsnelheid over tijd"})
    chart_wind.set_x_axis({"name": "Tijd sinds start (s)"})
    chart_wind.set_y_axis({"name": "Windsnelheid (m/s)"})
    
    worksheet.insert_chart("F2", chart_wind)
    
    # --- Grafiek 2: RPM ---
    chart_rpm = workbook.add_chart({"type": "line"})
    chart_rpm.add_series({
        "name":       "RPM",
        "categories": ["Data", 1, 1, len(df), 1],
        "values":     ["Data", 1, 3, len(df), 3],  # RPM
        "line":       {"color": "red"},
    })
    chart_rpm.set_title({"name": "RPM over tijd"})
    chart_rpm.set_x_axis({"name": "Tijd sinds start (s)"})
    chart_rpm.set_y_axis({"name": "RPM"})
    
    worksheet.insert_chart("F20", chart_rpm)

print(f"Excel bestand opgeslagen als: {excel_bestand}")