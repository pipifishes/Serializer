from django.contrib import admin
from .models import *
# 修改title和header
admin.site.site_title = '信息反馈后台系统'
admin.site.site_header = '信息反馈平台'

@admin.register(PersonInfo)
class PersonInfoAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','name','age','hireDate']
    # 再数据列表页右侧，以‘name’为过滤器
    list_filter = ['name']
    # 再数据列表页上方，设置日期选择器
    date_hierarchy = 'hireDate'

@admin.register(Vocation)
class VocationAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','job','title','payment','name']
    # 再数据列表页右侧，以‘job’为过滤器
    list_filter = ['job']
