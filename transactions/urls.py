from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_transactions, name='show-transactions'),
    # path('transactions/', include('transactions.urls')),
    path('delete_transaction/<str:pk>/', views.deleteTransaction, name='delete_transaction'),
    path('create_Transaction/', views.createTransaction, name="create_transaction"),
    path('update_Transaction/<str:pk>/', views.updateTransaction, name="update_transaction"),
    path('set_budget/', views.setBudget, name="set_budget"),
    path('redirect_home/', views.redirect_home, name="redirect_home"),
    path('export/', views.export, name="export")
]