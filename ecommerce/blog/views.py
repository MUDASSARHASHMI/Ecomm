from urllib import quote_plus
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post
from .forms import PostForm

def blog_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form
    }
    return render(request, 'blog/post_form.html', context)

def blog_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.all() #.order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List",
        'page_request_var': page_request_var,
        "today": today

    }
    return render(request, 'blog/list.html', context)







def blog_detail(request, id=None):

    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        'share_string': share_string
    }
    return render(request, 'blog/detail.html', context)



def blog_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    title = "Update"
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Updated Successfully")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": title,
        "instance": instance,
        "form": form
    }
    return render(request, 'blog/post_form.html', context)


def blog_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect('blog:list')
