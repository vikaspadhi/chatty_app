from django.shortcuts import redirect, render
from account.models import User
from django.contrib.auth import authenticate , login , logout
# Create your views here.
def signin(request):
    ctx = {}
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user = authenticate(mobile = mobile , password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            ctx['msg']='<p class="text-danger">Invalid Credentials. Try again.</p>'

    return render(request,'signin.html',ctx)

def signout(request):
    logout(request)
    return redirect('/')
    # return render(request,'index.html')

def register(request):
    ctx = {}
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password = request.POST.get('password')
        ctx = {}
        try:
            user = User.objects.create_user(mobile = mobile , first_name = fname , last_name = lname )
            user.set_password(password)
            user.save()
            ctx['msg']='<p class="text-success">User Created</p>'
        except Exception as e:
            ctx['msg']='<p class="text-danger">Mobile number is already in use. Try other number</p>'

    return render(request,'signup.html',ctx)