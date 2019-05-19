import requests
from bs4 import BeautifulSoup as bs
import time
import random
import sys
from multiprocessing import Pool #병렬처리

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}

start_time = time.time()
fp = open("C:\\users\\user\Downloads\crawldata_temp.txt", 'w', encoding = 'utf8')
print("File is successly opened!")

def get_links(gall):
    time.sleep(1)
    print("start crawling %s ...", gall)
    try:
        req = requests.get(gall, headers = headers)
    except requests.exceptions.ConnectionError:
        print("exception link : %s", gall)
        req.status_code = "Connection refused"
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.find_all('td', {"class" : "bbsSubject"})
    data = []
    
    for i in my_titles:
        j = i.find('a')
        
        if not(i.find('b') is None) and not(i.find('strong') is None):
            continue

        #title = j.get_text()
        ref = j.get('href')
        #if ref == 'javascript:;':
        #    continue
        #data.append(title)
        #fp.write(title)
        #link = 'https://gall.dcinside.com' + ref
        time.sleep(1)
        try:
            req2 = requests.get(ref, headers = headers)
        except requests.exceptions.ConnectionError:
            print("exception link : %s", ref)
            req2.status_code = "Connection refused"
        post = req2.text
        soup2 = bs(post, 'html.parser')
        #fp.write(soup2.select('.writing_view_box')[0].text)
        data.append(soup2.select('h1')[0].text)
        data.append(soup2.select('#powerbbsContent')[0].text)
        
    fp.write(' '. join(data))
    print("Writing Success")
        
#    return data
                           
    

if __name__=='__main__':
    gallery = 'http://www.inven.co.kr/board/hs/3509'
    pages = range(1, 1701)
    galleries = []
    result = []
    print("start crawling " + gallery + "...")
    for page in pages:
        gall = gallery
        galleries.append(gall+'?sort=PID&p='+str(page))

    for link in galleries:
        get_links(link)

    #pool = Pool(processes = 4)
    #result = pool.map(get_links, galleries)

    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
