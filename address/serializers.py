from rest_framework import serializers
from address.models import BrTitleInfo, Units, Realtors
from rest_framework_recursive.fields import RecursiveField
from drf_serializer_cache import SerializerCacheMixin
from django.db.models import Q, F


class BrTitleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrTitleInfo
        fields = '__all__'


class RealtorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtors
        # fields = ['biz_name', 'biz_tel', 'rep_name', 'rep_tel', 'sggnm', 'bdmgtsn', 'dongcd', 'rnmgtsn',
        #           'addr_raw', 'full_addr_jibun', 'full_addr_rn']
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'sub', 'name']


############################################################################################


class FilterdRoadListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(level='3', realtors_road__isnull=False).values().distinct()
        return super(FilterdRoadListSerializer, self).to_representation(data)


class UnitRoadSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilterdRoadListSerializer
        model = Units
        fields = ['id', 'name']


class SggRoadSerializer(serializers.ModelSerializer):
    children = UnitRoadSerializer(many=True, read_only=True)
    # children = serializers.SerializerMethodField('get_road')

    # def get_road(self, units):
    #     qs = Units.objects.filter(level='3')
    #     serializer = UnitSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class SidoRoadSerializer(serializers.ModelSerializer):
    children = SggRoadSerializer(many=True, read_only=True)

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class FilterdEmdListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(level='4', realtors_emd__isnull=False).values().distinct()
        return super(FilterdEmdListSerializer, self).to_representation(data)


class UnitEmdSerializer(serializers.ModelSerializer):
    # realtors_emd = RealtorsSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterdEmdListSerializer
        model = Units
        fields = ['id', 'name']



class SggEmdSerializer(serializers.ModelSerializer):
    children = UnitEmdSerializer(many=True, read_only=True)
    # children = serializers.SerializerMethodField('get_emd')

    # def get_emd(self, units):
    #     qs = Units.objects.filter(level='4', sub='11110')
    #     serializer = UnitSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class SidoEmdSerializer(serializers.ModelSerializer):
    # children = SggEmdSerializer(many=True, read_only=True)
    # children = serializers.ListField(child=RecursiveField())
    # children = serializers.SerializerMethodField()

    class Meta:
        model = Units
        fields = ['id', 'sub', 'name']



