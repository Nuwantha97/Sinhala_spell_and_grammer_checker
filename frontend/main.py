import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow


def main():
    """Initialize and run the application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application-wide font with Sinhala support
    font = QFont("Nirmala UI", 11)  # Nirmala UI has good Sinhala support
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Sinhala Spell and Grammar Checker")
    app.setOrganizationName("SinhalaChecker")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
