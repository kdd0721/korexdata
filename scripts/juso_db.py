import urllib.request
import os


#요청 url을 변수로 지정
url = "http://update.juso.go.kr/updateInfo.do?app_key=인증키" \
      "&date_gb=D&retry_in&cntc_cd=009000&req_dt=20180202&req_dt=20180203"
u = urllib.request.urlopen(url)

while True:

    # 파일 순번 존재 확인
    file_seq = u.read(2)

    # 파일 순번 미존재 시 종료
    if not file_seq:
        break

    # 수신정보 저장
    file_base_dt = u.read(8)
    file_name = u.read(50).strip().decode()
    file_size = int(u.read(10))
    res_code = u.read(5)
    req_code = u.read(6)
    replay = u.read(1)
    create_dt = u.read(8).decode()

    # 파일 다운로드 경로 지정
    outpath = "C:/Users/daeun/Desktop/openAPI/db" + create_dt[2:8] + "/"

    # 파일 다운로드 폴더 생성
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    # zip파일 데이터 읽기 & 쓰기
    zip_file = u.read(file_size + 10)
    f = open(outpath + file_name, 'wb')
    f.write(zip_file)
    f.close()
