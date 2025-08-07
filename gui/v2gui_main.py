import customtkinter as ctk

# Import page classes from the pages module
from .pages import HomePage, ForecastPage, TrendPage, HistoricalPage, FirePage

# Link Data and Feature files for interactions  
from features.language_select import set_language, get_language

""" default to dark mode but add variable and button """
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

""" TODO some comments are placed above or before the proceeding function that they reference. Explore a way to make that system still collapsible but so that comments are not missed. For now, TODO open the above function to double check for comments. """


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x1000")
        self.title("Weather Wonderland")
        self.resizable(True, True)

        """ Track theme state """
        self.theme_mode = "Dark"
        self.theme_buttons = []

        """ main frame for widgets using grid geometry """
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        '''ForecastPage, TrendPage, HistoricalPage, FirePage'''
        for pages in (HomePage, ForecastPage, TrendPage, HistoricalPage, FirePage):
            frame = pages(parent=main_frame, controller=self)
            self.frames[pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    """ toggle them parent """
    def toggle_theme(self):
        # Toggle theme mode
        if self.theme_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_mode = "Light"
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_mode = "Dark"

        # Update all theme toggle buttons' text
        for button in self.theme_buttons:
            button.configure(text="Dark Mode" if self.theme_mode == "Light" else "Light Mode")

    def update_language(self, selected_lang):
        from features.language_select import set_language
        set_language(selected_lang)

        # Optional: refresh weather if HomePage has it
        home_page = self.frames.get(HomePage)
        if home_page and hasattr(home_page, 'current_weather') and home_page.current_weather:
            city = home_page.current_weather.get('city')
            if city:
                home_page.update_weather(city)    


""" For testing layout """
# if __name__ == "__main__":
    
#     app = App()
#     app.mainloop()
