from django.shortcuts import render
from .init_form import InitForm,InitLogForm
from django.http.response import JsonResponse
from web.models import Init,UserProfile,InitLog
from utils.pagination import Pagination
import json
from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner,PlayBookRunner

def initlist(request):
    '''
    初始化列表
    :param request:
    :return:
    '''
    search=request.GET.get("table_search","")
    init=Init.objects.filter(name__contains=search)
    pages=Pagination(request.GET.get("page",1),init.count(),request.GET.copy(),10)
    return render(request, "init/initlist.html",
                  {"init": init[pages.start:pages.end], "page_html": pages.page_html, "page_title": "初始化列表"})



def create_init(request,pk=0):
    '''
    新增（编辑）初始化
    :param request:
    :param pk:
    :return:
    '''
    init = Init.objects.filter(pk=pk).first()
    form=InitForm(instance=init)
    if request.method=="POST":
        form=InitForm(request.POST,instance=init)
        #print(form.is_valid())
        if form.is_valid():

            #init表中创建者字段定义为当前登录用户
            form.instance.create_user=request.account
            form.save()
            return JsonResponse({"status":0,"msg":"操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request, "init/init_create.html", {"form":form, "pk":pk})


def del_init(request,pk):
    '''
    删除初始化
    :param request:
    :param pk:
    :return:
    '''
    Init.objects.filter(pk=pk).delete()
    return JsonResponse({"status": 0, "msg": "删除成功"})


def create_initlog(request,pk=0):
    '''
    新增初始化日志（负责具体初始化任务）
    :param request:
    :param pk:
    :return:
    '''
    form=InitLogForm()
    if request.method=="POST":
        form=InitLogForm(request.POST)
        if form.is_valid():
            #InitLog表中创建者字段定义为当前登录用户
            form.instance.user=request.account


            #调用playbook函数并传入值
            res=playbook(form.cleaned_data["hosts_list"],form.cleaned_data["init"].play_book)
            #定义InitLog表中result（结果）字段数据
            form.instance.result=res["stats"]

            form.save()
            return JsonResponse({"status":0,"msg":"操作成功"})
        else:
            #格式化报错信息：
            print(form.errors.as_json())
            #{"init": [{"message": "\u6267\u884c\u529f\u80fd\u4e0d\u80fd\u4e3a\u7a7a\uff01", "code": "required"}], "hosts_list": [{"message": "\u6267\u884c\u4e3b\u673a\u4e0d\u80fd\u4e3a\u7a7a\uff01", "code": "required"}]}

            error_list = []
            error = json.loads(form.errors.as_json())  #将报错信息转为字典格式
            print("error",error)
            #{'init': [{'message': '执行功能不能为空！', 'code': 'required'}], 'hosts_list': [{'message': '执行主机不能为空！', 'code': 'required'}]}
            for key, values in error.items():
                INFO = str(key) + ": " + str(values[0]["message"])   #报错信息拼接
                error_list.append(INFO)   #追加到列表中,应用到下面msg字典中👇
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(error_list)})
    return render(request, "init/initlog_create.html", {"form":form, "pk":pk})





def initlog(request,pk):
    '''
    执行详情页面展示
    :param request:
    :param pk: Init表的pk值，这里查询的是InitLog表数据。    InitLog与Init关系： 多对一
    :return:
    '''
    #先通过pk值获取init表对象
    #init=Init.objects.filter(pk=pk).first()

    #反向查询(表名小写后加set):
    #logs=init.initlog_set.all()

    #正向查询:
    #logs=InitLog.objects.filter(init=init)

    #或者:
    logs=InitLog.objects.filter(init__pk=pk)
    return render(request, "init/initlog.html", {"logs":logs})

def playbook(host_list,playbook_path):
    '''
    具体执行初始化功能 返回结果
    根据ansible api TestPlayBookRunner方法
    接收host_list 和 playbook_path 参数

    :param host_list: InitLog表 host_list 字段（多对多关联host表）。在直接获取主机表中相关字段，完成host_data(动态生成主机配置信息)
    :param playbook_path: 执行脚本路径
    :return: 返回执行结果
    '''
    host_data = [
        {
            "hostname": h.name,
            "ip": h.hostip,
            "port": h.ssh_port,
            "username": h.user,
        } for h in host_list
    ]
    inventory = Inventory(host_data)    #动态生成主机配置信息
    runner = PlayBookRunner(inventory).run(playbook_path)   #获取执行结果
    return runner   #返回结果
#
#
# def playbook(host_list,playbook_path):
#     host_data=[{"hostname":h.hostip,"ip":h.hostip,"port":h.ssh_port,"username":h.user} for h in host_list]
#     inventory = Inventory(host_data)  # 动态生成主机配置信息
#     runner= PlayBookRunner(inventory)
#     ret = runner.run(playbook_path)
#     return ret


## 初始化
## 初始化日志 ansible api 去执行playbook


# 实现项目的增删该查


