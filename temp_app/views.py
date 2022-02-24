from django.shortcuts import render
from django.http import Http404


'''
HttpResponse工作原理是将文件读取并载入内存，然后输出到浏览器上实现下载功能
StreamingHttpResponse,FileResponse，两者都是将下载的文件分批写入本地磁盘

视图类（class）实现视图功能，完成http的请求与响应处理
将网址首页的视图函数比如ind，basic改为了视图类，自定义视图类basic继承视图类TemplateView，并重设了4个属性，重写两个方法

ListView是实现网页和数据库之间的数据交互
CreateView是对模型新增数据的视图类，在listview的基础上加入数据新增的功能
'''

# 设置响应方式
def ind(request):
    value = {'title':'hello django'}
    content = {'title': 'hello xiaozhu'}
    return render(request,'index.html',locals())


# 页面异常响应
def page_not_found(request,ecception):
    return render(request,'404.html',status=404)
def page_error(request):
    return render(request,'500.html',status=500)

# 测试页面异常响应返回结果
def test(request):
    # request.Get是获取请求信息
    if request.GET.get('error',''):
        raise Http404("page does not exist")
    else:
        return render(request,'index.html')



from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.dates import MonthArchiveView
from .models import PersonInfo
from django.views.generic.dates import WeekArchiveView

# 再次用新增视图CreateView来给新建模型生成表里（temp_app_personinfo）数据
def result_new(request):
    return HttpResponse('success_new')

class createview_new(CreateView):
    initial = {'name':'Lala','age':'21','hireDate':'2019-01-01'}
    template_name = 'createview_new.html'
    success_url = '../createview_new/result_new'
    # 表单生成方式一,局限性大
    # form_class = PersonInfoForm
    # 表单生成方式二
    model = PersonInfo
    # field设置模型字段，从而生成表单字段
    fields = ['name','age','hireDate']
    extra_context = {'title':'人员信息表'}


# 月份视图MonthArchiveView实现数据筛选功能
class montharchiveview(MonthArchiveView):
    allow_empty = True
    allow_future = True
    # 如不设置，则模板上下文默认为personinfo
    context_object_name = 'mylist'
    template_name = 'montharchiveview.html'
    model = PersonInfo
    date_field = 'hireDate'
    queryset = PersonInfo.objects.all()
    year_format = '%Y'
    # month_format默认值为%b,支持英文日期，如Oct
    month_format = '%m'
    # 每页展示多少条数据
    paginate_by = 50

# 周期视图WeekArchiveView实现数据筛选功能
class weekarchiveview(WeekArchiveView):
    allow_empty = True
    allow_future = True
    # 如不设置，则模板上下文默认为personinfo
    context_object_name = 'weeklist'
    template_name = 'weekarchiveview.html'
    model = PersonInfo
    date_field = 'hireDate'
    queryset = PersonInfo.objects.all()
    year_format = '%Y'
    # week_format默认值为%U
    week_format = '%W'
    # 每页展示多少条数据
    paginate_by = 50


from .form import VocationForm
from .form import VocationForm_modelform
from .models import Vocation
from .form import VocationForm_modelformview

# form定义路由函数，显示在网页上
# def form_basic(request):
#     v = VocationForm()
#     # 添加一条，源码分析form,表单优化
#     v_form = VocationForm_form()
#     return render(request, 'form_basic.html', locals())

# 重写form_basic函数， 验证优化后的表单是否正确
def form_basic(request):
    # GET请求
    if request.method == 'GET':
        v_modelform = VocationForm_modelform()
        return render(request, 'form_basic.html', locals())
    # POST请求
    else:
        v_modelform = VocationForm_modelform(request.POST)
        if v_modelform.is_valid():
            # 获取网页控件的数据
            title = v_modelform['title']
            return  HttpResponse('提交成功')
        else:
            # 获取错误信息，并以json格式输出
            error_msg = v_modelform.errors.as_json()
            print(error_msg)
            return render(request, 'form_basic.html', locals())


