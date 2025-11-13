from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

# -------------------------------
# User authentication views
# -------------------------------

def user_login(request):
    """
    Handles user login via username and password.
    Renders login form on GET, authenticates user on POST.
    Returns appropriate HttpResponse on success or failure.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


# -------------------------------
# Dashboard
# -------------------------------

@login_required
def dashboard(request):
    """
    Displays the dashboard for logged-in users.
    Shows recent actions by people the user is following.
    """
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)

    # Optimize queries: join user and profile, prefetch target objects
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    context = {
        'section': 'dashboard',
        'actions': actions
    }
    return render(request, 'account/dashboard.html', context)


# -------------------------------
# User registration
# -------------------------------

def register(request):
    """
    Handles new user registration.
    Creates a User and Profile instance, logs the action.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Create profile for the new user
            Profile.objects.create(user=new_user)

            # Record user creation action for activity stream
            create_action(new_user, 'has created an account')

            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})


# -------------------------------
# Edit profile
# -------------------------------

@login_required
def edit(request):
    """
    Allows logged-in users to edit their profile and user info.
    Handles validation, saves changes, and shows success/error messages.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context)


# -------------------------------
# User listing and detail
# -------------------------------

@login_required
def user_list(request):
    """
    Lists all active users.
    Used for social features like following.
    """
    users = User.objects.filter(is_active=True)
    context = {
        'section': 'people',
        'users': users
    }
    return render(request, 'account/user/list.html', context)


@login_required
def user_detail(request, username):
    """
    Shows detailed profile for a given username.
    """
    user = get_object_or_404(User, username=username, is_active=True)
    context = {
        'section': 'people',
        'user': user
    }
    return render(request, 'account/user/detail.html', context)


# -------------------------------
# Follow/unfollow users
# -------------------------------

@require_POST
@login_required
def user_follow(request):
    """
    Handles AJAX requests to follow or unfollow other users.
    Creates or deletes Contact instances and logs the action.
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()

            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
