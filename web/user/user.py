#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import  JsonResponse
from .user_from import UserForm
from web.models import *
import json
#分页功能
from utils.pagination import Pagination
#搜索功能
from django.db.models import Q
def userlist(request):
    '''
    用户展示
    :param request:
    :return:
    '''
    #获取前端传来的搜索数据，默认为空
    search = request.GET.get("table_search","")

    #根据搜索从数据库查相应数据，并返回前端显示
    #如果搜索值为空，则全部显示
    #contains 数据库根据关键字查数据   icontains 不分大小写
    users=UserProfile.objects.filter(Q(name__contains=search)|Q(email__contains=search))

    #分页
    pages = Pagination(request.GET.get("page",1),users.count(),request.GET.copy(),5,5)
    return render(request, "user/userlist.html", {"users": users[pages.start:pages.end], "page_html":pages.page_html, "page_title": "用户列表"})



def create_edit_user(request,pk=0):
    '''
    用户新增，编辑用户
    :param request:
    :return:
    '''
    #通过pk获取user对象（新增获取不到因为没有pk值，编辑可以获取到）
    user=UserProfile.objects.filter(pk=pk).first()

    #UserForm传入对象    （新增相当于UserForm(),编辑是实际传入获取到的对象）
    form=UserForm(instance=user)
    print("用户")
    if request.method=="POST":
        print("用户操作1")
        form=UserForm(request.POST,instance=user)
        print("用户操作2")
        if form.is_valid():
            form.save()
            return JsonResponse({"status":0,"msg":"操作成功"})
        else:
            print(form.errors.as_json())
            error_list=[]
            error=json.loads(form.errors.as_json())
            for key,values in error.items():
                INFO=str(key)+": "+str(values[0]["message"])
                error_list.append(INFO)
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为:{}".format(error_list)})
    return render(request, "user/create_user.html", {"form":form, "pk":pk})

def del_user(request,pk):
    user=UserProfile.objects.filter(pk=pk).delete()
    return JsonResponse({"status":0,"msg":"删除成功!"})

