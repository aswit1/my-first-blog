from django.contrib.auth.models import AnonymousUser

from blog.models import Conversations
from user_manager.models import UserProfile


def new_message(request):
    context_data = dict()


    if request.user is not None and not request.user.is_anonymous:

        my_conversations = Conversations.objects.filter(recipient=request.user)
        user = request.user
        context_data['new_message'] = False
        for each_convo in my_conversations:
            if user in each_convo.marked_as_new.all():
                context_data['new_message'] = True

    else:
        context_data['new_message'] = False


    return context_data