from django import forms
from .models import PersonInfo
from django.core.exceptions import ValidationError
from .models import Vocation
'''
表单的作用是实现网页上的数据交互
模型表单是将模型字段转换成表单字段，由表单字段生成的HTML控件，从而生成网页表单
模型表单的作用是实现表单数据和模型数据之间的交互开发

模型表单VocationForm可分为3大部分：添加模型外得表单字段，模型与表单的关联设置，自定义表单字段payment的数据清洗函数
模型表单ModelForm比表单Form新增了数据保存方法save()
'''
# 最简单的表单
class VocationForm(forms.Form):
    job = forms.CharField(max_length=20,label='职位')
    title = forms.CharField(max_length=20,label='职称')
    payment = forms.IntegerField(label='薪资')
    # 设置下拉框的值
    # 查询PersonInfo的数据
    value = PersonInfo.objects.values('name')
    # 将数据以列表形式表示，列表元素为元组格式
    chname = [(i+1,v['name']) for i ,v in enumerate(value)]
    # 表单字段设为ChoiceField类型，以生成下拉框
    person = forms.ChoiceField(choices=chname,label='姓名')


# 源码分析form,表单优化
# 自定义数据验证函数
def payment_validate(value):
    if value>30000:
        raise ValidationError('请输入合理的薪资')

class VocationForm_form(forms.Form):
    job = forms.CharField(max_length=20, label='职位')
    # 设置字段参数widget,error_messages
    title = forms.CharField(max_length=20, label='职称',
                            widget=forms.widgets.TextInput(attrs={'class':'cl'}),
                            error_messages={'required':'职称不能为空'},)
    # 设置字段参数validators
    payment = forms.IntegerField(label='薪资',validators=[payment_validate])

    # 设置下拉框的值
    # 查询PersonInfo的数据
    value = PersonInfo.objects.values('name')
    # 将数据以列表形式表示，列表元素为元组格式
    chname = [(i + 1, v['name']) for i, v in enumerate(value)]
    # 表单字段设为ChoiceField类型，以生成下拉框
    person = forms.ChoiceField(choices=chname, label='姓名')

    #自定义表单字段title的数据清洗
    def clean_title(self):
        # 获取字段title的值
        data = self.cleaned_data['title']
        return '初级'+ data


# 源码分析modelform
class VocationForm_modelform(forms.ModelForm):
    # 添加模型外的表单字段
    LEVEL = (('L1','初级'),('L2','中级'),('L3','高级'))
    level = forms.ChoiceField(choices=LEVEL,label='级别')

    # 模型与表单设置
    class Meta:
        # 绑定模型
        model = Vocation
        # fields属性用于设置转换字段
        # ‘__all__’是将全部模型字段转换成表单字段
        # fields = '__all__'
        # exclude用于禁止模型字段转换成表单字段
        exclude = []

        # lables设置html元素控件的label标签
        labels = {'job':'职位','title':'职称','payment':'薪资','person':'姓名'}
        # 设置widgets，设置表单字段的CSS样式
        widgets = {'job':forms.widgets.TextInput(attrs={'class':'cl'})}

        # 重新定义字段类型
        # 一般情况下模型字段会自动转换成表单字段
        field_classws = {'job':forms.CharField}
        # 帮助提示信息
        help_texts = {'job':'请输入职业名称'}

        # 自定义错误信息
        error_message = {
            # __all__设置全部错误信息
            '__all__':{'required':'请输入内容','invalid':'请检查输入内容'},
            # 设置某个字段的错误信息
            'title':{'required':'请输入职称','invalid':'请检查职称是否正确'},
        }

    # 自定义表单字段payment的数据清洗
    def clean_payment(self):
        # 获取字段payment的值
        data = self.cleaned_data['payment']+1
        return  data


# 视图里使用ModelForm
'''
和源码分析modelform不一样，再视图中使用modelform是没有添加模型外的表单字段
'''
class VocationForm_modelformview(forms.ModelForm):
    class Meta:
        # 绑定模型
        model = Vocation
        # fields属性用于设置转换字段,‘__all__’是将全部模型字段转换成表单字段
        fields = '__all__'
        # lables设置html元素控件的label标签
        labels = {'job':'职位','title':'职称','payment':'薪资','person':'姓名'}
        # 自定义错误信息
        error_message = {
            # __all__设置全部错误信息
            '__all__': {'required': '请输入内容', 'invalid': '请检查输入内容'}}

        # 自定义表单字段payment的数据清洗
        def clean_payment(self):
            # 获取字段payment的值
            data = self.cleaned_data['payment'] + 1000
            return data
