from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST



# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            print(cd)
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            print(new_image.save())
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail view
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    context = {
        'section':'images',
        'form':form
    }

    return render(request,'images/image/create.html',context)

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    context = {
        'secion':'images',
        'image':image
    }

    return render(request,'images/image/detail.html',context)

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})
