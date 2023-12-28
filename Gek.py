import os
import json

# 특정 디렉토리 경로
input_directory = './card_info'

# 데이터를 저장할 리스트 초기화
data_list = []

# 디렉토리 내 모든 파일에 대해 처리
for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):  # 텍스트 파일만 처리
        file_path = os.path.join(input_directory, filename)

        # 텍스트 파일 읽어와서 JSON 데이터로 변환
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            new_text_data = txt_file.read()

        # 텍스트 데이터를 딕셔너리로 파싱 (이 예제에서는 텍스트를 줄 단위로 파싱)
        new_data = {}
        lines = new_text_data.strip().split('\n')
        for line in lines:
            key, value = map(str.strip, line.split(':', 1))
            new_data[key] = value

        # 데이터 리스트에 추가
        data_list.append(new_data)

# 데이터 리스트를 JSON 파일에 저장
with open('cookie_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, indent=4)

print("새로운 데이터가 추가되었습니다.")
