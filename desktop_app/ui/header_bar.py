# header_bar.py
#
# This module provides the header bar component.
# Displays user information, notifications, and search functionality.
#
# Usage: Used at the top of the main window for header information.

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from utils.config import AppConfig
from utils.icons import get_icon


class HeaderBar(QWidget):
    """
    Header bar component with user info, search, and notifications.
    
    Design: Dark header bar with user profile info, search box,
    and notification button. Displays user's name and role.
    """
    
    def __init__(self, user: dict, parent=None):
        """
        Initialize the header bar.
        
        Args:
            user: User dictionary with user information
            parent: Parent widget
        """
        super().__init__(parent)
        self.user = user
        self.setObjectName("headerBar")
        self.setFixedHeight(AppConfig.HEADER_HEIGHT)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the header bar UI and styling."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)
        
        # Search bar
        search_input = QLineEdit()
        search_input.setObjectName("globalSearch")
        search_input.setPlaceholderText("Search products, categories...")
        search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 1px solid {AppConfig.BORDER_COLOR};
                border-radius: 20px;
                padding: 8px 15px;
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                min-width: 300px;
            }}
            QLineEdit:focus {{
                border: 2px solid {AppConfig.PRIMARY_COLOR};
            }}
        """)
        
        layout.addWidget(search_input)
        layout.addStretch()
        
        # Notifications button
        notification_btn = QPushButton()
        notification_btn.setObjectName("notificationButton")
        notification_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        try:
            icon = get_icon("bell", color=AppConfig.TEXT_COLOR_ALT, size=20)
            notification_btn.setIcon(icon)
        except:
            notification_btn.setText("🔔")
        
        notification_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {AppConfig.BUTTON_RADIUS}px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.1);
            }}
        """)
        
        layout.addWidget(notification_btn)
        
        # User info
        user_name = self.user.get('full_name', self.user.get('username', 'User'))
        user_role = self.user.get('role', 'staff').title()
        
        user_label = QLabel(f"{user_name} ({user_role})")
        user_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                padding: 5px 10px;
            }}
        """)
        
        layout.addWidget(user_label)
        
        # Profile button
        profile_btn = QPushButton()
        profile_btn.setObjectName("profileButton")
        profile_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        try:
            icon = get_icon("user", color=AppConfig.TEXT_COLOR_ALT, size=20)
            profile_btn.setIcon(icon)
        except:
            profile_btn.setText("👤")
        
        profile_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {AppConfig.BUTTON_RADIUS}px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.1);
            }}
        """)
        
        layout.addWidget(profile_btn)
        
        # Apply header bar style
        self.setStyleSheet(f"""
            QWidget#headerBar {{
                background-color: {AppConfig.DARK_BACKGROUND};
                border-bottom: 1px solid {AppConfig.BORDER_COLOR};
                padding: 10px 20px;
            }}
        """)

