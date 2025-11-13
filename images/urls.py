from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    # URL to create a new image object
    path('create/', views.image_create, name='create'),

    # URL to view the detail of an image using its ID and slug
    path('detail/<int:id>/<slug:slug>', views.image_detail, name='detail'),

    # URL to like/unlike an image via AJAX
    path('like/', views.image_like, name='like'),

    # URL to list all images
    path('', views.image_list, name='list'),

    # URL to view the ranking of images based on total likes or other criteria
    path("ranking/", views.image_ranking, name="ranking")
]
