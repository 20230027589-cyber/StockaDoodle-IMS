# sidebar.py
#
# This module provides the sidebar navigation component.
# Modern, clean design with blue theme and SVG icons.
#
# Usage: Used in the main window for navigation between different pages.

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.icons import get_icon
from utils.font_loader import get_inter_font


class Sidebar(QWidget):
    """
    Sidebar navigation component with modern blue theme.
    
    Design:
    - Dark blue background (#0F172A)
    - SVG icons from assets/icons/
    - Active item: bright blue background (#3B82F6) + white text
    - Hover: subtle lighter blue
    - Logo at top
    - Role-based visibility
    """
    
    tab_selected = pyqtSignal(int)
    
    # Tab indices
    TAB_DASHBOARD = 0
    TAB_PRODUCTS = 1
    TAB_CATEGORIES = 2
    TAB_SALES = 3
    TAB_REPORTS = 4
    TAB_PROFILE = 5
    
    def __init__(self, user: dict, switch_callback=None, parent=None):
        """
        Initialize the sidebar.
        
        Args:
            user: User dictionary with role information
            switch_callback: Optional callback function for tab switching
            parent: Parent widget
        """
        super().__init__(parent)
        self.user = user
        self.switch_callback = switch_callback
        self.current_tab = self.TAB_DASHBOARD
        self.nav_buttons = {}  # Track buttons by tab index
        
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        
        # Blue theme background
        self.setStyleSheet(f"""
            QWidget#sidebar {{
                background-color: #0F172A;
                border: none;
            }}
        """)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the sidebar UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(8)
        
        # Logo/Brand section at top
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(12)
        
        # Logo
        logo_path = os.path.join(AppConfig.ICONS_DIR, "stockadoodle-transparent.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            logo_label.setFixedHeight(40)
            brand_layout.addWidget(logo_label)
        
        # Brand name
        brand_label = QLabel("StockaDoodle")
        brand_label.setFont(get_inter_font("Bold", 18))
        brand_label.setStyleSheet(f"color: {AppConfig.LIGHT_TEXT};")
        brand_layout.addWidget(brand_label)
        
        layout.addLayout(brand_layout)
        layout.addSpacing(24)
        
        # Navigation buttons based on role
        if self.user.get('role') in ['manager', 'admin']:
            self.create_nav_button("Dashboard", self.TAB_DASHBOARD, "layout-grid", layout)
            self.create_nav_button("Products", self.TAB_PRODUCTS, "package", layout)
            self.create_nav_button("Categories", self.TAB_CATEGORIES, "tag", layout)
            self.create_nav_button("Sales", self.TAB_SALES, "shopping-cart", layout)
            self.create_nav_button("Reports", self.TAB_REPORTS, "bar-chart-2", layout)
        
        # Profile is available to all authenticated users
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.create_nav_button("Profile", self.TAB_PROFILE, "user", layout)
    
    def create_nav_button(self, text: str, tab_index: int, icon_name: str, layout: QVBoxLayout):
        """
        Create a navigation button with icon.
        
        Args:
            text: Button text
            tab_index: Tab index this button represents
            icon_name: Icon name (from assets/icons/)
            layout: Layout to add button to
        """
        button = QPushButton(text)
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFont(get_inter_font("Medium", 13))
        
        # Set icon from SVG
        icon = get_icon(icon_name, color="#CBD5E1", size=20)
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(Qt.QSize(20, 20))
        
        # Style for inactive state
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: #CBD5E1;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
                font-size: 13pt;
            }}
            QPushButton:hover {{
                background-color: rgba(59, 130, 246, 0.1);
                color: white;
            }}
            QPushButton:checked {{
                background-color: #3B82F6;
                color: white;
            }}
        """)
        
        button.clicked.connect(lambda: self.on_tab_clicked(tab_index, button))
        
        # Set first button (Dashboard) as checked by default
        if tab_index == self.TAB_DASHBOARD:
            button.setChecked(True)
        
        # Store button reference
        self.nav_buttons[tab_index] = button
        
        layout.addWidget(button)
    
    def on_tab_clicked(self, tab_index: int, button: QPushButton):
        """
        Handle tab button click.
        
        Args:
            tab_index: Index of the tab to switch to
            button: The button that was clicked
        """
        # Uncheck all buttons
        for btn in self.nav_buttons.values():
            if btn.isCheckable():
                btn.setChecked(False)
        
        # Check clicked button
        button.setChecked(True)
        self.current_tab = tab_index
        
        # Emit signal and call callback
        self.tab_selected.emit(tab_index)
        if self.switch_callback:
            self.switch_callback(tab_index)
    
    def set_current_tab(self, tab_index: int):
        """
        Programmatically set the current tab.
        
        Args:
            tab_index: Index of the tab to set as current
        """
        if tab_index in self.nav_buttons:
            # Uncheck all
            for btn in self.nav_buttons.values():
                btn.setChecked(False)
            # Check selected
            self.nav_buttons[tab_index].setChecked(True)
            self.current_tab = tab_index
