from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner
import datetime
import json


@login_required(login_url='/webauth/login/')
def add_expense(request):
    return render(request, "expenses/add_expense.html")


def expense_category_summary(request):
    def get_amount_for_category(expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        # count = 0

        for expense in expenses:
            amount += expense.amount
            # count += 1

        return str(amount)
        # return {"amount": str(amount), "count": count}

    def get_category(expense):
        return expense.category

    today_date = datetime.date.today()
    ayear_ago = today_date - datetime.timedelta(days=30 * 12)

    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=ayear_ago, date__lte=today_date)

    final = {}

    categories = list(set(map(get_category, expenses)))
    for _category in categories:
        final[_category] = get_amount_for_category(expenses, _category)

    return JsonResponse({
        "expense_category_data": final,
        "user": str(request.user)
    }, safe=False)


@login_required(login_url='/webauth/login/')
def index(request):
    # categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        # 'currency': currency
    }
    return render(request, 'expenses/index.html', context)


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__startswith=search_str, owner=request.user) | \
                   Expense.objects.filter(date__startswith=search_str, owner=request.user) | \
                   Expense.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Expense.objects.filter(category__icontains=search_str, owner=request.user)
        data = expenses.values()

        # return JsonResponse({"search_str": json.loads(request.body)}, safe=False)
        return JsonResponse(list(data), safe=False)


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Expense.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
