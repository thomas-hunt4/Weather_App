"""App elements joining point"""

import setup_rich
from gui.v2gui_main import App
from data.history_management.auto_api_history_builder import ForecastArchiveAutomation

if __name__ == "__main__":
    # Run historical data update once on startup
    print("Updating historical weather data...")
    try:
        scheduler = ForecastArchiveAutomation()
        scheduler.run_once()
        print("Historical data update complete.")
    except Exception as e:
        print(f"Error updating historical data: {e}")
    
    # Start GUI
    app = App()
    app.mainloop()



