from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Transactions, Balance, Budget
from .forms import TransactionsForm, BudgetForm
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.http import HttpResponse
import csv

@login_required
def show_transactions(request):
    
    user = request.user
    userid = user.id

    transactions = Transactions.objects.filter(user = userid)
    paginator = Paginator(transactions, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print("transactions:",transactions)

    # context = {
    #     'transactions': transactions
    # }

    context = {
       "page_obj": page_obj 
    }


    return render(request, 'transactions/transactions.html', context)

@login_required
def deleteTransaction(request, pk):

    transactions = Transactions.objects.get(id=pk)
    if request.method == "POST":
        
        user = request.user
        userid = user.id
        balance_to_update = Balance.objects.get_or_create(
            user = userid,
            defaults = {'balance': 0}
        )


        if transactions.transaction_type == 'Incoming':
                balance_to_update_value = balance_to_update[0].amount - transactions.amount
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()

        if transactions.transaction_type == 'Outgoing':
                balance_to_update_value = balance_to_update[0].amount + transactions.amount
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()


        transactions.delete()

        return redirect('/transactions/')

    context = {
        'transactions': transactions
    }

    return render(request, 'transactions/delete.html', context)


@login_required
def createTransaction(request):
 
    if request.method == 'POST':
        # print("POST:", request.POST)
        form = TransactionsForm(request.POST)
        if form.is_valid():
            print("Form is Valid")
            transactions = form.save(commit=False)
            transactions.user = request.user
            print("transactions:", transactions)
            form.save()

            user = request.user
            userid = user.id
            balance_to_update = Balance.objects.get_or_create(
                user = userid,
                defaults = {'balance': 0}
            )
            # print("balance:",balance_to_update[0].amount)
            # print("balance_type",type(balance_to_update))

            if transactions.transaction_type == 'Incoming':
                balance_to_update_value = balance_to_update[0].amount + transactions.amount
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()

            if transactions.transaction_type == 'Outgoing':
                balance_to_update_value = balance_to_update[0].amount - transactions.amount
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()

            return redirect('show-transactions')
        else:
            print("Form errors", form.errors)
    else:
        print("Form is invalid")
        form = TransactionsForm()

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


@login_required
def updateTransaction(request, pk):


    transactions = Transactions.objects.get(id=pk)
    old_transactions = transactions.amount
    print("old_transaction: ",old_transactions)
    # form = TransactionsForm(instance=transactions)

    if request.method == 'POST':
        # print("POST:", request.POST)
        form = TransactionsForm(request.POST, instance=transactions)
        if form.is_valid():
            print("Form is Valid")
            transactions = form.save(commit=False)
            transactions.user = request.user
            form.save()


            user = request.user
            userid = user.id
            balance_to_update = Balance.objects.get_or_create(
                user = userid,
                defaults = {'balance': 0}
            )
            # print("balance:",balance_to_update[0].amount)
            # print("balance_type",type(balance_to_update))

            if transactions.transaction_type == 'Incoming':
                balance_to_update_value = (balance_to_update[0].amount - old_transactions) + transactions.amount 
                print("old_transaction: ",old_transactions)
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()

            if transactions.transaction_type == 'Outgoing':
                balance_to_update_value = (balance_to_update[0].amount + old_transactions) - transactions.amount
                print ("updated balance:",balance_to_update_value)
                print("type: ", type(balance_to_update_value))
                balance_to_update[0].amount = balance_to_update_value
                balance_to_update[0].save()

            return redirect('show-transactions')
        else:
            print("Form errors", form.errors)
    else:
        print("Form is invalid")
        form = TransactionsForm(instance=transactions)

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)

@login_required
def setBudget(request):

    user = request.user
    userid = user.id

    today = date.today()
    today_str = str(today)
    year_month = today_str[0:4] + today_str[5:7]
    print(year_month)

    form = BudgetForm(request.POST)

    budget_to_update = Budget.objects.get_or_create(
        user_id = userid,
        month_year = year_month
    )
    
    # print("form:",form)

    if form.is_valid():
        print("Form is Valid")
        # budget_form = form.save(commit=False)
        budget_value = form.cleaned_data['amount']
        budget_to_update[0].amount = budget_value
        budget_to_update[0].save()
        return redirect('show-transactions')
    else:
        print("Form errors", form.errors)

    context = {
        'form': form
    }

    return render(request, 'transactions/budget.html', context)

@login_required
def export(request):

    user = request.user
    userid = user.id

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['transaction_type','transaction_timestamp','amount','category'])
    # for transaction in Transactions.objects.all():
    #     writer.writerow(transaction)

    transactions = Transactions.objects.select_related('category').filter(user = userid).values_list('transaction_type','transaction_timestamp','amount','category__name')
    # print(type(transactions))

    for transaction in transactions:  
        # print(transaction)
        writer.writerow(transaction)

    response['Content-Disposition'] = 'attachement; filename="transactions.csv"'

    return response



@login_required
def redirect_home(request):
    return redirect('home')