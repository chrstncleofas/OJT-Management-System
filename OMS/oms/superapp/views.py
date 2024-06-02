from django.shortcuts import redirect
from superapp.forms import SuperuserForm
from app.models import CustomUser
from django.shortcuts import render, redirect

def superHome(request):
    return render(request, 'superapp/base.html')

def createSuperAccount(request):
    if request.method == 'POST':
        form = SuperuserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_superuser(username=username, email=email, password=password)
            user.is_superuser = True
            user.save()
            return redirect('success_page')
    else:
        form = SuperuserForm()  
    return render(request, 'superapp/base.html', {'form': form})
