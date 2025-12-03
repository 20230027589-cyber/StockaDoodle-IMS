# loading_spinner.py
#
# This module provides a loading spinner component.
# Displays a loading indicator with optional text.
#
# Usage: Used to show loading states in the UI.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from utils.config import AppConfig
from utils.styles import get_loading_spinner_style


class LoadingSpinner(QWidget):
    """
    Loading spinner widget component.
    
    Features:
    - Animated loading indicator (text-based)
    - Optional loading message
    - Centered layout
    """
    
    def __init__(self, message: str = "Loading...", parent=None):
        """
        Initialize the loading spinner.
        
        Args:
            message: Loading message to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.message = message
        
        self.setObjectName("loadingSpinner")
        self.setStyleSheet(get_loading_spinner_style())
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the loading spinner UI."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        
        # Loading text
        self.loading_label = QLabel(self.message)
        self.loading_label.setObjectName("loadingText")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
        """)
        layout.addWidget(self.loading_label)
    
    def set_message(self, message: str):
        """Update the loading message."""
        self.message = message
        self.loading_label.setText(message)
    
    def show_loading(self):
        """Show the loading spinner."""
        self.show()
    
    def hide_loading(self):
        """Hide the loading spinner."""
        self.hide()

