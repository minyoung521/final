# web/views.py
from django.views.generic import ListView, DetailView
from dorm.models import Dorm, Notice, Post, Inquiry

class DormListView(ListView):
    model = Dorm
    template_name = 'web/dorm_list.html'
    context_object_name = 'dorms'

class DormDetailView(DetailView):
    model = Dorm
    template_name = 'web/dorm_detail.html'
    context_object_name = 'dorm'

class NoticeListView(ListView):
    model = Notice
    template_name = 'web/notices_list.html'
    context_object_name = 'notices'
    ordering = ['-date']

class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'web/notices_detail.html'
    context_object_name = 'notice'

class PostListView(ListView):
    model = Post
    template_name = 'web/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'web/post_detail.html'
    context_object_name = 'post'

class InquiryListView(ListView):
    model = Inquiry
    template_name = 'web/inquiry_list.html'
    context_object_name = 'inquiries'
    ordering = ['-created_at']

class InquiryDetailView(DetailView):
    model = Inquiry
    template_name = 'web/inquiry_detail.html'
    context_object_name = 'inquiry'
