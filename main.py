import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def infoget(name,info_list,author,serial_list):
    info_str = ""
    print(type(name))
    if(info_list[0]=="레드"):
        info_list[0]="Red"
    elif(info_list[0]=="옐로"):
        info_list[0]="Yellow"
    elif(info_list[0]=="그린"):
        info_list[0]="Green"
    elif(info_list[0]=="레드 믹스"):
        info_list[0]="Red Mix"
    elif(info_list[0]=="옐로 믹스"):
        info_list[0]="Yellow Mix"
    elif(info_list[0]=="그린 믹스"):
        info_list[0]="Green Mix"
    info_str = (
        "CardName: " + str(name) + "\n" +
        "Illustrator: " + author + "\n" +
        "Cost: " + str(info_list[0]) + "\n" +
        "Level: " + str(info_list[1]) + "\n" +
        "HP: " + str(info_list[2]) + "\n" +
        "Number: " + str(serial_list[0]) + "\n" +
        "Rank: " + str(serial_list[1]) + "\n" +
        "Kind: " + str(serial_list[2])
    )
    return info_str

# 웹 페이지의 URL 설정
url = "https://cookierunbraverse.com/cardList"

base_url = "https://cookierunbraverse.com"

# 해당 URL에서 페이지 내용 가져오기
response = requests.get(url)

# 페이지 내용을 BeautifulSoup로 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 카드 목록을 담고 있는 부분을 식별
card_list = soup.find('div', id='card-section')

# 각 카드에 대한 정보를 추출
cards = card_list.find_all('div', class_='one_fifth')

# 각 카드의 정보와 이미지 다운로드
for card in cards:
    card_name = card.find('a', class_='card_open')['href']
    card_name = card_name.split("/")[-1]# URL에서 카드 이름 추출
    
    ############################################################ 카드 정보 url
    inurl = urljoin(base_url,"card/"+card_name)
    # 해당 URL에서 페이지 내용 가져오기
    response2 = requests.get(inurl)

    # 페이지 내용을 BeautifulSoup로 파싱
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    
    trap = soup2.find('div',class_='card_select_trap')
    
    wrapper = trap.find('div',class_='item__stage').find('div',class_='txt_wrapper')
    ############################################################## 타이틀 구역
    title_area = wrapper.find('div',class_="title_area")
    cardname = title_area.find('div',class_="card_title").text.strip()
    author = title_area.find('div',class_="author_area").find_all('span', class_='author')
    serial_get = title_area.find('div',class_="serial").find_all('span',class_=None)
    
    serial_list = []
    for serial in serial_get:
        serial_list.append(serial.text.strip())
    
    ############################################################ 인포
    info_area = wrapper.find('div',id = 'info')
    flex_list = info_area.find_all('div',class_='flex_container')
    info_list = []
    for flex in flex_list:
         info_wrapper = flex.find_all('div',class_='info_wrapper')
         for info in info_wrapper:
             info_list.append(info.find('span',class_='info_a').text.strip())
    
    desc_list = []
    info_desc = info_area.find_all('strong')
    for info in info_desc:
        desc_list.append(info.text.strip())
    print(desc_list)
    if 'FLIP' in desc_list:
        serial_list[2] = "FLIP"
    
    ########################################################### 카드정보 url
    ########info_list,cardname,author,serial
    
    
    card_name = card_name.replace("-", "_")  # 카드 이름에서 하이픈을 언더스코어로 변경
   
    # 카드 이미지 URL 추출
    image_tag = card.find('img')
    if image_tag:
        image_url_relative = image_tag['src']
        image_url_absolute = urljoin(base_url, image_url_relative)
        
        # 이미지 다운로드
        image_response = requests.get(image_url_absolute)
        if image_response.status_code == 200:
            with open(os.path.join("card_images", f"{card_name+'_'+serial_list[0]}.jpg"), 'wb') as image_file:
                image_file.write(image_response.content)
                print(f"{card_name} 이미지 다운로드 완료")
            with open(os.path.join("card_info", f"{card_name}정보.txt"), 'w',encoding='utf-8') as text_file:
                author_text = "\n".join([author_element.text.strip() for author_element in author])
                text_file.write(infoget(name=cardname, author=author_text, info_list=info_list, serial_list=serial_list))
                print(f"{card_name} 이미지 다운로드 완료")
        else:
            print(f"{card_name} 이미지 다운로드 실패")
    else:
        print(f"{card_name} 이미지를 찾을 수 없습니다.")

    print("카드 이름:", card_name)
    print("-" * 50)