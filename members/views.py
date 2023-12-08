from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User as AppUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .froms import LoginForm,Bins
from django.urls import reverse
from .models import BinsStats

def members(request):
    if request.user.is_authenticated:
        bins = BinsStats.objects.all()  
        return render(request,"index.html",{'user':request.user.username,'bins':bins})
    else:
        return redirect('UserLogin')


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = AppUser.objects.filter(username=username).first()
        print(user.password)
        
        if user and check_password(password,user.password):
            login(request, user)
            messages.add_message(request,1,'Logged ')
            print (request.user)
            print (request.user.is_authenticated)
            messages.success(request,f"Succesfuly logged in  as {user.username}")
            return redirect(reverse('members'))

        else:
            messages.error(request, 'Invalid username or password.')

    form = LoginForm()
    return render(request, 'login.html', {'form': form,'user':request.user.username})

def UserLogout(request):
    if request.user.is_authenticated:
        messages.success(request, f'The user {request.user.username} has succesfuly logged out')
        logout(request)
        return redirect('members')
    return redirect('UserLogin')

@csrf_exempt
def POSTDataUpdate(request):
    if request.method == 'POST':
        fillLevel = request.POST['fillLevel']
        BinID = request.POST['BinID']
        print(fillLevel,"    :FillLevel")
        print(BinID,":BinID")
        return HttpResponse(True)
    return HttpResponse(False)
        
def addBin(request):
    if request.user.is_authenticated:    
        if request.method == 'POST':
            form = Bins(request.POST)
            if form.is_valid():
                bin_instance = form.save(commit=False)
                bin_instance.lastRefresh = form.cleaned_data['lastRefresh']
                bin_instance.save() 
                form = Bins()
            else:
                print(form.errors)
            return render(request,"addBins.html",{'form':form})
        return render(request,"addBins.html",{'form':Bins(),'user':request.user.username})
    messages.error(request,'You need to login first to acces this page')
    return redirect(UserLogin)