from django.shortcuts import render
from .models import Transaction

def home(request):
    transactions = Transaction.objects.all().order_by('-date')  # Get all transactions ordered by date
    return render(request, 'mails/index.html', {'transactions': transactions})
