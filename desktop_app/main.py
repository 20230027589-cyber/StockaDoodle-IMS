# main.py
#
# This module is the main entry point for the StockaDoodle IMS desktop application.
# Initializes the application, shows splash screen, handles login, and launches dashboard.
#
# Usage: Run this file to start the desktop application.

import sys
import os

from PyQt6.QtWidgets import QApplication, QSplashScreen, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont

# Add the desktop_app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import AppConfig
from utils.font_loader import load_fonts
from utils.api_wrapper import set_api, get_api
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def show_splash_screen(app: QApplication) -> QSplashScreen:
    """
    Show splash screen with logo.
    
    Args:
        app: QApplication instance
        
    Returns:
        QSplashScreen: The splash screen widget
    """
    # Load logo for splash screen
    logo_path = os.path.join(AppConfig.ICONS_DIR, "stockadoodle-transparent.png")
    
    if os.path.exists(logo_path):
        pixmap = QPixmap(logo_path)
        # Scale logo for splash (300x300)
        scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    else:
        # Create a simple pixmap if logo not found
        scaled_pixmap = QPixmap(300, 300)
        scaled_pixmap.fill(Qt.GlobalColor.darkGray)
    
    splash = QSplashScreen(scaled_pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    
    # Add text to splash screen
    splash.showMessage(
        "Loading StockaDoodle IMS...",
        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        Qt.GlobalColor.white
    )
    
    splash.show()
    app.processEvents()  # Process events to show splash
    
    return splash


def main():
    """Main application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("StockaDoodle IMS")
    app.setApplicationVersion("3.0.0")
    
    # Set application style
    app.setStyle("Fusion")  # Use Fusion style for better cross-platform consistency
    
    # Load fonts
    print("Loading fonts...")
    font_ids = load_fonts()
    if font_ids:
        print(f"Successfully loaded {len(font_ids)} fonts.")
        # Set Inter as default font
        from PyQt6.QtGui import QFont
        default_font = QFont("Inter", 12)
        app.setFont(default_font)
    else:
        print("Warning: No fonts loaded.")
    
    # Show splash screen
    print("Showing splash screen...")
    splash = show_splash_screen(app)
    
    # Simulate loading time (2 seconds)
    QTimer.singleShot(2000, splash.close)
    
    # Initialize API client
    print("Initializing API client...")
    api_client = get_api()
    set_api(api_client)
    
    # Process events to show splash
    app.processEvents()
    
    # Wait for splash to show (small delay)
    QTimer.singleShot(100, lambda: None)
    
    # Show login window
    print("Showing login window...")
    login_window = LoginWindow()
    
    # Center login window on screen
    screen = app.primaryScreen().geometry()
    login_window.move(
        (screen.width() - login_window.width()) // 2,
        (screen.height() - login_window.height()) // 2
    )
    
    # Close splash after login window is ready
    splash.finish(login_window)
    
    # Execute login dialog
    if login_window.exec() == login_window.DialogCode.Accepted:
        user_data = login_window.get_user_data()
        
        if user_data:
            user_role = user_data.get('role', '').lower()
            print(f"Logged in as: {user_data.get('full_name', user_data.get('username', 'User'))} ({user_role})")
            
            # Show appropriate dashboard based on role
            if user_role in ['manager', 'admin']:
                print("Opening manager dashboard...")
                dashboard = MainWindow(user_data, api_client)
                
                # Center dashboard on screen
                screen = app.primaryScreen().geometry()
                dashboard.move(
                    (screen.width() - dashboard.width()) // 2,
                    (screen.height() - dashboard.height()) // 2
                )
                
                dashboard.show()
                
                # Run application event loop
                sys.exit(app.exec())
            
            elif user_role == 'retailer':
                # TODO: Implement retailer POS dashboard
                print("Retailer dashboard not yet implemented.")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(
                    None,
                    "Coming Soon",
                    "Retailer dashboard is coming soon!",
                    QMessageBox.StandardButton.Ok
                )
            
            else:
                print(f"Unknown role: {user_role}")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    None,
                    "Access Denied",
                    "Your role does not have access to the desktop application.",
                    QMessageBox.StandardButton.Ok
                )
        else:
            print("Login failed: No user data returned.")
    
    else:
        print("Login cancelled by user.")
    
    # Exit application
    sys.exit(0)


if __name__ == "__main__":
    main()

