from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Loan, LoanRequest, Transaction, Attendance, CustomUser
from .forms import CustomUserForm, LoanRequestForm
from django.contrib.auth.decorators import login_required

# User Registration (Membership Request)
def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.membership_status = 'Pending'  # Default status
            user.save()
            return redirect('registration_success')
    else:
        form = CustomUserForm()
    return render(request, 'register.html', {'form': form})
from django.contrib.auth import login, authenticate, logout
# Registration Success Page
def registration_success(request):
    return render(request, 'registration_success.html')
# User Login View (Django default authentication)
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.membership_status == "Approved":  # Check if admin approved
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "login.html", {"error": "Your membership is pending approval."})
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LoanRequest, Transaction, Attendance

@login_required
def dashboard(request):
    if request.user.membership_status != "Approved":
        return redirect("login")  # Only approved users can access

    transactions = Transaction.objects.filter(user=request.user)
    loan_requests = LoanRequest.objects.filter(user=request.user)  # Show only approved loans
    attendance = Attendance.objects.filter(user=request.user)
    
    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'loan_requests': loan_requests,
        'attendance': attendance
    })


# Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect("login")
@login_required
def loan_request(request):
    if request.method == "POST":
        form = LoanRequestForm(request.POST, request.FILES)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = request.user
            loan_request.save()
            return redirect('dashboard')
    else:
        form = LoanRequestForm()
    return render(request, 'loan_request.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, LoanRequest, Transaction, Attendance
from .forms import AdminTransactionForm

# Check if user is admin
def is_admin(user):
    return user.is_staff  # Admin users have is_staff = True

# Admin Dashboard View

# Admin Dashboard View
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_users = CustomUser.objects.filter(membership_status="Pending")
    pending_loans = LoanRequest.objects.filter(status="Pending")
    all_users = CustomUser.objects.filter(membership_status="Approved")
    transactions = Transaction.objects.all().order_by('-date')
    attendance_records = Attendance.objects.all()
    loan_repayments = LoanRequest.objects.filter(status="Approved")

    return render(request, 'admin_dashboard.html', {
        'pending_users': pending_users,
        'pending_loans': pending_loans,
        'all_users': all_users,
        'transactions': transactions,
        'attendance_records': attendance_records,
        'loan_repayments': loan_repayments
    })
# # Admin Approves Membership
@login_required
@user_passes_test(is_admin)
def approve_membership(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.membership_status = "Approved"
    user.save()
    return redirect('admin_dashboard')

# Admin Rejects Membership
@login_required
@user_passes_test(is_admin)
def reject_membership(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.membership_status = "Rejected"
    user.save()
    return redirect('admin_dashboard')


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LoanRequest
from datetime import timedelta, date
@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_loan(request, loan_id):
    """ Admin approves a loan and sets the first installment due date. """
    
    loan_request = get_object_or_404(LoanRequest, id=loan_id)

    if loan_request.status == "Pending":
        loan_request.status = "Approved"
        loan_request.approved_date = date.today()  # Set approval date
        loan_request.set_initial_due_date()  # Set the first due date
        loan_request.save()

    return redirect("admin_dashboard")

# Admin Rejects Loan
@login_required
@user_passes_test(is_admin)
def reject_loan(request, loan_id):
    loan_request = LoanRequest.objects.get(id=loan_id)
    loan_request.status = "Rejected"
    loan_request.save()
    return redirect('admin_dashboard')

# # Admin Marks Attendance
# @login_required
# @user_passes_test(is_admin)
# def mark_attendance(request, user_id, status):
#     user = CustomUser.objects.get(id=user_id)
#     Attendance.objects.create(user=user, status=status)
#     return redirect('admin_dashboard')

from django.shortcuts import get_object_or_404, redirect, render
from .models import CustomUser, Attendance
from datetime import datetime

def mark_attendance(request, user_id, status):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Get selected date from request or default to today
    date_str = request.GET.get('date', None)
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = datetime.today().date()

    # Mark attendance (update if exists)
    attendance, created = Attendance.objects.get_or_create(
        user=user, date=selected_date, defaults={'status': status}
    )
    if not created:
        attendance.status = status
        attendance.save()
    
    return redirect('admin_dashboard')  # Redirect to admin dashboard after marking


# Admin Adds Transactions
@login_required
@user_passes_test(is_admin)
def admin_add_transaction(request):
    if request.method == "POST":
        form = AdminTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.admin = request.user
            transaction.save()
            return redirect('admin_dashboard')
    else:
        form = AdminTransactionForm()
    return render(request, 'admin_add_transaction.html', {'form': form})


# Admin View: All User Transactions
@login_required
@user_passes_test(is_admin)
def admin_transaction_history(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'admin_transaction_history.html', {'transactions': transactions})

# User View: Only Their Own Transactions
@login_required
def user_transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'user_transaction_history.html', {'transactions': transactions})
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .forms import LoanRepaymentForm  # Create this form

# Check if user is admin
def is_admin(user):
    return user.is_staff


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date
from .models import LoanRequest
from .forms import LoanRepaymentForm

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_loan_repayment(request, loan_id):
    """ Admin updates the repayment details and can delete the loan if needed. """

    loan_request = get_object_or_404(LoanRequest, id=loan_id)

    if request.method == "POST":
        if "delete_loan" in request.POST:
            # Admin chooses to delete the loan
            loan_request.delete()
            messages.success(request, "Loan successfully deleted.")
            return redirect('admin_dashboard')

        form = LoanRepaymentForm(request.POST)
        if form.is_valid():
            installment = form.cleaned_data['installment_amount']
            new_due_date = form.cleaned_data['next_due_date']
            payment_date = form.cleaned_data['last_payment_date']

            # Update total repaid amount
            loan_request.total_repaid += installment
            
            # Update next due date
            loan_request.next_due_date = new_due_date if new_due_date else loan_request.update_next_due_date()

            # Update last payment date
            loan_request.last_payment_date = payment_date if payment_date else date.today()

            loan_request.save()
            messages.success(request, "Loan repayment details updated successfully.")
            return redirect('admin_dashboard')

    else:
        form = LoanRepaymentForm(initial={
            'installment_amount': 0, 
            'next_due_date': loan_request.next_due_date,
            'last_payment_date': loan_request.last_payment_date
        })

    return render(request, 'update_loan_repayment.html', {
        'form': form,
        'loan_request': loan_request
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser

# Ensure only admins can approve members
def is_admin(user):
    return user.is_staff
from .forms import CustomUserEditForm
@login_required
@user_passes_test(is_admin)
def verify_and_edit_member(request, user_id):
    """ Admin verifies user details, edits them if needed, and approves membership. """
    
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            action = request.POST.get("action")
            if action == "approve":
                user.membership_status = "Approved"
            elif action == "reject":
                user.membership_status = "Rejected"
            user.save()
            return redirect("admin_dashboard")

    else:
        form = CustomUserEditForm(instance=user)

    return render(request, "verify_and_edit_member.html", {"form": form, "user": user})

from django.shortcuts import render
from .models import Transaction

def admin_transactions(request):
    transactions = Transaction.objects.all().order_by("-date")  # Show latest first
    return render(request, "admin_transactions.html", {"transactions": transactions})
from django.shortcuts import render
from .models import Attendance

def admin_attendance(request):
    attendance_records = Attendance.objects.all().order_by("-date")  # Latest records first
    return render(request, "admin_attendance.html", {"attendance_records": attendance_records})
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Ensure user is an admin
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to the admin dashboard
        else:
            messages.error(request, "Invalid credentials or insufficient privileges.")

    return render(request, "admin_login.html")
