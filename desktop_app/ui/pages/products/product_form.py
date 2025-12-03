# product_form.py
#
# This module provides a dialog for adding and editing products.
# Features image upload, form validation, and proper error handling.
#
# Usage: Dialog shown when adding or editing products in the Products page.

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFormLayout,
                             QSpinBox, QDoubleSpinBox, QComboBox, QFileDialog,
                             QDateEdit, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success, warning
from utils.helpers import load_product_image, format_currency


class ProductFormDialog(QDialog):
    """
    Dialog for adding or editing products.
    
    Features:
    - Product name, brand, category, price
    - Stock quantity and minimum stock level
    - Expiration date with calendar popup
    - Image upload and preview
    - Form validation
    """
    
    def __init__(self, product_data: dict = None, parent=None):
        """
        Initialize the product form dialog.
        
        Args:
            product_data: Existing product data for editing (None for new product)
            parent: Parent widget
        """
        super().__init__(parent)
        self.api = get_api()
        self.product_data = product_data
        self.is_edit_mode = product_data is not None
        self.image_path = None
        self.image_base64 = None
        
        self.setWindowTitle("Edit Product" if self.is_edit_mode else "Add New Product")
        self.setMinimumSize(500, 700)
        self.setModal(True)
        
        self.init_ui()
        if self.is_edit_mode:
            self.load_product_data()
    
    def init_ui(self):
        """Initialize the form UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Product Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        form_layout.addRow("Product Name *:", self.name_input)
        
        # Brand
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Enter brand name")
        form_layout.addRow("Brand:", self.brand_input)
        
        # Category
        self.category_combo = QComboBox()
        self.category_combo.setPlaceholderText("Select category")
        form_layout.addRow("Category *:", self.category_combo)
        self.load_categories()
        
        # Price in ₱
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0.01)
        self.price_input.setMaximum(999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("₱ ")
        self.price_input.setValue(0.00)
        form_layout.addRow("Price *:", self.price_input)
        
        # Stock Quantity
        self.stock_input = QSpinBox()
        self.stock_input.setMinimum(0)
        self.stock_input.setMaximum(999999)
        self.stock_input.setValue(0)
        form_layout.addRow("Stock Quantity:", self.stock_input)
        
        # Minimum Stock Level
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setMinimum(0)
        self.min_stock_input.setMaximum(9999)
        self.min_stock_input.setValue(5)
        form_layout.addRow("Min Stock Level:", self.min_stock_input)
        
        # Expiration Date
        self.expiration_date = QDateEdit()
        self.expiration_date.setCalendarPopup(True)
        self.expiration_date.setDate(QDate.currentDate().addYears(1))
        self.expiration_date.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Expiration Date:", self.expiration_date)
        
        # Details/Description
        self.details_input = QTextEdit()
        self.details_input.setPlaceholderText("Enter product details or description")
        self.details_input.setMaximumHeight(100)
        form_layout.addRow("Details:", self.details_input)
        
        # Image upload
        image_layout = QHBoxLayout()
        
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(120, 120)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet(f"""
            QLabel {{
                border: 2px dashed {AppConfig.BORDER_COLOR};
                border-radius: 8px;
                background-color: {AppConfig.INPUT_BACKGROUND};
            }}
        """)
        self.image_preview.setText("No Image")
        image_layout.addWidget(self.image_preview)
        
        image_buttons = QVBoxLayout()
        
        upload_btn = QPushButton("Upload Image")
        upload_btn.clicked.connect(self.upload_image)
        image_buttons.addWidget(upload_btn)
        
        remove_btn = QPushButton("Remove Image")
        remove_btn.clicked.connect(self.remove_image)
        image_buttons.addWidget(remove_btn)
        
        image_layout.addLayout(image_buttons)
        image_layout.addStretch()
        
        form_layout.addRow("Product Image:", image_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Product")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 10px 20px;
            }}
        """)
        save_btn.clicked.connect(self.save_product)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_categories(self):
        """Load categories into the combo box."""
        try:
            categories = self.api.get_categories()
            self.category_combo.clear()
            self.category_combo.addItem("Select Category...", None)
            
            for category in categories:
                self.category_combo.addItem(
                    category.get('name', 'N/A'),
                    category.get('id')
                )
        except Exception as e:
            error(f"Failed to load categories: {str(e)}")
    
    def load_product_data(self):
        """Load existing product data into the form."""
        if not self.product_data:
            return
        
        self.name_input.setText(self.product_data.get('name', ''))
        self.brand_input.setText(self.product_data.get('brand', ''))
        self.price_input.setValue(float(self.product_data.get('price', 0)))
        self.stock_input.setValue(self.product_data.get('stock_level', 0) or self.product_data.get('stock', 0))
        self.min_stock_input.setValue(self.product_data.get('min_stock_level', 5))
        self.details_input.setPlainText(self.product_data.get('details', ''))
        
        # Set category
        category_id = self.product_data.get('category_id')
        if category_id:
            index = self.category_combo.findData(category_id)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        
        # Set expiration date
        exp_date = self.product_data.get('expiration_date')
        if exp_date:
            try:
                if isinstance(exp_date, str):
                    qdate = QDate.fromString(exp_date, "yyyy-MM-dd")
                    if qdate.isValid():
                        self.expiration_date.setDate(qdate)
            except:
                pass
        
        # Load image
        image_path = self.product_data.get('image_path') or self.product_data.get('image')
        if image_path:
            self.image_path = image_path
            pixmap = load_product_image(image_path, target_size=(120, 120))
            self.image_preview.setPixmap(pixmap)
            self.image_preview.setText("")
    
    def upload_image(self):
        """Open file dialog to upload product image and convert to base64."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Product Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.webp)"
        )
        
        if file_path:
            # Check file size (max 5MB)
            file_size = os.path.getsize(file_path)
            if file_size > 5 * 1024 * 1024:
                warning("Image file is too large. Maximum size is 5MB.")
                return
            
            self.image_path = file_path
            # Store base64 string for API submission
            import base64
            with open(file_path, "rb") as f:
                self.image_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Show preview
            pixmap = load_product_image(file_path, target_size=(120, 120))
            self.image_preview.setPixmap(pixmap)
            self.image_preview.setText("")
    
    def remove_image(self):
        """Remove the selected image."""
        self.image_path = None
        self.image_base64 = None
        self.image_preview.clear()
        self.image_preview.setText("No Image")
    
    def save_product(self):
        """Validate and save the product."""
        # Validation
        if not self.name_input.text().strip():
            error("Product name is required.")
            return
        
        category_id = self.category_combo.currentData()
        if not category_id:
            error("Please select a category.")
            return
        
        if self.price_input.value() <= 0:
            error("Price must be greater than 0.")
            return
        
        try:
            # Prepare product data
            name = self.name_input.text().strip()
            brand = self.brand_input.text().strip() or None
            price_cents = int(self.price_input.value() * 100)  # Convert to cents/int
            min_stock = self.min_stock_input.value()
            details = self.details_input.toPlainText().strip() or None
            expiration_date = self.expiration_date.date().toString("yyyy-MM-dd")
            stock = self.stock_input.value() if self.stock_input.value() > 0 else None
            
            # Handle image - use base64 string
            import base64
            image_base64_str = None
            if self.image_base64:
                image_base64_str = self.image_base64
            elif self.image_path:
                # Load from file path if base64 not set
                with open(self.image_path, 'rb') as f:
                    image_base64_str = base64.b64encode(f.read()).decode('utf-8')
            
            # Save via API
            if self.is_edit_mode:
                product_id = self.product_data.get('id')
                update_data = {
                    'name': name,
                    'brand': brand,
                    'category_id': category_id,
                    'price': price_cents,
                    'min_stock_level': min_stock,
                    'details': details,
                    'expiration_date': expiration_date,
                }
                if stock is not None:
                    update_data['stock_level'] = stock
                if image_base64_str:
                    update_data['image_base64'] = image_base64_str
                
                result = self.api.update_product(product_id, **update_data)
            else:
                # For create, pass base64 string directly
                result = self.api.create_product(
                    name=name,
                    price=price_cents,
                    brand=brand,
                    category_id=category_id,
                    min_stock_level=min_stock,
                    details=details,
                    stock_level=stock,
                    expiration_date=expiration_date,
                    image_base64=image_base64_str
                )
            
            success(f"Product {'updated' if self.is_edit_mode else 'created'} successfully!")
            self.accept()
            
        except Exception as e:
            error(f"Failed to save product: {str(e)}")
    
    def get_product_data(self) -> dict:
        """Get the product data from the form."""
        return {
            'name': self.name_input.text().strip(),
            'brand': self.brand_input.text().strip(),
            'category_id': self.category_combo.currentData(),
            'price': self.price_input.value(),
            'stock': self.stock_input.value(),
            'min_stock_level': self.min_stock_input.value(),
            'details': self.details_input.toPlainText().strip(),
            'expiration_date': self.expiration_date.date().toString("yyyy-MM-dd"),
            'image_path': self.image_path
        }

