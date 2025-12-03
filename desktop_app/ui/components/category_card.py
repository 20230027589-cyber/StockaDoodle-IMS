# category_card.py
#
# This module provides a modern category card widget component.
# Displays category information in a card format with image, name, description, and action buttons.
#
# Usage: Used in Categories page to display categories in a grid layout.

import os
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.helpers import load_product_image, shorten_text
from utils.styles import get_category_card_style


def load_category_image(image_data, target_size=(200, 200)):
    """
    Load a category image from base64 data or return placeholder.
    
    Args:
        image_data: Base64 string or None
        target_size: Tuple of (width, height) for the scaled QPixmap
        
    Returns:
        QPixmap: The scaled QPixmap or placeholder
    """
    if image_data:
        try:
            import base64
            # Handle both data:image format and raw base64
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    header, encoded = image_data.split(',', 1)
                    image_bytes = base64.b64decode(encoded)
                else:
                    image_bytes = base64.b64decode(image_data)
                
                pixmap = QPixmap()
                pixmap.loadFromData(image_bytes)
                if not pixmap.isNull():
                    return pixmap.scaled(
                        target_size[0], target_size[1],
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
        except Exception as e:
            print(f"Error loading category image: {e}")
    
    # Return placeholder
    return load_product_image(None, target_size=target_size)


class CategoryCard(QFrame):
    """
    Modern category card widget displaying category information in a card format.
    
    Features:
    - Category image (with placeholder if missing)
    - Category name and ID
    - Description (shortened with ellipsis if long)
    - Edit and Delete action buttons
    """
    
    def __init__(self, category_data: dict, on_view_details_callback=None,
                 on_edit_callback=None, on_delete_callback=None, parent=None):
        """
        Initialize the category card.
        
        Args:
            category_data: Dictionary containing category information
            on_view_details_callback: Callback function for view details (receives category_data)
            on_edit_callback: Callback function for edit button (receives category_data)
            on_delete_callback: Callback function for delete button (receives category_id, category_name)
            parent: Parent widget
        """
        super().__init__(parent)
        self.category_data = category_data
        self.on_view_details_callback = on_view_details_callback
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback
        
        # Apply card styling
        self.setObjectName("categoryCard")
        self.setProperty("class", "category-card")
        self.setStyleSheet(get_category_card_style())
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the category card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Category image container
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
        self.image_label.setProperty("class", "category-image")
        self.image_label.setStyleSheet("border: none; border-radius: 8px;")
        
        # Load category image
        image_data = self.category_data.get('image_base64') or self.category_data.get('category_image')
        pixmap = load_category_image(image_data, target_size=(200, 200))
        self.image_label.setPixmap(pixmap)
        
        image_layout.addWidget(self.image_label)
        layout.addWidget(image_container)
        
        # Category information
        info_container = QVBoxLayout()
        info_container.setSpacing(6)
        
        # Category name
        name_label = QLabel(self.category_data.get('name', 'N/A'))
        name_label.setProperty("class", "category-title")
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
        
        # Category ID
        category_id = self.category_data.get('id', 'N/A')
        id_label = QLabel(f"ID: {category_id}")
        id_label.setProperty("class", "category-detail")
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        id_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
            }}
        """)
        info_container.addWidget(id_label)
        
        # Description (shortened if long)
        description = self.category_data.get('description', 'No description')
        if description and description != 'N/A':
            short_desc = shorten_text(description, max_length=60)
            desc_label = QLabel(short_desc)
        else:
            desc_label = QLabel("No description")
        desc_label.setProperty("class", "category-detail")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_SMALL}pt;
            }}
        """)
        info_container.addWidget(desc_label)
        
        layout.addLayout(info_container)
        
        # Action buttons
        if self.on_view_details_callback or self.on_edit_callback or self.on_delete_callback:
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(10)
            
            # Use View Details callback if provided
            if self.on_view_details_callback:
                view_details_btn = QPushButton("View Details")
                view_details_btn.setProperty("class", "category-action-btn")
                view_details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                try:
                    from utils.helpers import get_feather_icon
                    view_details_btn.setIcon(get_feather_icon("eye", size=14))
                except:
                    pass
                view_details_btn.clicked.connect(lambda: self.on_view_details_callback(self.category_data))
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
                # Fallback to Edit/Delete buttons
                if self.on_edit_callback:
                    edit_btn = QPushButton("Edit")
                    edit_btn.setProperty("class", "category-action-btn")
                    edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    try:
                        from utils.helpers import get_feather_icon
                        edit_btn.setIcon(get_feather_icon("edit", size=14))
                    except:
                        pass
                    edit_btn.clicked.connect(lambda: self.on_edit_callback(self.category_data))
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
                    delete_btn.setProperty("class", "category-action-btn")
                    delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    try:
                        from utils.helpers import get_feather_icon
                        delete_btn.setIcon(get_feather_icon("trash-2", size=14))
                    except:
                        pass
                    delete_btn.clicked.connect(
                        lambda: self.on_delete_callback(
                            self.category_data.get('id'), 
                            self.category_data.get('name', 'Category')
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
        
        # Set fixed size for consistent card sizing (matches ProductCard)
        self.setFixedSize(280, 450)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click event to open category editor."""
        if self.on_edit_callback:
            self.on_edit_callback(self.category_data)
        elif self.on_view_details_callback:
            self.on_view_details_callback(self.category_data)
        super().mouseDoubleClickEvent(event)

