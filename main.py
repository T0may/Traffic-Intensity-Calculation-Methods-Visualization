import tkinter as tk
from tkinter import *
from tkinter import font, filedialog, IntVar, scrolledtext
from os.path import expanduser
import seaborn as sns
import matplotlib.pyplot as plt
import tempfile

#variables
BG_COLOR = "#606166"

# Main window
window = tk.Tk()
window.title("Traffic Intensity Calculation Methods Visualization")
window.geometry("620x520")
window.resizable(False, False)
window.configure(bg=BG_COLOR)
label_font = font.Font(size=13)

#Functions
def insert_CallIntensity_path(path):
    if path:
        entry_CallIntensity_path.delete(0, tk.END)
        entry_CallIntensity_path.insert(0, path)

def insert_HandlingTime_path(path):
    if path:
        entry_HandlingTime_path.delete(0, tk.END)
        entry_HandlingTime_path.insert(0, path)

def browse_HandlingTime_file():
    input_file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("TXT files", "*.txt")], initialdir=expanduser("~") + "/Desktop/")
    insert_HandlingTime_path(input_file_path)

def browse_CallIntensity_file():
    input_file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("TXT files", "*.txt")], initialdir=expanduser("~") + "/Desktop/")
    insert_CallIntensity_path(input_file_path)

def save_to_file(handling_time_data, intensity_time_data):
    temp_dir = tempfile.gettempdir()

    # Define file paths for saving handling time and intensity data
    handling_time_file_path = tempfile.mktemp(suffix='.txt', dir=temp_dir)
    intensity_file_path = tempfile.mktemp(suffix='.txt', dir=temp_dir)

    # Write handling time data to handling_time.txt
    with open(handling_time_file_path, "w") as handling_time_file:
        handling_time_file.write(handling_time_data)

    # Write intensity data to intensity.txt
    with open(intensity_file_path, "w") as intensity_file:
        intensity_file.write(intensity_time_data)

    insert_CallIntensity_path(intensity_file_path)
    insert_HandlingTime_path(handling_time_file_path)

    print(f"HadlingTime: {handling_time_data}\n IntensityTime: {intensity_time_data}")

def insert_data_manually():
    newWindow = Toplevel(window)
    newWindow.title("Insert Data Manually")

    handling_time_data = scrolledtext.ScrolledText(newWindow,wrap=tk.WORD, width=40, height=20)
    handling_time_data.grid(column=0, row=0)
    intensity_time_data = scrolledtext.ScrolledText(newWindow,wrap=tk.WORD, width=40, height=20)
    intensity_time_data.grid(column=1, row=0)

    save_data_button = tk.Button(newWindow, text="Save Data", command=lambda: save_to_file(handling_time_data.get("1.0", tk.END), intensity_time_data.get("1.0", tk.END)))
    save_data_button.grid(column = 0, row=1, padx=20, pady=15, columnspan = 2)

    handling_time_data.focus()

def generate_chart():
    start_time = int(entry_start_hour.get()) if entry_start_hour.get() else 0
    end_time = int(entry_end_hour.get()) if entry_end_hour.get() else 24

    input_data = entry_HandlingTime_path.get()
    with open(input_data, "r") as myfile:
        avg_time = time_average(myfile)

    input_data = entry_CallIntensity_path.get()
    time_table = []
    int_table = []
    with open(input_data, "r") as myfile:
        for el in myfile:
            el_table = el.split()
            time_table.append(el_table[0])

            if any(c.isalpha() for c in el_table[1]):
                int_table.append((float(el_table[1].replace(',', '.'))))
            else:
                int_table.append(float(el_table[1]))

    traffic_table = [intensity*avg_time for intensity in int_table]
    time_table_hours = [int(time) / 60 for time in time_table]

    filtered_traffic_table = []
    filtered_time_table = []
    for i in range(len(time_table_hours)):
        if start_time <= time_table_hours[i] <= end_time:
            filtered_traffic_table.append(traffic_table[i])
            filtered_time_table.append(time_table_hours[i])

    #generate chart
    plt.figure(figsize=(8, 6))
    sns.lineplot(x = filtered_time_table, y = filtered_traffic_table)
    plt.xlabel("Time (hours)")
    plt.ylabel("Traffic Intenisty")
    plt.title("Traffic Intensity Over Time")
    plt.xticks(range(start_time, end_time + 1))
    plt.xlim(start_time, end_time)

    plt.show()

def time_average(file):
    total = 0
    count = 0
    for line in file:
        num = float(line)
        total += num
        count += 1
    if count > 0:
         return total/count

# Choosing method
button_frame = tk.Frame(window)
button_frame.configure(bg=BG_COLOR)
button_frame.pack(pady = 50, padx=30)

input_label_methods = tk.Label(button_frame, text="Choose the calculation method", bg=BG_COLOR, font=label_font)
input_label_methods.grid(row=0, column=0, columnspan=2, pady=10)

v = IntVar(button_frame)

method1_button = tk.Radiobutton(button_frame, text="Method 1", variable=v, value=1)
method1_button.grid(row=1, column=0, padx=20, pady=5)
method2_button = tk.Radiobutton(button_frame, text="Method 2", variable=v, value=2)
method2_button.grid(row=1, column=1, padx=20, pady=5)

# Choose the method of inserting data
# Handling time
input_label_data = tk.Label(button_frame, text="Import 'Handling Time'", bg=BG_COLOR, font=label_font)
input_label_data.grid(row = 2, pady=(20, 5),  columnspan=2)

input_button = tk.Button(button_frame, text="Insert manually", command=insert_data_manually)
input_button.grid(row=3, padx=20, pady=5)
file_button = tk.Button(button_frame, text="Choose from file", command=browse_HandlingTime_file)
file_button.grid(row=3, column=1, padx=20, pady=5)

entry_HandlingTime_path = tk.Entry(button_frame, width=50, bg="#797a7e")
entry_HandlingTime_path.grid(row=4, padx=20, columnspan=2)

#Call intensity
input_label_data = tk.Label(button_frame, text="Import 'Call intensity'", bg=BG_COLOR, font=label_font)
input_label_data.grid(row = 5, pady=(20, 5),  columnspan=2)

input_button = tk.Button(button_frame, text="Insert manually", command = insert_data_manually)
input_button.grid(row=6, padx=20, pady=5)
file_button = tk.Button(button_frame, text="Choose from file", command=browse_CallIntensity_file)
file_button.grid(row=6, column=1, padx=20, pady=5)

entry_CallIntensity_path = tk.Entry(button_frame, width=50, bg="#797a7e", )
entry_CallIntensity_path.grid(row=7, padx=20, columnspan=2)

#Input range
label_start_hour = tk.Label(button_frame, text="Start Hour:", bg=BG_COLOR)
label_start_hour.grid(row=8, column=0, pady=(20, 5))

label_end_hour = tk.Label(button_frame, text="End Hour:", bg=BG_COLOR)
label_end_hour.grid(row=8, column=1, pady=(20, 5))

entry_start_hour = tk.Entry(button_frame, bg="#797a7e")
entry_start_hour.grid(row=9, column=0)

entry_end_hour = tk.Entry(button_frame, bg="#797a7e")
entry_end_hour.grid(row=9, column=1)

#Generate chart
generate_button = tk.Button(button_frame, text="Generate Chart", command=generate_chart)
generate_button.grid(row=10, padx=20, pady=15, columnspan = 2)

window.mainloop()