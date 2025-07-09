from django.contrib import admin
from django.urls import path
from dorm.views import (
    signup_api,
    login_api,
    mypage_api,
    give_point_api,
    apply_dorm_api,
    apply_outing_api,
    notices_api,
    posts_api,
    post_detail_api,
    comments_api,
    inquiries_api,
    inquiry_detail_api,
    dorm_applications_list_api,
    dorm_application_detail_api,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup_api, name='signup_api'),
    path('api/login/', login_api, name='login_api'),
    path('api/mypage/', mypage_api, name='mypage_api'),
    path('api/give_point/', give_point_api, name='give_point_api'),
    path('api/dorm_apply/', apply_dorm_api, name='dorm_apply_api'),
    path('api/outing_apply/', apply_outing_api, name='outing_apply_api'),
    path('api/notices/', notices_api, name='notices_api'),
    path('api/posts/', posts_api, name='posts_api'),
    path('api/posts/<int:pk>/', post_detail_api, name='post_detail_api'),
    path('api/posts/<int:post_id>/comments/', comments_api, name='comments_api'),
    path('api/inquiries/', inquiries_api, name='inquiries_api'),
    path('api/inquiries/<int:pk>/', inquiry_detail_api, name='inquiry_detail_api'),
    path('api/dorm-applications/', dorm_applications_list_api, name='dorm_applications_list_api'),
    path('api/dorm-applications/<int:pk>/', dorm_application_detail_api, name='dorm_application_detail_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
