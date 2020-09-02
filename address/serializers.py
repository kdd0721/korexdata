from rest_framework import serializers
from address.models import BrTitleInfo, UnitsSido, UnitsSgg, UnitsRoad, UnitsEmd, Units


class BrTitleInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BrTitleInfo
        fields = ['platplc'
                  '', 'sigungucd', 'bjdongcd', 'mgmbldrgstpk', 'archarea', 'grndflrcnt']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'name']


class SggRoadSerializer(serializers.ModelSerializer):
    # children = TestRoadSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField('get_road')

    def get_road(self, units):
        qs = Units.objects.filter(level='3')
        serializer = UnitSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class SidoRoadSerializer(serializers.ModelSerializer):
    children = SggRoadSerializer(many=True, read_only=True)

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class SggEmdSerializer(serializers.ModelSerializer):
    # children = TestRoadSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField('get_emd')

    def get_emd(self, units):
        qs = Units.objects.filter(level='4')
        serializer = UnitSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']


class SidoEmdSerializer(serializers.ModelSerializer):
    children = SggEmdSerializer(many=True, read_only=True)

    class Meta:
        model = Units
        fields = ['id', 'name', 'children']
