from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User as AppUser
from django.contrib.auth import login, logout
from django.shortcuts import render,redirect
from .froms import LoginForm,Bins,QR
from django.http import HttpResponse
from .models import BinsStats,BINQRs
from django.contrib import messages
from django.urls import reverse
import json
def members(request):
    if request.user.is_authenticated:
        # Fetch messages from the session
        messages_list = messages.get_messages(request)
        bins = BinsStats.objects.all().order_by('-fillUp')  
        qr_code = BINQRs.objects.all()
        return render(request, "index.html", {'user': request.user.username, 'bins': bins, 'QR': qr_code, 'messages': messages_list})
    else:
        messages.error(request, "Please Login First")
        return redirect('UserLogin')
@csrf_exempt
def UserLogin(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = AppUser.objects.filter(username=username).first()
        if user is not None:
            device = request.POST.get('device')
            if user and check_password(password,user.password):
                login(request, user)
                messages.add_message(request,1,'Logged ')
                messages.success(request,f"Succesfuly logged in  as {user.username}")
                if device == "NODE":
                    print("BIN LOGIN DETCETED")
                    return HttpResponse('SCCS\n')
                return redirect(reverse('members'))
        messages.error(request, 'Invalid username or password.')

    form = LoginForm()
    return render(request, 'login.html', {'form': form,'user':request.user.username})
def UserLogout(request):
    if request.user.is_authenticated:
        # messages.add_message(request, messages.SUCCESS, f'The user {request.user.username} has successfully logged out')
        logout(request)
        return redirect('UserLogin')
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

@csrf_exempt
def creatBin(request):
    if request.user.is_authenticated:    
        if request.method == 'POST':
            form = Bins(request.POST)
            if form.is_valid():
                refresh_stats = form.cleaned_data['refreshStats']
                last_refresh = form.cleaned_data['lastRefresh']
                fill_up = form.cleaned_data['fillUp']
                area = form.cleaned_data['Area']
                city = form.cleaned_data['City']
                qr_data = form.cleaned_data['qr_data']
                qr_data_json = json.loads(qr_data)
                lat = qr_data_json['Lat']
                lon = qr_data_json['Lon']
                global bin_id
                bin_id = qr_data_json['BinID']
                if fill_up >= 70:
                    status = 'HIGH'
                    form.refreshStats = 'Due'
                elif fill_up >= 40:
                    status = 'MID'
                    form.refreshStats = 'Due'
                else:
                    status = 'LOW'
                    form.refreshStats = 'Done'

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
            else:
                bin_id = None
                messages.error(request, 'Form submission error. Please check the form.')
                print(form.errors)
                
            return redirect('members')
        
        return render(request, "addBins.html", {'form': Bins(), 'user': request.user.username})
    
    messages.error(request, 'Please Login First')
    return redirect(UserLogin)

@csrf_exempt
def connect(request):
    global bin_id
    try:
        if bin_id:
            temp = "BinId:"+bin_id
            bin_id = None
            return HttpResponse(temp)   
        else:
            return HttpResponse("No bin id\n")
    except (NameError):
        return HttpResponse("No bin id\n")

@csrf_exempt
def update(request):
    try:
        if request.method == 'POST':
            BinID = request.POST['BinID']
            fillUp = int(request.POST['fillUp'])
            fillUp -= 100
            fillUp = abs(fillUp)
            bin_instance = BinsStats.objects.get(BinID=BinID)
            if fillUp >= 70:
                bin_instance.status = 'HIGH'
                bin_instance.refreshStats = 'Due'
            elif fillUp >= 40:
                bin_instance.status = 'MID'
                bin_instance.refreshStats = 'Due'
            else:
                bin_instance.status = 'LOW'
                bin_instance.refreshStats = 'Done'
            print(request.POST)
            bin_instance.fillUp = fillUp
            bin_instance.save()
            return HttpResponse('Succes')   

        return redirect('members')
    except(BinsStats.DoesNotExist):
        return HttpResponse('No Bin\n');
def genQRCODE(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = QR(request.POST)
            if form.is_valid():
                Lat = form.cleaned_data['Lat']
                Lon = form.cleaned_data['Lon']
                BinID = form.cleaned_data['BinID']
                data = "{"+f'"Lat":"{Lat}","Lon":"{Lon}","BinID":"{BinID}"'+"}"
                qr_code = BINQRs(data=data)
                qr_code.save()
                qr_code.generate_qr_code()

        form = QR()
        qrs = BINQRs.objects.all()
        return render(request, 'genQR.html', {'form': form, 'QR': qrs})
    else:
        messages.error(request,"Please Login First")
    return redirect('UserLogin')
