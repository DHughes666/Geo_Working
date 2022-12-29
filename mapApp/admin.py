from django.contrib import admin
from .models import Search

# Register your models here.
class SearchAdmin(admin.ModelAdmin):
    list_display = ['address', 'date']

admin.site.register(Search, SearchAdmin)