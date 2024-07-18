from django.urls import path
from .views import list_accounts, import_accounts, accounts_details, transfer_funds

urlpatterns = [
    path('', list_accounts, name='list_accounts'),
    path('import/', import_accounts, name='import_accounts'),
    path('transfer/', transfer_funds, name='transfer_funds'),
    path('<str:pk>/', accounts_details, name='account_detail'),

]