# 视图里使用表单modelForm和模型实现数据交互
# 相当于重写上面的form_basic函数，我们不想修改上面的函数，所有重新写一个函数
def form_modelview(request):
    # GET请求
    if request.method == 'GET':
        id = request.GET.get('id','')
        if id:
            i = Vocation.objects.filter(id=id).first()
            # 将参数i传入表单VocationForm_modelformview执行实例化
            v = VocationForm_modelformview(instance=i,prefix='vv')
        else:
            v = VocationForm_modelformview(prefix='vv')
        return render(request,'form_modelformview.html',locals())
    # post请求
    else:
        # 由于在GET请求设置了参数prefix
        # 因此实例化时必须设置参数prefix,否则无法获取POST的数据
        v = VocationForm_modelformview(data=request.POST,prefix='vv')
        # is_vaild()会使字段payment自增加10
        if v.is_valid():
            # 将数据更新到模型VocationForm_modelformview
            id = request.GET.get('id')
            result = Vocation.objects.filter(id=id)
            # 若数据不存在，则新增数据
            if not result:
                # 数据保存方法一：直接将数据保存到数据库
                # v.save()
                # 数据保存方法二；将save的参数commit=False,生成数据库对象v1，修改v1的属性值并保存
                v1 = v.save(commit=False)
                v1.title = '初级' + v1.title
                v1.save()
                # 数据保存方法三：save_m2m()保存MantToMany的数据模型
                # v.save_m2m()
                return HttpResponse('新增成功')

            # 若数据存在，则修改数据
            else:
                d = v.cleaned_data
                d['title'] = '中级'+ d['title']
                result.update(**d)
                return HttpResponse('修改成功')

        else:
            error_msg = v.errors.as_json()
            print(error_msg)
            return render(request, 'form_modelformview.html', locals())


from .models import PersonInfo,Vocation
from .serializers import MySerializer,VocationSerializer,nesting_PersonInfoSerializer,nesting_VocationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
'''
1. 路由mydef对应视图函数vocationDef,它以视图函数的方式使用MySerializer实现模型Vocation的API接口;
如使用视图函数开发API接口，则必须对视图函数使用修饰器api_view
2. 路由myclass对应视图类vocationClass,它以视图类的方式使用MySerializer实现模型Vocation的API接口;
如使用视图类，则必须继承父类APIView
3. 视图函数vocationDef和视图类vocationClass实现的功能是一致的；
'''
# 自定义序列化类Serializer,视图函数开发API接口
@api_view(['GET','POST'])
def vocationDef(request):
    if request.method == 'GET':
        q = Vocation.objects.all()
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request)
        # 将分页后的数据传递给MySerializer,生成JSON数据对象
        serializer = MySerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)
    elif request.method == 'POST':
        # 获取请求数据
        data = request.data
        id = data['name']
        data['name'] = PersonInfo.objects.filter(id =id).first()
        instance = Vocation.objects.filter(id =data.get('id',0))
        if instance:
            # 修改数据
            MySerializer().update(instance,data)
        else:
            # 创建数据
            MySerializer().create(data)
        return Response('Done',status=status.HTTP_201_CREATED)

# 自定义序列化类Serializer,视图类开发API接口
class vocationClass(APIView):
    # Get请求
    def get(self,request):
        q = Vocation.objects.all()
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request,view=self)
        # 将分页后的数据传递给MySerializer,生成JSON数据对象
        serializer = MySerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)

    # POST请求
    def post(self,request):
        data = request.data
        id = data['name']
        data['name'] = PersonInfo.objects.filter(id =id).first()
        instance = Vocation.objects.filter(id =data.get('id',0))
        if instance:
            # 修改数据
            MySerializer().update(instance,data)
        else:
            # 创建数据
            MySerializer().create(data)
        return Response('Done',status=status.HTTP_201_CREATED)

