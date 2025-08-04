from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_transactions, name='show-transactions'),
    # path('transactions/', include('transactions.urls')),
    path('delete_transaction/<str:pk>/', views.deleteTransaction, name='delete_transaction'),
    path('create_Transaction/', views.createTransaction, name="create_transaction")
]