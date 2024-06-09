import tkinter as tk
from tkinter import *
from tkinter import font, filedialog, IntVar, scrolledtext, messagebox
from os.path import expanduser
import seaborn as sns
import matplotlib.pyplot as plt
import tempfile

# variables
BG_COLOR = "#606166"

# Main window
window = tk.Tk()
window.title("Traffic Intensity Calculation Methods Visualization")
window.geometry("620x520")
window.resizable(False, False)
window.configure(bg=BG_COLOR)
label_font = font.Font(size=13)


# Functions
def insert_CallIntensity_path(path):
    if path:
        entry_CallIntensity_path.delete(0, tk.END)
        entry_CallIntensity_path.insert(0, path)


def insert_HandlingTime_path(path):
    if path:
        entry_HandlingTime_path.delete(0, tk.END)
        entry_HandlingTime_path.insert(0, path)


def browse_HandlingTime_file():
    input_file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("TXT files", "*.txt")],
                                                 initialdir=expanduser("~") + "/Desktop/")
    insert_HandlingTime_path(input_file_path)


def browse_CallIntensity_file():
    input_file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("TXT files", "*.txt")],
                                                 initialdir=expanduser("~") + "/Desktop/")
    insert_CallIntensity_path(input_file_path)


def save_to_file(handling_time_data, intensity_time_data, newWindow):
    temp_dir = tempfile.gettempdir()

    if handling_time_data:
        # Define file path for saving handling time
        handling_time_file_path = tempfile.mktemp(suffix='.txt', dir=temp_dir)

        # Write handling time data to handling_time.txt
        with open(handling_time_file_path, "w") as handling_time_file:
            handling_time_file.write(handling_time_data)

        insert_HandlingTime_path(handling_time_file_path)
        newWindow.destroy()

    if intensity_time_data:
        # Define file path for intensity data
        intensity_file_path = tempfile.mktemp(suffix='.txt', dir=temp_dir)

        # Write intensity data to intensity.txt
        with open(intensity_file_path, "w") as intensity_file:
            intensity_file.write(intensity_time_data)

        insert_CallIntensity_path(intensity_file_path)
        newWindow.destroy()

def insert_handling_time_manually():
    newWindow = Toplevel(window)
    newWindow.title("Insert Handling Time Manually")

    handling_time_data = scrolledtext.ScrolledText(newWindow, wrap=tk.WORD, width=60, height=30)
    handling_time_data.grid(column=0, row=0)

    save_data_button = tk.Button(newWindow, text="Save Data",
                                 command=lambda: save_to_file(handling_time_data.get("1.0", tk.END), False, newWindow))
    save_data_button.grid(column=0, row=1, padx=20, pady=15, columnspan=2)

    handling_time_data.focus()

def validate_hour(entry, name):
    try:
        value = int(entry.get())
        if 0 <= value <= 24:
            return True
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", f"{name} must be an integer between 0 and 24.")
        return False

def insert_intensity_time_manually():
    newWindow = Toplevel(window)
    newWindow.title("Insert Intensity Time Manually")

    intensity_time_data = scrolledtext.ScrolledText(newWindow, wrap=tk.WORD, width=60, height=30)
    intensity_time_data.grid(column=0, row=0)

    save_data_button = tk.Button(newWindow, text="Save Data",
                                 command=lambda: save_to_file(False, intensity_time_data.get("1.0", tk.END), newWindow))
    save_data_button.grid(column=0, row=1, padx=20, pady=15, columnspan=2)

    intensity_time_data.focus()

def generate_chart():

    if not (validate_hour(entry_start_hour, "Start Hour") and validate_hour(entry_end_hour, "End Hour")):
        return

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

            # if any(c.isdecimal() for c in el_table[1]):
            int_table.append((float(el_table[1].replace(',', '.'))))
            # else:
            # int_table.append(float(el_table[1]))

    traffic_table = [intensity * avg_time for intensity in int_table]
    time_table_hours = [int(time) / 60 for time in time_table]

    filtered_traffic_table = []
    filtered_time_table = []
    for i in range(len(time_table_hours)):
        if start_time <= time_table_hours[i] <= end_time:
            filtered_traffic_table.append(traffic_table[i])
            filtered_time_table.append(time_table_hours[i])

    # generate chart
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=filtered_time_table, y=filtered_traffic_table)
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
        return total / count

def calculate_intensity(file):
    total = 0
    for line in file:
        num = float(line)
        total += num
    return total/86400

