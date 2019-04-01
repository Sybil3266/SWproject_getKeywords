# parser.py
import requests
from bs4 import BeautifulSoup as bs
import time

start_time = time.time()

def get_links(gall): # 블로그의 게시글 링크들을 가져옵니다.
    req = requests.get(gall)
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.find_all('td', {"class" : "gall_tit"})
    
    data = []
    hrefs = []
    for i in my_titles:
        j = i.find('a')
        title = j.get_text()
        data.append(title)
        ref = j.get('href')

        print(ref)
        link = 'https://gall.dcinside.com' + ref
        req2 = requests.get(link)
        post = req2.text
        soup2 = bs(post, 'html.parser')
        data.append(soup2.select('.writing_view_box')[0].text)
    return data
                           
    

if __name__=='__main__':
    gallery = input('갤러리 링크 : ')
    pages = [1]
    fp = open("C:\\users\\user\Downloads\직렬test2.txt", 'w', encoding = 'utf8')
    for page in pages:
        print(page)
        gall = gallery
        link = gall.replace('lists?id', 'lists/?id')
        gall = link+'&page='+str(page)
        print(gall)
        result = get_links(gall)
        fp.write(' '.join(result))
    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
