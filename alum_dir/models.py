from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Alum(models.Model):

    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.email

    first_name.short_description = 'First name'
    last_name.short_description = 'Last name'
    school.short_description = 'Current school'
    year.short_description = 'Graduating year'


    def update(self, userProfile):
        self.email = userProfile.user.email
        self.first_name = userProfile.user.first_name
        self.last_name = userProfile.user.last_name
        self.school = userProfile.school
        self.year = userProfile.year        
        self.save()

#
# BEGIN: Source for user profile
# Title: User Authentication
# Url: http://www.tangowithdjango.com/book/chapters/login.html
#

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    school = models.CharField(max_length=200)
    year = models.CharField(max_length=200)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

#
# END: Source for user profile
#