"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from moments.views import submit_post, friends, show_status, show_user, signup, like_status, delete_status, add_comment, edit_profile

app_name = 'moments'
urlpatterns = [
    # path('admin/', admin.site.urls),
    # 由蓝鲸提供登录服务
    # path('', LoginView.as_view(template_name='moments/homepage.html')),
    path('', show_status),
    path('user', show_user, name='show_user'),
    path('user/edit', edit_profile, name='edit_profile'),
    path('post', submit_post),
    path('friends', friends),
    path('status', show_status, name='show_status'),
    path('status/<int:status_id>/like', like_status, name='like_status'),
    path('status/<int:status_id>/delete', delete_status, name='delete_status'),
    path('status/<int:status_id>/comment', add_comment, name='add_comment'),
    # 退出和注册也由蓝鲸PAAS接管
    # path('exit', LogoutView.as_view(next_page='/'), name='logout'),
    # path('signup/', signup, name='signup'),
]
