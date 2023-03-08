from django.urls import path
from . import views

urlpatterns = [
    path('post/all/', views.post_list, name='post_list'),
    path('', views.alex_post_list, name='alex_post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/comment/', views.post_comment, name='comment'),
    path('post/<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('post/<int:pk>/comment_edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/post_delete/', views.post_delete, name='post_delete'),
    path('manual_new_post_task', views.manual_new_post_task, name='manual_new_post_task'),
    path('direct_message', views.direct_message, name='direct_message'),
    path('message_list', views.message_list, name='message_list'),
    path('message_detail/<int:pk>/', views.message_detail, name='message_detail'),
    path('conversation_detail/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('reply_message/<int:pk>/', views.reply_message, name='reply_message'),

]