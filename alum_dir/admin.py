from django.contrib import admin
# Register your models here.
from .models import Alum

class AlumAdmin(admin.ModelAdmin):
   fieldsets = [
                # ('Name',               {'fields': ['question_text']}),
#                ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
                ('First name', {'fields': ['first_name']}),
                ('Last name', {'fields': ['last_name']}),
                ('Email', {'fields': ['email']}),
                ('Current School', {'fields': ['school']}),
                ('Graduating class', {'fields': ['year']}),
                ]
                # list_display = ('question_text', 'pub_date', 'was_published_recently')
   list_display = ( 'email', 'last_name', 'first_name','school', 'year')
#                 list_filter = ['pub_date']
   search_fields = ['school']

admin.site.register(Alum, AlumAdmin)