# 模型序列化类ModelSerializer,视图函数开发API接口
@api_view(['GET','POST'])
def vocation2Def(request):
    if request.method == 'GET':
        q = Vocation.objects.all().order_by('id')
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request)
        # 将分页后的数据传递给VocationSerializer,生成JSON数据对象
        serializer = VocationSerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)
    elif request.method == 'POST':
        # 获取请求数据
        id = request.data.get('id',0)
        # 判断请求参数id在模型Vocation中是否存在
        # 若存在，则执行数据修改：否则新增数据
        operation = Vocation.objects.filter(id=id).first()
        # 数据验证
        serializer = VocationSerializer(data=request.data)
        if serializer.is_valid():
            if operation:
                data = request.data
                id = data['name']
                data['name'] = PersonInfo.objects.filter(id=id).first()
                serializer.update(operation,data)
            else:
                # 保存到数据库
                serializer.save()
            # 返回对象Response由Django Rest Framework实现
            return Response(serializer.data)
        return Response(serializer.errors,status=404)

# 模型序列化类ModelSerializer,视图类开发API接口
class vocation2Class(APIView):
    # Get请求
    def get(self,request):
        q = Vocation.objects.all().order_by('id')
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request,view=self)
        # 将分页后的数据传递给VocationSerializer,生成JSON数据对象
        serializer = VocationSerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)

    # POST请求
    def post(self,request):
        # 获取请求数据
        id = request.data.get('id',0)
        # 判断请求参数id在模型Vocation中是否存在
        # 若存在，则执行数据修改：否则新增数据
        operation = Vocation.objects.filter(id=id).first()
        # 数据验证
        serializer = VocationSerializer(data=request.data)
        if serializer.is_valid():
            if operation:
                data = request.data
                id = data['name']
                data['name'] = PersonInfo.objects.filter(id=id).first()
                serializer.update(operation, data)
            else:
                # 保存到数据库
                serializer.save()
            # 返回对象Response由Django Rest Framework实现
            return Response(serializer.data)
        return Response(serializer.errors, status=404)

# 序列化的嵌套使用，视图函数开发API接口
@api_view(['GET','POST'])
def vocation3Def(request):
    if request.method == 'GET':
        q = Vocation.objects.all().order_by('id')
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request)
        # 将分页后的数据传递给nesting_VocationSerializer,生成JSON数据对象
        serializer = nesting_VocationSerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)
    elif request.method == 'POST':
        # 获取请求数据
        id = request.data.get('id',0)
        # 判断请求参数id在模型Vocation中是否存在
        # 若存在，则执行数据修改：否则新增数据
        operation = Vocation.objects.filter(id=id).first()
        # 数据验证
        serializer = nesting_VocationSerializer(data=request.data)
        if serializer.is_valid():
            if operation:
                serializer.update(operation,request.data)
            else:
                # 保存到数据库
                serializer.save()
            # 返回对象Response由Django Rest Framework实现
            return Response(serializer.data)
        return Response(serializer.errors,status=404)

# 序列化的嵌套使用，视图类开发API接口
class vocation3Class(APIView):
    # Get请求
    def get(self,request):
        q = Vocation.objects.all().order_by('id')
        # 分页查询，需要在setting.py中设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        p = pg.paginate_queryset(queryset=q,request=request,view=self)
        # 将分页后的数据传递给nesting_VocationSerializer,生成JSON数据对象
        serializer = nesting_VocationSerializer(instance=p,many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)

    # POST请求
    def post(self,request):
        # 获取请求数据
        id = request.data.get('id',0)
        # 判断请求参数id在模型Vocation中是否存在
        # 若存在，则执行数据修改：否则新增数据
        operation = Vocation.objects.filter(id=id).first()
        # 数据验证
        serializer = nesting_VocationSerializer(data=request.data)
        if serializer.is_valid():
            if operation:
                serializer.update(operation, request.data)
            else:
                # 保存到数据库
                serializer.save()
            # 返回对象Response由Django Rest Framework实现
            return Response(serializer.data)
        return Response(serializer.errors, status=404)