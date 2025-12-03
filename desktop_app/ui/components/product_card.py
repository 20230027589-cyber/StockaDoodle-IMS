# product_card.py
#
# This module provides a modern product card widget component.
# Displays product information in a card format with image, price, stock status, and action buttons.
#
# Usage: Used in Products page to display products in a grid layout.

import os
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.helpers import format_currency, load_product_image, get_stock_status_label
from utils.styles import get_product_card_style


class ProductCard(QFrame):
    """
    Modern product card widget displaying product information in a card format.
    
    Features:
    - Product image (with placeholder if missing)
    - Product name and brand
    - Price in ₱ (Philippine Peso)
    - Stock status with color coding
    - Category information
    - Edit and Delete action buttons
    """
    
    def __init__(self, product_data: dict, on_view_details_callback=None,
                 on_edit_callback=None, on_delete_callback=None, parent=None):
        """
        Initialize the product card.
        
        Args:
            product_data: Dictionary containing product information
            on_view_details_callback: Callback function for view details button (receives product_data)
            on_edit_callback: Callback function for edit button (receives product_data) - deprecated, use on_view_details_callback
            on_delete_callback: Callback function for delete button (receives product_id, product_name) - deprecated, use on_view_details_callback
            parent: Parent widget
        """
        super().__init__(parent)
        self.product_data = product_data
        self.on_view_details_callback = on_view_details_callback
        self.on_edit_callback = on_edit_callback  # Keep for backward compatibility
        self.on_delete_callback = on_delete_callback  # Keep for backward compatibility
        
        # Apply card styling
        self.setObjectName("productCard")
        self.setProperty("class", "product-card")
        self.setStyleSheet(get_product_card_style())
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the product card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Product image container
        image_container = QWidget()
        image_container.setFixedHeight(200)
        image_container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border-radius: 8px;
                border: 1px solid {AppConfig.BORDER_COLOR};
            }}
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        self.image_label.setFixedHeight(200)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: none; border-radius: 8px;")
        
        # Load product image
        image_path = self.product_data.get('image_path') or self.product_data.get('image')
        if image_path:
            # Check if it's a base64 string or file path
            if isinstance(image_path, str) and image_path.startswith('data:image'):
                # Base64 image - decode it
                try:
                    import base64
                    header, encoded = image_path.split(',', 1)
                    image_data = base64.b64decode(encoded)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    self.image_label.setPixmap(pixmap.scaled(200, 200, 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation))
                except:
                    pixmap = load_product_image(None, target_size=(200, 200))
                    self.image_label.setPixmap(pixmap)
            else:
                # File path
                pixmap = load_product_image(image_path, target_size=(200, 200))
                self.image_label.setPixmap(pixmap)
        else:
            pixmap = load_product_image(None, target_size=(200, 200))
            self.image_label.setPixmap(pixmap)
        
        image_layout.addWidget(self.image_label)
        layout.addWidget(image_container)
        
        # Product information
        info_container = QVBoxLayout()
        info_container.setSpacing(6)
        
        # Product name
        name_label = QLabel(self.product_data.get('name', 'N/A'))
        name_label.setProperty("class", "product-title")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                font-weight: bold;
                max-height: 40px;
            }}
        """)
        info_container.addWidget(name_label)
        
        # Brand
        brand_label = QLabel(f"Brand: {self.product_data.get('brand', 'N/A')}")
        brand_label.setProperty("class", "product-detail")
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
            }}
        """)
        info_container.addWidget(brand_label)
        
        # Price in ₱
        price = float(self.product_data.get('price', 0))
        price_label = QLabel(format_currency(price))
        price_label.setProperty("class", "product-price")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.SECONDARY_COLOR};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
            }}
        """)
        info_container.addWidget(price_label)
        
        # Stock status
        stock = self.product_data.get('stock_level', 0) or self.product_data.get('stock', 0)
        min_stock = self.product_data.get('min_stock_level', 5)
        status_text, status_class = get_stock_status_label(stock, min_stock)
        
        stock_label = QLabel(f"Stock: {stock} ({status_text})")
        stock_label.setProperty("class", status_class)
        stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set color based on status
        if status_class == "status-no-stock":
            stock_color = AppConfig.ACCENT_COLOR
        elif status_class == "status-low-stock":
            stock_color = AppConfig.WARNING_COLOR
        else:
            stock_color = AppConfig.SECONDARY_COLOR
        
        stock_label.setStyleSheet(f"""
            QLabel {{
                color: {stock_color};
                font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
            }}
        """)
        info_container.addWidget(stock_label)
        
        # Category
        category_name = self.product_data.get('category_name', 'N/A')
        category_label = QLabel(f"Category: {category_name}")
        category_label.setProperty("class", "product-detail")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_SMALL}pt;
            }}
        """)
        info_container.addWidget(category_label)
        
        layout.addLayout(info_container)
        
        # Action button - View Details (replaces Edit/Delete)
        if self.on_view_details_callback or self.on_edit_callback or self.on_delete_callback:
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(10)
            
            # Use View Details callback if provided, otherwise fall back to old callbacks
            if self.on_view_details_callback:
                view_details_btn = QPushButton("View Details")
                view_details_btn.setProperty("class", "product-action-btn")
                view_details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                try:
                    from utils.helpers import get_feather_icon
                    view_details_btn.setIcon(get_feather_icon("eye", size=14))
                except:
                    pass
                view_details_btn.clicked.connect(lambda: self.on_view_details_callback(self.product_data))
                view_details_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {AppConfig.PRIMARY_COLOR};
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
                        font-weight: 500;
                        width: 100%;
                    }}
                    QPushButton:hover {{
                        background-color: {AppConfig.PRIMARY_HOVER};
                    }}
                """)
                buttons_layout.addWidget(view_details_btn)
            else:
                # Fallback to old Edit/Delete buttons for backward compatibility
                if self.on_edit_callback:
                    edit_btn = QPushButton("Edit")
                    edit_btn.setProperty("class", "product-action-btn")
                    edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    try:
                        from utils.helpers import get_feather_icon
                        edit_btn.setIcon(get_feather_icon("edit", size=14))
                    except:
                        pass
                    edit_btn.clicked.connect(lambda: self.on_edit_callback(self.product_data))
                    edit_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {AppConfig.PRIMARY_COLOR};
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 8px 16px;
                            font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
                            font-weight: 500;
                        }}
                        QPushButton:hover {{
                            background-color: {AppConfig.PRIMARY_HOVER};
                        }}
                    """)
                    buttons_layout.addWidget(edit_btn)
                
                if self.on_delete_callback:
                    delete_btn = QPushButton("Delete")
                    delete_btn.setProperty("class", "product-action-btn")
                    delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    try:
                        from utils.helpers import get_feather_icon
                        delete_btn.setIcon(get_feather_icon("trash-2", size=14))
                    except:
                        pass
                    delete_btn.clicked.connect(
                        lambda: self.on_delete_callback(
                            self.product_data.get('id'), 
                            self.product_data.get('name', 'Product')
                        )
                    )
                    delete_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {AppConfig.ACCENT_COLOR};
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 8px 16px;
                            font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
                            font-weight: 500;
                        }}
                        QPushButton:hover {{
                            background-color: #c0392b;
                        }}
                    """)
                    buttons_layout.addWidget(delete_btn)
            
            layout.addLayout(buttons_layout)
        
        # Set fixed size for consistent card sizing
        self.setFixedSize(280, 450)

