"""App elements joining point"""

import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent))

from gui import App


if __name__ == "__main__":
    app = App()
    app.run_app()
    



