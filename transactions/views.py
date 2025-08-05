from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Transactions, Balance
from .forms import TransactionsForm


@login_required
def show_transactions(request):
    
    user = request.user
    userid = user.id

    transactions = Transactions.objects.filter(user = userid)
    # print("transactions:",transactions)

    context = {
        'transactions': transactions
    }
    return render(request, 'transactions/transactions.html', context)

@login_required
def deleteTransaction(request, pk):

    transactions = Transactions.objects.get(id=pk)
    if request.method == "POST":
           
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
