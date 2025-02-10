from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from django.db.models import Q
import csv
from django.http import HttpResponse


from .forms import SignUpForm, AddRecordForm

# Create your views here.
def home(request):
    records=Record.objects.all()

	# Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		# Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})



def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out!")
    return redirect('home')


def register_user(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have successfully registered! Welcome.")
            return redirect('home')
        
    #get request
    else:
        form=SignUpForm()
    return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    # only allow the loggedin user or authenticated user to view the record
    if request.user.is_authenticated:
        #look up record
        customer_record = Record.objects.get(id=pk)# here id is from the model named as Record and pk is from url
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in to view the record.")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        customer = Record.objects.get(id=pk)
        customer.delete()
        messages.success(request,"Record Deleted Successfully")
        return redirect('home')
    
    else:
        messages.success(request,"You must be logged in to delete the record.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record Added Successfully..")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None,instance=current_record) # instance=current_record will display old values
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been Updated.")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
     
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')

def search_record(request):
    if request.method == "POST":
        searched = request.POST['searched']
        full_name_query = searched  # Full name 
        name_parts = full_name_query.strip().split()

        #split example:
        # s = "hello world"
        #  by default Splits by whitespace
        # print(s.split())  output = ['hello', 'world']

        if len(name_parts) >= 2:
            first_name = name_parts[0]           # First word as first name
            last_name = name_parts[-1]           # Last word as last name
            searched_record = Record.objects.filter(
            Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
            )

        elif len(name_parts) == 1:
            # If only one name either (first_name or last_name) is provided, search in both fields
            name = name_parts[0]
            searched_record = Record.objects.filter(
            Q(first_name__iexact=name) | Q(last_name__iexact=name)
            )

        else:
            searched_record = Record.objects.none()
       
        # If you want to search for names that partially match the input, use icontains.
        # Record.objects.filter(first_name__icontains=first_name_query, last_name__icontains=last_name_query)

        return render(request,'search_record.html',{'searched_record':searched_record})
    
    else:
        return render(request,'search_record.html',{})
    

def download_customers(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_records.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write the headers
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Address', 'City', 'State', 'Joined Date'])

    # Write data rows
    customers = Record.objects.all()
    for customer in customers:
        writer.writerow([
            customer.id,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone,
            customer.address,
            customer.city,
            customer.state,
           customer.created_at.strftime('%Y-%m-%d')
        ])
    return response








    