import pandas as pd
from loan.models import Customer, Loan
import os


def import_customer_and_loan_data(customer_file_path, loan_file_path):
    if not os.path.exists(customer_file_path):
        print(f"Customer file not found: {customer_file_path}")
    else:
        try:
            customer_data = pd.read_excel(customer_file_path)
            for _, row in customer_data.iterrows():
                Customer.objects.update_or_create(
                    customer_id=row['customer_id'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'age': row['age'],
                        'monthly_income': row['monthly_income'],
                        'phone_number': row['phone_number'],
                        'approved_limit': row['approved_limit'],
                    },
                )
            print("Customer data imported successfully.")
        except Exception as e:
            print(f"Error importing customer data: {e}")

    if not os.path.exists(loan_file_path):
        print(f"Loan file not found: {loan_file_path}")
    else:
        try:
            loan_data = pd.read_excel(loan_file_path)
            for _, row in loan_data.iterrows():
                try:
                    customer_instance = Customer.objects.get(customer_id=row['customer_id'])
                    Loan.objects.create(
                        customer=customer_instance,
                        loan_amount=row['loan_amount'],
                        interest_rate=row['interest_rate'],
                        tenure=row['tenure'],
                        monthly_installment=row['monthly_installment'],
                        emis_paid=row['emis_paid'],
                        start_date=row['start_date'],
                        end_date=row['end_date'],
                    )
                except Customer.DoesNotExist:
                    print(f"Customer with ID {row['customer_id']} does not exist. Skipping loan creation.")
            print("Loan data imported successfully.")
        except Exception as e:
            print(f"Error importing loan data: {e}")
