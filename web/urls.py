#！/usr/bin/env python
#-*- coding:utf-8 -*-
from django.conf.urls import url
from web.user.user import *

from web.host.host import *
from web.init.init import *
from web.views import *
from web.project.project import *
from web.command.command import *
from web.cron.cron import  *
urlpatterns = [
    url(r'^index/',index,name="index"),
    url(r'^login/',login,name="login"),
    #url(r'^create_host/',create_host,name="create_host"),
    #用户信息
    url(r'^userlist/',userlist,name="userlist"),
    url(r'^create_user/',create_edit_user,name="create_user"),
    url(r'^edit_user/(\d+)$',create_edit_user,name="edit_user"),
    url(r'^del_user/(\d+)$',del_user,name="del_user"),
    #主机信息
    url(r'^hostlist/',Hostlist,name="hostlist"),
    url(r'^create_host/',Create_edit_host,name="create_host"),
    url(r'^edit_host/(\d+)$',Create_edit_host,name="edit_host"),
    url(r'^del_host/(\d+)$',del_host,name="del_host"),
    # init信息
    url(r'^initlist/$', initlist, name="initlist"),
    url(r'^createinit/$', create_init, name="create_init"),
    url(r'^editinit/(\d+)$', create_init, name="edit_init"),
    url(r'^delinit/(\d+)$', del_init, name="del_init"),
    # init log
    url(r'^createlog/$', create_initlog, name="create_log"),
    url(r'^logslist/(\d+)$', initlog, name="logslist"),

    #项目信息
    url(r'^projectlist/',Projectlist,name="project_list"),
    url(r'^create_project/',Create_edit_project,name="create_project"),
    url(r'^edit_project/(\d+)$',Create_edit_project,name="edit_project"),
    url(r'^del_project/(\d+)$',del_project,name="del_project"),

    #命令下发,展示,详情
    url(r'^command_list/$', command_list, name="command_list"),
    url(r'^command_issued/',command_issued,name="command_issued"),
    url(r'^command_details/(\d+)$',command_details,name="command_details"),

    # #定时任务
    url(r'^create_cron/', Create_edit_cron, name="create_cron"),
    url(r'^edit_cron/(\d+)$', Create_edit_cron, name="edit_cron"),
    url(r'^cron_list/$', cron_list, name="cron_list"),
    url(r'^delcron/(\d+)$', del_cron, name="del_cron"),
    url(r'^delcron/(\d+)$', del_cron, name="del_cron"),
]
