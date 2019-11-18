from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import  JsonResponse
from .models import *

#这个模块将model实例转换为dict
from django.forms.models import model_to_dict
import time
# Create your views here.

def login(request):
    '''
    用户登录
    :param request:
    :return:
    '''
    print("登录页面")
    error_msg=""
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=UserProfile.objects.filter(email=email,password=password).first()
        if user:
            # request.session["user_id"]=user.pk

            #设置session
            request.session["user"] = model_to_dict(user)
            return redirect(reverse("userlist"))
        error_msg="用户名密码错误!"
    return render(request,"login.html",{"error_msg":error_msg})

def index(request):
    return render(request, "index.html",{"page_title":"首页"})

def host(request):
    return render(request, "host/host.html", {"page_title": "主机列表"})

def create_host(request):
    if request.method=="POST":
        username=request.POST.get("username")
        print(username)
        # time.sleep(5)
    # 返回数据,status必填0代表成功，1代表失败。   msg:具体内容
        return JsonResponse({"status":0,"msg":"添加成功!"})
    return render(request, "host/create_host_test.html")