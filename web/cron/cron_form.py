#！/usr/bin/env python
#-*- coding:utf-8 -*-
from web.models import Cron
from utils.auth import NewModelForm
from django.core.exceptions import ValidationError
from django import forms


class CronForm(NewModelForm):

#定义分时日月周 数据格式(这里没有用这种,不好做前端左边屏幕选择后,右边屏幕立刻显示相应的数据：
   #定义分钟格式
    # mi=[]
    # for i in range(60):
    #     mi.append((i,i))
    #     mi.append(("*/{}".format(i),'*/{}'.format(i)))
    # minute=forms.ChoiceField(mi,label="分钟")

   #定义时日月周格式
    # hour=forms.ChoiceField([(i,i) for i in range(24)],label="小时")
    # day=forms.ChoiceField([(i,i) for i in range(1,32)],label="日")
    # month=forms.ChoiceField([(i,i) for i in range(1,13)],label="月")
    # weekday=forms.ChoiceField([(i,i) for i in range(7)],label="周")


    class Meta:
        model=Cron
        #通过这种方式控制页面显示顺序
        #fields=["minute","hour","day","month","weekday","name","hosts_list","job","user","note"]

        #排除以下两个字段（不需要用户添加修改）
        exclude=["time","create_user"]

