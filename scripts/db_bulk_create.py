from django.core.exceptions import ObjectDoesNotExist
import os
from address.models import AddrRoad, AddrInfo, AddrJibun, AddrAddinfo


def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        read_file(full_filename)


def read_file(filename):
    r = open(filename, mode='rt')
    bulk_list = []
    batch_size = 10000
    print(filename)
    for i, line in enumerate(r):
        row = line.strip().split('|')

        bulk_list.append(
            AddrInfo(
                bdmgtsn=row[0],
                rnmgtsn=row[1],
                emdno=row[2],
                udrtyn=row[3],
                buldmnnm=row[4],
                buldslno=row[5],
                areano=row[6],
                chgrsncd=row[7],
                ntcdate=row[8],
                stnmbfr=row[9],
                addrstus=row[10]
            )
        )
        if i % batch_size == 0:
            AddrInfo.objects.bulk_create(bulk_list)
            print(i)
            bulk_list = []

    AddrInfo.objects.bulk_create(bulk_list)

    r.close()
    print("finish")


def run():
    # read_file('C:/Users/daeun/Desktop/openAPI/db/addr_info/주소_경상남도.txt')
    search('C:/Users/daeun/Desktop/openAPI/db/addr_info')
    # search('C:/Users/daeun/Desktop/openAPI/db/addr_jibun')
    # search('C:/Users/daeun/Desktop/openAPI/db/addr_addinfo')

"""

            AddrRoad(
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
                expdate=row[16],
            )
            
            AddrInfo(
                bdmgtsn=row[0],
                rnmgtsn=row[1],
                emdno=row[2],
                udrtyn=row[3],
                buldmnnm=row[4],
                buldslno=row[5],
                areano=row[6],
                chgrsncd=row[7],
                ntcdate=row[8],
                stnmbfr=row[9],
                addrstus=row[10]
            )
            
            AddrJibun(
                bdmgtsn=row[0],
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
                chgrsncd=row[11]
                
            )
            
            AddrAddinfo(
                bdmgtsn=row[0],
                hjdongcd=row[1],
                hjdongnm=row[2],
                zipno=row[3],
                zipsrlno=row[4],
                lrgdlvry=row[5],
                bdrgstrbdnm=row[6],
                sggbdnm=row[7],
                bdkdcd=row[8],
                chgrsncd=row[9]
            )
"""