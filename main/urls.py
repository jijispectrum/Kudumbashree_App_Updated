from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loan-request/', views.loan_request, name='loan_request'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('admin-add-transaction/', views.admin_add_transaction, name='admin_add_transaction'),
    path('admin/transaction-history/', views.admin_transaction_history, name='admin_transaction_history'),
    path('user/transaction-history/', views.user_transaction_history, name='user_transaction_history'),
    path('update-loan-repayment/<int:loan_id>/', views.update_loan_repayment, name='update_loan_repayment'),
    path('verify-edit-member/<int:user_id>/', views.verify_and_edit_member, name='verify_and_edit_member'),
    path("admin-transactions/", views.admin_transactions, name="admin_transactions"),
    path("admin_attendance/", views.admin_attendance, name="admin_attendance"),
    path("admin-login/", views.admin_login, name="admin_login"),
    





    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-membership/<int:user_id>/', views.approve_membership, name='approve_membership'),
    path('reject-membership/<int:user_id>/', views.reject_membership, name='reject_membership'),
    path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('reject-loan/<int:loan_id>/', views.reject_loan, name='reject_loan'),
    path('mark-attendance/<int:user_id>/<str:status>/', views.mark_attendance, name='mark_attendance'),

]
