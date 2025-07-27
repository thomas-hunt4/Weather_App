import customtkinter as ctk


class ForecastPage(ctk.CTkFrame):
    """Connected to HomePage via button-> plt graphs or other graphics?"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Forecast Page")
        label.grid(row=0, column=0)

        """ Call builders """
        self._configure_grid()
        self._build_header()

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        """ current grid page/grid dimensions
        0 _1_2_   3_4_   5_6_7_
        0___H__e__a__d__e__r____
        
        1_______   ____   ______
        2_Temp__   _Nav   __Map_
        3_______   ____   ______
        
        4_Sun___   Butt   _Cont_
        5_______   ____   ______
        """

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, height=40)
        header_frame.grid(row=0, column=0, columnspan=8, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Menu Button
        header_frame.grid_columnconfigure(1, weight=1) # Light/Dark toggle, other settings?

        # Import here to avoid circular imports
        from .home_page import HomePage

        menu_button = ctk.CTkButton(header_frame, text="<- Back", width=120, height=28, command=lambda: self.controller.show_frame(HomePage)) # left aligned 
        menu_button.grid(row=0, column=0, padx=10, sticky="w")

        self.theme_button = ctk.CTkButton(header_frame,text="Dark Mode",command=self.controller.toggle_theme)
        self.theme_button.grid(row=0, column=1, sticky="e", padx=10)

        current_mode = ctk.get_appearance_mode()
        self.theme_button.configure(text="Dark Mode" if current_mode == "Light" else "Light Mode")

        # Register button with App for syncing text
        self.controller.theme_buttons.append(self.theme_button)