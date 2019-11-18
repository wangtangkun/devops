#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http.response import  JsonResponse
from web.models import Host,Command

# from .command_from import
import json

#分页功能
from utils.pagination import Pagination
#搜索功能
from django.db.models import Q

from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner,PlayBookRunner,CommandRunner
def command_issued(request):
    '''
    命令下发页面
    :param request:
    :return:
    '''
    hosts = Host.objects.all()
    ips = [{"id": 1, "pId": 0, "name": "随意勾选 1", "open": "true"}]
    for h in hosts:
        ips.append({"id": 11, "pId": 1, "name": h.hostip})
    if request.method == "POST":
        #print(request.method)
        #<QueryDict: {'node_ips[]': ['192.168.179.140'], 'command': ['lsss'], 'csrfmiddlewaretoken': ['A1psD6C6JxS4L0A87GkkchrJJLUWx7DozsSBvxkHI0DnYztzOK9xfMKlTXvqYY6r']}>

    #按照上面的格式，应该这样👇取数据:

        # 取命令:
        print("POST",request.POST)
        com = request.POST.get("command")

        #取主机列表:
        node_ips=request.POST.getlist("node_ips[]")
        # print(node_ips)  #['192.168.179.140', '192.168.179.142']


        #通过上面获取的node_ips（主机ip列表）,从host表获取hostip字段数据(hostip存在于node_ips列表中的数据)
        host_list=Host.objects.filter(hostip__in=node_ips)

        #执行command函数（传入主机ip,命令 两个参数）
        res=command(host_list,com)

        #将数据加到command表中:
        host=" ".join(node_ips)  #将node_ips列表转为字符串（列表形式也可以直接存到数据表,这样美观）
        Command.objects.create(hosts_list=host,result=res,user=request.account,command=com.strip().replace("\n",","))
        return JsonResponse({"status":0,"msg":res})
        



    return render(request, "command/commandissued.html",{"page_title": "命令下发","ips":ips})


def command_list(request):
    '''
    命令日志（展示页面）
    :param request:
    :return:
    '''
    search = request.GET.get("table_search", "")
    command = Command.objects.filter(Q(command__contains=search)|Q(user__name__contains=search)|Q(hosts_list__contains=search))
    pages = Pagination(request.GET.get("page", 1), command.count(), request.GET.copy(), 15)
    return render(request, "command/command_list.html",
                  {"command": command[pages.start:pages.end], "page_html": pages.page_html, "page_title": "命令下发历史"})

def command_details(request,pk):
    '''
    命令下发历史详情展示
    :param request:
    :param pk:
    :return:
    '''
    command_obj=Command.objects.filter(pk=pk).first()

    return render(request,"command/command_details.html",{"command_details":command_obj})

def command(hostlist,com):
    '''
    根据主机和命令，执行   本方法使用ansible api中的CommandRunner方法
    :param hostlist:  主机
    :param com:  命令
    :return:
    '''

    host_data = [{"hostname": h.hostip, "ip": h.hostip, "port": h.ssh_port} for h in hostlist]
    inventory = Inventory(host_data)  # 重新组成虚拟组
    runner = CommandRunner(inventory)
    res = runner.execute(com)   #执行命令
    return res.results_raw    #返回结果