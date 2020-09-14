from django.urls import path

from . import views

urlpatterns = [
    path("expense_summary/", views.ExpenseSummaryStats.as_view(), name="expense_summary"),
    path("income_summary/", views.IncomeSummaryStats.as_view(), name="income_summary"),
]
