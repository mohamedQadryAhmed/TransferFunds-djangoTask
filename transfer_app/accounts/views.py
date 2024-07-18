from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Account
import csv
import io
from decimal import Decimal

# Create your views here.

def import_accounts(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        # Ensure the file is read as a string
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Please upload a valid CSV file.")

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        reader = csv.reader(io_string, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            Account.objects.create(id=row[0], name=row[1], balance=row[2])

        return HttpResponse("Accounts imported successfully")
    return render(request, 'accounts/import.html')
def list_accounts(request):
    accounts = Account.objects.all()
    transfer_success = request.session.pop('transfer_success', False)  # Get and remove success flag from session
    return render(request, 'accounts/list.html', {'accounts': accounts, 'transfer_success': transfer_success})
def accounts_details(request, pk):
    account = get_object_or_404(Account , pk=pk)
    return render(request, 'accounts/details.html', {'account': account})




def transfer_funds(request):
    if request.method == 'POST':
        from_account_id = request.POST['from_account']
        to_account_id = request.POST['to_account']
        amount = Decimal(request.POST['amount'])  # Convert to Decimal

        # Check if from_account and to_account are the same
        if from_account_id == to_account_id:
            error_message = "You cannot transfer funds to the same account."
            accounts = Account.objects.all()
            return render(request, 'accounts/transfer.html', {'accounts': accounts, 'error_message': error_message})

        from_account = get_object_or_404(Account, pk=from_account_id)
        to_account = get_object_or_404(Account, pk=to_account_id)

        # Check if the transfer amount exceeds the balance
        if from_account.balance < amount:
            error_message = "Insufficient funds in the source account."
            accounts = Account.objects.all()
            return render(request, 'accounts/transfer.html',
                          {'accounts': accounts, 'error_message': error_message, 'from_account': from_account})

        try:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            request.session['transfer_success'] = True  # Set success message in session
            return redirect('list_accounts')
        except ValueError as e:
            return HttpResponse(str(e))
    else:
        from_account_id = request.GET.get('from_account')
        from_account = None
        if from_account_id:
            from_account = get_object_or_404(Account, pk=from_account_id)
        accounts = Account.objects.all()
        return render(request, 'accounts/transfer.html', {'accounts': accounts, 'from_account': from_account})
