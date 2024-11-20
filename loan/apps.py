from django.apps import AppConfig
from django.conf import settings
import os


class LoanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loan'

    def ready(self):
        # File paths for customer and loan data
        base_dir = settings.BASE_DIR
        customer_file_path = os.path.join(base_dir, "customer_data.xlsx")
        loan_file_path = os.path.join(base_dir, "loan_data.xlsx")

        # Import the data
        from .utils import import_customer_and_loan_data
        import_customer_and_loan_data(customer_file_path, loan_file_path)
