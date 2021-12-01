from django.contrib import admin

# Register your models here.
from home.models import Company, Employee, Card, Transaction, Restaurant, Refund


# class CardInline(admin.StackedInline):
#     model = Card
#     # readonly_fields = ["balance"]
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["employee", 'balance']
    # readonly_fields = ["balance"]
    class Meta:
        model = Card

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", 'balance', 'created_at']

    class Meta:
        model = Company

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [ "name", 'surname', 'company']
    class Meta:
        model = Employee

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [ "name","balance"]
    class Meta:
        model = Restaurant

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = [ "transaction","created_at"]
    class Meta:
        model = Refund

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [ "card", 'transaction_type', 'amount']
    list_filter = ['transaction_type']
    readonly_fields = ["is_success","status_message"]

    class Meta:
        model = Transaction



