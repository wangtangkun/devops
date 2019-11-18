from web.models import Project,UserProfile
from utils.auth import NewModelForm


class ProjectForm(NewModelForm):
    '''
    初始化
    '''
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        #页面通过部门选择人员时，部门只显示此部门的人
        self.fields["dev_user"].choices=[(du.pk,du.name) for du in UserProfile.objects.filter(role="0")]
        self.fields["test_user"].choices=[(tu.pk,tu.name) for tu in UserProfile.objects.filter(role="1")]
        self.fields["ops_user"].choices=[(ou.pk,ou.name) for ou in UserProfile.objects.filter(role="2")]

    #self.fields 表中所有字段  格式:字典  字段名:字段数据对象
    # 如果说model里面存在的字段,则需要写在__init__方法里面
    # 如果说是新增的字段,则要写在__init__外面

    class Meta:
        model=Project
        fields="__all__"


# class InitLogForm(NewModelForm):
#     '''
#     初始化日志（负责具体初始化任务）
#     '''
#     class Meta:
#         model=InitLog
#         fields=["init","hosts_list"]
#
#         # 定义报错
#         error_messages = {
#             "init": {
#                 'required': '执行功能不能为空！',
#             },
#             "hosts_list": {
#                 'required': '执行主机不能为空！',
#             }
#         }