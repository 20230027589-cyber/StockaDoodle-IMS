# product_detail.py
#
# This module provides a comprehensive product detail page.
# Shows product information, stock batches, and batch management actions.
#
# Usage: Displayed when user clicks "View Details" on a product card.

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QDialog, QFormLayout,
                             QSpinBox, QDateEdit, QTextEdit, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success, warning
from utils.helpers import load_product_image, format_currency
from ui.components.confirm_delete_dialog import ConfirmDeleteDialog
from ui.pages.products.product_form import ProductFormDialog


class DisposeBatchDialog(QDialog):
    """Dialog for disposing stock from a batch."""
    
    def __init__(self, batch: dict, parent=None):
        super().__init__(parent)
        self.batch = batch
        self.batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
        self.available_quantity = batch.get('quantity', 0)
        
        self.setWindowTitle("Dispose from Batch")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(f"Dispose from Batch #{self.batch_id}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title)
        
        # Available quantity
        available_label = QLabel(f"Available: {self.available_quantity} units")
        available_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
        """)
        layout.addWidget(available_label)
        
        # Quantity input
        form_layout = QFormLayout()
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(self.available_quantity)
        self.quantity_input.setValue(1)
        form_layout.addRow("Quantity to dispose:", self.quantity_input)
        
        # Reason textarea
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Enter reason for disposal (e.g., Damaged during handling)")
        self.reason_input.setMaximumHeight(100)
        form_layout.addRow("Reason:", self.reason_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        dispose_btn = QPushButton("Dispose")
        dispose_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.WARNING_COLOR};
                color: white;
                padding: 8px 20px;
            }}
        """)
        dispose_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(dispose_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_data(self) -> dict:
        """Get disposal data."""
        return {
            'quantity': self.quantity_input.value(),
            'reason': self.reason_input.toPlainText().strip() or "Disposed"
        }


class AddBatchDialog(QDialog):
    """Dialog for adding a new stock batch."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Batch")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        
        # Quantity
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setValue(1)
        form_layout.addRow("Quantity *:", self.quantity_input)
        
        # Expiration Date
        self.expiration_date = QDateEdit()
        self.expiration_date.setCalendarPopup(True)
        self.expiration_date.setDate(QDate.currentDate().addYears(1))
        self.expiration_date.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Expiration Date *:", self.expiration_date)
        
        # Reason
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Enter reason (e.g., Stock added, Restock)")
        self.reason_input.setMaximumHeight(80)
        form_layout.addRow("Reason:", self.reason_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("Add Batch")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 8px 20px;
            }}
        """)
        add_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(add_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_data(self) -> dict:
        """Get batch data."""
        return {
            'quantity': self.quantity_input.value(),
            'expiration_date': self.expiration_date.date().toString("yyyy-MM-dd"),
            'reason': self.reason_input.toPlainText().strip() or "Stock added"
        }


class EditBatchDialog(QDialog):
    """Dialog for editing batch expiration date and reason."""
    
    def __init__(self, batch: dict, parent=None):
        super().__init__(parent)
        self.batch = batch
        
        self.setWindowTitle("Edit Batch")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.init_ui()
        self.load_batch_data()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        
        # Expiration Date
        self.expiration_date = QDateEdit()
        self.expiration_date.setCalendarPopup(True)
        self.expiration_date.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Expiration Date *:", self.expiration_date)
        
        # Reason
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Enter reason")
        self.reason_input.setMaximumHeight(80)
        form_layout.addRow("Reason:", self.reason_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 8px 20px;
            }}
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_batch_data(self):
        """Load batch data into form."""
        exp_date = self.batch.get('expiration_date')
        if exp_date:
            try:
                if isinstance(exp_date, str):
                    qdate = QDate.fromString(exp_date, "yyyy-MM-dd")
                    if qdate.isValid():
                        self.expiration_date.setDate(qdate)
            except:
                pass
        
        reason = self.batch.get('reason', '')
        self.reason_input.setPlainText(reason)
    
    def get_data(self) -> dict:
        """Get updated batch data."""
        return {
            'expiration_date': self.expiration_date.date().toString("yyyy-MM-dd"),
            'reason': self.reason_input.toPlainText().strip() or "Updated"
        }


