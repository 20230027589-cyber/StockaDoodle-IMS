# custom_tab_widget.py
#
# This module provides a custom tab widget component with modern styling.
# Used for organizing content into tabs with a clean, modern appearance.
#
# Usage: Imported by UI pages that need tabbed interfaces (e.g., profile page, product detail).

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal
from utils.config import AppConfig
from utils.styles import get_modern_card_style


class CustomTabWidget(QWidget):
    """
    Custom tab widget with modern styling.
    Provides a horizontal tab bar above a stacked widget for tab content.
    
    Design: Dark theme tabs with rounded corners, smooth transitions,
    and clear active/inactive states.
    """
    
    currentChanged = pyqtSignal(int)  # Emitted when tab changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.tab_buttons = []
        self.current_index = 0
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI layout and styling."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab bar container
        self.tab_bar = QWidget()
        self.tab_bar_layout = QHBoxLayout(self.tab_bar)
        self.tab_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_bar_layout.setSpacing(5)
        
        self.tab_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {AppConfig.DARK_BACKGROUND};
                border-bottom: 1px solid {AppConfig.BORDER_COLOR};
                padding: 5px;
            }}
        """)
        
        layout.addWidget(self.tab_bar)
        
        # Stacked widget for tab content
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
    
    def addTab(self, widget: QWidget, label: str) -> int:
        """
        Add a new tab with the given widget and label.
        
        Args:
            widget: The widget to display in this tab
            label: The label text for the tab button
            
        Returns:
            int: The index of the newly added tab
        """
        index = len(self.tabs)
        self.tabs.append(widget)
        self.stacked_widget.addWidget(widget)
        
        # Create tab button
        button = QPushButton(label)
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {AppConfig.TEXT_COLOR_ALT};
                border: none;
                border-radius: {AppConfig.BUTTON_RADIUS}px;
                padding: 10px 20px;
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.05);
                color: {AppConfig.LIGHT_TEXT};
            }}
            QPushButton:checked {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: {AppConfig.LIGHT_TEXT};
                font-weight: bold;
            }}
        """)
        
        button.clicked.connect(lambda: self.setCurrentIndex(index))
        self.tab_buttons.append(button)
        self.tab_bar_layout.addWidget(button)
        
        # Set first tab as active by default
        if index == 0:
            button.setChecked(True)
        
        return index
    
    def setCurrentIndex(self, index: int):
        """
        Switch to the tab at the given index.
        
        Args:
            index: The index of the tab to switch to
        """
        if 0 <= index < len(self.tabs):
            self.current_index = index
            self.stacked_widget.setCurrentIndex(index)
            
            # Update button states
            for i, button in enumerate(self.tab_buttons):
                button.setChecked(i == index)
            
            self.currentChanged.emit(index)
    
    def currentIndex(self) -> int:
        """Get the index of the currently active tab."""
        return self.current_index

