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
        self._daily_temp_trend_frame()
        # Test the trend arrows with sample data
        test_max_trends = [2.5, -1.8, 0.3, 4.2, -2.1, 1.7, -0.5]  # 7 sample temperature changes
        test_min_trends = [1.2, -3.5, 0.8, 2.9, -1.3, 0.1, -4.1]  # 7 sample temperature changes
        self.update_trend_arrows(test_max_trends, test_min_trends)

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
        """ Parent frame and first frame blocks will be commented for clarity.
        Subsequent blocks follow the same parent child structure """
        """ Housing daily temperature widgets """
        daily_frame = ctk.CTkFrame(self, corner_radius=15)
        daily_frame.grid(row=1, column=0, columnspan=7, rowspan=4, padx=10, pady=10, sticky="nsew")
        daily_frame.grid_rowconfigure(0, weight=1)
        for col in range(7):
            daily_frame.grid_columnconfigure(col, weight=1)

        """ Child of daily_frame """
        one_frame = ctk.CTkFrame(daily_frame, corner_radius=15)
        one_frame.grid(row=0, column=0, columnspan=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        one_frame.grid_columnconfigure(0, weight=1)
        one_frame.grid_rowconfigure(0, weight=1)
        one_frame.grid_rowconfigure(1, weight=1)
        """ Child of one_frame/sibling of one_min_frame """
        one_max_frame = ctk.CTkFrame(one_frame, corner_radius=15)
        one_max_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        one_max_frame.grid_rowconfigure(0, weight=1)
        one_max_frame.grid_rowconfigure(1, weight=1)
        one_max_frame.grid_columnconfigure(0, weight=1)
        self.one_max_label = ctk.CTkLabel(one_max_frame, text="Max")
        self.one_max_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.one_max_value = ctk.CTkLabel(one_max_frame, text="35° C")
        self.one_max_value.grid(row=1, column=0, sticky="nsew")
        """ Child of one_frame/sibling of one_max_frame """
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
        """ Current Daily Temperature Anchor for trending data """
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
        """Build the MAX and MIN trend sections (rows 5-8)"""
        
        # ROW 5: MAX TREND header
        max_trend_header = ctk.CTkFrame(self, corner_radius=15)
        max_trend_header.grid(row=5, column=0, columnspan=7, padx=10, pady=(5,2), sticky="ew")
        max_trend_header.grid_columnconfigure(0, weight=1)
        
        max_trend_label = ctk.CTkLabel(max_trend_header, text="MAX TREND", 
                                      font=ctk.CTkFont(size=18, weight="bold"))
        max_trend_label.grid(row=0, column=0, pady=10)
        
        # ROW 6: MAX trend arrows (7 widgets)
        max_arrows_frame = ctk.CTkFrame(self, corner_radius=15)
        max_arrows_frame.grid(row=6, column=0, columnspan=7, padx=10, pady=2, sticky="ew")
        
        # Configure 7 columns for the 7 days
        for col in range(7):
            max_arrows_frame.grid_columnconfigure(col, weight=1)
            
        # Create 7 arrow widgets for MAX trends
        self.max_trend_arrows = []
        for day in range(7):
            arrow_widget = ctk.CTkLabel(max_arrows_frame, text="→", 
                                       font=ctk.CTkFont(size=32, weight="bold"),
                                       width=50, height=50)
            arrow_widget.grid(row=0, column=day, padx=5, pady=15, sticky="nsew")
            self.max_trend_arrows.append(arrow_widget)
        
        # ROW 7: MIN TREND header  
        min_trend_header = ctk.CTkFrame(self, corner_radius=15)
        min_trend_header.grid(row=7, column=0, columnspan=7, padx=10, pady=(5,2), sticky="ew")
        min_trend_header.grid_columnconfigure(0, weight=1)
        
        min_trend_label = ctk.CTkLabel(min_trend_header, text="MIN TREND",
                                      font=ctk.CTkFont(size=18, weight="bold"))
        min_trend_label.grid(row=0, column=0, pady=10)
        
        # ROW 8: MIN trend arrows (7 widgets)
        min_arrows_frame = ctk.CTkFrame(self, corner_radius=15)
        min_arrows_frame.grid(row=8, column=0, columnspan=7, padx=10, pady=2, sticky="ew")
        
        # Configure 7 columns for the 7 days
        for col in range(7):
            min_arrows_frame.grid_columnconfigure(col, weight=1)
            
        # Create 7 arrow widgets for MIN trends
        self.min_trend_arrows = []
        for day in range(7):
            arrow_widget = ctk.CTkLabel(min_arrows_frame, text="→",
                                       font=ctk.CTkFont(size=32, weight="bold"),
                                       width=50, height=50)
            arrow_widget.grid(row=0, column=day, padx=5, pady=15, sticky="nsew")
            self.min_trend_arrows.append(arrow_widget)
            
    def get_trend_arrow_and_color(self, trend_value):
        """Get arrow and color based on temperature trend value
        
        Args:
            trend_value: degrees of change (positive = warming, negative = cooling)
        """
        if trend_value >= 3:
            return "↑", "#FF0000"  # Steep up, red
        elif trend_value >= 1:
            return "↗", "#FFD700"  # Up, yellow
        elif trend_value >= -1:
            return "→", "#808080"  # Neutral, gray
        elif trend_value >= -3:
            return "↘", "#4169E1"  # Down, blue
        else:
            return "↓", "#000080"  # Steep down, dark blue

    def update_trend_arrows(self, max_trend_values, min_trend_values):
        """Update the trend arrows based on calculated temperature trend values
        
        Args:
            max_trend_values: List of 7 temperature change values for max temperatures
            min_trend_values: List of 7 temperature change values for min temperatures
            Values are in degrees (positive = warming, negative = cooling)
        """
        
        # Update MAX trend arrows
        for i, trend_value in enumerate(max_trend_values):
            if i < len(self.max_trend_arrows):
                arrow, color = self.get_trend_arrow_and_color(trend_value)
                self.max_trend_arrows[i].configure(
                    text=arrow,
                    text_color=color
                )
                
        # Update MIN trend arrows  
        for i, trend_value in enumerate(min_trend_values):
            if i < len(self.min_trend_arrows):
                arrow, color = self.get_trend_arrow_and_color(trend_value)
                self.min_trend_arrows[i].configure(
                    text=arrow,
                    text_color=color
                )