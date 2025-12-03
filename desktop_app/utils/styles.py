# styles.py
#
# This module provides centralized stylesheet functions for the entire application.
# All QSS (Qt Style Sheets) are defined here for consistency and maintainability.
#
# Usage: Imported by UI modules to apply consistent styling across the application.

import os
from utils.config import AppConfig
from PyQt6.QtWidgets import QTableWidget, QHeaderView
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

# Pre-compute icon paths for QSS
_ICONS_DIR = os.path.abspath(AppConfig.ICONS_DIR).replace('\\', '/')
_CHEVRON_DOWN_ICON = f"{_ICONS_DIR}/chevron-down.svg"
_CALENDAR_ICON = f"{_ICONS_DIR}/calendar.svg"


def get_global_stylesheet():
    """
    Returns the global stylesheet for the entire application.
    This includes base styling for all common widgets.
    """
    return f"""
    /* Main Window */
    QMainWindow {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
        font-family: {AppConfig.FONT_FAMILY};
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    
    /* Sidebar Styling */
    #sidebar {{
        background-color: {AppConfig.DARK_BACKGROUND}; 
        border-right: 2px solid rgba(255,255,255,0.1);
    }}
    
    #sidebar QPushButton {{
        background-color: transparent;
        color: {AppConfig.TEXT_COLOR_ALT};
        border: none;
        padding: 15px 20px;
        text-align: left;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        margin: 2px 5px;
    }}
    
    #sidebar QPushButton:hover {{
        background-color: rgba(108, 92, 231, 0.15);
        color: {AppConfig.LIGHT_TEXT};
    }}
    
    #sidebar QPushButton:checked {{
        background-color: rgba(108, 92, 231, 0.25);
        border-left: 4px solid {AppConfig.PRIMARY_COLOR};
        font-weight: bold;
        color: {AppConfig.LIGHT_TEXT};
    }}
    
    /* Content Area */
    #contentArea {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        padding: 20px;
    }}
    
    /* User Name Label */
    QLabel#userNameLabel {{
        color: {AppConfig.LIGHT_TEXT};
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        padding: 10px;
    }}
    
    /* General Table Styling */
    QTableWidget {{
        background-color: {AppConfig.CARD_BACKGROUND};
        color: {AppConfig.TEXT_COLOR};
        border: 1px solid {AppConfig.BORDER_COLOR};
        gridline-color: rgba(255,255,255,0.1);
        selection-background-color: {AppConfig.PRIMARY_COLOR};
        selection-color: white;
        border-radius: {AppConfig.CARD_RADIUS}px;
        alternate-background-color: rgba(255,255,255,0.02);
    }}
    
    QTableWidget::item {{
        padding: 10px 8px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }}
    
    QTableWidget::item:selected {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: white;
    }}
    
    QTableWidget QHeaderView::section {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        padding: 10px;
        border: none;
        border-right: 1px solid rgba(255,255,255,0.1);
        border-bottom: 2px solid rgba(255,255,255,0.1);
        font-weight: bold;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    
    QTableWidget QHeaderView::section:last-child {{
        border-right: none;
    }}
    
    /* General Button Styles */
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        padding: 10px 20px;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: 500;
    }}
    
    QPushButton:hover {{
        background-color: {AppConfig.PRIMARY_HOVER};
    }}
    
    QPushButton:pressed {{
        background-color: {AppConfig.PRIMARY_COLOR};
        border: 1px solid {AppConfig.LIGHT_TEXT};
    }}
    
    QPushButton:disabled {{
        background-color: #475569;
        color: {AppConfig.TEXT_COLOR_MUTED};
    }}
    
    /* Button Variants */
    QPushButton[class="danger"] {{
        background-color: {AppConfig.ACCENT_COLOR};
    }}
    
    QPushButton[class="danger"]:hover {{
        background-color: #B91C1C;
    }}
    
    QPushButton[class="success"] {{
        background-color: {AppConfig.SECONDARY_COLOR};
    }}
    
    QPushButton[class="success"]:hover {{
        background-color: #00A085;
    }}
    
    QPushButton[class="warning"] {{
        background-color: {AppConfig.WARNING_COLOR};
        color: {AppConfig.DARK_BACKGROUND};
    }}
    
    QPushButton[class="warning"]:hover {{
        background-color: #FDC14A;
    }}
    
    /* General Input Styles */
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit, QTextEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.INPUT_RADIUS}px;
        padding: 8px 12px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, 
    QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {{
        border: 2px solid {AppConfig.PRIMARY_COLOR};
        background-color: {AppConfig.CARD_BACKGROUND};
    }}
    
    QComboBox::drop-down {{
        border: 0px;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: url({_CHEVRON_DOWN_ICON});
        width: 16px;
        height: 16px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        selection-background-color: {AppConfig.PRIMARY_COLOR};
        selection-color: white;
        padding: 5px;
    }}
    
    QDateEdit::drop-down {{
        border: 0px;
        width: 30px;
    }}
    
    QDateEdit::down-arrow {{
        image: url({_CALENDAR_ICON});
        width: 16px;
        height: 16px;
    }}
    
    /* ScrollArea Styling */
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    
    QScrollBar:vertical {{
        border: none;
        background: rgba(255, 255, 255, 0.05);
        width: 12px;
        margin: 0px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background: rgba(255, 255, 255, 0.2);
        min-height: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: rgba(255, 255, 255, 0.05);
        height: 12px;
        margin: 0px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: rgba(255, 255, 255, 0.2);
        min-width: 30px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* Checkbox and Radio Button */
    QCheckBox, QRadioButton {{
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        spacing: 8px;
    }}
    
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {AppConfig.BORDER_COLOR};
        border-radius: 3px;
        background-color: {AppConfig.INPUT_BACKGROUND};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {AppConfig.PRIMARY_COLOR};
        border-color: {AppConfig.PRIMARY_COLOR};
    }}
    
    QRadioButton::indicator {{
        border-radius: 9px;
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {AppConfig.PRIMARY_COLOR};
        border-color: {AppConfig.PRIMARY_COLOR};
    }}
    
    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.INPUT_RADIUS}px;
        background-color: {AppConfig.INPUT_BACKGROUND};
        text-align: center;
        color: {AppConfig.TEXT_COLOR};
        height: 20px;
    }}
    
    QProgressBar::chunk {{
        background-color: {AppConfig.PRIMARY_COLOR};
        border-radius: {AppConfig.INPUT_RADIUS - 1}px;
    }}
    """


