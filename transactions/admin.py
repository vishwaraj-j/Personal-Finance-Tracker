from django.contrib import admin
from .models import Categories, Transactions, Balance, Budget
from django.contrib import admin

class BalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "amount")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user","transaction_type", "transaction_timestamp", "created_at", "amount", "category")
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(Categories)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Budget)

