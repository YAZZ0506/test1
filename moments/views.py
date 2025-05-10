from blueapps.conf.environ import SITE_URL
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Status, WeChatUser, Comment, Like


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
        return redirect('moments:show_status')

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


@login_required
@require_POST
def like_status(request, status_id):
    status = Status.objects.get(id=status_id)
    user = WeChatUser.objects.get(user=request.user)
    
    try:
        like = Like.objects.get(status=status, user=user)
        like.delete()
        liked = False
    except Like.DoesNotExist:
        Like.objects.create(status=status, user=user)
        liked = True
    
    # 获取按时间排序的点赞用户列表
    likes = status.like_set.all().select_related('user__user')
    likes_list = [{'username': like.user.user.username, 'time': like.created_at.strftime('%Y-%m-%d %H:%M')} for like in likes]
    
    return JsonResponse({
        'liked': liked,
        'likes_count': status.like_set.count(),
        'likes_list': likes_list
    })


@login_required
@require_POST
def delete_status(request, status_id):
    status = Status.objects.get(id=status_id)
    if status.user.user == request.user:
        status.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)


@login_required
@require_POST
def add_comment(request, status_id):
    status = Status.objects.get(id=status_id)
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get('text')
    parent_id = request.POST.get('parent_id')
    
    if parent_id:
        parent = Comment.objects.get(id=parent_id)
    else:
        parent = None
        
    comment = Comment.objects.create(
        status=status,
        user=user,
        text=text,
        parent=parent
    )
    
    return JsonResponse({
        'id': comment.id,
        'text': comment.text,
        'username': user.user.username,
        'pub_time': comment.pub_time.strftime('%Y-%m-%d %H:%M')
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = WeChatUser.objects.get(user=request.user)
        django_user = request.user
        
        # 更新Django User信息
        django_user.username = request.POST.get('username')
        django_user.save()
        
        # 更新WeChatUser信息
        user.email = request.POST.get('email')
        user.motto = request.POST.get('motto')
        user.region = request.POST.get('region')
        
        if 'user_pic' in request.FILES:
            uploaded_file = request.FILES['user_pic']
            name = 'static/image/' + uploaded_file.name
            with open("./moments/{}".format(name), 'wb') as handle:
                for block in uploaded_file.chunks():
                    handle.write(block)
            user.user_pic = name
            
        user.save()
        return redirect('moments:show_user')
    
    # 获取当前用户信息
    wechat_user = WeChatUser.objects.get(user=request.user)
    context = {
        'django_user': request.user,
        'wechat_user': wechat_user
    }
    return render(request, 'moments/edit_profile.html', context)
