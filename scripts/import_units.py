from django.db.models import Max, Count

from address.models import AddrRoad, AddrJibun, Units


def import_sgg():
    sggs = AddrJibun.objects.values('sinm','sggnm').annotate(Max('dongcd'))
    batch_size = 100
    for i, sgg in enumerate(sggs):

        Units.objects.create(
            id=sgg['dongcd__max'][:5],
            level='2',
            sub=Units.objects.get(id=sgg['dongcd__max'][:2]),
            name=sgg['sggnm']
        )
        if i % batch_size == 0:
            print(i)
    print("finish")


def import_road():
    roads = AddrRoad.objects.filter(rnmgtsn__startswith='50').values('rnmgtsn', 'rn').annotate(Count('rn'))
    batch_size = 100
    for i, road in enumerate(roads):
        Units.objects.create(
            id=road['rnmgtsn'],
            level='3',
            sub=Units.objects.get(id=road['rnmgtsn'][:5]),
            name=road['rn']
        )
        if i % batch_size == 0:
            print(i)
    print("finish")


def import_emd():
    emds = AddrJibun.objects.values('dongcd', 'sggnm', 'emdnm').annotate(Count('dongcd'))
    batch_size = 100
    for i, emd in enumerate(emds):
        Units.objects.create(
            id=emd['dongcd'],
            level='4',
            sub=Units.objects.get(id=emd['dongcd'][:5]),
            name=emd['emdnm']
        )
        if i % batch_size == 0:
            print(i)
    print("finish")


def run():
    # import_sgg()
    # import_emd()
    import_road()
