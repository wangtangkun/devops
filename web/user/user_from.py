#！/usr/bin/env python
#-*- coding:utf-8 -*-
from web.models import UserProfile
#from utils.auth import NewModelForm
from django.forms import ModelForm
#主动抛出异常
from django.core.exceptions import ValidationError

class UserForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})
    class Meta:
        model=UserProfile
        fields="__all__"

        #定义报错
        error_messages = {
            "password": {
                'required': '密码必填！',
            },
            "email":{
                'required': '邮箱必填！',
            }
        }


    #检测邮箱是否存在（存在则抛出异常）
    def clean_email(self):
        email=self.cleaned_data["email"] #前端传过来的数据
        print("email",email)
        # self.instance.email 数据库的值
        print("self.instance.email",self.instance.email)

        user=UserProfile.objects.filter(email=email)
        #如果没查到email对象（email不存在）,直接返回email数据
        if user.count()==0: return email.strip("")
        #如果查到email为1（存在），并且前端传来的email和当前编辑对象数据库里的email一致（不会与其他用户email冲突），直接返回email数据
        elif user.count()==1 and email==self.instance.email:
            return email.strip("")
        #否则报错
        else:
            raise ValidationError("邮箱已存在")

