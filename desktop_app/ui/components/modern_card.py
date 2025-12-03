# modern_card.py
#
# This module provides a modern card widget component.
# Used for displaying content in a styled card container with rounded corners and shadows.
#
# Usage: Imported by UI modules to create card-based layouts (e.g., dashboard cards, product cards).

from PyQt6.QtWidgets import QFrame, QVBoxLayout
from utils.config import AppConfig
from utils.styles import get_modern_card_style


class ModernCard(QFrame):
    """
    Modern card widget with rounded corners, shadows, and hover effects.
    
    Design: Dark theme card with subtle borders, smooth transitions,
    and hover effects for better interactivity.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        self.setProperty("class", "modern-card")
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the card UI and styling."""
        # Modern card with light background, soft shadow
        self.setStyleSheet(f"""
            QFrame#modernCard {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }}
        """)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
    
    def addWidget(self, widget):
        """Add a widget to the card's layout."""
        self.layout.addWidget(widget)
    
    def addLayout(self, layout):
        """Add a layout to the card's layout."""
        self.layout.addLayout(layout)

