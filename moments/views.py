from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import Status, WeChatUser


# Create your views here.

@login_required
def show_user(request):
    # wechat_user = None
    # if request.user.is_authenticated:
    #     # 获取 QuerySet 中的第一个对象，如果为空则返回 None
    #     wechat_user = WeChatUser.objects.filter(user=request.user).first()
    wechat_user, is_created = WeChatUser.objects.get_or_create(user=request.user)
    return render(request, 'moments/user.html', {'user': wechat_user})


@login_required
def friends(request):
    return render(request, 'moments/friends.html')


@login_required
def submit_post(request):
    if request.method == 'POST':
        user = WeChatUser.objects.get(user=request.user)
        text = request.POST.get('text')
        uploaded_file = request.FILES.get("pics")
        if uploaded_file:
            name = 'static/image/' + uploaded_file.name
            with open("./moments/{}".format(name), 'wb') as handle:
                for block in uploaded_file.chunks():
                    handle.write(block)
        else:
            name = ''
        if text:
            status = Status(user=user, text=text, pics=name)
            status.save()
        return redirect('/status')

    return render(request, 'moments/my_post.html')


@login_required
def show_status(request):
    statuses = Status.objects.all().order_by('-id')
    return render(request, 'moments/status.html', {'statuses': statuses})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('signup_name')
        email = request.POST.get('signup_email')
        password = request.POST.get('signup_password')

        if not username or not email or not password:
            messages.error(request, '请填写所有字段')
            return redirect('/')

        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return redirect('/')

        user = User.objects.create_user(username=username, email=email, password=password)
        WeChatUser.objects.create(user=user)  # 创建 WeChatUser 并与 User 关联
        login(request, user)  # 注册成功后直接登录
        return redirect('/status')  # 跳转到status页面
    else:
        return redirect('/')
