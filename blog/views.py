from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from user_manager.models import Weather, UserProfile
from .models import Post, PostComment, Direct_Message
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, AlexPostForm, Direct_MessageForm, Reply_MessageForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tasks import new_post_email, update_emails, comment_emails


# Create your views here.
def manual_new_post_task(request):
    update_emails()
    return redirect(request.META.get('HTTP_REFERER'))

def post_list(request):
    posts = Post.objects.filter(blog_post=False).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def alex_post_list(request):
    posts = Post.objects.filter(blog_post=True).order_by('published_date')
    return render(request, 'blog/alex_post_list.html', {'posts': posts})

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
        if form.is_valid():
            message = form.save(commit=False)
            message.send_date = timezone.now()
            message.author = request.user
            message.save()
            #we have to use this ON THE FORM for many to many fields because of commit=false. Thats just how it is ¯\_(ツ)_/¯
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "You sent message! woohooo!")
            return redirect('message_list')
    else:
        form = Direct_MessageForm()
    return render(request, 'blog/direct_message.html', {'form': form})

def reply_message(request):
    if request.method == "POST":
        form = Reply_MessageForm(request.POST)
        if form.is_valid():
            reply_message = form.save(commit=False)
            reply_message.reply_recipient = dmessage.author
            reply_message.send_date = timezone.now()
            reply_message.author = request.user
            reply_message.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "You sent reply!")
            return redirect('message_list')
    else:
        form = Reply_MessageForm()
    return render(request, 'blog/reply_message.html', {'form': form})

def message_list(request):
    dmessages = Direct_Message.objects.filter(recipient=request.user).order_by('send_date')
    # authors = User.objects.filter(pk__in=dmessages)
    authors = []
    for dmessage in dmessages:
        if dmessage.author not in authors:
            authors.append(dmessage.author)
    return render(request, 'blog/message_list.html', {'dmessages': dmessages, 'authors': authors,})

def message_detail(request, pk):
    dmessage = get_object_or_404(Direct_Message, pk=pk)
    return render(request, 'blog/message_detail.html', {'dmessage': dmessage})

def conversation_detail(request, pk):
    author = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = Reply_MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.send_date = timezone.now()
            message.author = request.user
            message.save()
            message.recipient.add(author)
            message.save()
            # we have to use this ON THE FORM for many to many fields because of commit=false. Thats just how it is ¯\_(ツ)_/¯
    all_messages = Direct_Message.objects.filter(Q(recipient=request.user, author=author) | Q(recipient=author, author=request.user)).order_by('-send_date')
    form = Reply_MessageForm
    return render(request, 'blog/conversation_detail.html', {'author': author, 'all_messages': all_messages, 'form': form})

def new_messages(request, pk):
    form = Reply_MessageForm(request.POST)
    author = get_object_or_404(User, pk=pk)
    new_message_list = []
    new_messages(default=False)
    for message in new_messages():
        if form.is_valid():
            message.new_messages = True
            message.save()
            new_message_list.append(message.author)
        # we have to use this ON THE FORM for many to many fields because of commit=false. Thats just how it is ¯\_(ツ)_/¯
            form.save_m2m()
    return render(request, 'blog/conversation_detail.html', {'author': author, 'form': form, 'new_message_list': new_message_list})

    # new_messages = Direct_Message.objects.filter(new_message=True)
    # if len(new_messages) < 1:
    #     return "no new messages"
    # if len(new_messages) > 0:
    #     return "new messages"
    # for message in new_messages:
    #     message.new_messages = False
    #     message.save()