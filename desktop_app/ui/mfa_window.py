# mfa_window.py
#
# This module provides the MFA (Multi-Factor Authentication) window.
# Modern, clean design with Google-style 6-digit code input.
#
# Usage: Displayed after login for admin/manager roles to verify MFA code.

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QKeyEvent
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error as show_error, success
from utils.font_loader import get_inter_font


class MFAWindow(QDialog):
    """
    MFA verification window with Google-style 6-digit code input.
    
    Features:
    - Separate, centered popup window
    - Owl logo at top
    - Real email from database displayed
    - Google-style 6-digit code input (auto-jump to next box)
    - Resend button with countdown
    - Clean, flat design with blue theme
    """
    
    def __init__(self, username: str, email: str, parent=None):
        """
        Initialize MFA window.
        
        Args:
            username: Username for MFA verification
            email: Email address from database (REAL email, not hardcoded)
            parent: Parent widget (login window)
        """
        super().__init__(parent)
        self.username = username
        self.email = email  # Real email from database
        self.api = get_api()
        self.user_data = None
        self.resend_timer = QTimer()
        self.resend_countdown = 60
        
        # Window setup - separate, centered popup
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setMinimumSize(420, 580)
        self.resize(420, 580)
        
        self.init_ui()
        self.send_mfa_code()
        self.center_window()
    
    def center_window(self):
        """Center window on screen."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())
    
    def init_ui(self):
        """Initialize the MFA window UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main container
        container = QFrame()
        container.setObjectName("mfaContainer")
        container.setStyleSheet(f"""
            QFrame#mfaContainer {{
                background-color: {AppConfig.DARK_BACKGROUND};
                border-radius: 16px;
                border: none;
            }}
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(24)
        
        # Close button (top right)
        title_bar = QHBoxLayout()
        title_bar.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {AppConfig.TEXT_COLOR};
                border: none;
                border-radius: 6px;
                font-size: 24px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        close_btn.clicked.connect(self.reject)
        title_bar.addWidget(close_btn)
        
        container_layout.addLayout(title_bar)
        
        # Logo
        logo_path = os.path.join(AppConfig.ICONS_DIR, "stockadoodle-transparent.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setFixedHeight(100)
            container_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Two-Factor Authentication")
        title_label.setFont(get_inter_font("Bold", 22))
        title_label.setStyleSheet(f"color: {AppConfig.LIGHT_TEXT};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title_label)
        
        # Description with REAL email from database
        desc_label = QLabel(f"Enter the 6-digit code sent to:\n{self.email}")
        desc_label.setFont(get_inter_font("Regular", 12))
        desc_label.setStyleSheet(f"color: {AppConfig.TEXT_COLOR_ALT};")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        container_layout.addWidget(desc_label)
        
        container_layout.addSpacing(30)
        
        # Google-style 6-digit code input
        code_layout = QHBoxLayout()
        code_layout.setSpacing(12)
        code_layout.addStretch()
        
        self.code_inputs = []
        for i in range(6):
            code_input = QLineEdit()
            code_input.setMaxLength(1)
            code_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            code_input.setFont(get_inter_font("Bold", 24))
            code_input.setValidator(QIntValidator(0, 9))
            code_input.setFixedSize(50, 60)
            code_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {AppConfig.INPUT_BACKGROUND};
                    border: 2px solid {AppConfig.BORDER_COLOR};
                    border-radius: 8px;
                    color: {AppConfig.LIGHT_TEXT};
                    font-size: 24pt;
                }}
                QLineEdit:focus {{
                    border: 2px solid #3B82F6;
                    background-color: {AppConfig.CARD_BACKGROUND};
                }}
            """)
            
            # Auto-jump to next field when digit entered
            if i < 5:
                code_input.textChanged.connect(lambda text, idx=i: self.move_to_next(text, idx))
            
            # Handle backspace to move to previous field
            code_input.textChanged.connect(lambda text, idx=i: self.handle_backspace(text, idx))
            
            # Auto-verify when last digit entered
            if i == 5:
                code_input.textChanged.connect(lambda text: self.on_last_digit(text))
            
            self.code_inputs.append(code_input)
            code_layout.addWidget(code_input)
        
        code_layout.addStretch()
        container_layout.addLayout(code_layout)
        
        container_layout.addSpacing(30)
        
        # Verify button
        self.verify_button = QPushButton("Verify Code")
        self.verify_button.setFont(get_inter_font("Medium", 14))
        self.verify_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.verify_button.setStyleSheet(f"""
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
            QPushButton:disabled {{
                background-color: {AppConfig.INPUT_BACKGROUND};
                color: {AppConfig.TEXT_COLOR_MUTED};
            }}
        """)
        self.verify_button.clicked.connect(self.on_verify)
        container_layout.addWidget(self.verify_button)
        
        # Resend button with countdown
        self.resend_button = QPushButton("Resend Code")
        self.resend_button.setFont(get_inter_font("Regular", 12))
        self.resend_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.resend_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: #3B82F6;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 10px;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: rgba(59, 130, 246, 0.1);
            }}
            QPushButton:disabled {{
                color: {AppConfig.TEXT_COLOR_MUTED};
                border-color: {AppConfig.BORDER_COLOR};
            }}
        """)
        self.resend_button.clicked.connect(self.resend_code)
        container_layout.addWidget(self.resend_button)
        
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
        
        # Setup resend timer
        self.resend_timer.timeout.connect(self.update_resend_countdown)
        self.resend_button.setEnabled(False)
        self.start_resend_countdown()
        
        # Focus first input
        if self.code_inputs:
            QTimer.singleShot(100, lambda: self.code_inputs[0].setFocus())
    
    def move_to_next(self, text: str, current_idx: int):
        """Move focus to next input field when digit entered (Google-style)."""
        if text and current_idx < len(self.code_inputs) - 1:
            self.code_inputs[current_idx + 1].setFocus()
            self.code_inputs[current_idx + 1].selectAll()
    
    def handle_backspace(self, text: str, current_idx: int):
        """Move focus to previous input field on backspace."""
        if not text and current_idx > 0:
            self.code_inputs[current_idx - 1].setFocus()
            self.code_inputs[current_idx - 1].clear()
            self.code_inputs[current_idx - 1].selectAll()
    
    def on_last_digit(self, text: str):
        """Auto-verify when last digit is entered."""
        if text:
            code = self.get_entered_code()
            if len(code) == 6:
                # Auto-verify after short delay
                QTimer.singleShot(300, self.on_verify)
    
    def get_entered_code(self) -> str:
        """Get the entered code from all input fields."""
        return ''.join([input.text() for input in self.code_inputs])
    
    def send_mfa_code(self):
        """Send MFA code to user's email."""
        try:
            result = self.api.send_mfa_code(self.username, self.email)
            if result:
                success("MFA code sent to your email.")
        except Exception as e:
            self.show_error_message(f"Failed to send MFA code: {str(e)}")
    
    def resend_code(self):
        """Resend MFA code and restart countdown."""
        self.send_mfa_code()
        self.start_resend_countdown()
    
    def start_resend_countdown(self):
        """Start the 60-second countdown for resend button."""
        self.resend_countdown = 60
        self.resend_button.setEnabled(False)
        self.update_resend_button_text()
        self.resend_timer.start(1000)
    
    def update_resend_countdown(self):
        """Update resend button countdown timer."""
        self.resend_countdown -= 1
        self.update_resend_button_text()
        
        if self.resend_countdown <= 0:
            self.resend_timer.stop()
            self.resend_button.setEnabled(True)
            self.resend_button.setText("Resend Code")
    
    def update_resend_button_text(self):
        """Update resend button text with countdown."""
        if self.resend_countdown > 0:
            self.resend_button.setText(f"Resend Code ({self.resend_countdown}s)")
        else:
            self.resend_button.setText("Resend Code")
    
    def on_verify(self):
        """Handle verify button click."""
        code = self.get_entered_code()
        
        if len(code) != 6:
            self.show_error_message("Please enter all 6 digits.")
            # Focus first empty field
            for i, input_field in enumerate(self.code_inputs):
                if not input_field.text():
                    input_field.setFocus()
                    break
            return
        
        self.verify_button.setEnabled(False)
        self.error_label.hide()
        
        try:
            result = self.api.verify_mfa_code(self.username, code)
            
            if result.get('user'):
                self.user_data = result.get('user')
                success("MFA verified successfully!")
                self.accept()
            else:
                self.show_error_message("Invalid or expired MFA code. Please try again.")
                self.clear_code_inputs()
                self.verify_button.setEnabled(True)
                if self.code_inputs:
                    self.code_inputs[0].setFocus()
        
        except Exception as e:
            error_msg = str(e)
            self.show_error_message(error_msg)
            self.clear_code_inputs()
            self.verify_button.setEnabled(True)
            if self.code_inputs:
                self.code_inputs[0].setFocus()
    
    def clear_code_inputs(self):
        """Clear all code input fields."""
        for input_field in self.code_inputs:
            input_field.clear()
    
    def show_error_message(self, message: str):
        """Show error message in the UI."""
        self.error_label.setText(f"⚠️ {message}")
        self.error_label.show()
    
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
