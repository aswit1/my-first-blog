from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url="/blog/alex", permanent=False)),
    path('blog/<str:blogtype>', views.PostListViewV2.as_view(), name='post_list_v2'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNewView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/comment/', views.post_comment, name='comment'),
    path('post/<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('post/<int:pk>/comment_edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/post_delete/', views.post_delete, name='post_delete'),
    path('manual_new_post_task', views.manual_new_post_task, name='manual_new_post_task'),
    path('direct_message', views.direct_message, name='direct_message'),
    path('message_list', views.message_list, name='message_list'),
    path('conversation_detail/<int:pk>/', views.conversation_detail, name='conversation_detail'),
]