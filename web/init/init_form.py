from web.models import Init,InitLog
from utils.auth import NewModelForm


class InitForm(NewModelForm):
    '''
    初始化
    '''
    class Meta:
        model=Init
        exclude=["create_user"]


class InitLogForm(NewModelForm):
    '''
    初始化日志（负责具体初始化任务）
    '''
    class Meta:
        model=InitLog
        fields=["init","hosts_list"]

        # 定义报错
        error_messages = {
            "init": {
                'required': '执行功能不能为空！',
            },
            "hosts_list": {
                'required': '执行主机不能为空！',
            }
        }