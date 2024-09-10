import requests
from retry import retry
import parsel
import os
from concurrent.futures import ThreadPoolExecutor
import threading

url = 'https://wxzmh.top/chapter/26568'
path = 'Z:\Bili'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
pool = ThreadPoolExecutor(100)

@retry(tries=50)
def get_html(url):
    response = requests.get(url=url, headers=headers, timeout=(3, 7)).text
    # print(response)
    return parsel.Selector(response)


@retry()
def save(url, path):
    req = requests.get(url, headers=headers, timeout=(2, 5))
    # req = requests.get(url, headers=headers)
    f = open(path, 'wb')
    f.write(req.content)
    f.close


def get_url(url):
    selector = get_html(url)
    jp_list = selector.css('.comicpage img::attr(data-original)').getall()
    return jp_list


def main(path_chap,url):
    url_list = get_url(url)
    if not os.path.exists(path_chap):
        os.makedirs(path_chap)
    for name, url in enumerate(url_list):
        jp_name = str(name) + '.jpg'
        jp_path = path_chap + '\\' + jp_name
        pool.submit(save, url, jp_path)
        # print('线程数：' + str(threading.active_count()) +'第' + str(name + 1) + '张' + '(' + str(len(url_list)) + ')')
        print('\r','线程数：' + str(threading.active_count()) +'  ' +path_chap.split('\\')[-1] +' 第' + str(name + 1) + '张' + '(' + str(len(url_list)) + ')',end ='')
        # print('\r',path_chap.split('\\')[-1] +' 第' + str(name + 1) + '张' + '(' + str(len(url_list)) + ')',end ='')



if __name__ == '__main__':
    main(path,url)
    # pool.shutdown(True)