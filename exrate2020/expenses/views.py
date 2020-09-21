import csv
import xlwt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.generic import ListView
from .serializers import ExpenseSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner
import datetime
import json
import logging
import tempfile
from weasyprint import HTML

logger = logging.getLogger("error_logger")


def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline;attachment;filename=Expenses" + str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = "binary"

    expenses = Expense.objects.filter(owner=request.user)
    expenses_sum = expenses.aggregate(Sum("amount"))

    html_string = render_to_string("expenses/output_pdf.html", {
        "expenses": expenses,
        "total": expenses_sum
    })

    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = "attachment;filename=Expenses" + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(["Amount", "Description", "Category", "Date"])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response["Content-Disposition"] = "attachment;filename=Expenses" + str(datetime.datetime.now()) + '.xls'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("Expense")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["Amount", "Description", "Category", "Date"]

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list("amount", "description", "category", "date")

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), font_style)

    workbook.save(response)
    return response


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


@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class ExpenseListView(ListView):
    model = Expense
    context_object_name = "expenses"
    template_name = "expenses/index.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', self.paginate_by)


# def index(request):
# logger.error("hello django???")
#
# page_number = request.GET.get('page', 1)
# per_page = request.GET.get('per_page', 10)
# expenses = Expense.objects.filter(owner=request.user)
# paginator = Paginator(expenses, per_page)
# page_obj = Paginator.get_page(paginator, page_number)
# # currency = UserPreference.objects.get(user=request.user).currency
# context = {
#     'expenses': expenses,
#     'page_obj': page_obj,
#     "per_page": per_page
# }
# return render(request, 'expenses/index.html', context)


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
