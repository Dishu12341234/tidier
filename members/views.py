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

# @csrf_exempt
# def POSTDataUpdate(request):
#     if request.method == 'POST':
#         fillLevel = request.POST['fillLevel']
#         BinID = request.POST['BinID']
#         print(fillLevel,"    :FillLevel")
#         print(BinID,":BinID")
#         return HttpResponse(True)
#     return HttpResponse(False)
def addBin(request):
    if request.user.is_authenticated:    
        if request.method == 'POST':
            form = Bins(request.POST)
            if form.is_valid():
                bin_id = form.cleaned_data['BinID']
                refresh_stats = form.cleaned_data['refreshStats']
                last_refresh = form.cleaned_data['lastRefresh']
                fill_up = form.cleaned_data['fillUp']
                lat = form.cleaned_data['Lat']
                lon = form.cleaned_data['Lon']
                area = form.cleaned_data['Area']
                city = form.cleaned_data['City']
                if fill_up >= 70:
                    status = 'HIGH'
                elif fill_up >= 40:
                    status = 'MID'
                else:
                    status = 'LOW'

                # Now you have individual variables for each form field
                # You can use these variables as needed, for example, save them to the database

                bin_instance = BinsStats(
                    BinID=bin_id,
                    status=status,
                    refreshStats=refresh_stats,
                    lastRefresh=last_refresh,
                    fillUp=fill_up,
                    Lat=lat,
                    Lon=lon,
                    Area=area,
                    City=city,
                )

                bin_instance.save()

                messages.success(request, 'Bin added successfully!')
                form = Bins()
            else:
                messages.error(request, 'Form submission error. Please check the form.')
                print(form.errors)
                
            return render(request, "addBins.html", {'form': form})
        
        return render(request, "addBins.html", {'form': Bins(), 'user': request.user.username})
    
    messages.error(request, 'You need to log in first to access this page')
    return redirect(UserLogin)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        BinID = request.POST['BinID']
        fillUp = int(request.POST['fillUp'])
        bin_instance = BinsStats.objects.get(BinID=BinID)
        if fillUp >= 70:
            bin_instance.status = 'HIGH'
        elif fillUp >= 40:
            bin_instance.status = 'MID'
        else:
            bin_instance.status = 'LOW'

        bin_instance.fillUp = fillUp
        bin_instance.save()
        return HttpResponse('Succes')   

    return redirect('members')