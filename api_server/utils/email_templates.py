"""
Professional HTML email templates for StockaDoodle IMS
Includes logo and corporate branding
"""

import os
import base64
from pathlib import Path


def get_logo_base64():
    """Get logo as base64 encoded string for email embedding"""
    possible_paths = [
        Path("desktop_app/assets/icons/stockadoodle-transparent.png"),
        Path("../desktop_app/assets/icons/stockadoodle-transparent.png"),
        Path("../../desktop_app/assets/icons/stockadoodle-transparent.png"),
        Path("desktop_app/assets/icons/stockadoodle.png"),
    ]
    
    for logo_path in possible_paths:
        if logo_path.exists():
            try:
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                    return f"data:image/png;base64,{logo_base64}"
            except Exception as e:
                print(f"Error encoding logo from {logo_path}: {e}")
                continue
    
    return None


def get_mfa_email_template(username: str, code: str, expiry_minutes: int = 5):
    """Generate professional MFA code email template"""
    logo_base64 = get_logo_base64()
    logo_html = f'<img src="{logo_base64}" alt="StockaDoodle Logo" style="max-width: 150px; height: auto; margin-bottom: 20px;">' if logo_base64 else ''
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StockaDoodle MFA Code</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td align="center" style="padding: 40px 20px 20px; background: linear-gradient(135deg, #1E293B 0%, #6C5CE7 100%); border-radius: 8px 8px 0 0;">
                                {logo_html}
                                <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">StockaDoodle IMS</h1>
                                <p style="margin: 5px 0 0; color: #E2E8F0; font-size: 14px;">Multi-Factor Authentication</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="margin: 0 0 20px; color: #1E293B; font-size: 20px; font-weight: 600;">Hello {username},</h2>
                                
                                <p style="margin: 0 0 20px; color: #334155; font-size: 15px; line-height: 1.6;">
                                    You have requested a Multi-Factor Authentication (MFA) code to access your StockaDoodle account.
                                </p>
                                
                                <div style="background-color: #F1F5F9; border-left: 4px solid #6C5CE7; padding: 20px; margin: 25px 0; border-radius: 4px;">
                                    <p style="margin: 0 0 10px; color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Your MFA Code</p>
                                    <p style="margin: 0; color: #1E293B; font-size: 32px; font-weight: 700; letter-spacing: 4px; font-family: 'Courier New', monospace;">{code}</p>
                                </div>
                                
                                <p style="margin: 20px 0; color: #64748B; font-size: 13px;">
                                    ⏰ This code will expire in <strong>{expiry_minutes} minutes</strong>.
                                </p>
                                
                                <div style="background-color: #FEF3C7; border: 1px solid #FCD34D; border-radius: 4px; padding: 15px; margin: 25px 0;">
                                    <p style="margin: 0; color: #92400E; font-size: 13px; line-height: 1.5;">
                                        <strong>⚠️ Security Notice:</strong> If you did not request this code, please ignore this email and contact your system administrator immediately. Never share your MFA code with anyone.
                                    </p>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-radius: 0 0 8px 8px;">
                                <p style="margin: 0 0 10px; color: #64748B; font-size: 12px; text-align: center; line-height: 1.5;">
                                    This is an automated message from StockaDoodle Inventory Management System.<br>
                                    Please do not reply to this email.
                                </p>
                                <p style="margin: 0; color: #94A3B8; font-size: 11px; text-align: center;">
                                    © {os.getenv('BRANCH_NAME', 'QuickMart')} - StockaDoodle IMS
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def get_low_stock_alert_template(products: list, timestamp: str):
    """Generate professional low stock alert email template"""
    logo_base64 = get_logo_base64()
    logo_html = f'<img src="{logo_base64}" alt="StockaDoodle Logo" style="max-width: 150px; height: auto; margin-bottom: 20px;">' if logo_base64 else ''
    
    products_html = ""
    for product in products[:10]:  # Limit to 10 for email
        shortage = product.min_stock_level - product.stock_level
        products_html += f"""
        <tr style="border-bottom: 1px solid #E2E8F0;">
            <td style="padding: 12px; color: #1E293B; font-weight: 600;">{product.name}</td>
            <td style="padding: 12px; color: #EF4444; font-weight: 600;">{product.stock_level}</td>
            <td style="padding: 12px; color: #334155;">{product.min_stock_level}</td>
            <td style="padding: 12px; color: #DC2626; font-weight: 600;">{shortage} units</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Low Stock Alert</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 700px; width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td align="center" style="padding: 40px 20px 20px; background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); border-radius: 8px 8px 0 0;">
                                {logo_html}
                                <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">🚨 Low Stock Alert</h1>
                                <p style="margin: 5px 0 0; color: #FEE2E2; font-size: 14px;">{len(products)} Products Need Attention</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px; color: #334155; font-size: 15px; line-height: 1.6;">
                                    The following products are running low on stock and require immediate attention:
                                </p>
                                
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 25px 0; border: 1px solid #E2E8F0; border-radius: 4px; overflow: hidden;">
                                    <thead>
                                        <tr style="background-color: #1E293B;">
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: left;">Product</th>
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: center;">Current</th>
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: center;">Minimum</th>
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: center;">Shortage</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {products_html}
                                    </tbody>
                                </table>
                                
                                <div style="background-color: #FEF3C7; border: 1px solid #FCD34D; border-radius: 4px; padding: 15px; margin: 25px 0;">
                                    <p style="margin: 0; color: #92400E; font-size: 14px; line-height: 1.5;">
                                        <strong>⚠️ Action Required:</strong> Please restock these items as soon as possible to avoid stockouts and maintain smooth operations.
                                    </p>
                                </div>
                                
                                <p style="margin: 20px 0 0; color: #64748B; font-size: 12px;">
                                    Alert generated on: <strong>{timestamp}</strong>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-radius: 0 0 8px 8px;">
                                <p style="margin: 0 0 10px; color: #64748B; font-size: 12px; text-align: center; line-height: 1.5;">
                                    This is an automated alert from StockaDoodle Inventory Management System.<br>
                                    Please review the full inventory status in your dashboard.
                                </p>
                                <p style="margin: 0; color: #94A3B8; font-size: 11px; text-align: center;">
                                    © {os.getenv('BRANCH_NAME', 'QuickMart')} - StockaDoodle IMS
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def get_expiration_alert_template(products_expiring: dict, batches: list, days_ahead: int, timestamp: str):
    """Generate professional expiration alert email template"""
    logo_base64 = get_logo_base64()
    logo_html = f'<img src="{logo_base64}" alt="StockaDoodle Logo" style="max-width: 150px; height: auto; margin-bottom: 20px;">' if logo_base64 else ''
    
    products_html = ""
    count = 0
    for product_name, product_batches in list(products_expiring.items())[:10]:
        if count >= 10:
            break
        # Handle both dict and object batches
        batches_list = list(product_batches) if product_batches else []
        batches_text = ", ".join([
            f"Batch #{b.id if hasattr(b, 'id') else b.get('id', 'N/A')} ({b.quantity if hasattr(b, 'quantity') else b.get('quantity', 0)} units)" 
            for b in batches_list[:3]
        ])
        if len(batches_list) > 3:
            batches_text += f" and {len(batches_list) - 3} more"
        products_html += f"""
        <tr style="border-bottom: 1px solid #E2E8F0;">
            <td style="padding: 12px; color: #1E293B; font-weight: 600;">{product_name}</td>
            <td style="padding: 12px; color: #334155;">{batches_text}</td>
        </tr>
        """
        count += 1
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expiration Alert</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 700px; width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td align="center" style="padding: 40px 20px 20px; background: linear-gradient(135deg, #F59E0B 0%, #FCD34D 100%); border-radius: 8px 8px 0 0;">
                                {logo_html}
                                <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">⏰ Expiration Alert</h1>
                                <p style="margin: 5px 0 0; color: #FEF3C7; font-size: 14px;">{len(products_expiring)} Products Expiring Within {days_ahead} Days</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px; color: #334155; font-size: 15px; line-height: 1.6;">
                                    The following products have batches expiring within the next <strong>{days_ahead} days</strong>:
                                </p>
                                
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 25px 0; border: 1px solid #E2E8F0; border-radius: 4px; overflow: hidden;">
                                    <thead>
                                        <tr style="background-color: #1E293B;">
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: left;">Product</th>
                                            <th style="padding: 12px; color: #ffffff; font-size: 13px; font-weight: 600; text-align: left;">Expiring Batches</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {products_html}
                                    </tbody>
                                </table>
                                
                                <div style="background-color: #FEF3C7; border: 1px solid #FCD34D; border-radius: 4px; padding: 15px; margin: 25px 0;">
                                    <p style="margin: 0; color: #92400E; font-size: 14px; line-height: 1.5;">
                                        <strong>⚠️ Action Required:</strong> Please prioritize selling or disposing of these items to minimize losses and maintain inventory quality.
                                    </p>
                                </div>
                                
                                <p style="margin: 20px 0 0; color: #64748B; font-size: 12px;">
                                    Alert generated on: <strong>{timestamp}</strong>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-radius: 0 0 8px 8px;">
                                <p style="margin: 0 0 10px; color: #64748B; font-size: 12px; text-align: center; line-height: 1.5;">
                                    This is an automated alert from StockaDoodle Inventory Management System.<br>
                                    Please review the full inventory status in your dashboard.
                                </p>
                                <p style="margin: 0; color: #94A3B8; font-size: 11px; text-align: center;">
                                    © {os.getenv('BRANCH_NAME', 'QuickMart')} - StockaDoodle IMS
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def get_daily_summary_template(low_stock: list, expiring: list, timestamp: str):
    """Generate professional daily summary email template"""
    logo_base64 = get_logo_base64()
    logo_html = f'<img src="{logo_base64}" alt="StockaDoodle Logo" style="max-width: 150px; height: auto; margin-bottom: 20px;">' if logo_base64 else ''
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Inventory Summary</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 700px; width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td align="center" style="padding: 40px 20px 20px; background: linear-gradient(135deg, #1E293B 0%, #6C5CE7 100%); border-radius: 8px 8px 0 0;">
                                {logo_html}
                                <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">📊 Daily Inventory Summary</h1>
                                <p style="margin: 5px 0 0; color: #E2E8F0; font-size: 14px;">{timestamp}</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 30px; color: #334155; font-size: 15px; line-height: 1.6;">
                                    Here's your daily inventory summary for today:
                                </p>
                                
                                {f'<div style="background-color: #FEE2E2; border-left: 4px solid #EF4444; padding: 20px; margin: 20px 0; border-radius: 4px;"><h3 style="margin: 0 0 10px; color: #991B1B; font-size: 16px;">🚨 Low Stock Alerts: {len(low_stock)} products</h3><p style="margin: 0; color: #7F1D1D; font-size: 14px;">Please review and restock these items.</p></div>' if low_stock else ''}
                                
                                {f'<div style="background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 20px; margin: 20px 0; border-radius: 4px;"><h3 style="margin: 0 0 10px; color: #92400E; font-size: 16px;">⏰ Expiration Alerts: {len(expiring)} batches</h3><p style="margin: 0; color: #78350F; font-size: 14px;">Please prioritize selling or disposing these items.</p></div>' if expiring else ''}
                                
                                {f'<div style="background-color: #D1FAE5; border-left: 4px solid #10B981; padding: 20px; margin: 20px 0; border-radius: 4px;"><p style="margin: 0; color: #065F46; font-size: 14px;">✅ No critical alerts at this time. All inventory levels are healthy.</p></div>' if not low_stock and not expiring else ''}
                                
                                <p style="margin: 30px 0 0; color: #64748B; font-size: 13px;">
                                    Please review the full reports in the StockaDoodle system dashboard for detailed information.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-radius: 0 0 8px 8px;">
                                <p style="margin: 0 0 10px; color: #64748B; font-size: 12px; text-align: center; line-height: 1.5;">
                                    This is an automated daily summary from StockaDoodle Inventory Management System.<br>
                                    Generated on: <strong>{timestamp}</strong>
                                </p>
                                <p style="margin: 0; color: #94A3B8; font-size: 11px; text-align: center;">
                                    © {os.getenv('BRANCH_NAME', 'QuickMart')} - StockaDoodle IMS
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html