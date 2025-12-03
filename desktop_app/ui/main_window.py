# main_window.py
#
# This module provides the main window for the manager dashboard.
# Contains the sidebar navigation, header bar, and stacked widget for page switching.
#
# Usage: Main entry point after login for manager role users.

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from utils.config import AppConfig
from utils.styles import get_global_stylesheet
from utils.app_state import set_api_client, set_current_user

from ui.sidebar import Sidebar
from ui.header_bar import HeaderBar
from ui.pages.dashboard import DashboardPage
from ui.pages.products.product_list import ProductListPage
from ui.pages.categories import CategoriesPage
from ui.pages.sales import SalesPage
from ui.pages.reports import ReportsPage
from ui.profile.profile_page import ProfilePage


class MainWindow(QMainWindow):
    """
    Main window for manager dashboard.
    
    Structure:
    - Header bar at top (user info, search, notifications)
    - Sidebar on left (navigation)
    - Stacked widget on right (page content)
    
    Pages: Dashboard, Products, Categories, Sales, Reports, Profile
    """
    
    def __init__(self, user: dict, api_client):
        """
        Initialize the main window.
        
        Args:
            user: User dictionary with user information
            api_client: StockaDoodleAPI client instance
        """
        super().__init__()
        self.user = user
        self.api_client = api_client
        
        # Set app state
        set_current_user(user)
        set_api_client(api_client)
        
        self.setWindowTitle(f"StockaDoodle IMS - {user.get('full_name', user.get('username', 'Manager'))}")
        self.setMinimumSize(AppConfig.WINDOW_MIN_WIDTH, AppConfig.WINDOW_MIN_HEIGHT)
        self.resize(AppConfig.WINDOW_DEFAULT_WIDTH, AppConfig.WINDOW_DEFAULT_HEIGHT)
        
        # Apply global stylesheet
        self.setStyleSheet(get_global_stylesheet())
        
        self.init_ui()
        
        # Start in full-screen mode (still allows minimize/restore/close via title bar)
        self.showMaximized()
    
    def init_ui(self):
        """Initialize the main window UI."""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header bar
        self.header = HeaderBar(self.user)
        main_layout.addWidget(self.header)
        
        # Content area (sidebar + pages)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(self.user, self.switch_tab)
        content_layout.addWidget(self.sidebar)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("contentArea")
        
        # Add pages
        self.dashboard_page = DashboardPage()
        self.products_page = ProductListPage()
        self.categories_page = CategoriesPage()
        self.sales_page = SalesPage()
        self.reports_page = ReportsPage()
        self.profile_page = ProfilePage(self.user)
        
        self.stacked_widget.addWidget(self.dashboard_page)  # Index 0: Dashboard
        self.stacked_widget.addWidget(self.products_page)   # Index 1: Products
        self.stacked_widget.addWidget(self.categories_page) # Index 2: Categories
        self.stacked_widget.addWidget(self.sales_page)      # Index 3: Sales
        self.stacked_widget.addWidget(self.reports_page)    # Index 4: Reports
        self.stacked_widget.addWidget(self.profile_page)    # Index 5: Profile
        
        content_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(content_layout)
        
        self.setCentralWidget(central_widget)
        
        # Set initial page to dashboard
        self.stacked_widget.setCurrentIndex(0)
    
    def switch_tab(self, index: int):
        """
        Switch to a different page tab.
        
        Args:
            index: Index of the tab to switch to (matches Sidebar tab indices)
        """
        if 0 <= index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)
            
            # Refresh page data when switching
            current_widget = self.stacked_widget.currentWidget()
            if hasattr(current_widget, 'refresh_data'):
                current_widget.refresh_data()

