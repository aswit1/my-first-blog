from blog.models import Conversations
from user_manager.models import UserProfile


def new_message(request):
    context_data = dict()

    my_conversations = Conversations.objects.filter(recipient=request.user)
    user = request.user
    context_data['new_message'] = False
    for each_convo in my_conversations:
        if user in each_convo.marked_as_new.all():
            context_data['new_message'] = True


    return context_data