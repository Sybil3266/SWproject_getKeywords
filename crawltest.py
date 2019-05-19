# parser.py
import requests
from bs4 import BeautifulSoup as bs
import time


def get_links(gall): # 블로그의 게시글 링크들을 가져옵니다.
    req = requests.get(gall)
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.select(
        'a'
        )
    data = []
    
    for title in my_titles:
        data.append(title.get('href'))
    return data

    
def get_content(gall, link): #def == 함수선언. 호출전에 정의되어있어야함
    abs_link = 'https://gall.dcinside.com' + link
    print(abs_link)
    req = requests.get(abs_link)
    html = req.text
    print(html)
    soup = bs(html, 'html.parser')
    # 가져온 데이터로 뭔가 할 수 있겠죠?
    # 하지만 일단 여기서는 시간만 확인해봅시다.
    print(soup.select('.writing_view_box')[0].text)
    #print(soup.select('h1')[0].text) # 첫 h1 태그를 봅시다.

if __name__=='__main__':
    gallery = input('갤러리 링크 : ')
    pages = [1,2]
    for page in pages:
        print(page)
        gall = gallery
        gall = gall+'&page='+str(page)
        print(gall)
        for link in get_links(gall):
                get_content(gall, link)

    print('FINISHED')
