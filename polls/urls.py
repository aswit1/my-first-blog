from django.urls import path
from . import views

urlpatterns = [
    # path('pollv2_list/', views.pollv2_list, name='pollv2_list'),
    path('pollv2_list/', views.Pollv2ListView.as_view(), name='pollv2_list'),
    path('poll/create/', views.poll_createv2, name='poll_createv2'),
    path('poll/<int:pk>/', views.poll_detailv2, name='poll_detailv2'),
    path('poll/vote/<int:pk>/', views.poll_vote, name='poll_vote'),
    path('poll/<int:pk>/poll_delete/', views.poll_delete, name='poll_delete'),
    path('poll/<int:pk>/add_options/', views.add_options, name='add_options'),
    path('poll/<int:pk>/options_delete/', views.options_delete, name='options_delete'),
    path('poll/<int:pk>/poll_edit/', views.poll_edit, name='poll_edit'),
    ]