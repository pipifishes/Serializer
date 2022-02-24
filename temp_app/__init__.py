from django.apps import AppConfig
import os
'''
1. 修改app在admin后台显示的名称
2. 将admin后台显示的名称下的模型名称后的’s‘去掉
'''

# default_app_config的值来自apps.py的类名
default_app_config = 'temp_app.TempAppConfig'

# 获取当前APP的命名
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

# 重写类TempAppConfig
class TempAppConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '展示模型'