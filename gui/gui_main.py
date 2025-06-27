import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk
import requests
import os 
from dotenv import load_dotenv
load_dotenv()




class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("Weather Wonderland")
        self.root.resizable(True, True)

        #unsure if this will function correctly inside __init__
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")
        # self.light_dark = ""

        



        self.setup_gui()

    def setup_gui(self):
        # self.main_frame = tk.Frame(self.root)
        # self.main_frame.grid(column=0, row=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3) 
        self.root.grid_columnconfigure(1, weight=1) 
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_main_weather_widget()
        
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=10)
        left_label = tk.Label(self.left_frame, text="Main Weather Stats", bg="lightblue")
        left_label.grid(row=0, column=0, rowspan=5, columnspan=3)

        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
        right_label = tk.Label(self.right_frame, text="Buttons Home", bg="lightgreen")
        right_label.grid(row=0, column=0, rowspan=8, columnspan=2)


    def create_main_weather_widget(self):

        title = ctk.CTkLabel(self.main_frame, text="PlaceHolder", font=ctk.CTkFont(size=24, weight="bold"))

        title.pack(pady=(20,10))

        temp_frame = ctk.CTkFrame(self.main_frame)
        temp_frame.pack(pady=20, padx=20, fill="x")

        self.temp_label = ctk.CTkLabel(temp_frame, text=f"Temperature holder", font=ctk.CTkFont(size=48, weight="bold"))
        self.temp_label.pack(pady=20)

        sub_readings = ctk.CTkFrame(self.main_frame)
        sub_readings.pack(pady=20, padx=20, fill="both", expand=True)

        sub_readings.grid_columnconfigure(0, weight=1)
        sub_readings.grid_columnconfigure(0, weight=1)

        humidity_frame = ctk.CTkFrame(sub_readings)
        humidity_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(humidity_frame, text="Humidity Holder", font=ctk.CTkFont(size=14, weight="bold"))
    

    """ User input to select and fetch weather and location """
    # def select_city():


        





        



    def run_app(self):
        self.root.mainloop()

if __name__=="__main__":
    app = App()
    app.run_app()
