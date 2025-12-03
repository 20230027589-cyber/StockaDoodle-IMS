# categories.py
#
# This module provides the categories management page for managers.
# Displays categories list with add/edit/delete functionality using card layout.
#
# Usage: Categories management page in manager dashboard.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QScrollArea, QGridLayout, QDialog)
from PyQt6.QtCore import Qt
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success
from utils.styles import get_page_title_style, get_primary_button_style
from ui.components.category_card import CategoryCard
from ui.dialogs.category_form_dialog import CategoryFormDialog
from ui.components.confirm_delete_dialog import ConfirmDeleteDialog


class CategoriesPage(QWidget):
    """
    Categories management page with modern card layout.
    
    Features:
    - Category cards in grid layout (4 cards per row)
    - Search functionality
    - Add/Edit/Delete category functionality
    - Category images displayed
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        self.all_categories = []
        self.cards_per_row = 4
        
        self.init_ui()
        self.load_categories()
    
    def init_ui(self):
        """Initialize the categories page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header section
        header_layout = QHBoxLayout()
        
        title = QLabel("Categories")
        title.setStyleSheet(get_page_title_style())
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Search bar
        search_label = QLabel("Search:")
        header_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search categories...")
        self.search_input.setMaximumWidth(300)
        self.search_input.textChanged.connect(self.filter_categories)
        header_layout.addWidget(self.search_input)
        
        # Add category button
        self.add_btn = QPushButton("Add Category")
        self.add_btn.setStyleSheet(get_primary_button_style())
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_category)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Container widget for grid
        self.cards_container = QWidget()
        self.grid_layout = QGridLayout(self.cards_container)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
    
    def load_categories(self):
        """Load categories from API."""
        try:
            result = self.api.get_categories(include_image=True)
            
            # Handle different response formats
            if isinstance(result, dict):
                self.all_categories = result.get('categories', [])
            elif isinstance(result, list):
                self.all_categories = result
            else:
                self.all_categories = []
            
            self.filter_categories()
            
        except Exception as e:
            error(f"Failed to load categories: {str(e)}")
    
    def filter_categories(self):
        """Filter categories and display in grid."""
        search_text = self.search_input.text().lower().strip()
        
        # Clear existing cards
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Filter categories
        filtered = []
        for category in self.all_categories:
            name = category.get('name', '').lower()
            description = category.get('description', '').lower()
            
            if not search_text or search_text in name or search_text in description:
                filtered.append(category)
        
        # Display categories in grid
        row = 0
        col = 0
        
        for category in filtered:
            card = CategoryCard(
                category,
                on_view_details_callback=self.view_category_details,
                on_edit_callback=self.edit_category,
                on_delete_callback=self.delete_category
            )
            
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= self.cards_per_row:
                col = 0
                row += 1
        
        # Add empty message if no categories
        if not filtered:
            no_categories_label = QLabel("No categories found. Click 'Add Category' to create one.")
            no_categories_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_categories_label.setStyleSheet(f"""
                QLabel {{
                    color: {AppConfig.TEXT_COLOR_ALT};
                    font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                    padding: 40px;
                }}
            """)
            self.grid_layout.addWidget(no_categories_label, 0, 0, 1, self.cards_per_row)
    
    def add_category(self):
        """Open dialog to add new category."""
        dialog = CategoryFormDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()
    
    def edit_category(self, category_data: dict):
        """Open dialog to edit category."""
        dialog = CategoryFormDialog(category_data=category_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()
    
    def view_category_details(self, category_data: dict):
        """View category details (opens edit dialog)."""
        self.edit_category(category_data)
    
    def delete_category(self, category_id: int, category_name: str):
        """Delete category with confirmation."""
        # Confirm deletion
        confirm_dialog = ConfirmDeleteDialog(
            confirmation_text=category_name,
            item_type="category",
            parent=self
        )
        
        if confirm_dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.api.delete_category(category_id)
                success(f"Category '{category_name}' deleted successfully!")
                self.load_categories()
            except Exception as e:
                error(f"Failed to delete category: {str(e)}")
    
    def refresh_data(self):
        """Refresh categories list (called when tab is switched to)."""
        self.load_categories()

