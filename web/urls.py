# web/urls.py
from django.urls import path
from .views import (
    DormListView, DormDetailView,
    NoticeListView, NoticeDetailView,
    PostListView, PostDetailView,
    InquiryListView, InquiryDetailView,
)

app_name = 'web'
urlpatterns = [
    path('',                DormListView.as_view(),      name='dorm_list'),
    path('dorm/<int:pk>/',  DormDetailView.as_view(),    name='dorm_detail'),

    path('notices/',             NoticeListView.as_view(),   name='notices_list'),
    path('notices/<int:pk>/',    NoticeDetailView.as_view(), name='notices_detail'),

    path('posts/',               PostListView.as_view(),     name='post_list'),
    path('posts/<int:pk>/',      PostDetailView.as_view(),   name='post_detail'),

    path('inquiries/',           InquiryListView.as_view(),  name='inquiry_list'),
    path('inquiries/<int:pk>/',  InquiryDetailView.as_view(),name='inquiry_detail'),
]
