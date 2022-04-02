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
            with connection.cursor() as cursor:
                args = (request.POST['full_name'], 
                        form.cleaned_data.get('email'),
                        request.POST['phone_number'],
                        request.POST['location'])
                cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s)", args)
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
            #POST request: create in company table
            with connection.cursor() as cursor:
                args = (request.POST['company_name'],
                        request.POST['industry'],
                        form.cleaned_data.get('email'))
                cursor.execute("INSERT INTO company VALUES(%s, %s, %s)", args)
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
    ## Apply, INSERT INTO applications this user
    if request.POST:
        if request.POST['action'] == 'apply':
            with connection.cursor() as cursor:
                print('user:', request.user.email)
                print('id:', request.POST['id'])
                args = (request.user.email, request.POST['id'])
                cursor.execute("INSERT INTO applications VALUES(%s, %s)", args)

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs ORDER BY job_id")
        jobs = cursor.fetchall()

    result_dict = {'jobs': jobs}

    return render(request,'app/user/userhome.html', result_dict)

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def company_home(request):
    ## Delete job
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                # need drop cascade foreign keys
                cursor.execute("DELETE FROM jobs WHERE job_id = %s", [request.POST['id']]) 

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        company = request.user.email
        cursor.execute("SELECT * FROM jobs WHERE email = %s", [company])
        jobs_by_company = cursor.fetchall()
    result_dict = {'jobs_by_company': jobs_by_company}

    return render(request,'app/company/companyhome.html', result_dict)

@unauthenticated_user
def user_view_job(request, id):
    ## Use raw query to get a customer
    print('request:', request)
    print('id:', id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", [id])
        job = cursor.fetchone()
    result_dict = {'job': job}

    return render(request,'app/user/viewjob.html', result_dict)

@unauthenticated_user
def company_view_job(request, id):
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", [id])
        job = cursor.fetchone()
    result_dict = {'job': job}

    return render(request,'app/company/viewjob.html', result_dict)  

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def add_job(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if job already exist in the table pkey: (email, job_title, dept)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs WHERE email = %s AND job_title = %s AND dept = %s", 
                            [request.user.email, 
                            request.POST['job_title'],
                            request.POST['dept']])
            job = cursor.fetchone()
            ## No job with same pkey
            if job == None:
                cursor.execute("SELECT name FROM company WHERE email = %s", [request.user.email])
                company_name = cursor.fetchone()
                if request.POST['est_pay'] == '':
                    est_pay = None
                else:
                    est_pay = request.POST['est_pay']

                query = "INSERT INTO jobs(name, email, job_title, descript, dept, est_pay, location, expiry) "\
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, 
                            [company_name, 
                            request.user.email, 
                            request.POST['job_title'],
                            request.POST['descript'] , 
                            request.POST['dept'], 
                            est_pay, 
                            request.POST['location'], 
                            request.POST['expiry']])
                return redirect('/company')    
            else:
                status = 'Job with company email %s, job_title %s and dept %s already exists' % (request.POST['email'], 
                                                                                                request.POST['job_title'], 
                                                                                                request.POST['dept'])
                print(status)

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
        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        with connection.cursor() as cursor:
            if request.POST['est_pay'] == '':
                # original val
                est_pay = obj[6]
            else:
                est_pay = request.POST['est_pay']

            if request.POST['expiry'] == '':
                expiry = obj[8]
            else:
                expiry = request.POST['expiry']

            cursor.execute(
                "UPDATE jobs\n"\
                "SET name = CASE WHEN %s != '' THEN %s ELSE name END, "\
	                "job_title = CASE WHEN %s != '' THEN %s ELSE job_title END, "\
                    "descript = CASE WHEN %s != '' THEN %s ELSE descript END, "\
                    "dept = CASE WHEN %s != '' THEN %s ELSE dept END, "\
                    "est_pay = %s, "\
                    "location = CASE WHEN %s != '' THEN %s ELSE location END, "\
                    "expiry = %s\n"\
                "WHERE job_id = %s", 
                    [request.POST['name'], request.POST['name'],
                    request.POST['job_title'], request.POST['job_title'],
                    request.POST['descript'], request.POST['descript'],
                    request.POST['dept'], request.POST['dept'],
                    est_pay,
                    request.POST['location'], request.POST['location'],
                    expiry,
                    id]
                )
            status = 'Job edited successfully!'
            cursor.execute("SELECT * FROM jobs WHERE job_id = %s", [id])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/company/editjob.html", context)

@unauthenticated_user
@allowed_users(allowed_roles=['company'])
def view_applicants(request, id):
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        query = "SELECT *"\
                "FROM skills"\
                "LEFT JOIN past_exp USING (email)"\
                "LEFT JOIN users USING (email)"\
                "WHERE email = (SELECT email FROM applications WHERE job_id = %s)"
        cursor.execute(query, [id])
        applicants = cursor.fetchall()
    result_dict = {'applicant': applicants}

    return render(request,'app/company/viewapplicants.html', result_dict)