from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def calculate_emi(principal, rate, tenure):
    """Calculate EMI based on principal, annual interest rate, and tenure (in months)."""
    r = rate / (12 * 100)  
    emi = principal * r * ((1 + r) ** tenure) / (((1 + r) ** tenure) - 1)
    return round(emi, 2)


def calculate_credit_score(customer, loans):
    """Calculate a simple credit score based on customer debt and loan history."""
    if customer.current_debt > customer.approved_limit:
        return 0

    score = 0
    for loan in loans:
        if loan.emis_paid == loan.tenure:  
            score += 20
        if loan.start_date.year == timezone.now().year:  
            score += 10

    return min(score, 100)  


@api_view(['POST'])
def register(request):
    """Register a new customer."""
    data = request.data
    try:
        required_fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number']
        for field in required_fields:
            if field not in data:
                raise KeyError(field)

        first_name = data['first_name']
        last_name = data['last_name']
        age = data['age']
        monthly_income = data['monthly_income']
        phone_number = data['phone_number']
        approved_limit = round(36 * monthly_income / 100000) * 100000
        customer_id = Customer.objects.all().count() + 1
        customer = Customer.objects.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_income=monthly_income,
            phone_number=phone_number,
            approved_limit=approved_limit
        )

        response_data = {
            "customer_id": customer.customer_id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_income,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """Check loan eligibility for a customer."""
    data = request.data
    try:
        required_fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']
        for field in required_fields:
            if field not in data:
                raise KeyError(field)

        customer_id = data['customer_id']
        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        customer = Customer.objects.get(customer_id=customer_id)
        loans = Loan.objects.filter(customer=customer)

        credit_score = calculate_credit_score(customer, loans)

        if credit_score > 50:
            approved_interest_rate = interest_rate
        elif 30 < credit_score <= 50:
            approved_interest_rate = max(12, interest_rate)
        elif 10 < credit_score <= 30:
            approved_interest_rate = max(16, interest_rate)
        else:
            return Response({"approval": False, "message": "Credit score too low for loan approval."})

        emi = calculate_emi(loan_amount, approved_interest_rate, tenure)

        if emi > 0.5 * customer.monthly_income:
            return Response({"approval": False, "message": "EMI exceeds 50% of monthly income."})

        return Response({
            "customer_id": customer_id,
            "approval": True,
            "interest_rate": interest_rate,
            "corrected_interest_rate": approved_interest_rate,
            "tenure": tenure,
            "monthly_installment": emi
        }, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
    """Create a loan for a customer."""
    data = request.data
    try:
    
        required_fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']
        for field in required_fields:
            if field not in data:
                raise KeyError(field)

    
        customer_id = data['customer_id']
        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        
        customer = Customer.objects.get(customer_id=customer_id)

        
        loans = Loan.objects.filter(customer=customer)

        
        credit_score = calculate_credit_score(customer, loans)
        if credit_score <= 10:  
            return Response({"loan_approved": False, "message": "Credit score too low for loan approval."})

       
        approved_interest_rate = max(
            12, interest_rate) if credit_score <= 50 else interest_rate

   
        emi = calculate_emi(loan_amount, approved_interest_rate, tenure)

   
        if emi > 0.5 * customer.monthly_income:
            return Response({"loan_approved": False, "message": "EMI exceeds 50% of monthly income."})

  
        start_date = data.get('start_date', datetime.now().date())
        end_date = start_date + relativedelta(months=tenure)
        loan_id = Loan.objects.all().count() + 1
        loan = Loan.objects.create(
            loan_id=loan_id,
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=approved_interest_rate,
            tenure=tenure,
            monthly_installment=emi,
            start_date=start_date,
            end_date=end_date
        )

    
        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "monthly_installment": loan.monthly_installment
        }, status=status.HTTP_201_CREATED)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    """View details of a specific loan."""
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        customer = loan.customer

        return Response({
            "loan_id": loan.loan_id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "tenure": loan.tenure
        }, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_loans(request, customer_id):
    """View all loans for a specific customer."""
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        response_data = []

        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid
            response_data.append({
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })

        return Response(response_data, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