def show_calculation_result():
    input_data = entry_HandlingTime_path.get()
    with open(input_data, "r") as myfile:
        CallIntensity_result = calculate_intensity(myfile)
    
    global result
    result = CallIntensity_result
    result_label.config(text=f"Wynik: {result}")

# Choosing method
def Method1_gui():
    entry_HandlingTime_path.grid(row=4, padx=20, columnspan=2)
    entry_CallIntensity_path.grid(row=7, padx=20, columnspan=2)
    entry_start_hour.grid(row=9, column=0)
    entry_end_hour.grid(row=9, column=1)
    intensity_label_data.grid(row=5, pady=(20, 5), columnspan=2)
    handling_label_data.grid(row=2, pady=(20, 5), columnspan=2)
    insert_CallIntensity_button.grid(row=6, padx=20, pady=5)
    input_CallIntensity_button.grid(row=6, column=1, padx=20, pady=5)
    generate_button.grid(row=10, padx=20, pady=15, columnspan=2)
    label_start_hour.grid(row=8, column=0, pady=(20, 5))
    label_end_hour.grid(row=8, column=1, pady=(20, 5))
    show_calculation_button.grid_forget()
    entry_HandlingTime_path.delete(0, tk.END)
    result_label.grid_forget()


def Method2_gui():
    entry_CallIntensity_path.grid_forget()
    entry_start_hour.grid_forget()
    entry_end_hour.grid_forget()
    intensity_label_data.grid_forget()
    insert_CallIntensity_button.grid_forget()
    input_CallIntensity_button.grid_forget()
    generate_button.grid_forget()
    label_start_hour.grid_forget()
    label_end_hour.grid_forget()
    show_calculation_button.grid(row=5, pady=(20, 5), columnspan=2)
    entry_HandlingTime_path.delete(0, tk.END)
    result_label.grid(row=6, pady=(20, 5), columnspan=2)

def open_help_window():
    help_window = Toplevel(window)
    help_window.title("Help")

    help_frame = Frame(help_window)
    help_frame.pack(pady=10, padx=10)

    help_text = """
    Witamy w Narzędziu do Wizualizacji i Obliczania Natężenia Ruchu!

    To narzędzie pozwala na wizualizację i obliczanie natężenia ruchu za pomocą dwóch różnych metod.

    1. **Wybór Metody Obliczeń:**
       - Metoda 1: Wizualizacja natężenia ruchu w określonym przedziale czasowym.
       - Metoda 2: Obliczanie całkowitego natężenia ruchu w ciągu dnia.
       Wybierz pożądaną metodę, klikając odpowiedni przycisk radiowy.

    2. **Wprowadzenie Danych o Czasie Obsługi:**
       - Wstaw ręcznie: Otwiera nowe okno, w którym możesz wprowadzić dane o czasie obsługi.
       - Wybierz z pliku: Otwiera okno dialogowe, aby wybrać plik tekstowy zawierający dane o czasie obsługi.
       Dane o czasie obsługi powinny być podane w sekundach, jedna wartość na linię w formacie jak na zdjęciu wyżej:

    3. **Wprowadzenie Danych o Natężeniu Ruchu (tylko Metoda 1):**
       - Wstaw ręcznie: Otwiera nowe okno, w którym możesz wprowadzić dane o natężeniu ruchu.
       - Wybierz z pliku: Otwiera okno dialogowe, aby wybrać plik tekstowy zawierający dane o natężeniu ruchu.
       Dane o natężeniu ruchu powinny być podane w Erlangach, z czasem i natężeniem oddzielonymi spacją w formacie jak na zdjęciu wyżej.

    4. **Określenie Przedziału Czasowego (tylko Metoda 1):**
       - Godzina początkowa: Godzina początkowa dla wizualizacji (0 do 24).
       - Godzina końcowa: Godzina końcowa dla wizualizacji (0 do 24).

    5. **Generowanie Wykresu (tylko Metoda 1):**
       - Kliknij "Generuj Wykres", aby wizualizować natężenie ruchu w określonym przedziale czasowym.

    6. **Obliczanie (tylko Metoda 2):**
       - Kliknij "Oblicz", aby obliczyć całkowite natężenie ruchu w ciągu dnia.


    **Obliczenia Matematyczne:**

    - **Średni Czas Obsługi:** Średni czas obsługi w sekundach, obliczony na podstawie wprowadzonych danych.
      Wzór: Średni Czas Obsługi = Suma Czasów Obsługi / Liczba Wpisów

    - **Natężenie Ruchu:** Całkowite natężenie ruchu, obliczone jako iloczyn natężenia ruchu i średniego czasu obsługi.
      Wzór: Natężenie Ruchu = Suma(Natężenie Ruchu * Średni Czas Obsługi) / 86400s

    """
    help_label = Label(help_window, text=help_text)

    example_image = PhotoImage(file="data_format_example.png")
    image_label = Label(help_frame, image=example_image)
    image_label.image = example_image 
    image_label.pack()

    help_label.pack()


