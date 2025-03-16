import sys
from PyQt5.QtWidgets import QApplication
from src.app_window import AppWindow

if __name__ == "__main__":
    try:
        print("Starting application...")
        app = QApplication(sys.argv)
        window = AppWindow()
        window.show()
        print("Application started successfully.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
