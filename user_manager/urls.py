from django.urls import path
from . import views

urlpatterns = [
    path('all_users/', views.all_users, name='all_users'),
    path('register/', views.register, name="register"),
    path('user_edit/<int:pk>', views.edit_user_profile, name='user_edit'),
    path('user_delete/<int:pk>', views.delete_user, name='user_delete'),
    path('user_profile_edit/', views.user_profile_edit, name='user_profile_edit'),
    path('this_user/', views.this_user, name='this_user'),
    path('meow/', views.update_weather_view, name='meow')

]