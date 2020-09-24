from django.contrib import admin
from .models import School, Student


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age")


admin.site.register(School)
admin.site.register(Student, StudentAdmin)
