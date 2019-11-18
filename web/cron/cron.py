#！/usr/bin/env python
#-*- coding:utf-8 -*-
#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import  JsonResponse
from .cron_form import CronForm
from web.models import *
import json
#分页功能
from utils.pagination import Pagination
#搜索功能
from django.db.models import Q

from web.cron.cron_time import Cron_time

from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner

# #django 日志模块
# import logging
#
# #生成一个logger实例
# logger=logging.getLogger("default")


def cron_list(request):
    '''
    定时任务列表
    :param request:
    :return:
    '''
    search=request.GET.get("table_search","")
    crons=Cron.objects.filter(name__contains=search)
    pages=Pagination(request.GET.get("page",1),crons.count(),request.GET.copy(),10)
    return render(request,"cron/cronlist.html",{"page_title":"计划任务列表","crons":crons[pages.start:pages.end],
                                           "page_html":pages.page_html})



def Create_edit_cron(request,pk=0):
    '''
    新增定时任务,编辑定时任务
    :param request:
    :return:
    '''

    #通过pk获取cron对象（新增获取不到因为没有pk值，编辑可以获取到）
    cron=Cron.objects.filter(pk=pk).first()

    #CronForm传入对象    （新增相当于CronForm(),编辑是实际传入获取到的对象）
    form=CronForm(instance=cron)

    times = Cron_time()
    #weeks=["周日","周一","周二","周三","周四","周五","周六"]
    if request.method=="POST":
        form=CronForm(request.POST,instance=cron)
        #从前端获取time列表
        time = request.POST.getlist("time")
        #print(request.POST)
        #结果：'time': ['0', '0', '1', '1', '0'], 'name': ['sadf'], 'hosts_list': ['6', '7'], 'user': ['root'], 'job': ['adsf'], 'note': ['afd']

        if form.is_valid():
            res = cron_module(form.cleaned_data["hosts_list"], time, form.cleaned_data["job"],
                              form.cleaned_data["name"], form.cleaned_data["user"])
            if res:
                #创建者字段
                form.instance.create_user = request.account
                #计划任务时间字段
                form.instance.time = " ".join(time)
                form.save()
                return JsonResponse({"status": 0, "msg": "操作成功"})
            else:
                return JsonResponse({"status": 0, "msg": "操作失败"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
#三元运算 定义time数据 和 标题
    #这里数据是通过cron对象从数据表里查出来的，用来编辑 显示编辑前的数据(默认是空(因为如果是新增,这里不为空会报错,如果是编辑(则通过cron对象.time字段查数据),   去除空格后通过" "为分隔符转为列表（因为存的时候按照字符串存的）

    old_time=None if not pk else cron.time.strip().split(" ")

    #计划任务标题
    page_title="创建计划任务" if not pk else "编辑计划任务"


    return render(request, "cron/create_edit_cron.html", {"page_title": page_title,"min": times.min(),"hour": times.hour(),"day": times.day(),"mouth": times.mouth(),"week": times.week(), "form": form, "pk": pk,"old_time":old_time})

def del_cron(request,pk):
    '''
    删除定时任务
    :param request:
    :param pk:
    :return:
    '''
    cron=Cron.objects.filter(pk=pk)

    #上面不能直接.first, 因为.first没有delete属性，不方便删除，所以单独创建一个first对象,方便下面查找
    cron_first=cron.first()
    #执行cron_module方法，传入主机对象,name(根据name来删除),type   1为删除
    cron_module(cron_first.hosts_list.all(),name=cron_first.name,type=1)
    #从数据库中删除
    cron.delete()
    return JsonResponse({"status": 0, "msg": "删除成功"})



#type 如果为1则是执行删除,否则是创建
def cron_module(host_list,time=None,job=None,name=None,user=None,type=None):
    host_data=[{"hostname":h.name,"ip":h.hostip,"port":h.ssh_port}for h in host_list]
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    if type ==1:
        tasks=[{"action":{"module":"cron","args":"name={}  state=absent".format(name)}}]
    else:
        tasks = [{"action": {"module": "cron",
                             "args": "minute={} hour={} day={} month={} weekday={} name={} job={} user={}".format(
                                 time[0], time[1],
                                 time[2], time[3], time[4], name, job, user)}, "name": "cron"}]
    ret = runner.run(tasks)

    if ret.results_raw["ok"]:
        return True
    else:
        return False