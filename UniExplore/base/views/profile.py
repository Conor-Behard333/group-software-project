from ..models import Category, Responses, Comments
from ..forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
import json
from decouple import config

"""
    Authors: Lucas Smith, Michael Hills
    Description: Profile page with completed tasks
"""
@login_required(login_url='/login')
def userProfile(request):
    responses = Responses.objects.filter(user=request.user).order_by('-created')
    comments = Comments.objects.all().order_by('-date_added')

    categories = Category.objects.all()
    context = {
        'responses': responses,
        'categories': categories,
        'comments' : comments
    }

    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def deleteProfile(request):
    if request.method == 'POST':
        User.objects.filter(id=request.user.id).delete()
        messages.success(request, 'Account Successfully Deleted')
        return redirect("login")

    return render(request,'base/deleteProfile.html')


"""
    Authors: Lucas Smith
    Description: Edit profile page
"""
@login_required(login_url='/login')
def editProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username').lower().capitalize()
            
            # Analyse image uploaded
            developer_mode = True
            invalid = False
            if developer_mode == False:
                if len(request.FILES) > 0:
                    img = request.FILES["picture"].file.getvalue()
                    invalid = analyse_image({'media': img})
        
            if invalid:
                messages.warning(request, 'ERROR: The photo you tried to upload goes against our terms of service!')
                return redirect('editProfile')
            else:
                try:
                    if request.user.username != username:
                        User.objects.get(username=username)
                    else:
                        raise BaseException()
                except BaseException:
                    user_form.save()
                    profile_form.save()
                    messages.success(request, f'Your account has been updated successfully.')
                    return redirect('profile')
                    
                messages.warning(request, "This username already exists")
                return redirect('editProfile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'base/profile_edit.html', context)

def analyse_image(img):
    params = { 'workflow': 'wfl_brNwJk9abjFRDu54kAc6y', 'api_user': config('image_analysis_api_user'),
                'api_secret': config('image_analysis_api_key')}

    request = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=img, data=params)
    output = json.loads(request.text)
    return output['summary']['action'] == 'reject'

# See another user's profile
# def profile(request, username):
#   person = User.objects.get(username=username)
#  return render(request, 'base/profile.html', {"person": person})