def get_dashboard_card_style(color):
    """
    Returns stylesheet for a general dashboard summary card.
    
    Args:
        color: Hex color code for the card accent
    """
    lighter_color = QColor(color).lighter(110).name()
    return f"""
    QFrame.dashboard-card {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                    stop:0 {color}, 
                                    stop:1 {lighter_color});
        border-radius: {AppConfig.CARD_RADIUS}px;
        padding: 20px;
        margin: 10px;
        min-width: 200px;
        min-height: 140px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    QLabel {{
        color: {AppConfig.LIGHT_TEXT};
    }}
    
    QLabel.card-title {{
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: bold;
        margin-bottom: 8px;
    }}
    
    QLabel.card-value {{
        font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
        font-weight: bold;
    }}
    
    QLabel.card-subtitle {{
        font-size: {AppConfig.FONT_SIZE_SMALL}pt;
        color: rgba(255,255,255,0.8);
    }}
    """


def get_product_card_style():
    """Returns stylesheet for product cards in ProductListWidget."""
    return f"""
    QFrame.product-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.CARD_RADIUS}px;
        padding: 15px;
    }}
    
    QFrame.product-card:hover {{
        border: 2px solid {AppConfig.PRIMARY_COLOR};
        background-color: rgba(108, 92, 231, 0.1);
    }}
    
    QLabel.product-image {{
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: {AppConfig.INPUT_RADIUS}px;
        background-color: rgba(0,0,0,0.1);
    }}
    
    QLabel.product-title {{
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        color: {AppConfig.LIGHT_TEXT};
    }}
    
    QLabel.product-detail {{
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        color: {AppConfig.TEXT_COLOR_ALT};
    }}
    
    QLabel.product-price {{
        font-size: {AppConfig.FONT_SIZE_XLARGE}pt;
        font-weight: bold;
        color: {AppConfig.SECONDARY_COLOR};
    }}
    
    QLabel.status-in-stock {{
        color: {AppConfig.SECONDARY_COLOR};
        font-weight: bold;
        background-color: rgba(46, 213, 115, 0.15);
        padding: 4px 8px;
        border-radius: 4px;
    }}
    
    QLabel.status-low-stock {{
        color: {AppConfig.WARNING_COLOR};
        font-weight: bold;
        background-color: rgba(253, 203, 110, 0.15);
        padding: 4px 8px;
        border-radius: 4px;
    }}
    
    QLabel.status-no-stock {{
        color: {AppConfig.ACCENT_COLOR};
        font-weight: bold;
        background-color: rgba(214, 48, 49, 0.15);
        padding: 4px 8px;
        border-radius: 4px;
    }}
    """


