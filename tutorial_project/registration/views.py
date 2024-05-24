from pyexpat.errors import messages

from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationAccountForm, ProfileForm, ChangePasswordForm
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings as conf_settings



# Create your views here.

def index(request):
    template_name = "index.html"
    if request.user.is_authenticated:
        msg = "you are authenticated"

    else:
        msg = "you are not authenticated"

    context = {
        "msg": msg
    }
    return render(request, template_name, context)


def login_page(request):
    template_name = "login.html"
    # print(request.POST)
    form = LoginForm()
    print("Just POST:", request.POST)
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(email=str(data["email"]), password=str(data["password"]))
            print("valid cleaned data:", data)
            if user is not None:
                print("test--4")
                login(request, user)
                return redirect("registration:index")



        else:
            print(form.errors)

    context = {
        "form": form
    }

    return render(request, template_name, context)


def registrationView(request, activation_url=None):
    template_name = "user_registration.html"

    form = RegistrationAccountForm()

    if request.POST:
        form = RegistrationAccountForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            data = form.save()
            print("clean_data:", data.uuid)
            activation_url = f'http://127.0.0.1:8000/activate/{data.uuid}'
            send_mail(
                'user activattion',
                activation_url,
                conf_settings.EMAIL_HOST_USER,
                [data.email],
                fail_silently=False,
            )
        else:
            print("errors:", form.errors)

    print("post data:", request.POST)

    context = {
        "form": form
    }

    return render(request, template_name, context)


def logoutView(request):
    logout(request)
    return redirect("registration:login")


def edit_profile(request):
    template_name = "editProfile.html"

    profile = request.user.profile

    form = ProfileForm(instance=profile)

    if request.POST:

        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('registration:index')

    context = {
        "form": form

    }

    return render(request, template_name, context)


def change_password(request):
    template_name = 'password_change.html'


    form = ChangePasswordForm()

    if request.POST:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print("change password form:", data)

            if request.user.check_password(data.get("current_password")):
                print("password is correct")
                request.user.set_password(data["password"])

                return redirect('registration:index')


            else:
                print("password is incorect")
        else:
            print(form.errors)




    context = {
        "form": form

    }

    return render(request, template_name, context)

from .models import User
def user_activate(request, uuid):
    print("activaciis flow datrigerda", uuid)
    user = User.objects.get(uuid=uuid)
    user.is_active = True
    user.save()

    messages.success(request, "you are activated")

    return redirect("registration:login")
