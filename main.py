import customtkinter
from tkinter import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

main_app = customtkinter.CTk()
main_app.geometry("500x350")

def login():
    print("Test")

frame = customtkinter.CTkFrame(master=main_app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System")
label.pack(pady=10, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=10, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=10, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=10, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember me")
checkbox.pack(pady=10, padx=10)

main_app.mainloop()
