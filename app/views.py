from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

from .decorators import unauthenticated_user, allowed_users

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def main_register(request):
    return render(request, 'registration/register.html')

def register_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='user')
            user.groups.add(group)
            messages.success(request, 'User account was created for ' + email)
            print('register user:', request.POST)
            # POST request: create in users table
            return redirect("/login")
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = CreateUserForm()
    return render(request, 'registration/registeruser.html', {"form": form})

def register_company(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            company = form.save()
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='company')
            company.groups.add(group)
            messages.success(request, 'Company account was created for ' + email)
            print('register company:', request.POST)
            return redirect("/login")
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = CreateUserForm()
    # POST request: create in company table
    return render(request, 'registration/registercompany.html', {"form": form})

@unauthenticated_user
def nav(request):
    return render(request,'app/nav.html')
    
@unauthenticated_user
@allowed_users(allowed_roles=['user'])
def user_home(request):
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers ORDER BY customerid")
        customers = cursor.fetchall()

    result_dict = {'records': customers}

    return render(request,'app/user/userhome.html',result_dict)

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def company_home(request):
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers ORDER BY customerid")
        customers = cursor.fetchall()

    result_dict = {'records': customers}

    return render(request,'app/company/companyhome.html',result_dict)

@unauthenticated_user
def user_view_job(request, id):
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/user/viewjob.html', result_dict)

@unauthenticated_user
def company_view_job(request, id):
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/company/viewjob.html',result_dict)  

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def add_job(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('/job')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/company/addjob.html", context)

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def edit_job(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/company/editjob.html", context)

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def view_applicants(request, id):
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/company/viewapplicants.html',result_dict)