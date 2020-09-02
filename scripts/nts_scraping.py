import requests
import xml.etree.ElementTree as ElementTree
import win32clipboard
"""
<map id=\"ATTABZAA001R08\">
  <pubcUserNo/>
  <mobYn>N</mobYn>
  <inqrTrgtClCd>1</inqrTrgtClCd>
  <txprDscmNo>3051577349</txprDscmNo>
  <dongCode>15</dongCode>
  <psbSearch>Y</psbSearch>
  <map id=\"userReqInfoVO\"/>
</map>

<map id='' >
    <map id='resultMsg' >
        <detailMsg></detailMsg>
        <msg></msg>
        <code></code>
        <result>S</result>
    </map>
    <trtEndCd>Y</trtEndCd>
    <smpcBmanEnglTrtCntn>The business registration number is registered</smpcBmanEnglTrtCntn>
    <nrgtTxprYn>N</nrgtTxprYn>
    <smpcBmanTrtCntn>등록되어 있는 사업자등록번호 입니다. </smpcBmanTrtCntn>
    <trtCntn>부가가치세 일반과세자 입니다.</trtCntn>
</map>

<map id='' >
    <map id='resultMsg' >
        <detailMsg></detailMsg>
        <msg></msg>
        <code></code>
        <result>S</result>
    </map>
    <trtEndCd>Y</trtEndCd>
    <smpcBmanEnglTrtCntn>The business registration number is not registered</smpcBmanEnglTrtCntn>
    <nrgtTxprYn>Y</nrgtTxprYn>
    <smpcBmanTrtCntn>등록되어 있지 않은 사업자등록번호 입니다. </smpcBmanTrtCntn>
    <trtCntn>사업을 하지 않고 있습니다.</trtCntn>
</map>
"""
PostUrl = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
XmlRaw = "<map id=\"ATTABZAA001R08\"><pubcUserNo/><mobYn>N</mobYn><inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>\{CRN\}</txprDscmNo><dongCode>15</dongCode><psbSearch>Y</psbSearch><map id=\"userReqInfoVO\"/></map>"


def call(crn):
    res = requests.post(PostUrl, data=XmlRaw.replace("\{CRN\}", crn), headers={'Content-Type': 'text/xml'})
    xml = ElementTree.fromstring(res.text).findtext("smpcBmanTrtCntn")
    result = crn + "\t" + xml.replace("\n", "").replace("\t", " ") + "\n"
    return result


def run():
    num = ['3051577349', '1111111111', '3051577349', '8995800075', '8996300123', '8997600079', '8997700057', '1010540144', '1010863774', '1011127195', '1011230533', '1011268892', '1011275340', '1011652137', '1012151049', '1020361041', '1021551153']

    result = ""

    for idx, value in enumerate(num):
        result += call(value)

    result = result.strip()
    print(result)
