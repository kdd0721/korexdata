from .get_br_title_info import parsing
from address.serializers import BrTitleInfoSerializer, UnitSerializer, RealtorsSerializer
from address.models import BrTitleInfo, Units, Realtors
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers, viewsets
from .pagination import SidoPageNumberPagination


class BrTitleInfoViewSet(viewsets.ModelViewSet):
    queryset = BrTitleInfo.objects.all()
    serializer_class = BrTitleInfoSerializer

    @action(methods=['get'], detail=False)
    def openapi(self, request):
        sgg_cd = "11680"  # 시군구코드
        bjdong_cd = "10300"  # 법정동코드
        bun = "0012"  # 번
        ji = "0003"  # 지
        info = parsing(sgg_cd, bjdong_cd, bun, ji)
        br_title_info = BrTitleInfo(
            platplc=info['platPlc'],
            sigungucd=sgg_cd,
            bjdongcd=bjdong_cd,
            mgmbldrgstpk=info['mgmBldrgstPk'],
            bun=bun,
            ji=ji,
            archarea=info['archArea'],
            mainpurpscdnm=info['mainPurpsCdNm'],
            grndflrcnt=info['grndFlrCnt'])
        br_title_info.save()
        serializer = BrTitleInfoSerializer(br_title_info)
        return Response(serializer.data)


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Realtors.objects.all()
    serializer_class = RealtorsSerializer
    pagination_class = SidoPageNumberPagination

    @action(methods=['get'], detail=False)
    def sido(self, request):
        qs = Units.objects.filter(level='1')
        serializer = UnitSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def sgg(self, request):
        qs = Units.objects.filter(level='2')
        serializer = UnitSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def road(self, request):
        qs = Units.objects.filter(level='3', realtors_road__isnull=False).distinct()
        serializer = UnitSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def emd(self, request):
        qs = Units.objects.filter(level='4', realtors_emd__isnull=False).distinct()
        serializer = UnitSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def realtors(self, request):
        qs = Realtors.objects.all()
        serializer = RealtorsSerializer(qs, many=True)
        return Response(serializer.data)
