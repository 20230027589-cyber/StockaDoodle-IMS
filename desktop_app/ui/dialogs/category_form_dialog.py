# category_form_dialog.py
#
# This module provides a dialog for adding and editing categories.
# Features image upload, form validation, and proper error handling.
#
# Usage: Dialog shown when adding or editing categories in the Categories page.

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFormLayout,
                             QFileDialog, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success, warning
from utils.helpers import load_product_image
from utils.styles import get_dialog_style, get_image_preview_style, get_primary_button_style


class CategoryFormDialog(QDialog):
    """
    Dialog for adding or editing categories.
    
    Features:
    - Category name, description
    - Image upload and preview
    - Form validation
    """
    
    def __init__(self, category_data: dict = None, parent=None):
        """
        Initialize the category form dialog.
        
        Args:
            category_data: Existing category data for editing (None for new category)
            parent: Parent widget
        """
        super().__init__(parent)
        self.api = get_api()
        self.category_data = category_data
        self.is_edit_mode = category_data is not None
        self.image_path = None
        self.image_base64 = None
        
        self.setWindowTitle("Edit Category" if self.is_edit_mode else "Add New Category")
        self.setMinimumSize(500, 600)
        self.setModal(True)
        
        self.init_ui()
        if self.is_edit_mode:
            self.load_category_data()
    
    def init_ui(self):
        """Initialize the form UI."""
        self.setStyleSheet(get_dialog_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Category Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter category name")
        form_layout.addRow("Category Name *:", self.name_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter category description")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_input)
        
        # Image upload
        image_layout = QHBoxLayout()
        
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(120, 120)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet(get_image_preview_style())
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
        
        form_layout.addRow("Category Image:", image_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Category")
        save_btn.setStyleSheet(get_primary_button_style())
        save_btn.clicked.connect(self.save_category)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_category_data(self):
        """Load existing category data into the form."""
        if not self.category_data:
            return
        
        self.name_input.setText(self.category_data.get('name', ''))
        self.description_input.setPlainText(self.category_data.get('description', ''))
        
        # Load image
        image_data = self.category_data.get('image_base64') or self.category_data.get('category_image')
        if image_data:
            try:
                import base64
                if isinstance(image_data, str):
                    if image_data.startswith('data:image'):
                        header, encoded = image_data.split(',', 1)
                        image_bytes = base64.b64decode(encoded)
                    else:
                        image_bytes = base64.b64decode(image_data)
                    
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_bytes)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(120, 120, 
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
                        self.image_preview.setPixmap(scaled_pixmap)
                        self.image_preview.setText("")
                        self.image_base64 = image_data if not image_data.startswith('data:image') else encoded
            except Exception as e:
                print(f"Error loading category image: {e}")
    
    def upload_image(self):
        """Open file dialog to upload category image and convert to base64."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Category Image",
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
    
    def save_category(self):
        """Validate and save the category."""
        # Validation
        if not self.name_input.text().strip():
            error("Category name is required.")
            return
        
        try:
            # Prepare category data
            name = self.name_input.text().strip()
            description = self.description_input.toPlainText().strip() or None
            
            # Save via API
            if self.is_edit_mode:
                category_id = self.category_data.get('id')
                update_data = {
                    'name': name,
                    'description': description,
                }
                if self.image_base64:
                    update_data['image_base64'] = self.image_base64
                
                result = self.api.update_category(category_id, **update_data)
            else:
                # For create, pass image_base64 directly
                result = self.api.create_category(
                    name=name,
                    description=description,
                    image_base64=self.image_base64
                )
            
            success(f"Category {'updated' if self.is_edit_mode else 'created'} successfully!")
            self.accept()
            
        except Exception as e:
            error(f"Failed to save category: {str(e)}")
    
    def get_category_data(self) -> dict:
        """Get the category data from the form."""
        return {
            'name': self.name_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'image_path': self.image_path
        }

