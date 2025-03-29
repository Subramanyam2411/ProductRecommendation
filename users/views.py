# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def DatasetView(request):
    path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'
    import pandas as pd
    df = pd.read_csv(path, nrows=100)
    df = df.drop(columns=['Uniq Id','Brand Name','Asin','Upc Ean Code',	'List Price','Quantity','About Product',
                          'Product Specification','Technical Details','Product Dimensions','Image','Variants',
                          'Product Url', 'Stock','Product Details','Dimensions','Color','Ingredients','Direction To '
                                                                                                      'Use','Is Amazon Seller',
                          'Size Quantity Variant','Product Description','Sku'])
    df = df.to_html
    return render(request, 'users/viewdataset.html', {'data': df})


def data_preprocess(request):
    from .utility.ecommerce_preprocess import pre_proccessed_data
    df = pre_proccessed_data()
    return render(request, 'users/pre_process_data.html',{'data': df})

def user_machine_learning(request):
    from .utility.predections import ml_scores
    linear_kernel, cosine_similarity, sig_score = ml_scores()
    return render(request,'users/ml_scores.html',{'lr': linear_kernel, 'cosine': cosine_similarity, 'sig': sig_score})

def user_predictions(request):
    if request.method=='POST':
        from .utility.predections import rec_lin
        productName = request.POST.get('pname')
        recommend = rec_lin(productName)
        recom = recommend.to_html
        path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'
        import pandas as pd
        df = pd.read_csv(path)
        df = df['Product Name'].values.tolist()
        return render(request,'users/testform.html',{'result': recom,'products':df,'productName':productName})
    else:
        path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'
        import pandas as pd
        df = pd.read_csv(path)
        df = df['Product Name'].values.tolist()
        return render(request, 'users/testform.html', {'products':df})

