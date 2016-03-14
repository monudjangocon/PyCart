from django.shortcuts import render, redirect,render_to_response,Http404
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
import re



def Login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        btn="Login"
        if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                user.emailconfirmed.active_user_email()
                return render_to_response("login.html", {'form':form,"submit_btn": btn}) 
        else:
            return HttpResponse("Invalid details...")
    else:
    	form=LoginForm()
    	return render_to_response("login.html",{'form':form})


def Logout(request):
    logout(request)
    messages.success(request, "Successfully Logged out. Feel free to login again.")
    return HttpResponseRedirect('%s'%(reverse("Login")))




def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "Join"
    if form.is_valid():
        new_user = form.save(commit=False)
        # new_user.first_name = "Justin" this is where you can do stuff with the model form
        new_user.save()
        messages.success(request, "Successfully Registered. Please confirm your email now.")
        return HttpResponseRedirect("/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context = {
             "form": form,
             "submit_btn": btn,
    }
    return render(request, "register.html", context)


SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        print "activation key is real"
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "There was an error with your request.")
            return HttpResponseRedirect("/")
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful! Welcome."
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed! Please login.")

        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed"
            messages.success(request, "Already Confirmed.")
        else:
            page_message = ""

        context = {"page_message": page_message}
        return render_to_response("activation_complete.html", context)

    else:
		raise Http404
