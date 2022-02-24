from django.db import models

'''
模型是指django通过一定的规则来映射数据库，从而方便django与数据库之间实现数据交互，这个交互过程是在视图里实现的
月份视图日期视图测试，需要重新定义models

模型：定义字段，重写__str__，Meta选项，是定义模型的基本要素
verbose_name:默认为None,在admin站点管理设置字段的显示名称
定义模型时，一般情况下都会重写__str__,这是设置模型的返回值
'''

class PersonInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    hireDate = models.DateField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='人员信息'
        # 将admin后台显示的名称下的模型名称后的’s‘去掉
        verbose_name_plural = '人员信息'

# 再定义一个模型Vocation
class Vocation(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    # 新增payment字段
    payment = models.IntegerField(null=True,blank=True)
    name = models.ForeignKey(PersonInfo,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name='职业信息'
        # 将admin后台显示的名称下的模型名称后的’s‘去掉
        verbose_name_plural = '职业信息'