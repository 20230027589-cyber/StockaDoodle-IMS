# font_loader.py
#
# This module provides font loading utilities for Inter fonts.
# Loads fonts from assets/fonts directory and makes them available to the application.
#
# Usage: Imported and called at application startup to load Inter fonts.

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtCore import QDir
import os
from utils.config import AppConfig


def load_fonts():
    """
    Load all Inter fonts from assets/fonts directory.
    Makes fonts available to the application via QFontDatabase.
    
    Returns:
        dict: Dictionary mapping font family names to font IDs
    """
    font_ids = {}
    fonts_dir = AppConfig.FONTS_DIR
    
    if not os.path.exists(fonts_dir):
        print(f"Warning: Fonts directory not found: {fonts_dir}")
        return font_ids
    
    # List of font files to load
    font_files = [
        "Inter-Regular.ttf",
        "Inter-Medium.ttf",
        "Inter-Bold.ttf",
        "Inter-Light.ttf"
    ]
    
    for font_file in font_files:
        font_path = os.path.join(fonts_dir, font_file)
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    font_name = families[0]
                    font_ids[font_file] = font_id
                    print(f"Loaded font: {font_name} from {font_file}")
            else:
                print(f"Warning: Failed to load font {font_file}")
        else:
            print(f"Warning: Font file not found: {font_path}")
    
    return font_ids


def get_inter_font(weight: str = "Regular", size: int = 12):
    """
    Get a QFont object for Inter font with specified weight and size.
    
    Args:
        weight: Font weight ("Regular", "Medium", "Bold", "Light")
        size: Font size in points
        
    Returns:
        QFont: Configured Inter font
    """
    from PyQt6.QtGui import QFont
    
    font_family = f"Inter-{weight}" if weight != "Regular" else "Inter"
    
    font = QFont(font_family, size)
    
    # Set weight based on font name
    if "Bold" in weight:
        font.setWeight(QFont.Weight.Bold)
    elif "Medium" in weight:
        font.setWeight(QFont.Weight.Medium)
    elif "Light" in weight:
        font.setWeight(QFont.Weight.Light)
    else:
        font.setWeight(QFont.Weight.Normal)
    
    return font

