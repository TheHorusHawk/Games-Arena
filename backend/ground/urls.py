from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_in', views.toggle_in, name="get_in"),
    path('arena',views.arena,name='arena')
]