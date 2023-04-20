from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone

from user_manager.models import Weather, UserProfile
from . import models
from .models import Post, PostComment, Direct_Message, Conversations
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, AlexPostForm, Direct_MessageForm, Reply_MessageForm, ConversationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tasks import new_post_email, update_emails, comment_emails
from django.views.generic.list import ListView


# Create your views here.
def manual_new_post_task(request):
    update_emails()
    return redirect(request.META.get('HTTP_REFERER'))


# def post_list(request):
#     posts = Post.objects.filter(blog_post=False).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    blogtype = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.blogtype == 'community':
            context["object_list"] = Post.objects.filter(blog_post=False).order_by('published_date')
            context["page_title"] = 'Community Blog'
        else:
            context["object_list"] = Post.objects.filter(blog_post=True).order_by('published_date')
            context["page_title"] = 'Main Blog'

        print(self.blogtype)
        return context





# def alex_post_list(request):
#     posts = Post.objects.filter(blog_post=True).order_by('published_date')
#     return render(request, 'blog/alex_post_list.html', {'posts': posts})

class AlexPostListView(ListView):
    model = Post
    template_name = 'blog/alex_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(blog_post=True).order_by('published_date')
        return context



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = PostComment.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


@login_required()
def post_new(request):
    if request.method == "POST":
        form = AlexPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    if request.user.username == 'aswit':
        form = AlexPostForm()
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        print(request.user.is_superuser)
        return redirect('post_detail', pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.edit_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required()
def post_comment(request, pk):
    this_post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_comment = form.save(commit=False)
            post_comment.author = request.user
            post_comment.post = this_post
            # post_comment.publish()
            post_comment.published_date = timezone.now()
            post_comment.save()
            post_author_email = this_post.author.email
            comment_emails.delay(post_comment.pk, post_author_email)
            return redirect('post_detail', pk=this_post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment.html', {'form': form, 'post': this_post})


@login_required()
def post_delete(request, pk):
    alex_posts = Post.objects.filter(blog_post=True).order_by('published_date')
    community_posts = Post.objects.filter(blog_post=False).order_by('published_date')
    this_post = get_object_or_404(Post, pk=pk)
    if this_post in alex_posts:
        this_post = get_object_or_404(Post, pk=pk)
        if request.user != this_post.author and request.user.is_superuser is False:
            messages.add_message(request, messages.ERROR, "You can't do that.")
            return redirect('alex_post_list', pk=this_post.pk)
        this_post.delete()
        return redirect('alex_post_list')
    if this_post in community_posts:
        this_post = get_object_or_404(Post, pk=pk)
        if request.user != this_post.author and request.user.is_superuser is False:
            messages.add_message(request, messages.ERROR, "You can't do that.")
            return redirect('post_list', pk=this_post.pk)
        this_post.delete()
        return redirect('post_list')


@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    if request.user != comment.author and request.user.is_superuser is False:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        print(request.user.is_superuser)
        return redirect('post_detail', pk=comment.post.pk)
    else:
        this_comment = PostComment.objects.get(pk=pk)
        this_post = this_comment.post
        this_comment.delete()
        return redirect('post_detail', pk=this_post.pk)


@login_required()
def comment_edit(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    if request.user != comment.author:
        messages.add_message(request, messages.ERROR, "You can't do that.")
        return redirect('post_detail', pk=comment.post.pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edit_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form})


@login_required()
def direct_message(request):
    if request.method == "POST":
        form = Direct_MessageForm(request.POST)
        form2 = ConversationForm(request.POST)
        if form2.is_valid():
            conversation = form2.save(commit=False)
            conversation.save()
            form2.save_m2m()
            conversation.recipient.add(request.user)

            for each in conversation.recipient.all():
                conversation.marked_as_new.add(each)
            conversation.marked_as_new.remove(request.user)
            this_conversation = conversation.save()
            if form.is_valid():
                message = form.save(commit=False)
                message.send_date = timezone.now()
                message.author = request.user
                message.conversation = conversation
                message.save()

                conversation_match = Conversations.objects.annotate(
                    total_members=Count('recipient'),
                    matching_members=Count('recipient', filter=Q(recipient__in=conversation.recipient.all()))
                ).filter(
                    matching_members=len(conversation.recipient.all()),
                    total_members=len(conversation.recipient.all())
                ).order_by('id')
                for each in conversation_match:
                    print(each.id)

                if len(conversation_match) == 1:
                    message.conversation = conversation_match[0]
                    message.save()
                    messages.add_message(request, messages.SUCCESS, "Added message to existing conversation!")

                elif len(conversation_match) > 1:
                    for each_convo in conversation_match:
                        message.conversation = None
                        message.save()
                        conversation.delete()

                else:
                    messages.add_message(request, messages.SUCCESS, "New conversation created!")

        return redirect('message_list')

    else:
        form = Direct_MessageForm()
        form2 = ConversationForm()
    return render(request, 'blog/direct_message.html', {'form': form, 'form2': form2})


# def reply_message(request):
#     if request.method == "POST":
#         form = Reply_MessageForm(request.POST)
#         if form.is_valid():
#             reply_message = form.save(commit=False)
#             reply_message.reply_recipient = dmessage.author
#             reply_message.send_date = timezone.now()
#             reply_message.author = request.user
#             reply_message.save()
#             form.save_m2m()
#             messages.add_message(request, messages.SUCCESS, "You sent reply!")
#             return redirect('message_list')
#     else:
#         form = Reply_MessageForm()
#     return render(request, 'blog/reply_message.html', {'form': form})


def message_list(request):
    my_conversations = Conversations.objects.filter(recipient=request.user)
    print(my_conversations)
    return render(request, 'blog/message_list.html', {'my_conversations': my_conversations})


def conversation_detail(request, pk):
    my_conversation = Conversations.objects.get(pk=pk)
    if request.method == "POST":
        form = Reply_MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.send_date = timezone.now()
            message.author = request.user
            message.conversation = my_conversation
            message.save()

            message.conversation.marked_as_new.set(message.conversation.recipient.all())
            message.conversation.marked_as_new.remove(request.user)
            message.conversation.save()
    all_messages = Direct_Message.objects.filter(conversation=my_conversation).order_by('send_date')

    form = Reply_MessageForm
    my_conversation.marked_as_new.remove(request.user)
    return render(request, 'blog/conversation_detail.html',
                  {'all_messages': all_messages, 'form': form, 'my_conversation': my_conversation})
