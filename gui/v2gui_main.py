import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk

""" default to dark mode but add variable and button """
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Weather Wonderland")
        self.resizable(True, True)

        """ main frame for widgets using grid geometry """
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        '''ForecastPage, TrendPage, HistoricalPage, FirePage'''
        for pages in (HomePage, ForecastPage):
            frame = pages(parent=main_frame, controller=self)
            self.frames[pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()



        

        

    
        """ landing/main page for app with buttons to navigate to other features. Base weather stats, map inserts """
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Home Page")
        label.grid(row=0, column=0)
        pass
        

        """ connected to HomePage via button-> plt graphs or other graphics? """
class ForecastPage(ctk.CTkFrame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Forecast Page")
        label.grid(row=0, column=0)

        pass
        

#         """ connected to HomePage via button-> This is for advanced feature and may be removed. Check on feature timeline. If required features not completed, remove TrendPage by 15/7/25 """
# class TrendPage(ctk.CTkFrame):
#     def __init__(self,App):
#         pass
        

#         """ connected to Homepage via button-> prepare db/API calls/test by 10/7/25 """
# class HistoricalPage(ctk.CTkFrame):
#     def __init__(self,App):
#         pass
        

#         """ Optional Fire information button-> Remove if not implemented by 10/7/25 """
# class FirePage(ctk.CTkFrame):
#     def __init__(self,App):
#         pass



""" For testing layout """
if __name__ == "__main__":
    
    app = App()
    app.mainloop()