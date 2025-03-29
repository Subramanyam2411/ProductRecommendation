from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import UserRegistrationModel
from django.conf import settings
# Create your views here.
def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request,'admins/viewregisterusers.html',{'data':data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/viewregisterusers.html',{'data':data})


def DeleteUser(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).delete()
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/viewregisterusers.html',{'data':data})



def product_recommendation(request):
    if request.method=='POST':
        from users.utility.predections import rec_lin
        productName = request.POST.get('pname')
        recommend = rec_lin(productName)
        recom = recommend.to_html
        path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'
        import pandas as pd
        df = pd.read_csv(path)
        df = df['Product Name'].values.tolist()
        return render(request,'admins/testform.html',{'result': recom,'products':df,'productName':productName})
    else:
        path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'
        import pandas as pd
        df = pd.read_csv(path)
        df = df['Product Name'].values.tolist()
        return render(request, 'admins/testform.html', {'products':df})

