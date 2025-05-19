import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Function to select files using tkinter file dialog
def select_file(title="Select a file"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title, filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")))
    return file_path

# Main function to merge tables
def merge_tables():
    # Step 1: Ask the user to select both files
    print("Please select the first table (CSV/Excel):")
    file1 = select_file("Select the first table")
    if not file1:
        print("No file selected for the first table. Exiting.")
        return

    print("Please select the second table (CSV/Excel):")
    file2 = select_file("Select the second table")
    if not file2:
        print("No file selected for the second table. Exiting.")
        return

    # Step 2: Load the tables into pandas DataFrames
    try:
        if file1.endswith('.csv'):
            table1 = pd.read_csv(file1)
        else:
            table1 = pd.read_excel(file1)
        
        if file2.endswith('.csv'):
            table2 = pd.read_csv(file2)
        else:
            table2 = pd.read_excel(file2)
        
        print(f"Successfully loaded {file1} and {file2}")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Step 3: Ask the user to input the name of the common column
    common_column = input("Enter the name of the common column: ")

    # Step 4: Merge the tables based on the common column
    try:
        merged_table = pd.merge(table1, table2, on=common_column, how='inner')  # 'inner' join by default
        print("Tables successfully merged!")
    except KeyError:
        print(f"Error: The column '{common_column}' does not exist in one or both tables.")
        return

    # Step 5: Ask where to save the merged file
    print("Please select a location to save the merged table:")
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")))

    if not save_path:
        print("No save location selected. Exiting.")
        return

    # Step 6: Save the merged table
    try:
        if save_path.endswith('.csv'):
            merged_table.to_csv(save_path, index=False)
        else:
            merged_table.to_excel(save_path, index=False)
        
        print(f"Merged table saved to {save_path}")
    except Exception as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    merge_tables()