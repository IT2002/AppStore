from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

def home(request):
    """Shows the product listing page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products ORDER BY productid")
        products = cursor.fetchall()

    result_dict = {'products': products}

    return render(request, 'app/home.html', result_dict)



# Create your views here.
def register(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        form = NewUserForm(request.POST)
        ## Check if userid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No customer with same id
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO allusers(userid, phoneno, password) VALUES (%s, %s, %s)"
                        , [request.POST['username'], request.POST['phoneno'], request.POST['password1'] ])
                newuser = form.save()
                login(request, newuser)
                messages.success(request, 'Registration successful.')
                return redirect('/')    
            else:
                status = 'User with ID %s already exists' % (request.POST['username'])

    form = NewUserForm()
    context['status'] = status
 
    return render(request, "app/register.html", context)

def signin(request):
    """Shows the login page"""
    context = {}
    status = ''

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password1=password1)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('app/')
            else:
                messages.error(request,'Invalid username or password.')
        else:
            status = 'Invalid username or password.' 
    form = AuthenticationForm()
    context['status'] = status
    return render(request, 'app/login.html', context)
			
		
def profile(request, id):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE userid =  %s",[id])
        user = cursor.fetchone()

    result_dict = {'users': users}

    return render(request, 'app/profile.html', result_dict)


def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)



"""
# Create your views here.
def index(request):


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

    return render(request, 'app/index_user_admin.html', result_dict)

# Create your views here.
def view(request, id):
    
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request, 'app/view_admin.html', result_dict)

# Create your views here.
def add(request):
    
    context = {}
    status = ''
   

    if request.POST:
        ## Check if phoneno is already in the table
        with connection.cursor() as cursor:
           
            cursor.execute("SELECT * FROM allusers WHERE phoneno = %s", [request.POST['phoneno']])
            user = cursor.fetchone()
            ## No customer with same id
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO allusers VALUES (%s, %s, %s)"
                               ,[request.POST['userid'], request.POS['phoneno'], request.POST['password']])
                return redirect('login')
            else:
                status = 'Customer with phone number %s already exists' % (request.POST['phoneno'])


    context['status'] = status
 
    return render(request, "app/register.html", context)

# Create your views here.
def edit(request, id):
    

    # dictionary for initial data with
    # field names as keys
    context ={}

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
 
    return render(request, "app/edit_admin.html", context)

# Create your views here.
def login(request):
    
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                cursor.execute("INSERT INTO customers VALUES (%s, %s)"
                        , [request.POST['first_name'], request.POST['last_name']])
                return redirect('index')
            else:
                status = 'Your User Id and Password is incorrect' % (request.POST['customerid'])

    return render(request, 'app/login.html', context)
"""

# Create your views here.
#def index_products(request):


    ## Use raw query to get all objects
#    with connection.cursor() as cursor:
#        cursor.execute("SELECT * FROM products ORDER BY productid")
#        products = cursor.fetchall()

#    result_dict = {'products': products}

#    return render(request, 'app/index_products.html', result_dict)

#def purchase(request, productid):


    ## Use raw query to get all objects
#    with connection.cursor() as cursor:
#        cursor.execute("SELECT * FROM products WHERE productid =  %s",[productid])
#        products = cursor.fetchone()

#    result_dict = {'products': products}

#    return render(request, 'app/purchase.html', result_dict)

#def profile(request, phoneno):
#    with connection.cursor() as cursor:
#        cursor.execute("SELECT * FROM allusers WHERE phoneno =  %s",[phoneno])
#        products = cursor.fetchone()

#    result_dict = {'allusers': allusers}

#    return render(request, 'app/profile.html', result_dict)
