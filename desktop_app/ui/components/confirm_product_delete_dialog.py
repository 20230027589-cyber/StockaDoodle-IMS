# confirm_product_delete_dialog.py
#
# This module provides a GitHub-style secure delete confirmation dialog for products.
# Requires user to type the current stock level to confirm deletion.
#
# Usage: Used when deleting products with secure confirmation.

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.config import AppConfig
from utils.styles import get_dialog_style


class ConfirmProductDeleteDialog(QDialog):
    """
    GitHub-style secure delete confirmation dialog for products.
    
    Requires user to type the current stock level to prevent accidental deletions.
    Shows detailed information about what will be deleted.
    """
    
    def __init__(self, product_name: str, product_id: int, current_stock: str, parent=None):
        """
        Initialize the confirmation dialog.
        
        Args:
            product_name: Name of the product to delete
            product_id: ID of the product
            current_stock: Current stock level (must match user input)
            parent: Parent widget
        """
        super().__init__(parent)
        self.product_name = product_name
        self.product_id = product_id
        self.current_stock = str(current_stock)
        self.setWindowTitle("⚠️ Delete Product")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.confirmed = False
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        self.setStyleSheet(get_dialog_style())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Warning title
        warning_label = QLabel("⚠️ Delete Product")
        warning_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.ACCENT_COLOR};
                font-size: 20pt;
                font-weight: bold;
            }}
        """)
        layout.addWidget(warning_label)
        
        # Main message
        message_label = QLabel("Are you absolutely sure you want to delete:")
        message_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
        """)
        layout.addWidget(message_label)
        
        # Product name and ID
        product_info = QLabel(f"        {self.product_name}\n        [Product ID: {self.product_id}]")
        product_info.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(product_info)
        
        # What will be removed
        removal_list = QLabel(
            "This will permanently remove:\n"
            "• All stock batches\n"
            "• Product history and logs\n"
            "• Category association"
        )
        removal_list.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(removal_list)
        
        # Confirmation instruction
        instruction = QLabel(f"👉 To confirm, type the current stock level: {self.current_stock}")
        instruction.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(instruction)
        
        # Input field with real-time validation
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"Type {self.current_stock} to confirm")
        self.input_field.textChanged.connect(self.validate_input)
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 2px solid {AppConfig.BORDER_COLOR};
                border-radius: {AppConfig.INPUT_RADIUS}px;
                padding: 12px;
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {AppConfig.ACCENT_COLOR};
            }}
        """)
        layout.addWidget(self.input_field)
        
        # Validation indicator (checkmark when correct)
        self.validation_label = QLabel("")
        self.validation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.validation_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.SECONDARY_COLOR};
                font-size: 18pt;
            }}
        """)
        layout.addWidget(self.validation_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.CARD_BACKGROUND};
                color: {AppConfig.TEXT_COLOR};
                padding: 10px 20px;
                border: 1px solid {AppConfig.BORDER_COLOR};
                border-radius: 6px;
            }}
        """)
        button_layout.addWidget(cancel_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setEnabled(False)  # Disabled until input matches
        self.delete_btn.clicked.connect(self.on_confirm)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.ACCENT_COLOR};
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:disabled {{
                background-color: {AppConfig.BORDER_COLOR};
                color: {AppConfig.TEXT_COLOR_ALT};
            }}
        """)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
    
    def validate_input(self, text: str):
        """Validate input in real-time."""
        entered_text = text.strip()
        
        # Case-sensitive, no spaces - exact match required
        if entered_text == self.current_stock:
            self.validation_label.setText("✓")
            self.delete_btn.setEnabled(True)
            self.delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppConfig.ACCENT_COLOR};
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                }}
            """)
        else:
            self.validation_label.setText("")
            self.delete_btn.setEnabled(False)
            self.delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppConfig.BORDER_COLOR};
                    color: {AppConfig.TEXT_COLOR_ALT};
                    padding: 10px 20px;
                    border: none;
                    border-radius: 6px;
                }}
            """)
    
    def on_confirm(self):
        """Handle confirm button click."""
        entered_text = self.input_field.text().strip()
        
        # Double-check (should already be validated, but be safe)
        if entered_text == self.current_stock:
            self.confirmed = True
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Confirmation Failed",
                f"Please type '{self.current_stock}' exactly to confirm deletion.",
                QMessageBox.StandardButton.Ok
            )
            self.input_field.clear()
            self.input_field.setFocus()
    
    def is_confirmed(self) -> bool:
        """Check if deletion was confirmed."""
        return self.confirmed

