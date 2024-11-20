# import_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from loan.models import Customer, Loan
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Imports customer and loan data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)

    def handle(self, *args, **options):
        # Read the Excel file
        excel_file = options['excel_file']
        df = pd.read_excel(excel_file)

        # Assuming the Excel file has 'customers' and 'loans' sheets
        customers_df = df['customer_data']  # Replace with your actual sheet name
        loans_df = df['loan_data']  # Replace with your actual sheet name

        # Import customer data
        for _, row in customers_df.iterrows():
            customer, created = Customer.objects.get_or_create(
                customer_id=row['customer_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                age=row['age'],
                monthly_income=row['monthly_income'],
                phone_number=row['phone_number'],
            )
            self.stdout.write(self.style.SUCCESS(f"Customer {row['first_name']} {row['last_name']} imported."))

        # Import loan data
        for _, row in loans_df.iterrows():
            customer = Customer.objects.get(customer_id=row['customer_id'])
            loan = Loan.objects.create(
                loan_id=row['loan_id'],
                customer=customer,
                loan_amount=row['loan_amount'],
                interest_rate=row['interest_rate'],
                monthly_installment=row['monthly_installment'],
                tenure=row['tenure'],
                emis_paid=row['emis_paid'],
                start_date=parse_date(row['start_date']),  # Make sure start_date is in the correct format
            )
            self.stdout.write(self.style.SUCCESS(f"Loan {row['loan_id']} imported."))

        self.stdout.write(self.style.SUCCESS('Data import completed.'))
