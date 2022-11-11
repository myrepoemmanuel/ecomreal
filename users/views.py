from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from vendors.models import Vendor
#from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .forms import UserRegisterForm
from .models import Profile
from django.http import JsonResponse
import json

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('username')
            # encode_usr = base64.b64encode(username.encode())
            # Customer.objects.create(
            #     user=encode_usr,
            #     name=username,
            #     email=email

            #     )
            # messages.success(request, f'Account for {username} created successfully')
            return redirect('users:site-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
#    u_form = UserUpdateForm()
#    p_form = ProfileUpdateForm()
#    
#    context = {
#        'u_form':u_form,
#        'u_form':u_form,
#    }
    profile = Profile.objects.filter(user=request.user).values()[0]

    vendor_u = Vendor.objects.filter(vendor_name=request.user.id)

    if str(vendor_u) == '<QuerySet []>':
        show_form = "yes"
    else:
        show_form = 'no'
    # errasing none from values...
    for key, value in profile.items():
        if value == None:
            profile[key] = ""
    
        
    context = {"profile":profile,"show_form":show_form, "username":request.user}
    return render(request, 'users/profile.html', context)

def process_profile(request):
    # transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    profile = Profile.objects.get(user=request.user)
    
    profile.first_name=data['profileInfo']['first_name']
    profile.last_name=data['profileInfo']['last_name']
    profile.phone=data['profileInfo']['phone']
    profile.address_one=data['profileInfo']['address_1']
    profile.address_two=data['profileInfo']['address_2']
    profile.postcode=data['profileInfo']['postalcode']
    profile.country=data['profileInfo']['country']
    profile.region=data['profileInfo']['region']
    
    
    profile.save()


    return JsonResponse('profile saved', safe=False)

def change_password(request):
    print("pass form.....>>>>>><<<<<<<<<......////")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('users:change_password')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {form: form})

 