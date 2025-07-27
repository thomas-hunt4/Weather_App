import customtkinter as ctk


class TrendPage(ctk.CTkFrame):
    """Connected to HomePage via button-> This is for advanced feature and may be removed. Check on feature timeline. If required features not completed, remove TrendPage by 15/7/25"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Trend Page")
        label.grid(row=0, column=0)

        """ Call builders """
        self._configure_grid()
        self._build_header()
        self._daily_temp_frame()

    """ TODO this is copied grid layout from HomePage and needs to be modified to the desired feature layout per page. Only used as boilerplate FramePage starter code. """
    def _configure_grid(self):
        for row in range(9):
            self.grid_rowconfigure(row, weight=1)
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)

        """ current grid page/grid dimensions
           _0 _1 _2 _3 _4 _5 _6 
        _0__H__E__A__D__E__R___
        _1 D  "  "  2  2  "  "
        _2 A  "  "  D  M  "  "
        _3 L  "  "  A  R  "  "
        _4 Y  "  "  Y  W  "  "
        _5___M_A_X___T_R_E_N_D
        _6 > ^ <
        _7___M_I_N___T_R_E_N_D
        _8 < ^ >
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

    def _daily_temp_frame(self):
        daily_frame = ctk.CTkFrame(self, corner_radius=15)
        daily_frame.grid(row=1, column=1, columnspan=5, rowspan=4, padx=20, pady=20, sticky="nsew")

        for row in range(4):
            daily_frame.grid_rowconfigure(row, weight=1)
        for column in range(7):
            daily_frame.grid_columnconfigure(column, weight=1)

        # DAY ONE
        one_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        one_frame.grid(row=0, column=0, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        one_frame.grid_columnconfigure(0, weight=1)
        one_frame.grid_rowconfigure(0, weight=1)
        one_frame.grid_rowconfigure(1, weight=1)
        one_max_frame = ctk.CTkFrame(one_frame, corner_radius=15)
        one_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        one_max_frame.grid_rowconfigure(0, weight=1)
        one_max_frame.grid_rowconfigure(1, weight=1)
        one_max_frame.grid_columnconfigure(0, weight=1)
        self.one_max_label = ctk.CTkLabel(one_max_frame, text="Max")
        self.one_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.one_max_value = ctk.CTkLabel(one_max_frame, text="35° C")
        self.one_max_value.grid(row=1, column=0, sticky="nsew")
        one_min_frame = ctk.CTkFrame(one_frame, corner_radius=15)
        one_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        one_min_frame.grid_rowconfigure(0, weight=1)
        one_min_frame.grid_rowconfigure(1, weight=1)
        one_min_frame.grid_columnconfigure(0, weight=1)
        self.one_min_label = ctk.CTkLabel(one_min_frame, text="Min")
        self.one_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.one_min_value = ctk.CTkLabel(one_min_frame, text="23° C")
        self.one_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY TWO
        two_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        two_frame.grid(row=0, column=1, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        two_frame.grid_columnconfigure(0, weight=1)
        two_frame.grid_rowconfigure(0, weight=1)
        two_frame.grid_rowconfigure(1, weight=1)
        two_max_frame = ctk.CTkFrame(two_frame, corner_radius=15)
        two_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        two_max_frame.grid_rowconfigure(0, weight=1)
        two_max_frame.grid_rowconfigure(1, weight=1)
        two_max_frame.grid_columnconfigure(0, weight=1)
        self.two_max_label = ctk.CTkLabel(two_max_frame, text="Max")
        self.two_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.two_max_value = ctk.CTkLabel(two_max_frame, text="35° C")
        self.two_max_value.grid(row=1, column=0, sticky="nsew")
        two_min_frame = ctk.CTkFrame(two_frame, corner_radius=15)
        two_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        two_min_frame.grid_rowconfigure(0, weight=1)
        two_min_frame.grid_rowconfigure(1, weight=1)
        two_min_frame.grid_columnconfigure(0, weight=1)
        self.two_min_label = ctk.CTkLabel(two_min_frame, text="Min")
        self.two_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.two_min_value = ctk.CTkLabel(two_min_frame, text="23° C")
        self.two_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY THREE
        three_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        three_frame.grid(row=0, column=2, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        three_frame.grid_columnconfigure(0, weight=1)
        three_frame.grid_rowconfigure(0, weight=1)
        three_frame.grid_rowconfigure(1, weight=1)
        three_max_frame = ctk.CTkFrame(three_frame, corner_radius=15)
        three_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        three_max_frame.grid_rowconfigure(0, weight=1)
        three_max_frame.grid_rowconfigure(1, weight=1)
        three_max_frame.grid_columnconfigure(0, weight=1)
        self.three_max_label = ctk.CTkLabel(three_max_frame, text="Max")
        self.three_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.three_max_value = ctk.CTkLabel(three_max_frame, text="35° C")
        self.three_max_value.grid(row=1, column=0, sticky="nsew")
        three_min_frame = ctk.CTkFrame(three_frame, corner_radius=15)
        three_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        three_min_frame.grid_rowconfigure(0, weight=1)
        three_min_frame.grid_rowconfigure(1, weight=1)
        three_min_frame.grid_columnconfigure(0, weight=1)
        self.three_min_label = ctk.CTkLabel(three_min_frame, text="Min")
        self.three_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.three_min_value = ctk.CTkLabel(three_min_frame, text="23° C")
        self.three_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY FOUR
        four_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        four_frame.grid(row=0, column=3, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        four_frame.grid_columnconfigure(0, weight=1)
        four_frame.grid_rowconfigure(0, weight=1)
        four_frame.grid_rowconfigure(1, weight=1)
        four_max_frame = ctk.CTkFrame(four_frame, corner_radius=15)
        four_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        four_max_frame.grid_rowconfigure(0, weight=1)
        four_max_frame.grid_rowconfigure(1, weight=1)
        four_max_frame.grid_columnconfigure(0, weight=1)
        self.four_max_label = ctk.CTkLabel(four_max_frame, text="Max")
        self.four_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.four_max_value = ctk.CTkLabel(four_max_frame, text="35° C")
        self.four_max_value.grid(row=1, column=0, sticky="nsew")
        four_min_frame = ctk.CTkFrame(four_frame, corner_radius=15)
        four_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        four_min_frame.grid_rowconfigure(0, weight=1)
        four_min_frame.grid_rowconfigure(1, weight=1)
        four_min_frame.grid_columnconfigure(0, weight=1)
        self.four_min_label = ctk.CTkLabel(four_min_frame, text="Min")
        self.four_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.four_min_value = ctk.CTkLabel(four_min_frame, text="23° C")
        self.four_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY FIVE
        five_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        five_frame.grid(row=0, column=4, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        five_frame.grid_columnconfigure(0, weight=1)
        five_frame.grid_rowconfigure(0, weight=1)
        five_frame.grid_rowconfigure(1, weight=1)
        five_max_frame = ctk.CTkFrame(five_frame, corner_radius=15)
        five_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        five_max_frame.grid_rowconfigure(0, weight=1)
        five_max_frame.grid_rowconfigure(1, weight=1)
        five_max_frame.grid_columnconfigure(0, weight=1)
        self.five_max_label = ctk.CTkLabel(five_max_frame, text="Max")
        self.five_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.five_max_value = ctk.CTkLabel(five_max_frame, text="35° C")
        self.five_max_value.grid(row=1, column=0, sticky="nsew")
        five_min_frame = ctk.CTkFrame(five_frame, corner_radius=15)
        five_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        five_min_frame.grid_rowconfigure(0, weight=1)
        five_min_frame.grid_rowconfigure(1, weight=1)
        five_min_frame.grid_columnconfigure(0, weight=1)
        self.five_min_label = ctk.CTkLabel(five_min_frame, text="Min")
        self.five_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.five_min_value = ctk.CTkLabel(five_min_frame, text="23° C")
        self.five_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY SIX
        six_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        six_frame.grid(row=0, column=5, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        six_frame.grid_columnconfigure(0, weight=1)
        six_frame.grid_rowconfigure(0, weight=1)
        six_frame.grid_rowconfigure(1, weight=1)
        six_max_frame = ctk.CTkFrame(six_frame, corner_radius=15)
        six_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        six_max_frame.grid_rowconfigure(0, weight=1)
        six_max_frame.grid_rowconfigure(1, weight=1)
        six_max_frame.grid_columnconfigure(0, weight=1)
        self.six_max_label = ctk.CTkLabel(six_max_frame, text="Max")
        self.six_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.six_max_value = ctk.CTkLabel(six_max_frame, text="35° C")
        self.six_max_value.grid(row=1, column=0, sticky="nsew")
        six_min_frame = ctk.CTkFrame(six_frame, corner_radius=15)
        six_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        six_min_frame.grid_rowconfigure(0, weight=1)
        six_min_frame.grid_rowconfigure(1, weight=1)
        six_min_frame.grid_columnconfigure(0, weight=1)
        self.six_min_label = ctk.CTkLabel(six_min_frame, text="Min")
        self.six_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.six_min_value = ctk.CTkLabel(six_min_frame, text="23° C")
        self.six_min_value.grid(row=1, column=0, sticky="nsew")

        # DAY SEVEN
        seven_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        seven_frame.grid(row=0, column=6, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        seven_frame.grid_columnconfigure(0, weight=1)
        seven_frame.grid_rowconfigure(0, weight=1)
        seven_frame.grid_rowconfigure(1, weight=1)
        seven_max_frame = ctk.CTkFrame(seven_frame, corner_radius=15)
        seven_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        seven_max_frame.grid_rowconfigure(0, weight=1)
        seven_max_frame.grid_rowconfigure(1, weight=1)
        seven_max_frame.grid_columnconfigure(0, weight=1)
        self.seven_max_label = ctk.CTkLabel(seven_max_frame, text="Max")
        self.seven_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.seven_max_value = ctk.CTkLabel(seven_max_frame, text="35° C")
        self.seven_max_value.grid(row=1, column=0, sticky="nsew")
        seven_min_frame = ctk.CTkFrame(seven_frame, corner_radius=15)
        seven_min_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        seven_min_frame.grid_rowconfigure(0, weight=1)
        seven_min_frame.grid_rowconfigure(1, weight=1)
        seven_min_frame.grid_columnconfigure(0, weight=1)
        self.seven_min_label = ctk.CTkLabel(seven_min_frame, text="Min")
        self.seven_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.seven_min_value = ctk.CTkLabel(seven_min_frame, text="23° C")
        self.seven_min_value.grid(row=1, column=0, sticky="nsew")

    def _daily_temp_trend_frame(self):
        trend_header = ctk.CTkFrame
        pass