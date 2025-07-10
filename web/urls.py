# web/urls.py
from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='home'),
    path('guide/', views.guide, name='guide'),
    path('community/', views.community, name='community'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('inquiry/<int:pk>/', views.inquiry_detail_view, name='inquiry_detail'),
    path('signup/', views.signup_views, name='signup'),
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('notice/', views.notice_list, name='notice'),
    path('notice_create/', views.notice_create, name='notice_create'),
    path('notice/delete/<int:pk>/', views.notice_delete, name='notice_delete'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notice/<int:notice_id>/edit/', views.notice_update, name='notice_update'),
    path('menu/', views.menu, name='menu'),
    path('check_in/', views.check_in, name='check_in'),
    path('outside/', views.outside, name='outside'),
    path('community_home/', views.community_home, name='community_home'),
    path('post/<int:pk>/', views.community_detail, name='community_detail'),
    path('post/create/', views.community_create, name='community_create'),
    path('post/<int:pk>/delete/', views.community_delete, name='community_delete'),
    path('post/<int:post_id>/edit/', views.community_update, name='community_update'),
    path('comment/add/<int:pk>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('bus/', views.bus, name='bus'),
    path('acc/', views.acc, name='acc'),
    path('info/', views.info, name='info'),
    path('rules/', views.rules, name='rules'),
    path('apply_success/', views.apply_success, name='apply_success'),
    path('outinfo/', views.outing_info, name='outing_info'),
    path('outinfo/approve/<int:pk>/', views.approve_outing, name='approve_outing'),
    path('outinfo/reject/<int:pk>/', views.reject_outing, name='reject_outing'),
    path('reward/', views.reward_penalty, name='reward_penalty'),
    path('dorminfo/', views.dorm_info_view, name='dorm_info'),
    path('assign_room/<int:dorm_id>/', views.assign_room, name='assign_room'),
]
