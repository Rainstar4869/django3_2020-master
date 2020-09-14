from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('top/', views.index, name="expenses_top"),
    path('add_expense/', views.add_expense, name="add_expense"),
    path('', views.ExpenseListAPIView.as_view(), name="expenses"),
    path('search-expenses', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name="expense"),
    path('category_summary/', views.expense_category_summary, name="expense_category_summary"),

]
