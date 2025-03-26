from django.contrib import admin
from .models import CustomUser, Transaction, Loan, LoanRequest, Attendance

# Custom User Admin Panel
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'aadhar', 'membership_status', 'is_staff')
    search_fields = ('username', 'email', 'phone_number', 'aadhar')
    list_filter = ('membership_status', 'is_staff')

# Transaction Admin Panel
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'transaction_type', 'amount')
    search_fields = ('user__username', 'transaction_type')
    list_filter = ('transaction_type', 'date')

# Loan Admin Panel
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'duration_months', 'interest_rate')
    search_fields = ('name',)
    list_filter = ('duration_months', 'interest_rate')

# Loan Request Admin Panel (Admin can approve/reject here)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'loan', 'status', 'document')
    search_fields = ('user__username', 'loan__name', 'status')
    list_filter = ('status',)

# Attendance Admin Panel (Admin can mark attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'status')
    search_fields = ('user__username',)
    list_filter = ('date', 'status')

# Register Models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)
admin.site.register(Attendance, AttendanceAdmin)
