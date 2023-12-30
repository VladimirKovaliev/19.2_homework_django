from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Post


class PostListView(ListView):
    model = Post
    extra_context = {'title': 'Posts'}

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        new_mat = super().get_object(queryset)
        new_mat.views_count += 1
        new_mat.save()
        return new_mat


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:post_list')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
