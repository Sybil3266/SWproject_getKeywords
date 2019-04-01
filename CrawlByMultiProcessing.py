import requests
from bs4 import BeautifulSoup as bs
import time
import ssl

from multiprocessing import Pool #병렬처리

start_time = time.time()
context = ssl._create_unverified_context()
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def get_links(gall):
    req = requests.get(gall, headers=headers)
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
        if ref == 'javascript:;':
            continue        
        link = 'https://gall.dcinside.com' + ref
        print(link)
        req2 = requests.get(link, headers=headers)
        post = req2.text
        soup2 = bs(post, 'html.parser')
        data.append(soup2.select('.writing_view_box')[0].text)
    return data
                           
    

if __name__=='__main__':
    gallery = input('갤러리 링크 : ')
    pages = [1,2,3,4,5,6,7,8]
    galleries = [];
    result = [];
    fp = open("C:\\users\\user\Downloads\병렬test2.txt", 'w', encoding = 'utf8')

    for page in pages:
        gall = gallery
        link = gall.replace('lists?id', 'lists/?id')
        galleries.append(link+'&page='+str(page))
        print(link+'&page='+str(page))


    pool = Pool(processes = 8)
    result = pool.map(get_links, galleries)

    for data in result:
        fp.write(' '. join(data))
    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
