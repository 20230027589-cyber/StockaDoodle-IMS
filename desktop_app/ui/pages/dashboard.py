# dashboard.py
#
# This module provides the dashboard page for the manager.
# Displays sales charts (line chart with 1/7/30 day filters) and category distribution (pie chart).
#
# Usage: Main overview page shown after login for manager role.

from datetime import datetime, timedelta
from typing import Dict, List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton
from PyQt6.QtCore import Qt, QThread, pyqtSignal
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
except ImportError:
    # Fallback for older matplotlib versions
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, warning
from utils.helpers import format_currency
from utils.font_loader import get_inter_font
from ui.components.modern_card import ModernCard


class DataLoaderThread(QThread):
    """Background thread for loading dashboard data without blocking UI."""
    
    sales_data_loaded = pyqtSignal(dict)
    categories_data_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api, days: int = 7):
        super().__init__()
        self.api = api
        self.days = days
    
    def run(self):
        """Load sales and categories data."""
        try:
            # Load sales data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.days)
            
            sales_response = self.api.get_sales(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            
            self.sales_data_loaded.emit(sales_response)
            
            # Load categories data (always latest, not date-dependent)
            categories = self.api.get_categories()
            
            # Load products to calculate category distribution (always latest, not date-filtered)
            # Category distribution should always show current/latest data
            products_response = self.api.get_products(per_page=1000)  # Get all products
            products = products_response.get('products', [])
            
            categories_data = {
                'categories': categories,
                'products': products
            }
            
            self.categories_data_loaded.emit(categories_data)
            
        except Exception as e:
            self.error_occurred.emit(str(e))


class DashboardPage(QWidget):
    """
    Manager dashboard page with sales charts and category distribution.
    
    Features:
    - Sales line chart with 1/7/30 day filters
    - Category distribution pie chart
    - Summary cards (total sales, products, etc.)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        self.current_days = 7
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the dashboard UI."""
        # Light background for main content
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #F8FAFC;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Page title
        title = QLabel("Dashboard Overview")
        title.setFont(get_inter_font("Bold", 28))
        title.setStyleSheet(f"""
            QLabel {{
                color: #1E293B;
                font-size: 28pt;
                font-weight: bold;
                padding: 0;
            }}
        """)
        layout.addWidget(title)
        
        # Charts container
        charts_layout = QHBoxLayout()
        
        # Sales line chart card
        sales_card = ModernCard()
        sales_layout = QVBoxLayout()
        sales_layout.setContentsMargins(0, 0, 0, 0)
        sales_layout.setSpacing(10)
        
        # Sales Trend header with filter in upper-right
        chart_header = QHBoxLayout()
        chart_label = QLabel("Sales Trend")
        chart_label.setFont(get_inter_font("Bold", 18))
        chart_label.setStyleSheet(f"""
            QLabel {{
                color: #1E293B;
                font-size: 18pt;
                font-weight: bold;
                padding: 0;
            }}
        """)
        chart_header.addWidget(chart_label)
        chart_header.addStretch()
        
        # Time period filter - inside Sales Trend card, upper-right
        period_label = QLabel("Time Period:")
        period_label.setFont(get_inter_font("Regular", 13))
        period_label.setStyleSheet("color: #64748B;")
        chart_header.addWidget(period_label)
        self.filter_combo = QComboBox()
        self.filter_combo.setFont(get_inter_font("Regular", 13))
        self.filter_combo.addItems(["1 Day", "7 Days", "30 Days"])
        self.filter_combo.setCurrentText("7 Days")
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 6px 12px;
                color: #1E293B;
            }}
            QComboBox:hover {{
                border-color: #3B82F6;
            }}
        """)
        chart_header.addWidget(self.filter_combo)
        
        sales_layout.addLayout(chart_header)
        
        # Matplotlib figure for sales chart - light background
        self.sales_figure = Figure(facecolor='white', figsize=(6, 4))
        self.sales_canvas = FigureCanvas(self.sales_figure)
        sales_layout.addWidget(self.sales_canvas)
        
        sales_card.layout.addLayout(sales_layout)
        charts_layout.addWidget(sales_card, stretch=2)
        
        # Category pie chart card
        category_card = ModernCard()
        category_layout = QVBoxLayout()
        
        pie_label = QLabel("Category Distribution")
        pie_label.setFont(get_inter_font("Bold", 18))
        pie_label.setStyleSheet(f"""
            QLabel {{
                color: #1E293B;
                font-size: 18pt;
                font-weight: bold;
                padding: 0;
            }}
        """)
        category_layout.addWidget(pie_label)
        
        # Matplotlib figure for pie chart - light background
        self.pie_figure = Figure(facecolor='white', figsize=(5, 4))
        self.pie_canvas = FigureCanvas(self.pie_figure)
        category_layout.addWidget(self.pie_canvas)
        
        category_card.layout.addLayout(category_layout)
        charts_layout.addWidget(category_card, stretch=1)
        
        layout.addLayout(charts_layout)
        
        layout.addStretch()
    
    def on_filter_changed(self, text: str):
        """
        Handle filter change.
        
        Args:
            text: Selected filter text (1 Day, 7 Days, 30 Days)
        """
        days_map = {"1 Day": 1, "7 Days": 7, "30 Days": 30}
        self.current_days = days_map.get(text, 7)
        self.load_data()
    
    def load_data(self):
        """Load dashboard data from API."""
        self.loader_thread = DataLoaderThread(self.api, self.current_days)
        self.loader_thread.sales_data_loaded.connect(self.update_sales_chart)
        self.loader_thread.categories_data_loaded.connect(self.update_category_chart)
        self.loader_thread.error_occurred.connect(lambda msg: error(f"Failed to load data: {msg}"))
        self.loader_thread.start()
    
    def update_sales_chart(self, sales_response: Dict):
        """
        Update the sales line chart with new data.
        
        Args:
            sales_response: API response with sales data
        """
        try:
            # Extract sales data
            sales_data = sales_response.get('sales', [])
            summary = sales_response.get('summary', {})
            
            # Aggregate sales by date
            daily_sales = {}
            for sale in sales_data:
                sale_date = sale.get('created_at', '')
                if sale_date:
                    # Parse date (assuming ISO format)
                    try:
                        if isinstance(sale_date, str):
                            date_obj = datetime.fromisoformat(sale_date.replace('Z', '+00:00'))
                        else:
                            date_obj = sale_date
                        
                        date_key = date_obj.date().isoformat()
                        daily_sales[date_key] = daily_sales.get(date_key, 0) + sale.get('total_amount', 0)
                    except:
                        continue
            
            # Sort dates
            sorted_dates = sorted(daily_sales.keys())
            dates = sorted_dates
            amounts = [daily_sales[date] for date in dates]
            
            # Clear and redraw chart
            self.sales_figure.clear()
            ax = self.sales_figure.add_subplot(111)
            
            if amounts:
                ax.plot(dates, amounts, color='#3B82F6', linewidth=2.5, marker='o', markersize=5)
                ax.fill_between(dates, amounts, alpha=0.2, color='#3B82F6')
            else:
                ax.text(0.5, 0.5, 'No sales data available', 
                       ha='center', va='center', 
                       transform=ax.transAxes,
                       color='#64748B',
                       fontsize=13)
            
            ax.set_facecolor('white')
            ax.tick_params(colors='#475569')
            ax.set_xlabel('Date', color='#1E293B', fontsize=11)
            ax.set_ylabel('Sales Amount (₱)', color='#1E293B', fontsize=11)
            ax.set_title(f'Sales Trend - {self.current_days} Days', color='#1E293B', fontsize=14, fontweight='bold')
            
            # Rotate x-axis labels
            if len(dates) > 5:
                ax.set_xticklabels(dates, rotation=45, ha='right')
            else:
                ax.set_xticklabels(dates)
            
            # Format y-axis as currency
            ax.yaxis.set_major_formatter(
                lambda x, p: format_currency(x)
            )
            
            self.sales_figure.tight_layout()
            self.sales_canvas.draw()
            
        except Exception as e:
            error(f"Failed to update sales chart: {str(e)}")
    
    def update_category_chart(self, categories_data: Dict):
        """
        Update the category pie chart with new data.
        
        Args:
            categories_data: Dictionary with categories and products (always latest data)
        """
        try:
            categories = categories_data.get('categories', [])
            products = categories_data.get('products', [])
            
            # Calculate category distribution from products (always latest, not date-dependent)
            category_counts = {}
            category_id_to_name = {cat.get('id'): cat.get('name', 'Unknown') for cat in categories}
            
            # Count products per category
            for product in products:
                category_id = product.get('category_id')
                if category_id and category_id in category_id_to_name:
                    category_name = category_id_to_name[category_id]
                    category_counts[category_name] = category_counts.get(category_name, 0) + 1
                else:
                    category_counts['Uncategorized'] = category_counts.get('Uncategorized', 0) + 1
            
            # If no products, use category count directly
            if not category_counts:
                for cat in categories:
                    category_counts[cat.get('name', 'Unknown')] = 1
            
            category_sales = category_counts
            
            # Clear and redraw chart
            self.pie_figure.clear()
            ax = self.pie_figure.add_subplot(111)
            
            if category_sales:
                labels = list(category_sales.keys())
                sizes = list(category_sales.values())
                
                # Modern blue color palette
                colors = [
                    '#3B82F6',  # Blue
                    '#8B5CF6',  # Purple
                    '#10B981',  # Green
                    '#F59E0B',  # Orange
                    '#EF4444',  # Red
                    '#06B6D4',  # Cyan
                ]
                
                # Extend colors if needed
                while len(colors) < len(labels):
                    colors.append('#3B82F6')
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                      colors=colors[:len(labels)],
                      textprops={'color': '#1E293B', 'fontsize': 10})
                ax.set_title('Category Distribution', color='#1E293B', fontsize=14, fontweight='bold')
            else:
                ax.text(0.5, 0.5, 'No category data available', 
                       ha='center', va='center', 
                       transform=ax.transAxes,
                       color='#64748B',
                       fontsize=13)
            
            ax.set_facecolor('white')
            self.pie_figure.tight_layout()
            self.pie_canvas.draw()
            
        except Exception as e:
            error(f"Failed to update category chart: {str(e)}")
    
    def refresh_data(self):
        """Refresh dashboard data (called when tab is switched to)."""
        self.load_data()