def get_category_card_style():
    """Returns stylesheet for category cards (matches product card style)."""
    return f"""
    QFrame.category-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.CARD_RADIUS}px;
        padding: 15px;
    }}
    
    QFrame.category-card:hover {{
        border: 2px solid {AppConfig.PRIMARY_COLOR};
        background-color: rgba(108, 92, 231, 0.1);
    }}
    
    QLabel.category-image {{
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: {AppConfig.INPUT_RADIUS}px;
        background-color: rgba(0,0,0,0.1);
    }}
    
    QLabel.category-title {{
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        color: {AppConfig.LIGHT_TEXT};
    }}
    
    QLabel.category-detail {{
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        color: {AppConfig.TEXT_COLOR_ALT};
    }}
    
    QPushButton.category-action-btn {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        font-weight: 500;
        width: 100%;
    }}
    
    QPushButton.category-action-btn:hover {{
        background-color: {AppConfig.PRIMARY_HOVER};
    }}
    """


def get_dialog_style():
    """Returns stylesheet for general dialog windows."""
    return f"""
    QDialog {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        border-radius: {AppConfig.CARD_RADIUS}px;
        color: {AppConfig.TEXT_COLOR};
        font-family: {AppConfig.FONT_FAMILY};
        border: 1px solid {AppConfig.BORDER_COLOR};
    }}
    
    QLabel {{
        color: {AppConfig.TEXT_COLOR};
    }}
    
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit, QTextEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.INPUT_RADIUS}px;
        padding: 8px 12px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, 
    QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {{
        border: 2px solid {AppConfig.PRIMARY_COLOR};
    }}
    
    QComboBox::drop-down {{
        border: 0px;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: url({_CHEVRON_DOWN_ICON});
        width: 16px;
        height: 16px;
    }}
    
    QDateEdit::drop-down {{
        border: 0px;
        width: 30px;
    }}
    
    QDateEdit::down-arrow {{
        image: url({_CALENDAR_ICON});
        width: 16px;
        height: 16px;
    }}
    
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        padding: 10px 20px;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    
    QPushButton:hover {{
        background-color: {AppConfig.PRIMARY_HOVER};
    }}
    
    #imagePreviewLabel {{
        border: 2px dashed {AppConfig.PRIMARY_COLOR};
        background-color: {AppConfig.INPUT_BACKGROUND};
        border-radius: {AppConfig.INPUT_RADIUS}px;
        padding: 10px;
    }}
    """


def get_header_bar_style():
    """Returns stylesheet for the header bar."""
    return f"""
    QWidget#headerBar {{
        background-color: {AppConfig.DARK_BACKGROUND};
        border-bottom: 1px solid {AppConfig.BORDER_COLOR};
        padding: 10px 20px;
        min-height: {AppConfig.HEADER_HEIGHT}px;
    }}
    
    QPushButton#notificationButton {{
        background-color: transparent;
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        padding: 8px;
    }}
    
    QPushButton#notificationButton:hover {{
        background-color: rgba(255,255,255,0.1);
    }}
    
    QPushButton#profileButton {{
        background-color: transparent;
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        padding: 5px;
    }}
    
    QPushButton#profileButton:hover {{
        background-color: rgba(255,255,255,0.1);
    }}
    
    QLineEdit#globalSearch {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 20px;
        padding: 8px 15px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    
    QLineEdit#globalSearch:focus {{
        border: 2px solid {AppConfig.PRIMARY_COLOR};
    }}
    """


def get_title_bar_style():
    """Returns stylesheet for custom title bar (frameless window)."""
    return f"""
    QWidget#titleBar {{
        background-color: {AppConfig.DARK_BACKGROUND};
        border-bottom: 1px solid {AppConfig.BORDER_COLOR};
        padding: 5px 10px;
        height: 35px;
    }}
    
    QPushButton#minimizeButton, QPushButton#maximizeButton, QPushButton#closeButton {{
        background-color: transparent;
        border: none;
        border-radius: 4px;
        padding: 5px;
        width: 30px;
        height: 30px;
    }}
    
    QPushButton#minimizeButton:hover {{
        background-color: rgba(255,255,255,0.1);
    }}
    
    QPushButton#maximizeButton:hover {{
        background-color: rgba(255,255,255,0.1);
    }}
    
    QPushButton#closeButton:hover {{
        background-color: {AppConfig.ACCENT_COLOR};
    }}
    """


