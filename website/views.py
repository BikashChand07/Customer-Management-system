from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record

from .forms import SignUpForm

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
