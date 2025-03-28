from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, LoanRequest

# User Registration Form (Membership Request)
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'age', 'address', 'aadhar', 'ration_card_number', 'phone_number']

from django import forms
from .models import LoanRequest, Loan

class LoanRequestForm(forms.ModelForm):
    loan = forms.ModelChoiceField(
        queryset=Loan.objects.all(),
        label="Select Loan Type",
        empty_label="Select a Loan",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LoanRequest
        fields = ['loan', 'document']

from django import forms
from .models import Transaction

from django import forms
from .models import Transaction, CustomUser

class AdminTransactionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(membership_status="Approved"), label="Select User")

    class Meta:
        model = Transaction
        fields = ['user', 'transaction_type', 'amount']
from django import forms
from .models import LoanRequest

from django import forms
from .models import LoanRequest

from django import forms
from .models import LoanRequest

from django import forms
from .models import LoanRequest

class LoanRepaymentForm(forms.ModelForm):
    installment_amount = forms.FloatField(label="Installment Amount", min_value=1, required=True)
    next_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    last_payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = LoanRequest
        fields = ['installment_amount', 'next_due_date', 'last_payment_date']
from django import forms
from .models import CustomUser
from django import forms
from .models import CustomUser

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "address", "aadhar", "ration_card_number", "profile_picture"]
