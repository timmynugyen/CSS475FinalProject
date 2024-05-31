from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.frontpage, name='frontpage'),
    path('submitted/', views.submitted, name='submitted'),
]
