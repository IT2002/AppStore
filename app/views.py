from tabnanny import check
from unittest import result
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
    context = {}
    status = ''
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
            if request.POST['action'] == 'register':
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
                    user = cursor.fetchone()
                ## No user with same id
                if user == None:
                    ##TODO: date validation
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)"
                                , [request.POST['full_name'], request.POST['email'],
                                request.POST['phone_number'] , request.POST['location'] ])
                        for skill in request.POST['skills'][0].split(sep = ', '):
                            cursor.execute("INSERT INTO skills VALUES(%s, %s)",
                                [request.POST['email'], str(skill)])
                        cursor.execute("INSERT INTO past_exp VALUES(%s, %s, %s, %s, %s)",
                            [request.POST['email'], request.POST['past_company'], request.POST['past_dept'], request.POST['past_title'], request.POST['past_years']])
                    return redirect('/login')    
                else:
                    status = 'User with email %s already exists' % (request.POST['email'])
            return redirect("/login")
        else:
            messages.error(request, 'Invalid form submission')
    else:
        context['status'] = status
        context['form'] = CreateUserForm()
    return render(request, 'registration/registeruser.html', context)#{"form": form})

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
@allowed_users(allowed_roles=['user'])
def user_search(request):
    print("user_search")
    print(request.POST)
    context = {}
    status = ''
    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                word = "%" + request.POST['search'].lower() + "%" #request.POST['search'].lower()
                print(word)
                cursor.execute("SELECT * FROM jobs WHERE (lower(descript) LIKE %s OR lower(job_title) LIKE %s OR lower(name) LIKE %s OR lower(dept) LIKE %s) \
                    OR (est_pay >= %s::INTEGER) \
                    OR (location = %s) AND expiry <= NOW()",
                [word, word, word, word, request.POST['value'],request.POST['location']]\
                )
                check = cursor.arraysize
                jobs = cursor.fetchall()
                print(check)
                result_dict = {'records': jobs}
            ## No result
            if check == 0:
                return redirect('/user/search/fail')
            else:
                return render(request, 'app/user/searchresult.html', result_dict)
    else:
        pass
    return render(request, 'app/user/usersearch.html')

#i dont think is used
@unauthenticated_user
@allowed_users(allowed_roles=['user'])
def user_search_result(request):
    print("user_search_result")
    print(request.POST)
    result_dict = {}
    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM jobs WHERE (name LIKE %s OR job_title LIKE %s OR descript LIKE %s) or (est_pay >= %s::INTEGER) or (location = %s) and expiry <= NOW()",
                [request.POST['search'], request.POST['search'], request.POST['search'], request.POST['value'],request.POST['location']])
                jobs = cursor.fetchall()
                result_dict = {'records': jobs}
                print(result_dict)
                print(result_dict['records'])
    return render(request, 'app/user/searchresult.html', result_dict)

@unauthenticated_user
@allowed_users(allowed_roles=['user'])
def search_fail(request):
    return render(request, 'app/user/searchfail.html')

@unauthenticated_user
def nav(request):
    return render(request,'app/nav.html')
    
@unauthenticated_user
@allowed_users(allowed_roles=['user'])
def user_home(request):
    if request.POST:
        if request.POST['action'] == 'search':
            return redirect('/user/search')
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY email")
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
@allowed_users(allowed_roles=['user'])
def user_view_job(request, id):
    context={}
    status=""
    email = request.user.email
    if request.POST:
        if request.POST['action'] == 'search':
            return redirect('/user/search')
        if request.POST['action'] == 'apply':
            #check if already have
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM applications WHERE email = %s and job_id = %s::INTEGER",\
                [email, request.POST['job_id']])
                check = cursor.fetchone()
                print(check)
            if check == None:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO applications VALUES (%s, %s::INTEGER)", [email, request.POST['job_id']])
                return redirect('/user/job/success')
            else:
                status = 'you have already applied for this job'
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", [id])
        job = cursor.fetchone()
        print(job)
    
    context['status'] = status
    context['job'] = job

    return render(request,'app/user/viewjob.html', context)

def user_apply_job(request):
    pass
    email = request.user.email
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO applications VALUES (%s, %s::INTEGER)", [email, request.POST[2]])
    return render(request, '')

def user_job_success(request):
    return render(request, 'app/user/applysuccess.html')

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