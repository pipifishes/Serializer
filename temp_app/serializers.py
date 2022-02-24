from rest_framework import serializers
from .models import PersonInfo,Vocation
'''
该文件用于定义Django Rest Framework的序列化类,将使用DRF快速开发API
1.序列化类Serializer定义的字段必须与模型字段相互契合
2.模型序列化类ModelSerializer与模型完美结合，无须开发者定义序列化字段（就很方便）
3.序列化的嵌套使用，比如模型1和模型2的数据组合存在在同一个json数据中，两个模型的数据通过外键字段name关联
'''
# 自定义序列化类Serializer
# values方法，数据以列表返回，列表元素以字典表示
nameList = PersonInfo.objects.values('name').all()
NAME_CHOICES = [item['name'] for item in nameList]
# 设置模型Vocation的字段name的下拉内容
class MySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    job = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    payment = serializers.CharField(max_length=100)
    # 模型Vocation的字段name是外键字段，它指向模型PersonInfo,因此可用PrimaryKeyRelatedField
    name = serializers.PrimaryKeyRelatedField(queryset=nameList)

    # 重写cerate函数，将API数据保存到数据表temp_app_vocation
    def create(self,validated_data):
        return Vocation.objects.create(**validated_data)
    # 重写update函数，将API数据更新到数据表temp_app_vocation
    def update(self,instance,validated_data):
        return instance.update(**validated_data)

# 模型序列化类ModelSerializer
class VocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocation
        fields = '__all__'
        # fields=('id','job','title','payment','name')




# 序列化的嵌套使用
# 定义ModelSerializer类
class nesting_PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonInfo
        fields = '__all__'
# 定义ModelSerializer类
class nesting_VocationSerializer(serializers.ModelSerializer):
    name = nesting_PersonInfoSerializer()
    class Meta:
        model = Vocation
        # fields = '__all__'
        fields = ('id', 'job', 'title', 'payment', 'name')

        def create(self,validated_data):
            # 从validated_data中获取模型PersonInfo的数据
            name = validated_data.get('name','')
            id = name.get('id',0)
            p = PersonInfo.objects.filter(id=id).first()
            # 根据id判断模型PersonInfo是否存在数据对象，如存在数据对象，则只对Vocation新增数据；
            # 若不存在，则先对模型PersonInfo新增数据，再对模型Vocation新增数据
            if not p:
                p = PersonInfo.objects.create(**name)
            data = validated_data
            data['name'] = p
            v = Vocation.objects.create(**data)
            return v

        def update(self,instance,validated_data):
            # 从validated_data中获取模型PersonInfo的数据
            name = validated_data.get('name','')
            id = name.get('id',0)
            p = PersonInfo.objects.filter(id=id).first()
            # 判断外键name是否存在模型PersonInfo
            if p:
                # 若存在，则先更新模型PersonInfo的数据
                PersonInfo.objects.filter(id=id).update(**name)
                # 再更新模型Vocation的数据
                data = validated_data
                data['name']=p
                id= validated_data.get('id','')
                v = Vocation.objects.filter(id=id).update(**data)
                return v