button_frame = tk.Frame(window)
button_frame.configure(bg=BG_COLOR)
button_frame.pack(pady=50, padx=30)

helpim = PhotoImage(file="help.png").subsample(30)

help = tk.Button(window, bd=0, image=helpim, command=open_help_window)
help.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

input_label_methods = tk.Label(button_frame, text="Choose the calculation method", bg=BG_COLOR, font=label_font)
input_label_methods.grid(row=0, column=0, columnspan=2, pady=10)

v = IntVar(button_frame, value=1)

method1_button = tk.Radiobutton(button_frame, text="Method 1", variable=v, value=1, command=Method1_gui)
method1_button.grid(row=1, column=0, padx=20, pady=5)
method2_button = tk.Radiobutton(button_frame, text="Method 2",variable=v, value=2, command=Method2_gui)
method2_button.grid(row=1, column=1, padx=20, pady=5)

# Choose the method of inserting data
# Handling time
handling_label_data = tk.Label(button_frame, text="Import 'Handling Time'", bg=BG_COLOR, font=label_font)
handling_label_data.grid(row=2, pady=(20, 5), columnspan=2)

insert_HandlingTime_button = tk.Button(button_frame, text="Insert manually", command=insert_handling_time_manually)
insert_HandlingTime_button.grid(row=3, padx=20, pady=5)
input_handlingTime_button = tk.Button(button_frame, text="Choose from file", command=browse_HandlingTime_file)
input_handlingTime_button.grid(row=3, column=1, padx=20, pady=5)

entry_HandlingTime_path = tk.Entry(button_frame, width=50, bg="#797a7e")
entry_HandlingTime_path.grid(row=4, padx=20, columnspan=2)

# Call intensity
intensity_label_data = tk.Label(button_frame, text="Import 'Call intensity'", bg=BG_COLOR, font=label_font)
intensity_label_data.grid(row=5, pady=(20, 5), columnspan=2)

insert_CallIntensity_button = tk.Button(button_frame, text="Insert manually", command=insert_intensity_time_manually)
insert_CallIntensity_button.grid(row=6, padx=20, pady=5)
input_CallIntensity_button = tk.Button(button_frame, text="Choose from file", command=browse_CallIntensity_file)
input_CallIntensity_button.grid(row=6, column=1, padx=20, pady=5)

entry_CallIntensity_path = tk.Entry(button_frame, width=50, bg="#797a7e", )
entry_CallIntensity_path.grid(row=7, padx=20, columnspan=2)

# Input range
label_start_hour = tk.Label(button_frame, text="Start Hour:", bg=BG_COLOR)
label_start_hour.grid(row=8, column=0, pady=(20, 5))

label_end_hour = tk.Label(button_frame, text="End Hour:", bg=BG_COLOR)
label_end_hour.grid(row=8, column=1, pady=(20, 5))

entry_start_hour = tk.Entry(button_frame, bg="#797a7e")
entry_start_hour.grid(row=9, column=0)

entry_end_hour = tk.Entry(button_frame, bg="#797a7e")
entry_end_hour.grid(row=9, column=1)

# Generate chart
generate_button = tk.Button(button_frame, text="Generate Chart", command=generate_chart)
generate_button.grid(row=10, padx=20, pady=15, columnspan=2)

#Calculate Button
show_calculation_button = tk.Button(button_frame, text="Calculate", command=show_calculation_result)
show_calculation_button.grid(row=5, pady=(20, 5), columnspan=2)
show_calculation_button.grid_forget()

# Method 2 result
result = 0
result_label = tk.Label(button_frame, text=f"Wynik: {result}", bg = BG_COLOR, font=16 )
result_label.grid(row=6, pady=(20, 5), columnspan=2)
result_label.grid_forget()

window.mainloop()