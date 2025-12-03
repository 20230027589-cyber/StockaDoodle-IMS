# sales.py
#
# This module provides the sales management page for managers.
# Displays sales records with filtering and viewing capabilities.
#
# Usage: Sales viewing page in manager dashboard.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error
from utils.styles import apply_table_styles
from utils.helpers import format_currency, format_datetime


class SalesPage(QWidget):
    """
    Sales management page.
    
    Features:
    - Sales table with date filtering
    - View sale details
    - Filter by date range
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        
        self.init_ui()
        self.load_sales()
    
    def init_ui(self):
        """Initialize the sales page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Page header
        header_layout = QHBoxLayout()
        
        title = QLabel("Sales")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Date filters
        header_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setCalendarPopup(True)
        header_layout.addWidget(self.start_date)
        
        header_layout.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        header_layout.addWidget(self.end_date)
        
        filter_btn = QPushButton("Filter")
        filter_btn.clicked.connect(self.load_sales)
        header_layout.addWidget(filter_btn)
        
        layout.addLayout(header_layout)
        
        # Sales table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Sale ID", "Retailer", "Items", "Total"])
        apply_table_styles(self.table)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
    
    def load_sales(self):
        """Load sales from API."""
        try:
            start_date_str = self.start_date.date().toString('yyyy-MM-dd')
            end_date_str = self.end_date.date().toString('yyyy-MM-dd')
            
            sales_response = self.api.get_sales(
                start_date=start_date_str,
                end_date=end_date_str
            )
            
            # Handle different response formats
            if isinstance(sales_response, dict):
                sales = sales_response.get('sales', [])
            elif isinstance(sales_response, list):
                sales = sales_response
            else:
                sales = []
            
            # Populate table
            self.table.setRowCount(len(sales))
            
            for row, sale in enumerate(sales):
                # Date
                created_at = sale.get('created_at', '')
                date_item = QTableWidgetItem(format_datetime(created_at) if created_at else 'N/A')
                self.table.setItem(row, 0, date_item)
                
                # Sale ID
                sale_id = sale.get('id') or sale.get('_id') or sale.get('sale_id', 'N/A')
                self.table.setItem(row, 1, QTableWidgetItem(str(sale_id)))
                
                # Retailer
                retailer_name = sale.get('retailer_name', 'N/A')
                self.table.setItem(row, 2, QTableWidgetItem(retailer_name))
                
                # Items count
                items = sale.get('items', [])
                items_count = len(items) if items else 0
                self.table.setItem(row, 3, QTableWidgetItem(str(items_count)))
                
                # Total
                total = sale.get('total_amount', 0)
                total_item = QTableWidgetItem(format_currency(total))
                self.table.setItem(row, 4, total_item)
            
            # Resize columns to content
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            error(f"Failed to load sales: {str(e)}")
    
    def refresh_data(self):
        """Refresh sales list (called when tab is switched to)."""
        self.load_sales()