class ProductDetailPage(QWidget):
    """
    Comprehensive product detail page.
    
    Features:
    - Product information display
    - Stock batch selector and management
    - Add/Edit/Dispose/Delete batch actions
    - Delete product with GitHub-style confirmation
    - Back to list and Edit Product Info buttons
    """
    
    back_requested = pyqtSignal()  # Signal to go back to product list
    
    def __init__(self, product_data: dict, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.product_id = product_data.get('id')
        self.api = get_api()
        self.batches = []  # Store loaded batches
        
        # Get current user for role-based actions
        from utils.app_state import get_current_user
        self.current_user = get_current_user()
        
        self.init_ui()
        self.load_product_details()
    
    def init_ui(self):
        """Initialize the product detail page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header with Back and Edit buttons
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back to List")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        
        edit_product_btn = QPushButton("Edit Product Info")
        edit_product_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_product_btn.clicked.connect(self.edit_product_info)
        edit_product_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 8px 16px;
            }}
        """)
        header_layout.addWidget(edit_product_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Product Information Section
        product_info_layout = QHBoxLayout()
        product_info_layout.setSpacing(20)
        
        # Product Image
        image_container = QWidget()
        image_container.setFixedSize(300, 300)
        image_container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border-radius: 12px;
                border: 1px solid {AppConfig.BORDER_COLOR};
            }}
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(10, 10, 10, 10)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        image_layout.addWidget(self.image_label)
        
        product_info_layout.addWidget(image_container)
        
        # Product Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)
        
        name_label = QLabel(self.product_data.get('name', 'N/A'))
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: 28pt;
                font-weight: bold;
            }}
        """)
        details_layout.addWidget(name_label)
        
        brand_label = QLabel(f"Brand: {self.product_data.get('brand', 'N/A')}")
        brand_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
            }}
        """)
        details_layout.addWidget(brand_label)
        
        price = float(self.product_data.get('price', 0))
        price_label = QLabel(format_currency(price))
        price_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.SECONDARY_COLOR};
                font-size: 24pt;
                font-weight: bold;
            }}
        """)
        details_layout.addWidget(price_label)
        
        stock = self.product_data.get('stock_level', 0) or self.product_data.get('stock', 0)
        stock_label = QLabel(f"Stock: {stock} units")
        stock_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
            }}
        """)
        details_layout.addWidget(stock_label)
        
        category_label = QLabel(f"Category: {self.product_data.get('category_name', 'N/A')}")
        category_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
            }}
        """)
        details_layout.addWidget(category_label)
        
        details_layout.addStretch()
        product_info_layout.addLayout(details_layout)
        
        content_layout.addLayout(product_info_layout)
        
        # Stock Batch Management Section
        batch_section_label = QLabel("Stock Batch Management")
        batch_section_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
            }}
        """)
        content_layout.addWidget(batch_section_label)
        
        # Stock Batch Selector - we'll create a custom one without built-in buttons
        batch_selector_layout = QVBoxLayout()
        batch_selector_layout.setSpacing(10)
        
        batch_label = QLabel("Stock Batches:")
        batch_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                font-weight: bold;
            }}
        """)
        batch_selector_layout.addWidget(batch_label)
        
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
        """)
        self.batch_combo.currentIndexChanged.connect(self.on_batch_selected)
        batch_selector_layout.addWidget(self.batch_combo)
        
        self.load_batches()
        content_layout.addLayout(batch_selector_layout)
        
        # Batch Action Buttons
        batch_buttons_layout = QHBoxLayout()
        batch_buttons_layout.setSpacing(10)
        
        self.add_batch_btn = QPushButton("Add New Batch")
        self.add_batch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_batch_btn.clicked.connect(self.add_batch)
        batch_buttons_layout.addWidget(self.add_batch_btn)
        
        self.edit_batch_btn = QPushButton("Edit Batch")
        self.edit_batch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_batch_btn.clicked.connect(self.edit_batch)
        self.edit_batch_btn.setEnabled(False)
        batch_buttons_layout.addWidget(self.edit_batch_btn)
        
        self.dispose_batch_btn = QPushButton("Dispose")
        self.dispose_batch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dispose_batch_btn.clicked.connect(self.dispose_batch)
        self.dispose_batch_btn.setEnabled(False)
        self.dispose_batch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.WARNING_COLOR};
                color: white;
            }}
        """)
        batch_buttons_layout.addWidget(self.dispose_batch_btn)
        
        self.delete_batch_btn = QPushButton("Delete Batch")
        self.delete_batch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_batch_btn.clicked.connect(self.delete_batch)
        self.delete_batch_btn.setEnabled(False)
        self.delete_batch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.ACCENT_COLOR};
                color: white;
            }}
        """)
        batch_buttons_layout.addWidget(self.delete_batch_btn)
        
        batch_buttons_layout.addStretch()
        content_layout.addLayout(batch_buttons_layout)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Delete Product Button (Admin/Manager only)
        is_admin_or_manager = False
        if self.current_user:
            role = self.current_user.get('role', '').lower()
            is_admin_or_manager = role in ['admin', 'manager']
        
        if is_admin_or_manager:
            footer_layout = QHBoxLayout()
            footer_layout.addStretch()
            
            delete_product_btn = QPushButton("Delete Product")
            delete_product_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_product_btn.clicked.connect(self.delete_product)
            delete_product_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {AppConfig.ACCENT_COLOR};
                    color: white;
                    padding: 10px 20px;
                    font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                }}
                QPushButton:hover {{
                    background-color: #c0392b;
                }}
            """)
            footer_layout.addWidget(delete_product_btn)
            
            main_layout.addLayout(footer_layout)
    
    def load_product_details(self):
        """Load and display product details."""
        try:
            # Load product image
            image_path = self.product_data.get('image_path') or self.product_data.get('image')
            if image_path:
                pixmap = load_product_image(image_path, target_size=(300, 300))
                self.image_label.setPixmap(pixmap)
            else:
                # Placeholder
                placeholder = QPixmap(300, 300)
                placeholder.fill(AppConfig.INPUT_BACKGROUND)
                self.image_label.setPixmap(placeholder)
        except Exception as e:
            error(f"Failed to load product image: {str(e)}")
    
    def load_batches(self):
        """Load stock batches for the product."""
        try:
            response = self.api.get_stock_batches(self.product_id)
            
            # Handle different response formats
            if isinstance(response, dict):
                self.batches = response.get('batches', response.get('stock_batches', []))
            elif isinstance(response, list):
                self.batches = response
            else:
                self.batches = []
            
            self.batch_combo.clear()
            
            if self.batches:
                for batch in self.batches:
                    batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
                    quantity = batch.get('quantity', 0)
                    expiration = batch.get('expiration_date', 'N/A')
                    
                    # Format expiration date
                    try:
                        if expiration and expiration != 'N/A':
                            from utils.helpers import format_date
                            expiration = format_date(expiration)
                    except:
                        pass
                    
                    display_text = f"Batch {batch_id} - {quantity} units (Exp: {expiration})"
                    self.batch_combo.addItem(display_text, batch_id)
            else:
                self.batch_combo.addItem("No batches available")
                
        except Exception as e:
            error(f"Failed to load batches: {str(e)}")
            self.batch_combo.clear()
            self.batch_combo.addItem("Error loading batches")
            self.batches = []
    
    def get_selected_batch(self):
        """Get the currently selected batch."""
        index = self.batch_combo.currentIndex()
        if index >= 0 and index < len(self.batches):
            return self.batches[index]
        return None
    
    def on_batch_selected(self, index: int):
        """Handle batch selection change."""
        batch = self.get_selected_batch()
        if batch:
            quantity = batch.get('quantity', 0)
            self.edit_batch_btn.setEnabled(True)
            self.dispose_batch_btn.setEnabled(quantity > 0)
            self.delete_batch_btn.setEnabled(quantity == 0)
        else:
            self.edit_batch_btn.setEnabled(False)
            self.dispose_batch_btn.setEnabled(False)
            self.delete_batch_btn.setEnabled(False)
    
    def add_batch(self):
        """Open dialog to add a new batch."""
        dialog = AddBatchDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                self.api.add_stock_batch(
                    self.product_id,
                    quantity=data['quantity'],
                    expiration_date=data['expiration_date'],
                    reason=data['reason']
                )
                success("Batch added successfully!")
                self.load_batches()
                # Refresh product data to update stock
                self.refresh_product_data()
            except Exception as e:
                error(f"Failed to add batch: {str(e)}")
    
    def edit_batch(self):
        """Open dialog to edit selected batch."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to edit.")
            return
        
        dialog = EditBatchDialog(batch, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
                
                # Update batch metadata via API
                self.api.update_stock_batch(
                    self.product_id, 
                    batch_id,
                    expiration_date=data.get('expiration_date'),
                    reason=data.get('reason')
                )
                
                success("Batch updated successfully!")
                self.load_batches()
            except Exception as e:
                error(f"Failed to update batch: {str(e)}")
    
    def dispose_batch(self):
        """Open dialog to dispose stock from selected batch."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to dispose.")
            return
        
        dialog = DisposeBatchDialog(batch, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
                
                # Dispose via API - use batch-specific dispose method
                self.api.dispose_stock_batch(
                    batch_id,
                    quantity=data['quantity'],
                    reason=data['reason'],
                    product_id=self.product_id
                )
                
                success("Stock disposed successfully!")
                self.load_batches()
                self.refresh_product_data()
            except Exception as e:
                error(f"Failed to dispose stock: {str(e)}")
    
    def delete_batch(self):
        """Delete selected batch with confirmation."""
        batch = self.get_selected_batch()
        if not batch:
            warning("Please select a batch to delete.")
            return
        
        batch_id = batch.get('id') or batch.get('_id') or batch.get('batch_id')
        quantity = batch.get('quantity', 0)
        
        if quantity > 0:
            error("Cannot delete batch with remaining stock. Please dispose of all stock first.")
            return
        
        # Secure delete confirmation
        dialog = ConfirmDeleteDialog(
            confirmation_text=str(quantity),
            item_type="batch",
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.is_confirmed():
            try:
                self.api.delete_stock_batch(self.product_id, batch_id)
                success("Batch deleted successfully!")
                self.load_batches()
                self.refresh_product_data()
            except Exception as e:
                error(f"Failed to delete batch: {str(e)}")
    
    def delete_product(self):
        """Delete product with GitHub-style confirmation."""
        product_name = self.product_data.get('name', 'Product')
        current_stock = str(self.product_data.get('stock_level', 0) or self.product_data.get('stock', 0))
        
        # Use GitHub-style confirmation dialog
        from ui.components.confirm_product_delete_dialog import ConfirmProductDeleteDialog
        dialog = ConfirmProductDeleteDialog(product_name, self.product_id, current_stock, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.api.delete_product(self.product_id)
                success(f"Product '{product_name}' deleted successfully.")
                self.go_back()  # Return to product list
            except Exception as e:
                error(f"Failed to delete product: {str(e)}")
    
    def edit_product_info(self):
        """Open dialog to edit product information."""
        dialog = ProductFormDialog(product_data=self.product_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_product_data()
            success("Product updated successfully!")
    
    def refresh_product_data(self):
        """Refresh product data from API."""
        try:
            updated_product = self.api.get_product(self.product_id, include_image=True)
            self.product_data.update(updated_product)
            self.load_product_details()
        except Exception as e:
            error(f"Failed to refresh product data: {str(e)}")
    
    def go_back(self):
        """Emit signal to go back to product list."""
        self.back_requested.emit()

