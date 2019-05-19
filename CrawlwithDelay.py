import requests
from bs4 import BeautifulSoup as bs
import time
import random
import sys
from multiprocessing import Pool #병렬처리


start_time = time.time()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}

fp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\CrawlingData_pebble2.txt", 'a', encoding = 'utf8')


def get_links(gall):
    time.sleep(2.5)
    try:
        req = requests.get(gall, headers = headers)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
        
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.find_all('td', {"class" : "gall_tit"})

    for i in my_titles:
        j = i.find('a')
        title = j.get_text()
        ref = j.get('href')
        checkBtag = i.find('b')
        if not (checkBtag is None):
            continue
        if ref == 'javascript:;':
            continue
        fp.write(title)
        link = 'https://gall.dcinside.com' + ref
        time.sleep(2.5)
        try:
            req2 = requests.get(link, headers = headers)
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
        post = req2.text
        soup2 = bs(post, 'html.parser')
        wvb = soup2.select('.writing_view_box')
        if wvb == []:
            fp.write('continue')
            continue       
        paragraph = wvb[0].text
        fp.write(paragraph)

    #fp.write(' '. join(data))
        
#    return data
                           
    

if __name__=='__main__':
    gallery = 'https://gall.dcinside.com/mgallery/board/lists?id=pebble'
    pages = range(1, 1351)
    galleries = []
    result = []

    for page in pages:
        gall = gallery
        link = gall.replace('lists?id', 'lists/?id')
        galleries.append(link+'&page='+str(page))
        print(link+'&page='+str(page))

    pool = Pool(processes = 4)
    result = pool.map(get_links, galleries)

    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
