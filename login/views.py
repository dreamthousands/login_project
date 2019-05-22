from django.shortcuts import render, redirect, reverse
import datetime
import pytz
import hashlib
from .models import UserInfo, ConfirmString
from .forms import UserForm, RegisterForm
from myfirst_project import settings
# Create your views here.


def hash_code(s, salt='first_project'):
    h = hashlib.md5()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.127.0.1/confirm</a>，\
                    这里是jxq的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = UserInfo.objects.filter(username=username)[0]
            except IndexError:
                message = '用户不存在！'
                return render(request, 'login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session['password'] = user.password
                return redirect(reverse('index'))
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            try:
                user_name = UserInfo.objects.filter(username=username)[0]
                message = '名字%s已经被使用' % user_name.username
                return render(request, 'register.html', locals())
            except IndexError:
                password1 = register_form.cleaned_data.get('password1')
                password2 = register_form.cleaned_data.get('password2')
                if password1 != password2:
                    message = '两次密码的输入不一致'
                    return render(request, 'register.html', locals())
                else:
                    email = register_form.cleaned_data.get('email')
                    try:
                        user_email = UserInfo.objects.filter(email=email)[0]
                        message = '邮箱%s已经被使用' % user_email.email
                        return render(request, 'register.html', locals())
                    except IndexError:
                        sex = register_form.cleaned_data.get('sex')
                        user = UserInfo.objects.create(username=username, password=hash_code(password1), sex=sex, email=email)
                        code = make_confirm_string(user)
                        send_email(email, code)
                        message = '请前往邮箱进行确认！'
                        return render(request, 'confirm.html', locals())
        else:
            return render(request, 'register.html', locals())
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    request.session.flush()
    return redirect(reverse('login'))

def user_confirm(request):
    code = request.GET.get('code', None)
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'confirm.html', locals())
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    time_delta = confirm.c_time + datetime.timedelta(settings.CONFIRM_DAYS)

    if now > time_delta:
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirm = True
        confirm.user.save()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())
