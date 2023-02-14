from django.utils import timezone

from user_manager.models import Weather
from .models import Post, PostComment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, AlexPostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tasks import new_post_email, update_emails


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

