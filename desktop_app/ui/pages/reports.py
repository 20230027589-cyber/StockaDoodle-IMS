# reports.py
#
# This module provides the reports page for managers.
# Displays download buttons for PDF, Excel, and CSV report formats.
#
# Usage: Reports download page in manager dashboard.

from datetime import datetime
import os
import tempfile
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QDateEdit, QComboBox, QFileDialog, QMessageBox,
                             QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from utils.config import AppConfig
from utils.api_wrapper import get_api
from utils.notifications import error, success, info
from utils.icons import get_icon


class ReportsPage(QWidget):
    """
    Reports page with PDF download and preview functionality.
    
    Features:
    - Date range selection (calendar popup)
    - Report type selection
    - PDF preview before download
    - PDF download only (Excel/CSV removed)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = get_api()
        self.temp_pdf_path = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the reports page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Page title
        title = QLabel("Reports")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AppConfig.LIGHT_TEXT};
                font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
                font-weight: bold;
                padding: 10px 0;
            }}
        """)
        layout.addWidget(title)
        
        # Date range selection with calendar popup
        date_layout = QHBoxLayout()
        
        date_layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.start_date)
        
        date_layout.addWidget(QLabel("End Date:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.end_date)
        
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
        # Report type selection
        report_layout = QHBoxLayout()
        report_layout.addWidget(QLabel("Report Type:"))
        
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Sales Performance",
            "Category Distribution",
            "Retailer Performance",
            "Alerts",
            "Managerial Activity",
            "Transactions",
            "User Accounts"
        ])
        report_layout.addWidget(self.report_type)
        report_layout.addStretch()
        
        layout.addLayout(report_layout)
        
        layout.addSpacing(20)
        
        # Action buttons - Preview and Download
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        preview_btn = QPushButton("Preview PDF")
        preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        preview_btn.clicked.connect(self.preview_pdf)
        buttons_layout.addWidget(preview_btn)
        
        download_btn = QPushButton("Download PDF")
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        try:
            icon = get_icon("download", color=AppConfig.LIGHT_TEXT, size=20)
            download_btn.setIcon(icon)
        except:
            pass
        download_btn.clicked.connect(self.download_pdf)
        buttons_layout.addWidget(download_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        layout.addStretch()
    
    def get_report_type_string(self) -> str:
        """Get the API report type string from combo box selection."""
        report_types = [
            "sales-performance",
            "category-distribution",
            "retailer-performance",
            "alerts",
            "managerial-activity",
            "transactions",
            "user-accounts"
        ]
        
        report_index = self.report_type.currentIndex()
        return report_types[report_index] if report_index < len(report_types) else "sales-performance"
    
    def get_report_params(self) -> dict:
        """Get report parameters including date range."""
        params = {}
        start_date_str = self.start_date.date().toString('yyyy-MM-dd')
        end_date_str = self.end_date.date().toString('yyyy-MM-dd')
        
        # Only add date params if report type supports them
        report_type = self.get_report_type_string()
        date_based_reports = ['sales-performance', 'transactions']
        
        if report_type in date_based_reports:
            params['start_date'] = start_date_str
            params['end_date'] = end_date_str
        
        return params
    
    def preview_pdf(self):
        """Preview PDF report in system default PDF viewer."""
        try:
            report_type = self.get_report_type_string()
            params = self.get_report_params()
            
            # Download PDF to temporary file
            pdf_content = self.api.download_pdf_report(report_type=report_type, **params)
            
            # Save to temp file
            if self.temp_pdf_path and os.path.exists(self.temp_pdf_path):
                os.remove(self.temp_pdf_path)
            
            temp_dir = tempfile.gettempdir()
            self.temp_pdf_path = os.path.join(temp_dir, f"report_preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            with open(self.temp_pdf_path, 'wb') as f:
                f.write(pdf_content)
            
            # Open with system default PDF viewer
            import platform
            import subprocess
            
            if platform.system() == 'Windows':
                os.startfile(self.temp_pdf_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', self.temp_pdf_path])
            else:  # Linux
                subprocess.run(['xdg-open', self.temp_pdf_path])
            
            success("PDF preview opened in default viewer.")
        
        except Exception as e:
            error(f"Failed to preview PDF: {str(e)}")
    
    def download_pdf(self):
        """Download PDF report to user-specified location."""
        try:
            report_type = self.get_report_type_string()
            params = self.get_report_params()
            
            # Open file dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report as PDF",
                f"report_{report_type}_{datetime.now().strftime('%Y%m%d')}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                # Download PDF report
                pdf_content = self.api.download_pdf_report(report_type=report_type, **params)
                
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                
                success(f"Report downloaded successfully to {file_path}")
        
        except Exception as e:
            error(f"Failed to download report: {str(e)}")
    
    def refresh_data(self):
        """Refresh reports page (called when tab is switched to)."""
        pass

