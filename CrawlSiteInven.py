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
path = "C:\\Users\sybil\OneDrive\Documents\GitHub\SWproject_getKeywords\hsinvennews.txt"
fp = open(path, 'w', encoding = 'utf8')

print("File is successly opened!")

def get_links(gall):
    time.sleep(1)
    try:
        req = requests.get(gall, headers = headers)
    except requests.exceptions.ConnectionError:
        print("exception link : %s", gall)
        req.status_code = "Connection refused"
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.find_all('span', {"class" : "title"})
    data = []

    for i in my_titles:
        j = i.find('a')
        
        if not(i.find('b') is None) and not(i.find('strong') is None):
            continue

        #title = j.get_text()
        ref = j.get('href')

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
        data.append(soup2.select('#imageCollectDiv')[0].text)
        
    fp.write(' '. join(data))
    print("Writing Success")

        
#    return data
                           
    

if __name__=='__main__':
    gallery = 'http://www.inven.co.kr/webzine/news/?site=hs'
    pages = [8, 11, 10, 14, 10, 18, 15, 18, 13]
    galleries = []
    premonth = range(1,10)
    print("start crawling " + gallery + "...")
    for i in premonth:
        for page in pages:
            val = range(1, page)
            for i in val:
                galleries.append(gallery+'&page='+str(page)+"&premonth="+str(i))
                

    #for link in galleries:
    #    get_links(link)

    pool = Pool(processes = 2)
    result = pool.map(get_links, galleries)

    fp.close()             
    print('=== Time : %s sec ===' %(time.time() - start_time))
