from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from .models import Seller

# Create your views here.
def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {'information':'Either Username or Password is invalid'})

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def user(request):
    if(request.method=='POST'):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if (User.objects.filter(email=email).exists()):
            return render(request, 'signup.html', {'error':"You already have an account."})
        
        elif(User.objects.filter(username=username).exists()):
            return render(request, 'signup.html', {'error':"Username already taken."})
        
        else:
            if(password==confirm_password):
                user=User.objects.create_user(first_name=first_name, username=username, last_name=last_name, email=email, password=password)

                user.save()
                return redirect('/login')
            
            else:
                return render(request, 'signup.html', {'error':"The password you entered did not matched."})
    else:
        return render(request, 'signup.html')

def seller(request):
    if request.user.is_authenticated:
        if(request.method=="POST"):
            shop_name=request.POST["shop_name"]
            upi_id=request.POST["upi_id"]
            contact_no=request.POST["contact_no"]

            Seller.objects.create(user_linked=request.user, shop_name=shop_name, contact_no=contact_no, upi_id=upi_id)

            return redirect('/')
            
        else:
            return render(request, 'become-seller.html')
    
    else:
        return redirect('/login')
        