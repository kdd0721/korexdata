import logging

from address.models import AddrRoad, AddrInfo, AddrJibun, AddrAddinfo
import pymysql


def import_addr_road(filename):

    r = open(filename, mode='rt')
    batch_size = 100
    print(filename)

    for i, line in enumerate(r):
        row = line.strip().split('|')
        addr_road = AddrRoad.objects.filter(rnmgtsn=row[0], emdno=row[3])
        if len(addr_road):
            AddrRoad.objects.filter(rnmgtsn=row[0], emdno=row[3]).update(
                rn=row[1],
                rneng=row[2],
                sinm=row[4],
                sinmeng=row[5],
                sggnm=row[6],
                sggnmeng=row[7],
                emdnm=row[8],
                emdnmeng=row[9],
                emddiv=row[10],
                emdcd=row[11],
                usage=row[12],
                chgrsn=row[13],
                chginfo=row[14],
                ntcdate=row[15],
                expdate=row[16]
            )
        else:
            AddrRoad.objects.create(
                rnmgtsn=row[0],
                rn=row[1],
                rneng=row[2],
                emdno=row[3],
                sinm=row[4],
                sinmeng=row[5],
                sggnm=row[6],
                sggnmeng=row[7],
                emdnm=row[8],
                emdnmeng=row[9],
                emddiv=row[10],
                emdcd=row[11],
                usage=row[12],
                chgrsn=row[13],
                chginfo=row[14],
                ntcdate=row[15],
                expdate=row[16]
            )
        if i % batch_size == 0:
            print(i)

    r.close()
    print("finish")


def import_addr_info(filename):
    r = open(filename, mode='rt')
    batch_size = 100
    print(filename)

    for i, line in enumerate(r):
        row = line.strip().split('|')
        print(row[0])
        addr_road = AddrRoad(rnmgtsn=row[1], emdno=row[2])
        try:
            addr_info = AddrInfo.objects.get(bdmgtsn=row[0])
            addr_info.rnmgtsn = addr_road
            addr_info.emdno = addr_road
            addr_info.udrtyn = row[3]
            addr_info.buldmnnm = row[4]
            addr_info.buldslno = row[5]
            addr_info.areano = row[6]
            addr_info.chgrsncd = row[7]
            addr_info.ntcdate = row[8]
            addr_info.stnmbfr = row[9]
            addr_info.addrstus = row[10]
            addr_info.save()

        except AddrInfo.DoesNotExist:
            AddrInfo.objects.create(
                bdmgtsn=row[0],
                rnmgtsn_id=addr_road,
                emdno_id=addr_road,
                udrtyn=row[3],
                buldmnnm=row[4],
                buldslno=row[5],
                areano=row[6],
                chgrsncd=row[7],
                ntcdate=row[8],
                stnmbfr=row[9],
                addrstus=row[10]
            )

        if i % batch_size == 0:
            print(i)

    r.close()
    print("finish")


def import_addr_jibun(filename):
    r = open(filename, mode='rt')
    batch_size = 100
    print(filename)

    for i, line in enumerate(r):
        row = line.strip().split('|')
        addr_info = AddrInfo(bdmgtsn=row[0])
        addr_jibun = AddrJibun.objects.filter(bdmgtsn=addr_info, srlno=row[1])

        if len(addr_jibun):
            AddrJibun.objects.filter(bdmgtsn=addr_info, srlno=row[1]).update(
                dongcd=row[2],
                sinm=row[3],
                sggnm=row[4],
                emdnm=row[5],
                linm=row[6],
                mtyn=row[7],
                lnbrmnnm=row[8],
                lnbrslno=row[9],
                repyn=row[10]
            )

        else:
            AddrJibun.objects.create(
                bdmgtsn=addr_info,
                srlno=row[1],
                dongcd=row[2],
                sinm=row[3],
                sggnm=row[4],
                emdnm=row[5],
                linm=row[6],
                mtyn=row[7],
                lnbrmnnm=row[8],
                lnbrslno=row[9],
                repyn=row[10],
            )

        if i % batch_size == 0:
            print(i)

    r.close()
    print("finish")


def import_addr_addinfo(filename):
    r = open(filename, mode='rt')
    batch_size = 100
    print(filename)

    for i, line in enumerate(r):
        row = line.strip().split('|')
        addr_info = AddrInfo(bdmgtsn=row[0])
        try:
            addr_addinfo = AddrAddinfo.objects.get(bdmgtsn=addr_info)
            addr_addinfo.hjdongcd = row[1]
            addr_addinfo.hjdongnm = row[2]
            addr_addinfo.zipno = row[3]
            addr_addinfo.zipsrlno = row[4]
            addr_addinfo.lrgdlvry = row[5]
            addr_addinfo.bdrgstrbdnm = row[6]
            addr_addinfo.sggbdnm = row[7]
            addr_addinfo.bdkdcd = row[8]
            addr_addinfo.save()

        except AddrAddinfo.DoesNotExist:
            AddrAddinfo.objects.create(
                bdmgtsn=addr_info,
                hjdongcd=row[1],
                hjdongnm=row[2],
                zipno=row[3],
                zipsrlno=row[4],
                lrgdlvry=row[5],
                bdrgstrbdnm=row[6],
                sggbdnm=row[7],
                bdkdcd=row[8]
            )
        if i % batch_size == 0:
            print(i)

    r.close()
    print("finish")


def run():
    # import_addr_road('C:/Users/daeun/Desktop/openAPI/20200823_dailymatchingdata/AlterD.JUSUMT.20200824.MATCHING_ROAD.txt')
    import_addr_info('C:/Users/daeun/Desktop/openAPI/20200824_dailymatchingdata/AlterD.JUSUMT.20200825.MATCHING_JUSO.txt')
    # import_addr_jibun('C:/Users/daeun/Desktop/openAPI/20200823_dailymatchingdata/AlterD.JUSUMT.20200824.MATCHING_JIBUN.TXT')
    # import_addr_addinfo('C:/Users/daeun/Desktop/openAPI/20200823_dailymatchingdata/AlterD.JUSUMT.20200824.MATCHING_JIBUN.TXT')

