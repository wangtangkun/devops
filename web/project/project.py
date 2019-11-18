from django.shortcuts import render
from .project_form import ProjectForm
from django.http.response import JsonResponse
from web.models import Project,UserProfile
#分页
from utils.pagination import Pagination
import json
from utils.ansible2.inventory import Inventory
from utils.ansible2.runner import AdHocRunner,PlayBookRunner

def Projectlist(request):
    '''
    项目列表
    :param request:
    :return:
    '''
    search=request.GET.get("table_search","")
    project=Project.objects.filter(name__contains=search)
    pages=Pagination(request.GET.get("page",1),project.count(),request.GET.copy(),10)
    return render(request, "project/projectlist.html",
                  {"projects": project[pages.start:pages.end], "page_html": pages.page_html, "page_title": "项目列表"})



def Create_edit_project(request,pk=0):
    '''
    新增（编辑）项目
    :param request:
    :param pk:
    :return:
    '''
    project = Project.objects.filter(pk=pk).first()
    form=ProjectForm(instance=project)
    if request.method=="POST":
        form=ProjectForm(request.POST,instance=project)
        #print(form.is_valid())
        if form.is_valid():

            #project表中创建者字段定义为当前登录用户
            form.instance.create_user=request.account
            form.save()
            return JsonResponse({"status":0,"msg":"操作成功"})
        else:
            return JsonResponse({"status": 1, "msg": "操作失败,失败原因为{}".format(form.errors)})
    return render(request, "project/create_project.html", {"form":form, "pk":pk})


def del_project(request,pk):
    '''
    删除项目
    :param request:
    :param pk:
    :return:
    '''
    Project.objects.filter(pk=pk).delete()
    return JsonResponse({"status": 0, "msg": "删除成功"})




def playbook(host_list,playbook_path):
    '''
    具体执行项目功能 返回结果
    根据ansible api TestPlayBookRunner方法
    接收host_list 和 playbook_path 参数

    :param host_list: ProjectLog表 host_list 字段（多对多关联host表）。在直接获取主机表中相关字段，完成host_data(动态生成主机配置信息)
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

