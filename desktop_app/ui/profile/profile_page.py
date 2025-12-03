# profile_page.py
#
# This module provides the profile page for users.
# Contains two tabs: Personal Info and Security.
# Enhanced with profile picture upload, role field, and better layout.
#
# Usage: Profile management page accessible from all user roles.

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QMessageBox, QComboBox, QFormLayout,
                             QFileDialog, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import success, error
from ui.components.custom_tab_widget import CustomTabWidget
from utils.helpers import load_product_image, get_feather_icon


class PersonalInfoTab(QWidget):
    """Personal information tab in profile page."""
    
    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        # Get current_user from parent or use user as fallback
        self.current_user = getattr(parent, 'current_user', None) if parent else None
        if not self.current_user:
            self.current_user = user  # Fallback to user dict
        self.api = get_api()
        self.profile_image_path = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize personal info tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Profile Information")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_XLARGE}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(title)
        
        # Profile picture section
        profile_picture_layout = QHBoxLayout()
        profile_picture_layout.setSpacing(20)
        
        # Profile picture container
        picture_container = QWidget()
        picture_container.setFixedSize(150, 150)
        
        self.profile_picture_label = QLabel()
        self.profile_picture_label.setFixedSize(150, 150)
        self.profile_picture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_picture_label.setStyleSheet(f"""
            QLabel {{
                border: 3px solid {AppConfig.BORDER_COLOR};
                border-radius: 75px;
                background-color: {AppConfig.INPUT_BACKGROUND};
            }}
        """)
        
        # Load existing profile picture
        self.load_profile_picture()
        
        picture_container_layout = QVBoxLayout(picture_container)
        picture_container_layout.setContentsMargins(0, 0, 0, 0)
        picture_container_layout.addWidget(self.profile_picture_label)
        
        profile_picture_layout.addWidget(picture_container)
        
        # Picture buttons
        picture_buttons_layout = QVBoxLayout()
        picture_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        upload_btn = QPushButton("Upload Photo")
        upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_btn.clicked.connect(self.upload_profile_picture)
        picture_buttons_layout.addWidget(upload_btn)
        
        remove_btn = QPushButton("Remove Photo")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(self.remove_profile_picture)
        picture_buttons_layout.addWidget(remove_btn)
        
        picture_buttons_layout.addStretch()
        
        profile_picture_layout.addLayout(picture_buttons_layout)
        profile_picture_layout.addStretch()
        
        layout.addLayout(profile_picture_layout)
        
        # Form layout for user details
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Full Name
        self.name_input = QLineEdit()
        self.name_input.setText(self.user.get('full_name', ''))
        self.name_input.setPlaceholderText("Enter your full name")
        form_layout.addRow("Full Name *:", self.name_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setText(self.user.get('email', ''))
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addRow("Email *:", self.email_input)
        
        # Role (read-only for non-admin)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Manager", "Retailer"])
        
        # Set current role
        current_role = self.user.get('role', '').capitalize()
        role_index = self.role_combo.findText(current_role)
        if role_index >= 0:
            self.role_combo.setCurrentIndex(role_index)
        
        # Make role read-only if user is not admin
        is_admin = False
        if self.current_user and isinstance(self.current_user, dict):
            is_admin = self.current_user.get('role', '').lower() == 'admin'
        if self.role_combo:
            self.role_combo.setEnabled(is_admin)
        if not is_admin:
            self.role_combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: {AppConfig.CARD_BACKGROUND};
                    color: {AppConfig.TEXT_COLOR_ALT};
                }}
            """)
        
        form_layout.addRow("Role:", self.role_combo)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        # Save button
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel Changes")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reset_form)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 10px 30px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {AppConfig.PRIMARY_HOVER};
            }}
        """)
        save_btn.clicked.connect(self.save_changes)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_profile_picture(self):
        """Load existing profile picture."""
        image_path = self.user.get('image_path') or self.user.get('image')
        if image_path:
            pixmap = load_product_image(image_path, target_size=(150, 150))
            self.profile_picture_label.setPixmap(pixmap)
        else:
            # Show default avatar
            self.profile_picture_label.setText("👤")
            self.profile_picture_label.setStyleSheet(f"""
                QLabel {{
                    border: 3px solid {AppConfig.BORDER_COLOR};
                    border-radius: 75px;
                    background-color: {AppConfig.INPUT_BACKGROUND};
                    font-size: 60pt;
                    color: {AppConfig.TEXT_COLOR_ALT};
                }}
            """)
    
    def upload_profile_picture(self):
        """Open file dialog to upload profile picture."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Profile Picture",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.webp)"
        )
        
        if file_path:
            # Check file size (max 5MB)
            file_size = os.path.getsize(file_path)
            if file_size > 5 * 1024 * 1024:
                error("Image file is too large. Maximum size is 5MB.")
                return
            
            self.profile_image_path = file_path
            pixmap = load_product_image(file_path, target_size=(150, 150))
            self.profile_picture_label.setPixmap(pixmap)
            self.profile_picture_label.setText("")
    
    def remove_profile_picture(self):
        """Remove profile picture."""
        self.profile_image_path = None
        self.load_profile_picture()  # Reload default
    
    def reset_form(self):
        """Reset form to original values."""
        self.name_input.setText(self.user.get('full_name', ''))
        self.email_input.setText(self.user.get('email', ''))
        current_role = self.user.get('role', '').capitalize()
        role_index = self.role_combo.findText(current_role)
        if role_index >= 0:
            self.role_combo.setCurrentIndex(role_index)
        self.profile_image_path = None
        self.load_profile_picture()
    
    def save_changes(self):
        """Save personal information changes."""
        try:
            user_id = self.user.get('id')
            if not user_id:
                error("User ID not found.")
                return
            
            # Validate required fields
            if not self.name_input.text().strip():
                error("Full name is required.")
                return
            
            if not self.email_input.text().strip():
                error("Email is required.")
                return
            
            # Validate email format
            email = self.email_input.text().strip()
            if '@' not in email or '.' not in email.split('@')[-1]:
                error("Please enter a valid email address.")
                return
            
            updates = {
                'full_name': self.name_input.text().strip(),
                'email': email
            }
            
            # Update role if admin
            is_admin = False
            if self.current_user and isinstance(self.current_user, dict):
                is_admin = self.current_user.get('role', '').lower() == 'admin'
            if is_admin:
                role_text = self.role_combo.currentText()
                updates['role'] = role_text.lower()
            
            # Handle profile picture
            if self.profile_image_path:
                with open(self.profile_image_path, 'rb') as f:
                    image_bytes = f.read()
                updates['user_image'] = image_bytes
            
            # Update via API
            self.api.update_user(user_id, **updates)
            
            # Update local user data
            self.user.update(updates)
            
            success("Personal information updated successfully.")
            
            # Reload profile picture if changed
            if self.profile_image_path:
                self.load_profile_picture()
        
        except Exception as e:
            error(f"Failed to update personal information: {str(e)}")


class SecurityTab(QWidget):
    """Security settings tab in profile page."""
    
    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        # Get current_user from parent or use user as fallback
        self.current_user = getattr(parent, 'current_user', None) if parent else None
        if not self.current_user:
            self.current_user = user  # Fallback to user dict
        self.api = get_api()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize security tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Security Settings")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_XLARGE}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(title)
        
        # Account Email display
        email_label = QLabel(f"Account Email: {self.user.get('email', 'N/A')}")
        email_label.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.TEXT_COLOR_ALT};
                font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                padding: 5px 0;
            }}
        """)
        layout.addWidget(email_label)
        
        layout.addSpacing(10)
        
        # Change Password section
        password_title = QLabel("Change Password")
        password_title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(password_title)
        
        # Form layout for password fields
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Current password
        self.old_password = QLineEdit()
        self.old_password.setPlaceholderText("Enter current password")
        self.old_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Current Password *:", self.old_password)
        
        # New password
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter new password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("New Password *:", self.new_password)
        
        # Confirm password
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm new password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirm Password *:", self.confirm_password)
        
        layout.addLayout(form_layout)
        
        # Two-Factor Authentication (only for admin/manager)
        is_admin_or_manager = False
        if self.current_user and isinstance(self.current_user, dict):
            role = self.current_user.get('role', '')
            is_admin_or_manager = role in ['admin', 'manager']
        if is_admin_or_manager:
            layout.addSpacing(15)
            
            mfa_title = QLabel("Two-Factor Authentication")
            mfa_title.setStyleSheet(f"""
                QLabel {{
                    color: {AppConfig.LIGHT_TEXT};
                    font-size: {AppConfig.FONT_SIZE_LARGE}pt;
                    font-weight: bold;
                    padding: 10px 0;
                }}
            """)
            layout.addWidget(mfa_title)
            
            self.mfa_checkbox = QCheckBox("Enable MFA (Email)")
            self.mfa_checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {AppConfig.TEXT_COLOR};
                    font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
                }}
            """)
            # Set checkbox based on user's MFA status (if available)
            self.mfa_checkbox.setChecked(self.user.get('mfa_enabled', False))
            layout.addWidget(self.mfa_checkbox)
        
        layout.addStretch()
        
        # Change password button
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        change_pwd_btn = QPushButton("Update Password")
        change_pwd_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        change_pwd_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppConfig.PRIMARY_COLOR};
                color: white;
                padding: 10px 30px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {AppConfig.PRIMARY_HOVER};
            }}
        """)
        change_pwd_btn.clicked.connect(self.change_password)
        buttons_layout.addWidget(change_pwd_btn)
        
        layout.addLayout(buttons_layout)
    
    def change_password(self):
        """Change user password."""
        try:
            user_id = self.user.get('id')
            if not user_id:
                error("User ID not found.")
                return
            
            old_pwd = self.old_password.text()
            new_pwd = self.new_password.text()
            confirm_pwd = self.confirm_password.text()
            
            # Validation
            if not old_pwd:
                error("Please enter your current password.")
                return
            
            if not new_pwd:
                error("Please enter a new password.")
                return
            
            if new_pwd != confirm_pwd:
                error("New password and confirmation do not match.")
                return
            
            if len(new_pwd) < AppConfig.MIN_PASSWORD_LENGTH:
                error(f"Password must be at least {AppConfig.MIN_PASSWORD_LENGTH} characters long.")
                return
            
            # Change password via API
            self.api.change_password(user_id, old_pwd, new_pwd)
            
            # Clear fields
            self.old_password.clear()
            self.new_password.clear()
            self.confirm_password.clear()
            
            success("Password changed successfully.")
        
        except Exception as e:
            error(f"Failed to change password: {str(e)}")


class ProfilePage(QWidget):
    """
    Profile page with two tabs: Personal Info and Security.
    
    Features:
    - Personal Info tab: Edit name, email, role (admin only), profile picture
    - Security tab: Change password, MFA setup (admin/manager only)
    """
    
    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self.current_user = user  # For role checks
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the profile page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Custom tab widget
        tabs = CustomTabWidget()
        
        # Create tabs with parent reference for current_user access
        personal_tab = PersonalInfoTab(self.user, self)
        personal_tab.current_user = self.current_user
        
        security_tab = SecurityTab(self.user, self)
        security_tab.current_user = self.current_user
        
        tabs.addTab(personal_tab, "Personal Info")
        tabs.addTab(security_tab, "Security")
        
        layout.addWidget(tabs)
    
    def refresh_data(self):
        """Refresh profile data (called when tab is switched to)."""
        pass
