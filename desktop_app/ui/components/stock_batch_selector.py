# stock_batch_selector.py
#
# This module provides a stock batch selector component.
# Used for managing stock batches: viewing, adding, editing, disposing, and deleting.
#
# Usage: Used in product detail pages for batch management.

from typing import Optional, List, Dict
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import success, error, warning
from utils.helpers import format_date
from ui.components.confirm_delete_dialog import ConfirmDeleteDialog


class StockBatchSelector(QWidget):
    """
    Stock batch selector component for product batch management.
    
    Features:
    - Dropdown to select batches
    - Add batch button
    - Edit batch button
    - Dispose batch button
    - Delete batch button (with secure confirmation)
    """
    
    batch_changed = pyqtSignal(int)  # Emitted when selected batch changes
    
    def __init__(self, product_id: int, parent=None):
        """
        Initialize the stock batch selector.
        
        Args:
            product_id: ID of the product to manage batches for
            parent: Parent widget
        """
        super().__init__(parent)
        self.product_id = product_id
        self.api = get_api()
        self.batches: List[Dict] = []
        self.current_batch_id: Optional[int] = None
        
        self.init_ui()
        self.load_batches()
    
    def init_ui(self):
        """Initialize the batch selector UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label = QLabel("Stock Batches:")
        label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                font-weight: bold;
            }}
        """)
        layout.addWidget(label)
        
        # Batch dropdown
        self.batch_combo = QComboBox()
        self.batch_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 1px solid {AppConfig.BORDER_COLOR};
                border-radius: {AppConfig.INPUT_RADIUS}px;
                padding: 8px 12px;
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
            QComboBox:focus {{
                border: 2px solid {AppConfig.PRIMARY_COLOR};
            }}
        """)
        self.batch_combo.currentIndexChanged.connect(self.on_batch_selected)
        layout.addWidget(self.batch_combo)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_btn = QPushButton("Add Batch")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_batch)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Edit Batch")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.clicked.connect(self.edit_batch)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        self.dispose_btn = QPushButton("Dispose")
        self.dispose_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dispose_btn.clicked.connect(self.dispose_batch)
        self.dispose_btn.setEnabled(False)
        self.dispose_btn.setProperty("class", "warning")
        button_layout.addWidget(self.dispose_btn)
        
        self.delete_btn = QPushButton("Delete Batch")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.delete_batch)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setProperty("class", "danger")
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
    
    def load_batches(self):
        """Load stock batches for the product from API."""
        try:
            response = self.api.get_stock_batches(self.product_id)
            
            # Handle different response formats
            if isinstance(response, dict):
                batches = response.get('batches', response.get('stock_batches', []))
            elif isinstance(response, list):
                batches = response
            else:
                batches = []
            
            self.batches = batches
            self.batch_combo.clear()
            
            if batches:
                for batch in batches:
                    batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
                    quantity = batch.get('quantity', 0)
                    expiration = batch.get('expiration_date', 'N/A')
                    
                    # Format expiration date
                    try:
                        if expiration and expiration != 'N/A':
                            expiration = format_date(expiration)
                    except:
                        pass
                    
                    display_text = f"Batch {batch_id} - {quantity} units (Exp: {expiration})"
                    self.batch_combo.addItem(display_text, batch_id)
                
                # Enable buttons
                self.edit_btn.setEnabled(True)
                self.dispose_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            else:
                self.batch_combo.addItem("No batches available")
                self.edit_btn.setEnabled(False)
                self.dispose_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
            
        except Exception as e:
            error(f"Failed to load batches: {str(e)}")
            self.batch_combo.clear()
            self.batch_combo.addItem("Error loading batches")
    
    def on_batch_selected(self, index: int):
        """Handle batch selection change."""
        if index >= 0 and self.batches:
            batch_data = self.batch_combo.itemData(index)
            if batch_data:
                self.current_batch_id = batch_data
                self.batch_changed.emit(self.current_batch_id)
    
    def get_selected_batch(self) -> Optional[Dict]:
        """Get the currently selected batch data."""
        index = self.batch_combo.currentIndex()
        if index >= 0 and index < len(self.batches):
            return self.batches[index]
        return None
    
    def add_batch(self):
        """Open dialog to add a new batch."""
        # This would open a dialog - for now, emit signal for parent to handle
        from PyQt6.QtCore import QObject
        if hasattr(self.parent(), 'add_batch_dialog'):
            self.parent().add_batch_dialog()
        else:
            warning("Add batch dialog not implemented. Please implement in parent component.")
    
    def edit_batch(self):
        """Open dialog to edit selected batch."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to edit.")
            return
        
        # This would open a dialog - for now, emit signal for parent to handle
        if hasattr(self.parent(), 'edit_batch_dialog'):
            self.parent().edit_batch_dialog(batch)
        else:
            warning("Edit batch dialog not implemented. Please implement in parent component.")
    
    def dispose_batch(self):
        """Dispose of selected batch using FEFO."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to dispose.")
            return
        
        # This would open a disposal dialog - for now, emit signal for parent to handle
        if hasattr(self.parent(), 'dispose_batch_dialog'):
            self.parent().dispose_batch_dialog(batch)
        else:
            warning("Dispose batch dialog not implemented. Please implement in parent component.")
    
    def delete_batch(self):
        """Delete selected batch with secure confirmation."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to delete.")
            return
        
        batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
        quantity = batch.get('quantity', 0)
        
        # Secure delete confirmation - user must type quantity
        dialog = ConfirmDeleteDialog(
            confirmation_text=str(quantity),
            item_type="batch",
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.is_confirmed():
            try:
                self.api.delete_stock_batch(self.product_id, batch_id)
                success("Batch deleted successfully.")
                self.load_batches()  # Reload batches
            except Exception as e:
                error(f"Failed to delete batch: {str(e)}")

