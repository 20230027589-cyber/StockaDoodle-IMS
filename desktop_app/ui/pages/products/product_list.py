# product_list.py
#
# This module provides the products list page for managers.
# Displays products in a modern card grid layout with filtering and sorting.
#
# Usage: Products management page in manager dashboard.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QScrollArea, QGridLayout,
                             QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success
from utils.helpers import get_feather_icon
from ui.components.product_card import ProductCard
from ui.pages.products.product_form import ProductFormDialog
from ui.pages.products.product_detail import ProductDetailPage
from PyQt6.QtWidgets import QStackedWidget


class ProductListPage(QWidget):
    """
    Products list page with modern card layout.
    
    Features:
    - Product cards in grid layout (4 cards per row)
    - Search functionality
    - Category filter dropdown
    - Sort by dropdown (Name, Price, Stock)
    - Add/Edit/Delete product functionality
    - Product images displayed
    - Prices in ₱ (Philippine Peso)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        self.all_products = []
        self.categories = []
        self.cards_per_row = 4
        
        self.init_ui()
        self.load_products()
        self.load_categories()
    
    def init_ui(self):
        """Initialize the products page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header section
        header_layout = QHBoxLayout()
        
        title = QLabel("Products")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
                font-weight: bold;
                padding: 5px 0;
            }}
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Search bar
        search_label = QLabel("Search:")
        header_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.filter_products)
        header_layout.addWidget(self.search_input)
        
        # Category filter
        category_label = QLabel("Category:")
        header_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setMaximumWidth(200)
        self.category_combo.currentIndexChanged.connect(self.filter_products)
        header_layout.addWidget(self.category_combo)
        
        # Sort by
        sort_label = QLabel("Sort by:")
        header_layout.addWidget(sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.setMaximumWidth(200)
        self.sort_combo.addItems([
            "Name (A-Z)",
            "Name (Z-A)",
            "Price (Low to High)",
            "Price (High to Low)",
            "Stock (Low to High)",
            "Stock (High to Low)"
        ])
        self.sort_combo.currentIndexChanged.connect(self.filter_products)
        header_layout.addWidget(self.sort_combo)
        
        # View setting (cards per row)
        view_label = QLabel("View:")
        header_layout.addWidget(view_label)
        
        view_display = QLabel(f"{self.cards_per_row} Cards per Row")
        view_display.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
            }}
        """)
        header_layout.addWidget(view_display)
        
        header_layout.addStretch()
        
        # Add Product button
        self.add_btn = QPushButton("+ Add New Product")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {AppConfig.PRIMARY_HOVER};
            }}
        """)
        try:
            icon = get_feather_icon("plus", size=18)
            self.add_btn.setIcon(icon)
        except:
            pass
        self.add_btn.clicked.connect(self.add_product)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # Products grid in scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Grid container
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.grid_container)
        layout.addWidget(self.scroll_area)
    
    def load_categories(self):
        """Load categories for filter dropdown."""
        try:
            self.categories = self.api.get_categories()
            self.category_combo.clear()
            self.category_combo.addItem("All Categories", None)
            
            for category in self.categories:
                self.category_combo.addItem(
                    category.get('name', 'N/A'),
                    category.get('id')
                )
        except Exception as e:
            error(f"Failed to load categories: {str(e)}")
    
    def load_products(self):
        """Load all products from API."""
        try:
            response = self.api.get_products(per_page=1000, include_image=True)
            
            # Handle different response formats
            if isinstance(response, dict):
                self.all_products = response.get('products', response.get('items', []))
            elif isinstance(response, list):
                self.all_products = response
            else:
                self.all_products = []
            
            # Resolve category names
            category_map = {cat.get('id'): cat.get('name', 'N/A') for cat in self.categories}
            for product in self.all_products:
                category_id = product.get('category_id')
                product['category_name'] = category_map.get(category_id, 'Uncategorized')
            
            self.filter_products()
            
        except Exception as e:
            error(f"Failed to load products: {str(e)}")
    
    def filter_products(self):
        """Filter and sort products, then display in grid."""
        # Clear existing cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        # Get filter criteria
        search_text = self.search_input.text().lower()
        selected_category_id = self.category_combo.currentData()
        
        # Filter products
        filtered = []
        for product in self.all_products:
            # Search filter
            if search_text:
                if search_text not in product.get('name', '').lower() and \
                   search_text not in product.get('brand', '').lower():
                    continue
            
            # Category filter
            if selected_category_id is not None:
                if product.get('category_id') != selected_category_id:
                    continue
            
            filtered.append(product)
        
        # Sort products
        sort_option = self.sort_combo.currentText()
        if "Name (A-Z)" in sort_option:
            filtered.sort(key=lambda p: p.get('name', '').lower())
        elif "Name (Z-A)" in sort_option:
            filtered.sort(key=lambda p: p.get('name', '').lower(), reverse=True)
        elif "Price (Low to High)" in sort_option:
            filtered.sort(key=lambda p: float(p.get('price', 0)))
        elif "Price (High to Low)" in sort_option:
            filtered.sort(key=lambda p: float(p.get('price', 0)), reverse=True)
        elif "Stock (Low to High)" in sort_option:
            filtered.sort(key=lambda p: p.get('stock_level', 0) or p.get('stock', 0))
        elif "Stock (High to Low)" in sort_option:
            filtered.sort(key=lambda p: p.get('stock_level', 0) or p.get('stock', 0), reverse=True)
        
        # Display products in grid
        row = 0
        col = 0
        
        for product in filtered:
            card = ProductCard(
                product,
                on_view_details_callback=self.view_product_details,
                on_edit_callback=self.edit_product,  # Keep for backward compatibility
                on_delete_callback=self.delete_product  # Keep for backward compatibility
            )
            
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= self.cards_per_row:
                col = 0
                row += 1
        
        # Add empty message if no products
        if not filtered:
            no_products_label = QLabel("No products found. Click 'Add New Product' to create one.")
            no_products_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_products_label.setStyleSheet(f"""
                QLabel {{
                    color: {AppConfig.TEXT_COLOR_ALT};
                    font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                    padding: 40px;
                }}
            """)
            self.grid_layout.addWidget(no_products_label, 0, 0, 1, self.cards_per_row)
    
    def add_product(self):
        """Open dialog to add new product."""
        dialog = ProductFormDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()
            self.load_categories()
    
    def edit_product(self, product_data: dict):
        """Open dialog to edit product."""
        dialog = ProductFormDialog(product_data=product_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()
            self.load_categories()
    
    def delete_product(self, product_id: int, product_name: str):
        """Delete product with GitHub-style confirmation."""
        try:
            # Get current stock for confirmation
            product = next((p for p in self.all_products if p.get('id') == product_id), None)
            if not product:
                error("Product not found.")
                return
            
            current_stock = str(product.get('stock_level', 0) or product.get('stock', 0) or 0)
            
            # Show GitHub-style confirmation dialog - requires typing stock level
            from ui.components.confirm_product_delete_dialog import ConfirmProductDeleteDialog
            dialog = ConfirmProductDeleteDialog(product_name, product_id, current_stock, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.api.delete_product(product_id)
                success(f"Product '{product_name}' deleted successfully.")
                self.load_products()
        
        except Exception as e:
            error(f"Failed to delete product: {str(e)}")
    
    def view_product_details(self, product_data: dict):
        """Open product detail page in a dialog."""
        from PyQt6.QtWidgets import QDialog
        
        # Create dialog window
        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle(f"Product Details - {product_data.get('name', 'Product')}")
        detail_dialog.setMinimumSize(1000, 700)
        
        # Create product detail page
        detail_page = ProductDetailPage(product_data, detail_dialog)
        detail_page.back_requested.connect(detail_dialog.close)
        
        # Layout for dialog
        layout = QVBoxLayout(detail_dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(detail_page)
        
        # Show dialog
        detail_dialog.exec()
        
        # Refresh product list after dialog closes (in case product was edited/deleted)
        self.load_products()
        self.load_categories()
    
    def refresh_data(self):
        """Refresh products list (called when tab is switched to)."""
        self.load_products()
        self.load_categories()
