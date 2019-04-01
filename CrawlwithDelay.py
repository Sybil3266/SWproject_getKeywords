import requests
from bs4 import BeautifulSoup as bs
import time
import random
import sys
from multiprocessing import Pool #병렬처리

start_time = time.time()
fp = open("C:\\users\\user\Downloads\병렬test2.txt", 'a', encoding = 'utf8')

def get_links(gall):
    time.sleep(1.5)
    req = requests.get(gall)
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.find_all('td', {"class" : "gall_tit"})
    
    data = []
    hrefs = []
    for i in my_titles:
        j = i.find('a')
        title = j.get_text()
        ref = j.get('href')
        if ref == 'javascript:;':
            continue
        data.append(title)
        link = 'https://gall.dcinside.com' + ref
        time.sleep(1.5)
        req2 = requests.get(link)
        post = req2.text
        soup2 = bs(post, 'html.parser')
        data.append(soup2.select('.writing_view_box')[0].text)

    fp.write(' '. join(data))
        
#    return data
                           
    

if __name__=='__main__':
    gallery = input('갤러리 링크 : ')
    pages = range(1, 751)
    galleries = []
    result = []

    for page in pages:
        gall = gallery
        link = gall.replace('lists?id', 'lists/?id')
        galleries.append(link+'&page='+str(page))
        print(link+'&page='+str(page))


    pool = Pool(processes = 8)
    result = pool.map(get_links, galleries)

    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
