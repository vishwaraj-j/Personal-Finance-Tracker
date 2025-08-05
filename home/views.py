from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from transactions.models import Transactions, Balance
from django.db.models import Sum
from datetime import date, timedelta



@login_required
def home(request):
    user = request.user
    username = user.username
    userid = user.id

    total_income = Transactions.objects.filter(user = userid).filter(transaction_type='Incoming').aggregate(Sum('amount'))
    total_expenses = Transactions.objects.filter(user = userid).filter(transaction_type='Outgoing').aggregate(Sum('amount'))
    # transactions = Transactions.objects.filter(user = userid)
    # for item in range(len(transactions)):

    today = date.today()
    recent_transactions_date = today - timedelta(days=7)
    # print(recent_transactions_date)
    recent_transactions = Transactions.objects.filter(user = userid).filter(transaction_timestamp__gt=recent_transactions_date)

    balance_to_show = Balance.objects.get_or_create(
                user = userid,
                defaults = {'balance': 0}
            )
    balance = balance_to_show[0].amount
    # print("Balance:",balance_to_show[0].amount)


    context = {
        'username': username,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'recent_transactions': recent_transactions,
        'balance': balance
    }

    return render(request, 'home/home.html', context)

