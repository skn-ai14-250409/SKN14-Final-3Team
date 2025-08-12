import requests
import pandas as pd
import xml.etree.ElementTree as ET

def download_and_save_dart_corp_codes():
    """
    DART에서 제공하는 전체 기업 고유번호 XML을 직접 다운로드하여
    실제 파일 구조에 맞게 파싱하고 CSV 파일로 저장합니다.
    """
    try:
        # 1. DART 고유번호 XML 파일 URL (API 키 불필요)
        url = "https://opendart.fss.or.kr/api/corpCode.xml"
        
        print("DART 고유번호 파일을 다운로드합니다...")
        response = requests.get(url)
        response.raise_for_status() # HTTP 요청이 200 OK가 아니면 에러 발생
        print("다운로드 완료.")

        # 2. 다운로드한 XML 텍스트를 직접 파싱
        print("XML 파싱을 시작합니다...")
        root = ET.fromstring(response.content)
        
        # 3. 데이터를 담을 리스트 초기화
        corp_data = []
        
        # XML의 각 'list' 태그를 순회하며 데이터 추출
        for item in root.findall('list'):
            corp_data.append({
                'corp_code': item.find('corp_code').text,
                'corp_name': item.find('corp_name').text,
                'stock_code': item.find('stock_code').text.strip() if item.find('stock_code').text else '',
                'modify_date': item.find('modify_date').text
            })
            
        print("파싱 완료. DataFrame을 생성합니다.")
        
        if not corp_data:
            print("오류: 파싱된 데이터가 없습니다. DART 응답을 확인해주세요.")
            return None
            
        # 4. 리스트를 Pandas DataFrame으로 변환 후 CSV로 저장
        df_corps = pd.DataFrame(corp_data)
        csv_file_name = 'dart_corp_codes.csv'
        df_corps.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
        
        print(f"\n성공! 총 {len(df_corps)}개의 기업 정보를 '{csv_file_name}' 파일로 저장했습니다.")
        
        return df_corps

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        return None
    except ET.ParseError as e:
        print(f"XML 파싱 오류: 다운로드된 파일이 올바른 XML 형식이 아닙니다. 오류: {e}")
        return None
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return None

# --- 메인 코드 실행 ---
if __name__ == "__main__":
    df = download_and_save_dart_corp_codes()
    
    if df is not None and not df.empty:
        print("\n--- 활용 예시 ---")
        target_corp_name = '삼성전자'
        corp_info = df[df['corp_name'] == target_corp_name]
        if not corp_info.empty:
            corp_code = corp_info.iloc[0]['corp_code']
            print(f"'{target_corp_name}'의 고유번호는 '{corp_code}' 입니다.")