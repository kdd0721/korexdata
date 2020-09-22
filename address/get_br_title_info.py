import requests
import xmltodict


# items model def로 선언하기
def parsing(sgg_cd, bjdong_cd, bun, ji):
    # public api settings
    key = "hR1c9PXeUu2s6g0W0KyWCDzf6LJz810huqBy9f6mt6qclvP8G4F3MZV%2FKr52W%2FSss%2BIto1locQn5snYAkY60wg%3D%3D"
    url = "http://apis.data.go.kr/1611000/BldRgstService/getBrTitleInfo?sigunguCd="+sgg_cd\
        +"&bjdongCd="+bjdong_cd\
        +"&bun="+bun\
        +"&ji="+ji\
        +"&ServiceKey="+key

    req = requests.get(url).content
    xml_object = xmltodict.parse(req)

    all_data = xml_object['response']['body']['items']['item']

    return all_data
