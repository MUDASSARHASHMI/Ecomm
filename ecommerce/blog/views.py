from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm

def blog_create(request):
    title = 'Create'
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": title
    }
    return render(request, 'blog/post_form.html', context)

def blog_list(request):
    title = "List"
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": title
    }
    return render(request, 'blog/list.html', context)

def blog_detail(request, id):
    title = "Detail"
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": title,
        "instance": instance
    }
    return render(request, 'blog/detail.html', context)



def blog_update(request, id=None):
    title = "Update"
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
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
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect('blog:list')
