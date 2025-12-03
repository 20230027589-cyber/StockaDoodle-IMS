# confirm_delete_dialog.py
#
# This module provides a secure delete confirmation dialog.
# Requires user to type in confirmation text to prevent accidental deletions.
#
# Usage: Used when deleting products, batches, or other critical items.

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from utils.config import AppConfig
from utils.styles import get_dialog_style


class ConfirmDeleteDialog(QDialog):
    """
    Secure delete confirmation dialog.
    
    Requires user to type confirmation text (e.g., stock level or product name)
    to prevent accidental deletions. Used for critical operations like
    deleting stock batches, products, etc.
    """
    
    def __init__(self, confirmation_text: str, item_type: str = "item", parent=None):
        """
        Initialize the confirmation dialog.
        
        Args:
            confirmation_text: Text the user must type to confirm (e.g., stock level)
            item_type: Type of item being deleted (e.g., "batch", "product")
            parent: Parent widget
        """
        super().__init__(parent)
        self.confirmation_text = str(confirmation_text)
        self.item_type = item_type
        self.setWindowTitle(f"Confirm Delete {item_type.title()}")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self.confirmed = False
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        self.setStyleSheet(get_dialog_style())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Warning message
        warning_label = QLabel(f"⚠️ Are you sure you want to delete this {self.item_type}?")
        warning_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.ACCENT_COLOR};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
                padding: 10px;
            }}
        """)
        layout.addWidget(warning_label)
        
        # Instruction
        instruction = QLabel(f"Type '{self.confirmation_text}' to confirm:")
        instruction.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                padding: 5px;
            }}
        """)
        layout.addWidget(instruction)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter confirmation text...")
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 2px solid {AppConfig.BORDER_COLOR};
                border-radius: {AppConfig.INPUT_RADIUS}px;
                padding: 10px;
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {AppConfig.ACCENT_COLOR};
            }}
        """)
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setProperty("class", "danger")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(self.on_confirm)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
    
    def on_confirm(self):
        """Handle confirm button click."""
        entered_text = self.input_field.text().strip()
        
        if entered_text == self.confirmation_text:
            self.confirmed = True
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Confirmation Failed",
                f"Please type '{self.confirmation_text}' exactly to confirm deletion.",
                QMessageBox.StandardButton.Ok
            )
            self.input_field.clear()
            self.input_field.setFocus()
    
    def is_confirmed(self) -> bool:
        """Check if deletion was confirmed."""
        return self.confirmed

