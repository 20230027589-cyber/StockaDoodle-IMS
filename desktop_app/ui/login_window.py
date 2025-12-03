# login_window.py
#
# This module provides the login window for user authentication.
# Modern, clean design with blue theme, owl logo, and flat styling.
#
# Usage: Entry point for user authentication before accessing the dashboard.

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QFrame, QGraphicsEffect, QWidget)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QColor
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error as show_error
from utils.font_loader import get_inter_font
from ui.mfa_window import MFAWindow


class LoginWindow(QDialog):
    """
    Login window with modern, clean design.
    
    Features:
    - Deep blue theme (#1E3A8A / #3B82F6)
    - Owl logo at top
    - "StockaDoodle" in large bold text
    - Flat, clean inputs and buttons (no shadows, gradients, or glow)
    - MFA integration with dimmed background
    """
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        self.settings = QSettings("StockaDoodle", "IMS")
        self.user_data = None
        self.mfa_window = None
        
        # Window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(450, 650)
        self.resize(450, 650)
        
        self.init_ui()
        self.load_saved_credentials()
        self.center_window()
    
    def center_window(self):
        """Center window on screen."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())
    
    def init_ui(self):
        """Initialize the login window UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container
        container = QFrame()
        container.setObjectName("loginContainer")
        container.setStyleSheet(f"""
            QFrame#loginContainer {{
                background-color: {AppConfig.DARK_BACKGROUND};
                border-radius: 16px;
                border: none;
            }}
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(24)
        
        # Logo at top
        logo_path = os.path.join(AppConfig.ICONS_DIR, "stockadoodle-transparent.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setFixedHeight(120)
            container_layout.addWidget(logo_label)
        
        # StockaDoodle title
        title_label = QLabel("StockaDoodle")
        title_label.setFont(get_inter_font("Bold", 32))
        title_label.setStyleSheet(f"color: {AppConfig.LIGHT_TEXT};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title_label)
        
        container_layout.addSpacing(20)
        
        # Username input
        username_label = QLabel("Username")
        username_label.setFont(get_inter_font("Medium", 13))
        username_label.setStyleSheet(f"color: {AppConfig.TEXT_COLOR};")
        container_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(get_inter_font("Regular", 13))
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 1px solid {AppConfig.BORDER_COLOR};
                border-radius: 8px;
                padding: 12px 16px;
                color: {AppConfig.TEXT_COLOR};
                font-size: 13pt;
            }}
            QLineEdit:focus {{
                border: 2px solid #3B82F6;
            }}
        """)
        container_layout.addWidget(self.username_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setFont(get_inter_font("Medium", 13))
        password_label.setStyleSheet(f"color: {AppConfig.TEXT_COLOR};")
        container_layout.addWidget(password_label)
        
        password_layout = QHBoxLayout()
        password_layout.setSpacing(0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(get_inter_font("Regular", 13))
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                border: 1px solid {AppConfig.BORDER_COLOR};
                border-radius: 8px;
                padding: 12px 16px;
                color: {AppConfig.TEXT_COLOR};
                font-size: 13pt;
            }}
            QLineEdit:focus {{
                border: 2px solid #3B82F6;
            }}
        """)
        
        self.password_toggle = QPushButton("👁")
        self.password_toggle.setFixedSize(40, 40)
        self.password_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.password_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: 18px;
            }}
            QPushButton:hover {{
                color: {AppConfig.LIGHT_TEXT};
            }}
        """)
        self.password_toggle.clicked.connect(self.toggle_password)
        
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.password_toggle)
        container_layout.addLayout(password_layout)
        
        # Remember Me
        self.remember_checkbox = QCheckBox("Remember Me")
        self.remember_checkbox.setFont(get_inter_font("Regular", 12))
        self.remember_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {AppConfig.TEXT_COLOR_ALT};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {AppConfig.BORDER_COLOR};
                border-radius: 4px;
                background-color: {AppConfig.INPUT_BACKGROUND};
            }}
            QCheckBox::indicator:checked {{
                background-color: #3B82F6;
                border-color: #3B82F6;
            }}
        """)
        container_layout.addWidget(self.remember_checkbox)
        
        container_layout.addSpacing(10)
        
        # Login button - flat, clean, blue
        self.login_button = QPushButton("Login")
        self.login_button.setFont(get_inter_font("Medium", 14))
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 14pt;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
            QPushButton:pressed {{
                background-color: #1E40AF;
            }}
            QPushButton:disabled {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                color: {AppConfig.TEXT_COLOR_MUTED};
            }}
        """)
        self.login_button.clicked.connect(self.on_login)
        container_layout.addWidget(self.login_button)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setFont(get_inter_font("Regular", 11))
        self.error_label.setStyleSheet(f"color: {AppConfig.ACCENT_COLOR};")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        container_layout.addWidget(self.error_label)
        
        container_layout.addStretch()
        main_layout.addWidget(container)
        
        # Enter key triggers login
        self.username_input.returnPressed.connect(self.on_login)
        self.password_input.returnPressed.connect(self.on_login)
    
    def toggle_password(self):
        """Toggle password visibility."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_toggle.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_toggle.setText("👁")
    
    def load_saved_credentials(self):
        """Load saved username from QSettings."""
        remember = self.settings.value("remember_me", False, type=bool)
        if remember:
            username = self.settings.value("username", "", type=str)
            self.username_input.setText(username)
            self.remember_checkbox.setChecked(True)
    
    def save_credentials(self):
        """Save credentials to QSettings."""
        if self.remember_checkbox.isChecked():
            self.settings.setValue("remember_me", True)
            self.settings.setValue("username", self.username_input.text())
        else:
            self.settings.setValue("remember_me", False)
            self.settings.remove("username")
    
    def dim_window(self):
        """Dim the login window when MFA opens."""
        # Create semi-transparent overlay
        if not hasattr(self, 'overlay'):
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.overlay.setGeometry(self.rect())
        self.overlay.raise_()
        self.overlay.show()
        self.overlay.setEnabled(False)  # Don't intercept clicks
    
    def undim_window(self):
        """Remove dim effect."""
        if hasattr(self, 'overlay'):
            self.overlay.hide()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging frameless window."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging frameless window."""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def on_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            self.show_error_message("Please enter your username.")
            return
        
        if not password:
            self.show_error_message("Please enter your password.")
            return
        
        self.login_button.setEnabled(False)
        self.error_label.hide()
        
        try:
            result = self.api.login(username, password)
            
            if result.get('mfa_required'):
                # Get email from API response (REAL email from database)
                mfa_username = result.get('username', username)
                mfa_email = result.get('email', '')  # This comes from the database
                
                if not mfa_email:
                    self.show_error_message("Email not found. Please contact administrator.")
                    self.login_button.setEnabled(True)
                    return
                
                # Dim login window
                self.dim_window()
                
                # Create MFA window as separate, centered popup
                self.mfa_window = MFAWindow(mfa_username, mfa_email, self)
                self.mfa_window.setWindowFlags(
                    Qt.WindowType.Dialog |
                    Qt.WindowType.FramelessWindowHint |
                    Qt.WindowType.WindowStaysOnTopHint
                )
                self.mfa_window.setModal(True)
                self.mfa_window.center_window()
                
                # Show MFA window
                if self.mfa_window.exec() == QDialog.DialogCode.Accepted:
                    self.user_data = self.mfa_window.user_data
                    self.save_credentials()
                    self.undim_window()
                    self.accept()
                else:
                    self.undim_window()
                    self.login_button.setEnabled(True)
            else:
                # Login successful (no MFA)
                self.user_data = result.get('user')
                if self.user_data:
                    self.save_credentials()
                    self.accept()
                else:
                    self.show_error_message("Login failed. Please try again.")
                    self.login_button.setEnabled(True)
        
        except Exception as e:
            error_msg = str(e)
            self.show_error_message(error_msg)
            self.login_button.setEnabled(True)
    
    def show_error_message(self, message: str):
        """Show error message in the UI."""
        self.error_label.setText(message)
        self.error_label.show()
    
    def get_user_data(self) -> dict:
        """Get the authenticated user data."""
        return self.user_data or {}
