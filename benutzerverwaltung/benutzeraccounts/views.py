from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from benutzeraccounts.models import Profile
from benutzeraccounts.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction, models

def profile(request, pk=None):
    if pk:   #pk = id  pk ist unabhaengiger vom eigentlichen Primaerschluesselfeld, d. h. man muss sich nicht darum kuemmern, ob das Primaerschluesselfeld "id" oder "object_id" oder was auch immer heisst.
        user = User.object.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, ('benutzeraccounts/profile.html'), args)

@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('user:profile'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    args = {'user_form': user_form, 'profile_form':profile_form}
    return render(request, 'benutzeraccounts/edit_profile.html', args)
