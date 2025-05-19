import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Function to select files using tkinter file dialog
def select_file(title="Select a file"):
    root = tk.Tk()
    root.lift()  # Bring window to front
    root.attributes("-topmost", True)  # Keep on top
    root.after_idle(root.attributes, "-topmost", False)  # Reset after it's visible
    root.withdraw()  # Hide the root window
    
    file_path = filedialog.askopenfilename(
        parent=root,
        title=title,
        filetypes=(("All supported files", "*.csv *.xlsx *.xls"), ("All files", "*.*"))
    )
    root.destroy()
    return file_path

# Function to select save location
def select_save_path():
    root = tk.Tk()
    root.lift()
    root.attributes("-topmost", True)
    root.focus_force()

    save_path = filedialog.asksaveasfilename(
        parent=root,
        defaultextension=".xlsx",  # Default to Excel
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))  # Default filter is Excel
    )

    root.destroy()
    return save_path

# Main function to merge tables
def merge_tables():
    print("Please select AC_IDs_benchling:")
    file1 = select_file("Select AC_IDs_benchling")
    if not file1:
        print("No file selected for the first table. Exiting.")
        return

    print("Please select platesample_name:")
    file2 = select_file("Select platesample_name")
    if not file2:
        print("No file selected for the second table. Exiting.")
        return

    # Load the tables
    try:
        table1 = pd.read_csv(file1) if file1.endswith('.csv') else pd.read_excel(file1)
        table2 = pd.read_csv(file2) if file2.endswith('.csv') else pd.read_excel(file2)
        print(f"Successfully loaded {file1} and {file2}")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Get common column
    common_column = input("Enter the name of the common column: ")

    # Merge tables
    try:
        merged_table = pd.merge(table1, table2, on=common_column, how='inner')
        print("Tables successfully merged!")
    except KeyError:
        print(f"Error: The column '{common_column}' does not exist in one or both tables.")
        return

    # Ask where to save
    print("Please select a location to save the merged table:")
    save_path = select_save_path()

    if not save_path:
        print("No save location selected. Exiting.")
        return

    # Save merged file
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