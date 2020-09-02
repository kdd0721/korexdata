from django.db import models

# Create your models here.


class Address(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'address'


class AddrRoad(models.Model):
    rnmgtsn = models.CharField(db_column='rnMgtSn', primary_key=True, max_length=12)  # 도로명코드
    rn = models.CharField(db_column='rn', max_length=80)  # 도로명
    rneng = models.CharField(db_column='rnEng', max_length=80)  # 도로명로마자
    emdno = models.CharField(db_column='emdNo', max_length=2)  # 읍면동일련번호
    sinm = models.CharField(db_column='siNm', max_length=20)  # 시도명
    sinmeng = models.CharField(db_column='siNmEng', max_length=40)  # 시도로마자
    sggnm = models.CharField(db_column='sggNm', max_length=20)  # 시군구명
    sggnmeng = models.CharField(db_column='sggNmEng', max_length=40)  # 시군구로마자
    emdnm = models.CharField(db_column='emdNm', max_length=20, blank=True, null=True)  # 읍면동명
    emdnmeng = models.CharField(db_column='emdNmEng', max_length=40, blank=True, null=True)  # 읍면동로마자
    emddiv = models.CharField(db_column='emdDiv', max_length=1)  # 읍면동구분 - 0:읍면, 1:동, 2:미부여
    emdcd = models.CharField(db_column='emdCd', max_length=3, blank=True, null=True)  # 법정동 기준 읍면동코드
    usage = models.CharField(db_column='usage', max_length=1)  # 사용여부 - 0:사용, 1:미사용
    chgrsn = models.CharField(db_column='chgRsn', max_length=1, blank=True, null=True)  # 변경사유 - 0:도로명변경, 1:도로명폐지, 2:시도시군구변경, 3:읍면동변경, 4:영문도로명변경, 9:기타
    chginfo = models.CharField(db_column='chgInfo', max_length=14, blank=True, null=True)  # 변경이력정보 - 도로명코드(12)+읍면동일련번호(2) 신규 정보일 경우 "신규"로 표시
    ntcdate = models.CharField(db_column='ntcDate', max_length=8, blank=True, null=True)  # 고시일자 - YYYYMMDD
    expdate = models.CharField(db_column='expDate', max_length=8, blank=True, null=True)  # 고시일자 - YYYYMMDD

    class Meta:
        managed = False
        db_table = 'addr_road'
        unique_together = (('rnmgtsn', 'emdno'),)


class AddrInfo(models.Model):
    bdmgtsn = models.CharField(db_column='bdMgtSn', primary_key=True, max_length=25)  # 관리번호
    rnmgtsn = models.ForeignKey('AddrRoad', on_delete=models.CASCADE, related_name='rnmgtsn_info', db_column='rnMgtSn')  # 도로명코드
    emdno = models.ForeignKey('AddrRoad', on_delete=models.CASCADE, related_name='emdno_info', db_column='emdNo')  # 읍면동일련번호
    udrtyn = models.CharField(db_column='udrtYn', max_length=1)  # 지하여부 - 0:지상, 1:지하
    buldmnnm = models.IntegerField(db_column='buldMnnm')  # 건물본번
    buldslno = models.IntegerField(db_column='buldSlno')  # 건물부번
    areano = models.CharField(db_column='areaNo', max_length=5)  # 기초구역번호
    chgrsncd = models.CharField(db_column='chgRsnCd', max_length=2, blank=True, null=True)  # 변경사유코드 - 31:신규, 34:변경, 63:폐지
    ntcdate = models.CharField(db_column='ntcDate', max_length=8, blank=True, null=True)  # 고시일자
    stnmbfr = models.CharField(db_column='stNmBfr', max_length=25, blank=True, null=True)  # 변경전도로명주소
    addrstus = models.CharField(db_column='addrStus', max_length=1)  # 상세주소부여 여부 - 0:미부여, 1:부여

    class Meta:
        managed = False
        db_table = 'addr_info'


class AddrJibun(models.Model):
    bdmgtsn = models.OneToOneField('AddrInfo', on_delete=models.CASCADE, db_column='bdMgtSn', primary_key=True)  # 관리번호
    srlno = models.IntegerField(db_column='srlNo')  # 일련번호
    dongcd = models.CharField(db_column='dongCd', max_length=10, blank=True, null=True)  # 법정동코드
    sinm = models.CharField(db_column='siNm', max_length=20, blank=True, null=True)  # 시도명
    sggnm = models.CharField(db_column='sggNm', max_length=20, blank=True, null=True)  # 시군구명
    emdnm = models.CharField(db_column='emdNm', max_length=20, blank=True, null=True)  # 법정읍면동명
    linm = models.CharField(db_column='liNm', max_length=20, blank=True, null=True)  # 법정리명
    mtyn = models.CharField(db_column='mtYn', max_length=1, blank=True, null=True)  # 산여부 - 0:대지, 1:산
    lnbrmnnm = models.IntegerField(db_column='lnbrMnnm', blank=True, null=True)  # 지번본번(번지)
    lnbrslno = models.IntegerField(db_column='lnbrSlno', blank=True, null=True)  # 지번부번(호)
    repyn = models.CharField(db_column='repYn', max_length=1, blank=True, null=True)  # 대표여부 - 0:관련지번, 1:대표지번

    class Meta:
        managed = True
        db_table = 'addr_jibun'
        unique_together = (('bdmgtsn', 'srlno'),)

    def split_dong_cd(self):
        return self.dongcd[:5], self.dongcd[5:]


class AddrAddinfo(models.Model):
    bdmgtsn = models.OneToOneField('AddrInfo', on_delete=models.CASCADE, db_column='bdMgtSn', primary_key=True)  # 관리번호
    hjdongcd = models.CharField(db_column='hjdongCd', max_length=10, blank=True, null=True)  # 행정동코드
    hjdongnm = models.CharField(db_column='hjdongNm', max_length=20, blank=True, null=True)  # 행정동이름
    zipno = models.CharField(db_column='zipNo', max_length=5, blank=True, null=True)  # 우편번호
    zipsrlno = models.CharField(db_column='zipSrlNo', max_length=3, blank=True, null=True)  # 우편번호일련번호
    lrgdlvry = models.CharField(db_column='lrgDlvry', max_length=40, blank=True, null=True)  # 다량배달처명
    bdrgstrbdnm = models.CharField(db_column='bdRgstrBdNm', max_length=40, blank=True, null=True)  # 건축물대장 건물명
    sggbdnm = models.CharField(db_column='sggBdNm', max_length=40, blank=True, null=True)  # 시군구 건물명
    bdkdcd = models.CharField(db_column='bdKdcd', max_length=1, blank=True, null=True)  # 공동주택여부 - 0:비공동주택, 1:공동주택

    class Meta:
        managed = True
        db_table = 'addr_addinfo'


class BrTitleInfo(models.Model):
    platplc = models.CharField(db_column='platPlc', max_length=200)  # 대지위치
    sigungucd = models.CharField(db_column='sigunguCd', max_length=5)  # 시군구코드
    bjdongcd = models.CharField(db_column='bjdongCd', max_length=5)  # 법정동코드
    bun = models.CharField(db_column='bun', max_length=4)  # 번
    ji = models.CharField(db_column='ji', max_length=4)  # 지
    mgmbldrgstpk = models.CharField(db_column='mgmBldrgstPk', primary_key=True, max_length=33)  # 관리건축물대장PK
    archarea = models.CharField(db_column='archArea', max_length=45, blank=True, null=True)  # 건축면적
    grndflrcnt = models.IntegerField(db_column='grndFlrCnt', blank=True, null=True)  # 지상층수

    class Meta:
        managed = False
        db_table = 'br_title_info'

    def get_dong_cd(self):
        return "%s%s" % (self.sigungucd, self.bjdongcd)


class UnitsSido(models.Model):
    sidocd = models.IntegerField(db_column='sidoCd', primary_key=True)  # Field name made lowercase.
    sinm = models.CharField(db_column='siNm', max_length=20)  # Field name made lowercase.
    sinmeng = models.CharField(db_column='siNmEng', max_length=40)  # Field name made lowercase.
    treeord = models.IntegerField(db_column='treeOrd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'units_sido'


class UnitsSgg(models.Model):
    sggcd = models.IntegerField(db_column='sggCd', primary_key=True)  # Field name made lowercase.
    sidocd = models.ForeignKey('UnitsSido', related_name='sgg', db_column='sidoCd', on_delete=models.CASCADE)  # Field name made lowercase.
    sggnm = models.CharField(db_column='sggNm', max_length=20)  # Field name made lowercase.
    sggnmeng = models.CharField(db_column='sggNmEng', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'units_sgg'


class UnitsRoad(models.Model):
    roadcd = models.IntegerField(db_column='roadCd', primary_key=True)  # Field name made lowercase.
    sggcd = models.ForeignKey('UnitsSgg', related_name='road', db_column='sggCd', on_delete=models.CASCADE)  # Field name made lowercase.
    roadnm = models.CharField(db_column='roadNm', max_length=20)  # Field name made lowercase.
    roadnmeng = models.CharField(db_column='roadNmEng', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'units_road'


class UnitsEmd(models.Model):
    emdcd = models.IntegerField(db_column='emdCd', primary_key=True)  # Field name made lowercase.
    sggcd = models.ForeignKey('UnitsSgg', related_name='emd', db_column='sggCd', on_delete=models.CASCADE)  # Field name made lowercase.
    emdnm = models.CharField(db_column='emdNm', max_length=20)  # Field name made lowercase.
    emdnmeng = models.CharField(db_column='emdNmEng', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'units_emd'


class Units(models.Model):
    id = models.CharField(db_column='id', max_length=12, primary_key=True)
    level = models.CharField(max_length=1, blank=True, null=True)
    sub = models.ForeignKey('self', models.DO_NOTHING, db_column='sub', related_name='children', blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units'
