from django.db.models.functions import Length
from django.shortcuts import render
from .get_br_title_info import parsing
from address.serializers import BrTitleInfoSerializer, SidoRoadSerializer, SidoEmdSerializer
from address.models import BrTitleInfo, Units
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers, viewsets


class BrTitleInfoViewSet(viewsets.ModelViewSet):
    queryset = BrTitleInfo.objects.all()
    serializer_class = BrTitleInfoSerializer

    @action(methods=['get'], detail=False)
    def openapi(self, request):
        sgg_cd = "11680"  # 시군구코드
        bjdong_cd = "10300"  # 법정동코드
        bun = "0012"  # 번
        ji = "0004"  # 지
        info = parsing(sgg_cd, bjdong_cd, bun, ji)
        br_title_info = BrTitleInfo(
            platplc=info['platPlc'],
            sigungucd=sgg_cd,
            bjdongcd=bjdong_cd,
            mgmbldrgstpk=info['mgmBldrgstPk'],
            bun=bun,
            ji=ji,
            archarea=info['archArea'],
            grndflrcnt=info['grndFlrCnt'])
        br_title_info.save()
        serializer = BrTitleInfoSerializer(br_title_info)
        return Response(serializer.data)

"""
class RoadViewSet(viewsets.ModelViewSet):
    queryset = UnitsSido.objects.all()
    serializer_class = RoadSerializer


class EmdViewSet(viewsets.ModelViewSet):
    queryset = UnitsSido.objects.all()
    serializer_class = EmdSerializer
"""


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Units.objects.filter(level='1')
    serializer_class = SidoRoadSerializer

    @action(methods=['get'], detail=False)
    def road(self, request):
        qs = Units.objects.filter(level='1')
        serializer = SidoRoadSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def emd(self, request):
        qs = Units.objects.filter(level='1')
        serializer = SidoEmdSerializer(qs, many=True)
        return Response(serializer.data)

