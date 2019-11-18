from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from web import models
from django import forms
from django.forms import ModelForm
class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info.startswith('/admin/'):
            return
        if request.path_info in [reverse('login')]:
            return
        # 获取用户ID
        try:
            user_pk = request.session.get("user")["id"]
        except TypeError:
            # 如果不存在跳转到登录页面
            return redirect(reverse('login'))

        #通过用户ID 获取用户对象
        user = models.UserProfile.objects.filter(pk=user_pk).first()
        #给request赋值
        request.account = user

class Response(MiddlewareMixin):
    def process_template_response(self,request,reponse):
        reponse.context_data.update({"user":request.account})
        return reponse


class NewModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(NewModelForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})