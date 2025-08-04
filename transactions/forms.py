from django.forms import ModelForm
from .models import Transactions

class TransactionsForm(ModelForm):
    class Meta:
        model = Transactions
        # fields = ['user','category']
        fields = '__all__'