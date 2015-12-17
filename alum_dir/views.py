from django.shortcuts import render
from .models import Alum
from .models import UserProfile
from .forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseRedirect
import re
from django.db.models import Q

# Create your views here.
def index(request):
    alum_list = Alum.objects.order_by('-last_name')[:5]
    context = {'alum_list': alum_list}
    return render(request, 'alum_dir/index.html', context)

#
# BEGIN: Source for search functions
# Author: Julien Phalip
# Title: Adding search to a Django site in a snap
# Url: http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
#

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['school',])
        
        found_entries = Alum.objects.filter(entry_query).order_by('-last_name')

    return render_to_response('alum_dir/search.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

#
# END: Source for search functions
#

#
# BEGIN: Source for 3 functions: register, user_login, and user_logout
# Title: User Authentication
# Url: http://www.tangowithdjango.com/book/chapters/login.html
#

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            alum = Alum.objects.create()            
            alum.update(profile)        
            alum.save()    

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'alum_dir/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)        


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/alum_dir/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            # print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")            

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('alum_dir/login.html', {}, context)    

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/alum_dir/') 

#
# END: Source for 3 functions: register, user_login, and user_logout
#


@login_required
def user_profile(request):

    updated = False
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # get the user in the request
    user = request.user
    # the alum associated with the user
    alum = Alum.objects.get(email=user.email)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        
        # get new data from the form
        last_name = request.POST['last_name']
        # check to see if user enters anything
        if last_name != '':
            # update data
            user.last_name = last_name
            alum.last_name = last_name

        # get new data from the form    
        first_name = request.POST['first_name']  
        # check to see if user enters anything  
        if first_name != '':
            # update data
            user.first_name = first_name
            alum.first_name = first_name

        # get new data from the form    
        email = request.POST['email']    
        # check to see if user enters anything
        if email != '':
            # update data
            user.email = email
            alum.email = email

        # get new data from the form
        year = request.POST['year']
        # check to see if user enters anything
        if year != '':
            # update data
            alum.year = year

        # get new data from the form   
        school = request.POST['school']    
        # check to see if user enters anything
        if school != '':
            # update data
            alum.school = school

        # save new information    
        alum.save()
        user.save()

        # successfully updated
        updated = True
   
    # return 
    return render_to_response(
        'alum_dir/profile.html',
        {'updated': updated, 'alum': alum},
        context)  