def get_loading_spinner_style():
    """Returns stylesheet for loading spinner component."""
    return f"""
    QWidget#loadingSpinner {{
        background-color: transparent;
    }}
    
    QLabel#loadingText {{
        color: {AppConfig.TEXT_COLOR_ALT};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
    }}
    """


def get_modern_card_style():
    """Returns stylesheet for modern card component."""
    return f"""
    QFrame.modern-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: {AppConfig.CARD_RADIUS}px;
        padding: 20px;
    }}
    
    QFrame.modern-card:hover {{
        border-color: {AppConfig.PRIMARY_COLOR};
    }}
    """


def get_badge_style(color=None):
    """Returns stylesheet for badge/pill components."""
    if not color:
        color = AppConfig.PRIMARY_COLOR
    return f"""
    QLabel.badge {{
        background-color: {color};
        color: white;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: {AppConfig.FONT_SIZE_SMALL}pt;
        font-weight: bold;
    }}
    """


def apply_table_styles(table_widget: QTableWidget):
    """
    Applies consistent styling and sizing to a QTableWidget.
    
    Args:
        table_widget: The QTableWidget to style
    """
    table_widget.setStyleSheet(f"""
        QTableWidget {{
            background-color: {AppConfig.CARD_BACKGROUND};
            color: {AppConfig.TEXT_COLOR};
            border: 1px solid {AppConfig.BORDER_COLOR};
            gridline-color: rgba(255,255,255,0.1);
            selection-background-color: {AppConfig.PRIMARY_COLOR};
            selection-color: white;
            border-radius: {AppConfig.CARD_RADIUS}px;
            alternate-background-color: rgba(255,255,255,0.02);
        }}
        
        QTableWidget::item {{
            padding: 10px 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        }}
        
        QTableWidget::item:selected {{
            background-color: {AppConfig.PRIMARY_COLOR};
            color: white;
        }}
        
        QTableWidget QHeaderView::section {{
            background-color: {AppConfig.PRIMARY_COLOR};
            color: {AppConfig.LIGHT_TEXT};
            padding: 12px;
            border: none;
            border-right: 1px solid rgba(255,255,255,0.1);
            border-bottom: 2px solid rgba(255,255,255,0.1);
            font-weight: bold;
            font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        }}
        
        QTableWidget QHeaderView::section:last-child {{
            border-right: none;
        }}
    """)
    
    # Set default row height
    table_widget.verticalHeader().setDefaultSectionSize(AppConfig.TABLE_ROW_HEIGHT)
    table_widget.verticalHeader().setVisible(False)  # Hide row numbers
    
    # Set header font
    header_font = QFont(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_MEDIUM, QFont.Weight.Bold)
    table_widget.horizontalHeader().setFont(header_font)
    
    # Enable alternating row colors
    table_widget.setAlternatingRowColors(True)
    
    # Set header stretch
    header = table_widget.horizontalHeader()
    header.setStretchLastSection(True)


def get_page_title_style():
    """Returns stylesheet for page titles."""
    return f"""
    QLabel {{
        color: {AppConfig.LIGHT_TEXT};
        font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
        font-weight: bold;
        padding: 5px 0;
    }}
    """


def get_image_preview_style():
    """Returns stylesheet for image preview labels."""
    return f"""
    QLabel {{
        border: 2px dashed {AppConfig.BORDER_COLOR};
        border-radius: 8px;
        background-color: {AppConfig.INPUT_BACKGROUND};
    }}
    """


def get_warning_label_style():
    """Returns stylesheet for warning labels."""
    return f"""
    QLabel {{
        color: {AppConfig.ACCENT_COLOR};
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        padding: 10px;
    }}
    """


def get_info_label_style():
    """Returns stylesheet for info/instruction labels."""
    return f"""
    QLabel {{
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        padding: 5px;
    }}
    """


def get_primary_button_style():
    """Returns stylesheet for primary action buttons."""
    return f"""
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {AppConfig.PRIMARY_HOVER};
    }}
    """


def get_danger_button_style():
    """Returns stylesheet for danger/delete buttons."""
    return f"""
    QPushButton {{
        background-color: {AppConfig.ACCENT_COLOR};
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: {AppConfig.BUTTON_RADIUS}px;
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: #c0392b;
    }}
    QPushButton:disabled {{
        background-color: {AppConfig.BORDER_COLOR};
        color: {AppConfig.TEXT_COLOR_ALT};
    }}
    """


def get_input_field_style():
    """Returns stylesheet for input fields with focus state."""
    return f"""
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
    """

