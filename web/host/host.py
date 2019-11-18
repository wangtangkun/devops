#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import  JsonResponse
from .host_from import HostForm
from web.models import *
import json
#分页功能
from utils.pagination import Pagination
#搜索功能
from django.db.models import Q

# #django 日志模块
# import logging
#
# #生成一个logger实例
# logger=logging.getLogger("default")


def Hostlist(request):
    '''
    主机展示
    :param request:
    :return:
    '''
    #获取前端传来的搜索数据，默认为空
    search = request.GET.get("table_search","")

    #根据搜索从数据库查相应数据，并返回前端显示
    #如果搜索值为空，则全部显示
    #contains 数据库根据关键字查数据   icontains 不分大小写
    hosts=Host.objects.filter(Q(hostip__contains=search)|Q(name__contains=search))

    #分页
    pages = Pagination(request.GET.get("page",1),hosts.count(),request.GET.copy(),5,5)
    return render(request, "host/hostlist.html", {"hosts": hosts[pages.start:pages.end], "page_html":pages.page_html, "page_title": "主机列表"})



def Create_edit_host(request,pk=0):
    '''
    主机新增，编辑主机
    :param request:
    :return:
    '''
    #通过pk获取host对象（新增获取不到因为没有pk值，编辑可以获取到）
    host=Host.objects.filter(pk=pk).first()

    #HostForm传入对象    （新增相当于HostForm(),编辑是实际传入获取到的对象）
    form=HostForm(instance=host)
    if request.method=="POST":
        form=HostForm(request.POST,instance=host)
        if form.is_valid():
        ####ansible  api 使用代码:
            #form.cleaned 使用（本实例中form_cleaned获取到的值用于给ping_module函数传值）:
            print("cleaned_date", form.cleaned_data)
            #cleaned_date数据格式：（cleaned_data 就是读取表单返回的值，返回类型为字典dict型）：
            # {'name': 'wang', 'hostip': '192.168.12.133', 'env': '3', 'version': None, 'type': '3', 'user': 'root',
            #  'ssh_port': '22', 'status': '0'}
            ##########
            print("cleaned_date_name", form.cleaned_data["name"])
            #打印结果: cleaned_date_name wang123
            #name = cleaned_data['name'] 读取name为 ‘name’的字段提交值

            #使用clean.form:
            status = ping_module(form.cleaned_data["hostip"], form.cleaned_data["ssh_port"], form.cleaned_data["user"])

            #判断主机是否在线（在线则保存到数据库，不在线则提示并不保存）
            if status:
                form.save()
                return JsonResponse({"status":0,"msg":"操作成功"})
            else:
                return JsonResponse({"status": 1, "msg": "该主机不在线,请检查主机或者网络"})
        else:
            print(form.errors.as_json())
            error_list=[]
            #form.errors.as_json()  报错信息
            #转为字典格式
            error=json.loads(form.errors.as_json())
            for key,values in error.items():
                INFO=str(key)+": "+str(values[0]["message"])
                error_list.append(INFO)
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为:{}".format(error_list)})
    return render(request, "host/create_host.html", {"form":form, "pk":pk})

def del_host(request,pk):
    host=Host.objects.filter(pk=pk).delete()
    return JsonResponse({"status":0,"msg":"删除成功!"})


from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner
def ping_module(hostip,port,username):
    '''
    通过ansible  api  通过ping命令检测远程主机是否在线
    :param hostip:
    :param port:
    :param username:
    :return:
    '''
    host_data = [
        {
            "hostname": "主机:%s"%hostip,  # key值
            "ip": hostip,
            "port": port,
            "username": username,
        },
    ]
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    tasks = [{"action": {"module": "ping"}, "name": "ping"}]

    #获取执行结果:
    ret = runner.run(tasks)
    # 打印执行结果:
    print(ret.results_raw)

    if ret.results_raw["ok"]:
        return True
    else:
        return False