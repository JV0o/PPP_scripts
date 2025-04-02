import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class SamplingSchemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sampling Scheme Generator")

        # Set the window size to be larger
        self.root.geometry("1000x700")

        # Plate type selection
        self.plate_type_var = tk.StringVar(value="24 well plate")
        self.plate_types = ["24 well plate", "96 well plate"]
        self.create_plate_type_frame()

        # Reactor and sample input
        self.reactor_var = tk.IntVar(value=1)
        self.sample_var = tk.IntVar(value=1)
        self.starting_reactor_var = tk.IntVar(value=1)
        self.create_input_frame()

        # End batch sample option
        self.end_batch_var = tk.BooleanVar(value=False)
        self.create_end_batch_frame()

        # Generate and Save buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.generate_button = tk.Button(button_frame, text="Generate Scheme", command=self.generate_scheme)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.save_button = tk.Button(button_frame, text="Save to Excel", command=self.save_to_excel)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Output frame with scrollbars
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.output_frame)
        self.scrollbar_y = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.output_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Storage for the sampling scheme
        self.scheme = []
        self.end_batch_samples = []

    def create_plate_type_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        label = tk.Label(frame, text="Select Plate Type:")
        label.pack(side=tk.LEFT)
        for plate_type in self.plate_types:
            radio_button = tk.Radiobutton(frame, text=plate_type, variable=self.plate_type_var, value=plate_type)
            radio_button.pack(side=tk.LEFT)

    def create_input_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Number of Reactors:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.reactor_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Number of Samples per Reactor:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.sample_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Starting Reactor Number:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.starting_reactor_var).grid(row=2, column=1, padx=5, pady=5)

    def create_end_batch_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        label = tk.Label(frame, text="Take End Batch Sample:")
        label.pack(side=tk.LEFT)
        check_button = tk.Checkbutton(frame, variable=self.end_batch_var)
        check_button.pack(side=tk.LEFT)

    def generate_scheme(self):
        plate_type = self.plate_type_var.get()
        num_reactors = self.reactor_var.get()
        num_samples = self.sample_var.get()
        starting_reactor = self.starting_reactor_var.get()

        if plate_type == "24 well plate":
            columns = 6
            wells_per_plate = 24
            text_height = 8  # Display 4 rows
        else:
            columns = 12
            wells_per_plate = 96
            text_height = 16  # Display 8 rows (double the height for better visibility)

        self.scheme = self.create_sampling_scheme(num_reactors, num_samples, columns, wells_per_plate, starting_reactor)
        self.display_scheme(self.scheme, text_height)

    def create_sampling_scheme(self, num_reactors, num_samples, columns, wells_per_plate, starting_reactor):
        scheme = []
        plate = []
        well_counter = 0
        plate_counter = 1

        # Add end batch samples first if the option is selected
        if self.end_batch_var.get():
            end_batch_samples = [f"R{reactor}S81" for reactor in range(starting_reactor, starting_reactor + num_reactors)]
            plate.extend(end_batch_samples)
            well_counter += len(end_batch_samples)

        # Add normal samples
        for sample in range(num_samples):
            for reactor in range(starting_reactor, starting_reactor + num_reactors):
                well_name = f"R{reactor}S{sample}"
                plate.append(well_name)
                well_counter += 1

                if well_counter == wells_per_plate:
                    scheme.append((plate_counter, plate))
                    plate = []
                    well_counter = 0
                    plate_counter += 1

        # Add any remaining samples to the last plate
        if plate:
            while len(plate) < wells_per_plate:
                plate.append("Empty")
            scheme.append((plate_counter, plate))

        return scheme

    def display_scheme(self, scheme, text_height):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for i, (plate_number, plate) in enumerate(scheme, start=1):
            frame = tk.Frame(self.scrollable_frame, borderwidth=2, relief=tk.GROOVE)
            frame.pack(pady=5)

            # Determine the correct plate name based on the new convention
            plate_row = (plate_number - 1) % 3 + 1
            plate_col = (plate_number - 1) // 3 + 1
            plate_name = f"Frozen {plate_row}{plate_col}"

            label = tk.Label(frame, text=plate_name, font=("Arial", 14))
            label.pack()

            plate_text = tk.Text(frame, height=text_height, width=100)
            plate_text.pack()
            plate_text.insert(tk.END, self.format_plate_text(plate))
            plate_text.config(state=tk.DISABLED)

    def format_plate_text(self, plate):
        plate_type = self.plate_type_var.get()
        if (plate_type == "24 well plate"):
            columns = 6
        else:
            columns = 12

        plate_text = ""
        rows = len(plate) // columns
        for i in range(rows):
            row_text = plate[i * columns:(i + 1) * columns]
            plate_text += "\t".join(row_text) + "\n"
        return plate_text

    def save_to_excel(self):
        if not self.scheme:
            messagebox.showwarning("Warning", "No scheme generated to save.")
            return

        # Collect data for Excel
        excel_data = []
        for i, (plate_number, plate) in enumerate(self.scheme):
            plate_row = (plate_number - 1) % 3 + 1
            plate_col = (plate_number - 1) // 3 + 1
            plate_name = f"Frozen {plate_row}{plate_col}"
            excel_data.append((plate_name, plate))

        # Create DataFrame for the first sheet (list format)
        df_data = {}
        for name, plate in excel_data:
            df_data[name] = plate

        df1 = pd.DataFrame(df_data)

        # Create DataFrame for the second sheet (tabular format)
        def create_plate_df(plate, columns):
            rows = len(plate) // columns
            plate_rows = []
            for i in range(rows):
                row_text = plate[i * columns:(i + 1) * columns]
                plate_rows.append(row_text)
            return pd.DataFrame(plate_rows)

        tabular_data = {}
        for name, plate in excel_data:
            if "24 well plate" in self.plate_type_var.get():
                tabular_data[name] = create_plate_df(plate, 6)
            else:
                tabular_data[name] = create_plate_df(plate, 12)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if not file_path:
            return

        with pd.ExcelWriter(file_path) as writer:
            df1.to_excel(writer, sheet_name='List Format', index=False)
            for name, df in tabular_data.items():
                df.to_excel(writer, sheet_name=name, index=False, header=False)

            # Additional sheets for 24 well plate
            if self.plate_type_var.get() == "24 well plate":
                # Create 1Col_List sheet
                one_col_list = df1.melt(var_name='Plate', value_name='Sample').dropna()['Sample'].reset_index(drop=True)
                one_col_list.to_excel(writer, sheet_name='1Col_List', index=False, header=False)

                # Create new sheet from 1Col_List with columns of 16 rows
                col_count = -(-len(one_col_list) // 16)  # Ceiling division to get the number of columns needed
                rows_16 = [one_col_list[i:i + 16].reset_index(drop=True) for i in range(0, len(one_col_list), 16)]
                df_16 = pd.concat(rows_16, axis=1)
                df_16.columns = [f'Col{i + 1}' for i in range(col_count)]
                df_16.to_excel(writer, sheet_name='Cols_16_Rows', index=False, header=False)

                # Create new sheets with 8x12 matrices filled column-wise
                matrix_count = (len(one_col_list) + 95) // 96  # Calculate the number of 8x12 matrices needed
                for sheet_num in range(matrix_count):
                    matrix_8x12 = pd.DataFrame(index=range(8), columns=range(12))
                    for i in range(96):
                        sample_index = sheet_num * 96 + i
                        if sample_index >= len(one_col_list):
                            break
                        col, row = divmod(i, 8)
                        matrix_8x12.iloc[row, col] = one_col_list[sample_index]
                    sheet_name = f'Matrix_8x12_{sheet_num + 1}'
                    matrix_8x12.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

        messagebox.showinfo("Success", "File saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SamplingSchemeApp(root)
    root.mainloop()