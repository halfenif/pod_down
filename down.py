import os
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from itertools import count
import z_utils

#http://www.podbbang.com/ch/7418


def linkToFile(pid, link, title):
    # Const
    constOutputFolder = './output_response/{pid}/'.format(pid=pid)

    headers = {'Referer': 'http://www.podbbang.com/ch/{pid}'.format(pid=pid)}

    # Folder Safe
    try:
        os.stat(constOutputFolder)
    except:
        os.makedirs(constOutputFolder)

    file_full_path = constOutputFolder + title + '.mp3'
    if os.path.exists(file_full_path):
        print('Exist:', file_full_path)
        return


    mp3_bin = requests.get(link, headers=headers).content

    try:
        with open(file_full_path, 'wb') as f:
            f.write(mp3_bin)
        print('New  : ' + file_full_path)
    except:
        print('File Write Error')

    print('Sleep 5Min')
    time.sleep(300)
    return


def url_call(pid):
    for page in count(1):
        page_url = 'http://www.podbbang.com/podbbangchnew/episode_list'
        params = {'id': pid, 'page': page}

        response = requests.get(page_url, params)
        if response.status_code != 200:
            print('Request Error:', response.status_code)
            return response.status_code
        response.encoding = 'utf-8'
        html = response.text
        #z_utils.strToFile(html, 'podbbang', 'html')

        headers = {'Referer': 'http://www.podbbang.com/ch/{pid}'.format(pid=pid)}
        soup = BeautifulSoup(html, 'html.parser')
        for li_tag in soup.select('li'):
            try:
                title = li_tag.find('dt')['title']
                title = title.replace('/','')
                link = urljoin(page_url, li_tag.find('a')['href'])
                #eid = link.replace('http://www.podbbang.com/download?pid={}&eid='.format(pid),'')

                dd_date = li_tag.find('dd', attrs={"class": "dd_date"}).text.strip()
                title = dd_date + '_' + title
                #print(link, dd_date, title)
                #print(link, title)
                linkToFile(pid, link, title)
            except (TypeError, KeyError):
                print('End')
                return None


    return None

#---------------------------------
# Main Suit
if __name__ == "__main__":
    print('---------------------------------------------------')
    #pid = 7418 #지대넓얍
    #pid = 12757 #송은이 비밀보장
    #pid = 9126 #나는 프로그래머다
    #pid = 487 #POG
    pid = 3709 #빨간책방
    url_call(pid)
