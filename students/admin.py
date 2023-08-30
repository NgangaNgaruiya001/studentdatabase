from django.contrib import admin

# Register your models here.

from .models import Student

# admin.site.register(Student)

from import_export.admin import ImportExportModelAdmin

@admin.register(Student)


class ViewAdmin(ImportExportModelAdmin):
	pass
