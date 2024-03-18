import tkinter as tk
from tkinter import *
from tkinter import font

#variables
BG_COLOR = "#606166"

# Main window
window = tk.Tk()
window.title("Traffic Intensity Calculation Methods Visualization")
window.geometry("620x420")
window.resizable(False, False)
window.configure(bg=BG_COLOR)
label_font = font.Font(size=13)


#Functions
###########################

# Choosing method
button_frame = tk.Frame(window, width=720, height=720)
button_frame.configure(bg=BG_COLOR)
button_frame.pack(pady = 50, padx=30)

input_label_methods = tk.Label(button_frame, text="Choose the calculation method", bg=BG_COLOR, font=label_font)
input_label_methods.grid(row=0, column=0, columnspan=3, pady=10)

v = IntVar(button_frame)

method1_button = tk.Radiobutton(button_frame, text="Method 1", variable=v, value=1)
method1_button.grid(row=1, column=0, padx=20, pady=5)
method2_button = tk.Radiobutton(button_frame, text="Method 2", variable=v, value=2)
method2_button.grid(row=1, column=1, padx=20, pady=5)


# Choose the method of inserting data
input_label_data = tk.Label(button_frame, text="How do you want to import your data?", bg=BG_COLOR, font=label_font)
input_label_data.grid(row = 2, pady=(20, 5),  columnspan=3)

input_button = tk.Button(button_frame, text="Insert manually")
input_button.grid(row=3, padx=20, pady=5)
file_button = tk.Button(button_frame, text="Choose from file")
file_button.grid(row=3, column=1, padx=20, pady=5)

entry_path = tk.Entry(button_frame)
entry_path.grid(row=4, padx=20, columnspan=2)

generate_button = tk.Button(button_frame, text="Generate Chart")
generate_button.grid(row=5, padx=20, pady=15, columnspan = 2)

window.mainloop()