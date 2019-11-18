#！/usr/bin/env python
#-*- coding:utf-8 -*-
from web.models import Host

from utils.auth import NewModelForm
#主动抛出异常
from django.core.exceptions import ValidationError

class HostForm(NewModelForm):


    class Meta:
        model=Host
        fields="__all__"


    #检测hostip是否存在（存在则抛出异常）
    def clean_hostip(self):
        hostip=self.cleaned_data["hostip"] #前端传过来的数据
        print("hostip",hostip)
        # self.instance.hostip 数据库的值
        print("self.instance.hostip",self.instance.hostip)

        host=Host.objects.filter(hostip=hostip)
        #如果没查到hostip对象（hostip不存在）,直接返回hostip数据
        if host.count()==0: return hostip.strip("")
        #如果查到hostip为1（存在），并且前端传来的hostip和当前编辑对象数据库里的hostip一致（不会与其他用户hostip冲突），直接返回hostip数据
        elif host.count()==1 and hostip==self.instance.hostip:
            return hostip.strip("")
        #否则报错
        else:
            raise ValidationError("%s已存在"%hostip)

