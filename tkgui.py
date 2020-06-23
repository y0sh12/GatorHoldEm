import tkinter as tk

# Add window and name it
window = tk.Tk()
window.title("GatorHoldEm")
window.geometry('800x600')


def handle_keypress(event):
    print(event.char)


def handle_click(event):
    if name_entry.get() == '' or room_entry.get() == '':
        print("Invalid entry. Try again!")
        return
    print("Name entered: " + name_entry.get())
    print("Room name entered: " + room_entry.get())


# Title
title = tk.Label(
    # master=frame_a,
    font=(None, 24),
    text="GatorHoldEm",
    height=3,
    width=20,
    fg="black"
)
title.grid(row=0, column=1, padx=100, pady=50, sticky='S')

# Name label
name_label = tk.Label(
    text="Enter your name here:",
    foreground="black"
)
name_label.grid(row=1, column=0)

# Name input
name_entry = tk.Entry(
    fg="black",
    bg="white",
    width=50
)
name_entry.grid(row=1, column=1)

# Room label
room_label = tk.Label(
    text="Enter name of room to join:",
    foreground="black"
)
room_label.grid(row=2, column=0)

# Room input
room_entry = tk.Entry(
    fg="black",
    bg="white",
    width=50
)
room_entry.grid(row=2, column=1)

button = tk.Button(
    text="Submit",
    bg="blue",
    width=25
)
button.grid(row=3, column=1, padx=0, pady=25)

button.bind("<Button-1>", handle_click)

# Start loop to display window
window.mainloop()
