# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 13:14:36 2024

@author: jvorth
"""

#Script to assign timepoint samples to Sample names and placement in wells.
#If you have issues running the script several times it can help to restart spyder or just restart the kernel under consoles
#This is because Tkinter, the standard GUI toolkit in Python, can encounter issues when run multiple times in the same session, especially in interactive development environments like Spyder

import pandas as pd
import tkinter as tk
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re


def choose_plate():
    # Initialize the global variable to store the plate choice
    global plate_used
    plate_used = None
    
    # Function to handle button click for 96 well plate
    def set_96():
        nonlocal root
        global plate_used
        plate_used = 96
        root.destroy()

    # Function to handle button click for 24 well plate
    def set_24():
        nonlocal root
        global plate_used
        plate_used = 24
        root.destroy()
    
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Choose Plate Type")

    # Create label
    label = tk.Label(root, text="Select the type of plate used:")
    label.pack(pady=10)

    # Create buttons for 96 well plate and 24 well plate
    button_96 = tk.Button(root, text="96 Well Plate", command=set_96)
    button_96.pack(pady=5)

    button_24 = tk.Button(root, text="24 Well Plate", command=set_24)
    button_24.pack(pady=5)

    # Run the Tkinter event loop
    root.mainloop()
    

    # Return the choice
    return plate_used, root

# Function to open a file dialog and return the selected file path
def get_file_path(filetypes, title):
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename(filetypes=filetypes, title=title)
    return file_path

# Function to save a file dialog and return the selected file path
def save_file_path(defaultextension, filetypes, title):
    Tk().withdraw()
    file_path = asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes, title=title)
    return file_path

# Function to process the Excel file
def process_excel(file_path):
    # Read the "List Format" sheet from the Excel file
    df = pd.read_excel(file_path, sheet_name="List Format")
    
    # List of well positions in the desired order depending on if it is 24 or 96 well plate
    if plate_used==24:
        well_positions = [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6'
        ]
    elif plate_used==96:
        well_positions = [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9','A10','A11','A12',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6','B7', 'B8', 'B9','B10','B11','B12',
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6','C7', 'C8', 'C9','C10','C11','C12',
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6','D7', 'D8', 'D9','D10','D11','D12',
            'E1', 'E2', 'E3', 'E4', 'E5', 'E6','E7', 'E8', 'E9','E10','E11','E12',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6','F7', 'F8', 'F9','F10','F11','F12',
            'G1', 'G2', 'G3', 'G4', 'G5', 'G6','G7', 'G8', 'G9','G10','G11','G12',
            'H1', 'H2', 'H3', 'H4', 'H5', 'H6','H7', 'H8', 'H9','H10','H11','H12'
        ]
    # Number of samples in each column
    num_samples = len(well_positions)
    
    # Initialize lists to store the combined data
    combined_samples = []
    plate_info = []
    well_info = []
    reactor_number_info=[]
    sample_number_info=[]

    #sample_number_info=[]
    
    # Process each column
    for column in df.columns:
        plate_number = column.split()[-1]  # Extract the plate number from the column name
        samples = df[column].dropna().tolist()  # Get the samples in the column
        
        
        # Assign wells and store data
        for i, sample in enumerate(samples):
            ###
            if sample =='Empty':
                reactor_number='Empty'
                sample_number='Empty'
            else:
                reactor_part = sample.split('S')[0]
                sample_part = sample.split('S')[1]
                # Formatting with leading zeros
                reactor_number = 'R' + reactor_part[1]+reactor_part[2] if len(reactor_part) >= 3 else 'R0' + reactor_part[1]
                sample_number = 'S' + sample_part.zfill(2)
            ###
            #sample_number = re.search(r'S\d+', samples[i]).group(0)
            combined_samples.append(sample)
            plate_info.append(plate_number)
            well_info.append(well_positions[i % num_samples])
            reactor_number_info.append(reactor_number)
            sample_number_info.append(sample_number)
            #sample_number_info.append(sample_number)
            
    # Create a new DataFrame with the combined data
    combined_df = pd.DataFrame({
        'Sample': combined_samples,
        'Plate': plate_info,
        'Well': well_info,
        'Reactor':reactor_number_info,
        'Timepoint (#)':sample_number_info,
    })
    return combined_df    
        
# Function to process the text or CSV file and extract timepoint information
def process_text_file(file_path):
    #### GEt the stage runs from benchling file
    # Get the text or CSV file path from the user
    text_file_path_benchling = get_file_path(filetypes=[("Text and CSV files", "*.txt *.csv")], title="Select a text or CSV file with benchling stage runs")
    if not text_file_path_benchling:
        print('No text or CSV file selected.')
        return
    df = pd.read_csv(text_file_path_benchling)
    df2 = df[['Reactor/Plate Number', 'Stage Run']]  # Extracting info regarding StageID and Reactor number
    # Apply the function to the 'reactors' column
    #df2['Reactor/Plate Number'] = df['Reactor/Plate Number'].apply(remove_leading_zeros) 
    dmb = dict(df2.values)
    
    # Name to number dict:
    n2n = {chr(65 + i): i + 1 for i in range(8)}  # A-H to 1-8

    with open(file_path, 'r') as infile:
        lines = infile.readlines()
    
    data = []
    regex = r"Bioreactor\s+(\d+)\"\,(\S+)\,\"Sample\s+(\S+)\s+mL+\s.+\s+(\d+)\/([A-Z]+\d+)"
    
    for line in lines:
        matches = re.search(regex, line)
        if matches:
            # Extract and convert timepoint to a numerical value
            time_str = matches.group(2)
            if 'h' in time_str:
                time_value = float(time_str.replace('h', ''))
            else:
                time_value = float(time_str)
                
            data.append({
                #'Reactor': f'R{matches.group(1)}',  # Pad single-digit reactors with leading zeros
                'Reactor': f'R{int(matches.group(1)):02d}',  # Pad single-digit reactors with leading zeros
                'Timepoint (h)': time_str,
                'Time_Value': time_value,
                'Volume': matches.group(3),
                'Plate': matches.group(4),
                'Well': matches.group(5),
                'Well_Number': n2n[matches.group(5)[0]]
            })
    
    ### Removing lines with specific volumes
    #data=data[data.Volume !=2.00]

    csv_df = pd.DataFrame(data)
    csv_df=csv_df[csv_df.Volume != '2.00'] ####### Here you can delete rows with a specific volume. 
    csv_df['Stage run'] = csv_df['Reactor'].map(dmb)  # Coupling StageID to reactor number
    return csv_df

# Main function
def main():
    # Get the Excel file path from the user
    excel_file_path = get_file_path(filetypes=[("Excel files", "*.xlsx *.xls")], title="Select an Excel file with sample placements")
    if not excel_file_path:
        print('No Excel file selected.')
        return

    # Get the text or CSV file path from the user
    text_file_path = get_file_path(filetypes=[("Text and CSV files", "*.txt *.csv")], title="Select a text or CSV file with timepoints")
    if not text_file_path:
        print('No text or CSV file selected.')
        return

    # Process the Excel and text/CSV files
    combined_df = process_excel(excel_file_path)
    timepoints_df = process_text_file(text_file_path)

    # Merge the data on Plate and Well
    merged_df = pd.merge(combined_df, timepoints_df, on=['Plate', 'Well','Reactor'], how='left')

    # Sort the merged DataFrame by 'Reactor' and 'Time_Value' columns
    merged_df = merged_df.sort_values(by=['Reactor', 'Time_Value'])

    # Prompt user to select the base filename and destination directory
    output_file_path = save_file_path(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save the combined Excel file")
    if not output_file_path:
        print('No file path selected to save the combined data.')
        return

    # Save the merged and sorted DataFrame to a new Excel file
    benchling_df = merged_df[merged_df['Time_Value'].notna() & (merged_df['Time_Value'] != '')]
    ## Adding three columns before the one existing and three after for (#) (benchling sample name) (Plate name benchling) (Dilution) (OD1) (OD2)
    # Define the new column titles
    columns_before = ['Benchling sample', 'Plate Benchling', 'Benchling sample SOA']
    columns_after = ['Dilution', 'Raw Absorbance Value #1', 'Raw Absorbance Value #2']
    
    # Create empty DataFrames for the new columns
    df_before = pd.DataFrame(columns=columns_before)
    df_after = pd.DataFrame(columns=columns_after)
    # Concatenate the new columns with the existing DataFrame
    # Here we assume benchling_df is already defined as per your original code
    benchling_df = pd.concat([df_before, benchling_df, df_after], axis=1)
    # Add the sequential numbers to the first column
    benchling_df.insert(0, '#', range(1, len(benchling_df) + 1))
    benchling_df.rename(columns={'Reactor': 'Reactor/Plate Number'}, inplace=True)

    #merged_df.to_excel(output_file_path, index=False)
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        # Write the filtered DataFrame to the 'benchling' sheet
        benchling_df.to_excel(writer, sheet_name='benchling', index=False)
        # Write the original DataFrame to the 'overview' sheet
        merged_df.to_excel(writer, sheet_name='overview', index=False)
        
        
        
        
        # Access the XlsxWriter workbook and worksheet objects
        workbook  = writer.book
        worksheet = writer.sheets['benchling']
        
        # Write text into a specific cell (e.g., A1)
        worksheet.write('T2', 'XXX_PD_001')
        worksheet.write('T3', 'Plate name benchling')
        worksheet.write('T4', 'XXX_PD_001_AMBR_SOA_plate#1')
        worksheet.write('U3','Plate Nr (from AMBR)')
        worksheet.write('U4','11')
        worksheet.write('U2','CAREFUL TO WRITE THE PLATE NR AS TEXT')
        worksheet.write('R1','CDW')
        worksheet.write('S1','Not used')
        worksheet.write('T1','Not used')
        worksheet.write('U1','Not used')
        # Write the formula in the appropriate column (for example, 'OD1' starts from column H)
        # Assuming 'E2' refers to the 2nd row of column E, and 'T4' and 'S4' refer to absolute cells
        for row in range(2, len(benchling_df) + 2):  # Adjusting for Excel 1-based index (DataFrame is 0-based)
            formula = f'=IF(F{row}=$U$4,$T$4,IF(F{row}=$U$5,$T$5))'  # Adjust for absolute references
            worksheet.write_formula(f'C{row}', formula)  # Writing formula to 'OD1' column (H)
        for row in range(2, len(benchling_df) + 2):  # Adjusting for Excel 1-based index (DataFrame is 0-based)
            formula = f'=$T$2&"_"&H{row}&"__"&I{row}&"_"&"SOA"&"_"&"#1"'  # Adjust for absolute references
            worksheet.write_formula(f'D{row}', formula)  # Writing formula to 'OD1' column (H)

        print(f'Combined and sorted data saved as {output_file_path}')
        
    # Return DataFrames for variable explorer visibility
    return combined_df, timepoints_df, merged_df

# Run the main function and capture the returned DataFrames
if __name__ == "__main__":
    # Call the function and save the result in a variable
    plate_used, root = choose_plate()
    combined_df, timepoints_df, merged_df = main()
    
#if 'root' in globals():
#   root.destroy()