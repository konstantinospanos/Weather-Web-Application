from django.urls import path
from .import views

urlpatterns = [
    path('weather', views.index, name='weather'), # the function to call weather page
    path('delete/<city_name>', views.delete_city, name='delete_city') # the function for delete
]
