from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Transactions
from .forms import TransactionsForm


@login_required
def show_transactions(request):
    
    user = request.user
    userid = user.id

    transactions = Transactions.objects.filter(user = userid)
    print("transactions:",transactions)

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


def createTransaction(request):

    form = TransactionsForm()
    if request.method == 'POST':
        print("POST:", request.POST)
        form = TransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/transactions')


    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)
