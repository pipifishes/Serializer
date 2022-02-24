from django.urls import path
from .views import ind

from .views import createview_new,result_new
from .views import montharchiveview
from .views import weekarchiveview

from .views import form_basic
from .views import form_modelview

from .views import vocationClass,vocationDef
from .views import vocation2Class,vocation2Def
from .views import vocation3Class,vocation3Def
'''
1. 若使用视图类turnTo处理http请求，需要使用as_view()方法，这是对视图类进行实例化处理
2. 修改视图和删除视图如果都是设置成n.html，这样我们在网页上测试的时候，可能会有问题
我们既然不能在n.html前加一个静态路径，那么就修改为n.html1;n.html2
'''

urlpatterns = [
    # 首页地址
    path('',ind,name='inda'),    #  这里设置name，为了在模板文件中，写name，就能找到这个路由


    # 为新表添加数据
    path('createview_new/', createview_new.as_view(), name='createviewer_new'),
    path('createview_new/result_new/', result_new, name='resulter_new'),

    # 月份视图MonthArchiveView
    path('<int:year>/<int:month>.html_new/',montharchiveview.as_view(),name='month'),

    # 周期视图WeekArchiveView
    path('<int:year>/<int:week>.html_week/',weekarchiveview.as_view(),name='week'),

    # form定义路由函数，显示在首页中
    path('form_basic/',form_basic,name='formbasic'),

    # modelform定义路由函数，显示在首页中
    path('form_modelview/', form_modelview, name='formmodelbasic'),

    # 自定义序列化类Serializer,视图函数开发API接口
    path('mydef/',vocationDef,name='myDef'),
    # 自定义序列化类Serializer,视图类开发API接口
    path('myclass/',vocationClass.as_view(),name='myclass'),

    # 模型序列化类ModelSerializer,视图函数开发API接口
    path('mydef2/', vocation2Def, name='myDef2'),
    # 模型序列化类ModelSerializer,视图类开发API接口
    path('myclass2/', vocation2Class.as_view(), name='myclass2'),

    # 序列化的嵌套使用,视图函数开发API接口
    path('mydef3/', vocation3Def, name='myDef3'),
    # 序列化的嵌套使用,视图类开发API接口
    path('myclass3/', vocation3Class.as_view(), name='myclass3'),

]