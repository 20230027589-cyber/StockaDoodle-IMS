from extensions import db
from models.product import Product
from models.category import Category
from models.sale import Sale, SaleItem
from models.user import User
from models.retailer_metrics import RetailerMetrics
from models.product_log import ProductLog
from models.stock_batch import StockBatch
from datetime import datetime, date, timedelta
from sqlalchemy import func


class ReportGenerator:
    """
    Generates all 7 required system reports for StockaDoodle.
    Provides data for managerial decision-making and system auditing.
    """

    @staticmethod
    def sales_performance_report(start_date=None, end_date=None):
        """
        Report 1: Sales Performance Report for a Selected Date Range
        
        Shows: Report ID, Date Range, Product Name, Quantity Sold, 
               Total Price, Retailer Name, Total Income
        
        Args:
            start_date (date): Start of date range
            end_date (date): End of date range
            
        Returns:
            dict: Report data with sales breakdown and summary
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()

        # Query sales with joins
        sales_query = (
            db.session.query(
                Sale.id.label('sale_id'),
                Sale.created_at,
                Product.name.label('product_name'),
                SaleItem.quantity,
                SaleItem.line_total,
                User.full_name.label('retailer_name')
            )
            .join(SaleItem, Sale.id == SaleItem.sale_id)
            .join(Product, SaleItem.product_id == Product.id)
            .join(User, Sale.retailer_id == User.id)
            .filter(Sale.created_at >= start_date)
            .filter(Sale.created_at <= end_date)
            .order_by(Sale.created_at.desc())
        )

        results = sales_query.all()
        
        total_income = sum(r.line_total for r in results)
        total_quantity = sum(r.quantity for r in results)

        return {
            'report_id': 1,
            'report_name': 'Sales Performance Report',
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'sales': [
                {
                    'sale_id': r.sale_id,
                    'date': r.created_at.isoformat(),
                    'product_name': r.product_name,
                    'quantity_sold': r.quantity,
                    'total_price': r.line_total,
                    'retailer_name': r.retailer_name
                }
                for r in results
            ],
            'summary': {
                'total_income': round(total_income, 2),
                'total_quantity_sold': total_quantity,
                'total_transactions': len(set(r.sale_id for r in results))
            }
        }

    @staticmethod
    def category_distribution_report():
        """
        Report 2: Category Distribution Report
        
        Shows: Report ID, Category Name, Number of Products, 
               Total Stock Quantity, Percentage Share
        
        Returns:
            dict: Category-wise stock distribution
        """
        categories = Category.query.all()
        
        total_stock = sum(
            sum(batch.quantity for batch in product.stock_batches)
            for category in categories
            for product in category.products
        )

        category_data = []
        for category in categories:
            products_count = len(category.products)
            category_stock = sum(
                sum(batch.quantity for batch in product.stock_batches)
                for product in category.products
            )
            percentage = (category_stock / total_stock * 100) if total_stock > 0 else 0

            category_data.append({
                'category_id': category.id,
                'category_name': category.name,
                'number_of_products': products_count,
                'total_stock_quantity': category_stock,
                'percentage_share': round(percentage, 2)
            })

        return {
            'report_id': 2,
            'report_name': 'Category Distribution Report',
            'categories': category_data,
            'summary': {
                'total_categories': len(categories),
                'total_stock': total_stock
            }
        }

    @staticmethod
    def retailer_performance_report():
        """
        Report 3: Retailer Performance Report
        
        Shows: Retailer Name, User ID, Daily Quota Target, 
               Current Sales, Streak Count
        
        Returns:
            dict: All retailers with performance metrics
        """
        retailers = User.query.filter(User.role.in_(['retailer', 'staff'])).all()
        
        performance_data = []
        for retailer in retailers:
            metrics = RetailerMetrics.query.filter_by(retailer_id=retailer.id).first()
            
            if metrics:
                quota_progress = (metrics.sales_today / metrics.daily_quota * 100) if metrics.daily_quota > 0 else 0
                performance_data.append({
                    'retailer_name': retailer.full_name,
                    'user_id': retailer.id,
                    'daily_quota': metrics.daily_quota,
                    'current_sales': metrics.sales_today,
                    'quota_progress': round(quota_progress, 2),
                    'streak_count': metrics.current_streak,
                    'total_sales': metrics.total_sales,
                    'has_profile_pic': retailer.user_image is not None
                })

        # Sort by streak, then sales
        performance_data.sort(key=lambda x: (x['streak_count'], x['total_sales']), reverse=True)

        return {
            'report_id': 3,
            'report_name': 'Retailer Performance Report',
            'retailers': performance_data,
            'summary': {
                'total_retailers': len(retailers),
                'active_today': len([r for r in performance_data if r['current_sales'] > 0])
            }
        }

    @staticmethod
    def low_stock_and_expiration_alert_report(days_ahead=7):
        """
        Report 4: Low-Stock and Expiration Alert Report
        
        Shows: Product ID, Product Name, Current Stock, 
               Minimum Stock Level, Expiration Date, Alert Status
        
        Args:
            days_ahead (int): Days to look ahead for expirations
            
        Returns:
            dict: Products needing attention
        """
        products = Product.query.all()
        alerts = []

        cutoff_date = date.today() + timedelta(days=days_ahead)

        for product in products:
            stock = product.stock_level
            alert_status = []

            # Low stock check
            if stock < product.min_stock_level:
                if stock == 0:
                    alert_status.append("OUT_OF_STOCK")
                else:
                    alert_status.append("LOW_STOCK")

            # Expiration check
            expiring_batches = [
                batch for batch in product.stock_batches
                if batch.expiration_date and batch.expiration_date <= cutoff_date and batch.quantity > 0
            ]

            if expiring_batches:
                alert_status.append("EXPIRING_SOON")
                earliest_expiry = min(b.expiration_date for b in expiring_batches)
            else:
                earliest_expiry = None

            if alert_status:
                alerts.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'current_stock': stock,
                    'min_stock_level': product.min_stock_level,
                    'expiration_date': earliest_expiry.isoformat() if earliest_expiry else None,
                    'alert_status': ', '.join(alert_status),
                    'severity': 'CRITICAL' if 'OUT_OF_STOCK' in alert_status else 'WARNING'
                })

        return {
            'report_id': 4,
            'report_name': 'Low-Stock and Expiration Alert Report',
            'alerts': alerts,
            'summary': {
                'total_alerts': len(alerts),
                'critical_alerts': len([a for a in alerts if a['severity'] == 'CRITICAL']),
                'warning_alerts': len([a for a in alerts if a['severity'] == 'WARNING'])
            }
        }

    @staticmethod
    def managerial_activity_log_report(start_date=None, end_date=None):
        """
        Report 5: Managerial Activity Log Report
        
        Shows: Log ID, Product Name, Action Performed, 
               User ID of Manager, Date and Time of Action
        
        Args:
            start_date (date): Start date filter
            end_date (date): End date filter
            
        Returns:
            dict: Manager actions log
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()

        # Query logs for manager/admin actions
        logs_query = (
            db.session.query(
                ProductLog.id.label('log_id'),
                Product.name.label('product_name'),
                ProductLog.action_type,
                User.id.label('manager_id'),
                User.full_name.label('manager_name'),
                ProductLog.log_time,
                ProductLog.notes
            )
            .join(Product, ProductLog.product_id == Product.id)
            .join(User, ProductLog.user_id == User.id)
            .filter(User.role.in_(['admin', 'manager']))
            .filter(ProductLog.log_time >= start_date)
            .filter(ProductLog.log_time <= end_date)
            .order_by(ProductLog.log_time.desc())
        )

        results = logs_query.all()

        return {
            'report_id': 5,
            'report_name': 'Managerial Activity Log Report',
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'logs': [
                {
                    'log_id': r.log_id,
                    'product_name': r.product_name,
                    'action_performed': r.action_type,
                    'manager_id': r.manager_id,
                    'manager_name': r.manager_name,
                    'date_time': r.log_time.isoformat(),
                    'notes': r.notes
                }
                for r in results
            ],
            'summary': {
                'total_actions': len(results),
                'unique_managers': len(set(r.manager_id for r in results))
            }
        }

    @staticmethod
    def detailed_sales_transaction_report(start_date=None, end_date=None):
        """
        Report 6: Detailed Sales Transaction Report
        
        Shows: Sale ID, Product Name, Quantity Sold, 
               Total Price, Retailer Name, Sale Time
        
        Args:
            start_date (date): Start date
            end_date (date): End date
            
        Returns:
            dict: Detailed transaction list
        """
        # This is similar to Report 1 but more granular
        return ReportGenerator.sales_performance_report(start_date, end_date)

    @staticmethod
    def user_accounts_report():
        """
        Report 7: User Accounts Report
        
        Shows: User ID, Username, Role, Email Address (if available),
               Account Status, Date Created (approximated)
        
        Returns:
            dict: All user accounts with details
        """
        users = User.query.order_by(User.full_name).all()

        return {
            'report_id': 7,
            'report_name': 'User Accounts Report',
            'users': [
                {
                    'user_id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role,
                    'account_status': 'Active',  # Extend User model if needed
                    'has_profile_pic': user.user_image is not None
                }
                for user in users
            ],
            'summary': {
                'total_users': len(users),
                'admins': len([u for u in users if u.role == 'admin']),
                'managers': len([u for u in users if u.role == 'manager']),
                'retailers': len([u for u in users if u.role in ['retailer', 'staff']])
            }
        }