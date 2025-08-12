import requests
import pandas as pd
import os
from dotenv import load_dotenv

def download_financial_data(corp_code, start_year, end_year):
    """
    .env 파일에서 API 키를 사용하여 특정 기업의 지정된 기간 동안의 재무 데이터를 수집합니다.
    """
    # .env 파일에서 환경 변수를 로드합니다.
    load_dotenv()
    
    # 환경 변수에서 API 키를 가져옵니다.
    API_KEY = os.getenv("dart_corp_api_key")
    
    # API 키가 로드되었는지 확인합니다.
    if not API_KEY:
        print("오류: .env 파일에서 'dart_corp_api_key'를 찾을 수 없습니다.")
        print(".env 파일을 확인해주세요.")
        return None

    all_financial_data = []
    print(f"\n{corp_code} 기업의 {start_year}년부터 {end_year}년까지 재무 데이터를 수집합니다.")

    for year in range(start_year, end_year + 1):
        print(f"-> {year}년 데이터 처리 중...")
        url = (
            f"https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
            f"crtfc_key={API_KEY}"
            f"&corp_code={corp_code}"
            f"&bsns_year={year}"
            f"&reprt_code=11011"
            f"&fs_div=CFS"
        )
        try:
            response = requests.get(url)
            data = response.json()

            if data['status'] == '000' and data['list']:
                all_financial_data.extend(data['list'])
                print(f"   {year}년 데이터 수집 완료.")
            else:
                print(f"   API 오류 또는 데이터 없음: {data.get('message', 'N/A')}")
        except Exception as e:
            print(f"   요청 중 오류 발생: {e}")

    if all_financial_data:
        df = pd.DataFrame(all_financial_data)
        file_name = f"{corp_code}_financials_{start_year}_{end_year}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"\n모든 데이터 수집 완료! '{file_name}' 파일로 저장되었습니다.")
        return df
    else:
        print("\n수집된 데이터가 없습니다.")
        return None

# --- 메인 코드 실행 ---
if __name__ == "__main__":
    # 예시: 삼성전자의 5년치 데이터 다운로드
    # 이 코드를 실행하기 전에 dart_corp_codes.csv 파일이 있어야 합니다.
    # 또는 고유번호를 직접 알고 있다면 바로 사용할 수 있습니다.
    
    target_corp_code = "00126380"  # 삼성전자
    target_start_year = 2021
    target_end_year = 2025
    
    download_financial_data(target_corp_code, target_start_year, target_end_year)
    
    # 다른 기업 예시: SK하이닉스 (00066381)
    # download_financial_data("00066381", 2019, 2023)