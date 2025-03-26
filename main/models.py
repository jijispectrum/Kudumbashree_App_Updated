from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True, default=18)  # Default age
    address = models.TextField(null=True, blank=True)  # Allow empty addresses
    aadhar = models.CharField(max_length=12, unique=True)
    ration_card_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Allow optional phone numbers
    membership_status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], 
        default='Pending'
    )

class Loan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.FloatField()
    duration_months = models.IntegerField()
    interest_rate = models.FloatField()

    def __str__(self):
        return self.name  # This ensures the dropdown displays the loan name instead of "Loan object"


# # Loan Request Model (Admin Approval Required)
# class LoanRequest(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
#     document = models.FileField(upload_to='loan_docs/')
#     status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
# Loan Request Model (Now Includes Installment Tracking)
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, date

class LoanRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    document = models.FileField(upload_to='loan_docs/')
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], 
        default='Pending'
    )
    approved_date = models.DateField(null=True, blank=True)
    total_repaid = models.FloatField(default=0)
    next_due_date = models.DateField(null=True, blank=True)
    last_payment_date = models.DateField(null=True, blank=True)  # New field to track installment payment

    @property
    def remaining_balance(self):
        return max(self.loan.amount - self.total_repaid, 0)  # Prevents negative balance

    def set_initial_due_date(self):
        """ Sets the first installment due date (e.g., 10 days after approval). """
        if self.approved_date and not self.next_due_date:
            self.next_due_date = self.approved_date + timedelta(days=10)  # First due in 10 days
            self.save()

    def update_next_due_date(self):
        """ Updates the due date after each installment is paid. """
        if not self.next_due_date:
            self.set_initial_due_date()  # Ensure first due date is set
        else:
            self.next_due_date = self.next_due_date + timedelta(days=30)  # Move to next month
            self.last_payment_date = date.today()  # Record last installment payment
            self.save()


# Transaction Model (Admin controls deposits & withdrawals)
class Transaction(models.Model):
    TRANSACTION_TYPES = [('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User receiving the transaction
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='admin_transactions')  # Admin performing the transaction
    date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"

# Attendance Model (Admin Marks Attendance)
class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
