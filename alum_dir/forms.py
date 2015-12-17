from .models import UserProfile, Alum
from django.contrib.auth.models import User
from django import forms
# from haystack.forms import SearchForm

#
# BEGIN: Source for user profile
# Title: User Authentication
# Url: http://www.tangowithdjango.com/book/chapters/login.html
#

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())	

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name' ,'email')        


class UserProfileForm(forms.ModelForm):
	year = forms.CharField(label='Graduated year', required=False)
	school = forms.CharField(label='Current school', required=False)
	
	class Meta:
		model = UserProfile
		fields = ('year', 'school')                     

#
# END: Source for user profile
#
