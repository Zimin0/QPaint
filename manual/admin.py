from django.contrib import admin
from .models import AssemblyCode, Constructor

@admin.register(AssemblyCode)
class AssemblyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'created', 'amount_of_usage']
    search_fields = ['code']
    list_filter = ['created']

@admin.register(Constructor)
class ConstructorAdmin(admin.ModelAdmin):
    list_display = ['manual_file', 'slug', 'picture', 'assemblycode']
    search_fields = ['slug', 'assemblycode__code']
    list_filter = ['manual_file']
    raw_id_fields = ['assemblycode'] 
    prepopulated_fields = {"slug": ("manual_file",)}
