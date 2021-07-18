from django.contrib import admin
from django.urls import path , include

from . import views

urlpatterns = [
    
    path('add_city' , views.index , name="index"),
    path('delete_city/<str:city_name>/' , views.delete_city ,name='delete_city'),
    path('edit_city/<str:city_name>/' , views.edit_city ,name='edit_city'),
    path('' ,views.home , name='home'),
    path('multiple_select' ,views.multiple_select ,name="multi"),
    path('location' ,views.location ,name="location"),
    path('view_data' ,views.view_data ,name="view_data"),
    
]