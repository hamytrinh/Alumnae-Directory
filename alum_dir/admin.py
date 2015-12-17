from django.contrib import admin
# Register your models here.
from .models import Alum

class AlumAdmin(admin.ModelAdmin):
   fieldsets = [                
                ('First name', {'fields': ['first_name']}),
                ('Last name', {'fields': ['last_name']}),
                ('Email', {'fields': ['email']}),
                ('Current School', {'fields': ['school']}),
                ('Graduating class', {'fields': ['year']}),
                ]                
   list_display = ( 'email', 'last_name', 'first_name','school', 'year')
   search_fields = ['school']

admin.site.register(Alum, AlumAdmin)
