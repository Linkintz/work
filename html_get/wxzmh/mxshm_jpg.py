import requests
import re
import parsel
import threading
from retry import retry
import os
import time
from concurrent.futures import ThreadPoolExecutor

path = r'Z:\jpg'


# list_id = ["493","356"]
list_id  = [file.split("--")[-1] for file in os.listdir(path)]
# base_url = "http://www.92hm.top"
base_url = "https://wxzmh.top/"
pool = ThreadPoolExecutor(50)
w_title = []
g_title = []
z_title = []
err_id = {}


@retry(tries=150)
def get_html(url):
    time.sleep(3)
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    response = requests.get(url=url, headers=head, timeout=(3, 9))
    # print(response.status_code) 
    return response.text


def get_list(reponse, xpath):
    selector = parsel.Selector(reponse)  # 将字符串转换为Selector对象
    list = selector.xpath(xpath).getall()  # 选择需要的内容右键复制
    return list


@retry()
def save(url, path):
    # se.acquire()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
    req = requests.get(url, headers=headers, timeout=(2, 5))
    # req = requests.get(url, headers=headers)
    f = open(path, 'wb')
    f.write(req.content)
    f.close
    # se.release()


def delete(path):
    for i in os.listdir(path):
        # size = os.path.getsize(path)
        cou = 0
        print(i)
        for title in os.listdir(path + '\\' + i):
            # print(title)
            if title.endswith('.zip'):
                print(path + '\\' + i + '\\' + title)
                os.remove(path + '\\' + i + '\\' + title)
            else:
                for jpg in os.listdir(path + '\\' + i + '\\' + title):
                    # print(jpg)
                    if os.path.getsize(path + '\\' + i + '\\' + title + '\\' + jpg) == 0 and jpg.endswith('.jpg'):
                        cou += 1
                        print(str(cou) + path + '\\' + i + '\\' + title + '\\' + jpg)
                        os.remove(path + '\\' + i + '\\' + title + '\\' + jpg)
    print(cou)


def main():
    for id in list_id:
        try:
            response_chap = get_html(base_url + "/book/" + id)
            xpath_chap = '//*[@id="detail-list-select"]/li'
            list_chap = [re.findall('href="(.*?)"', i) + re.findall('rel="nofollow">(.*?)</a>', i) for i in
                         get_list(response_chap, xpath_chap)]
            xpath_title = '/html/body/div[1]/section/div[2]/div[2]/h1'
            title = re.findall('<h1>(.*?)</h1>', get_list(response_chap, xpath_title)[0])[0]
            print(title + '\n', end='')
            path_title = path + '\\' + title + "--" + id

            # if len([chap for chap in list_chap if '最終話' in chap[1]]) > 0:
            #     print(title + "  ---->已完结\n", end='')
            #     w_title.append(title)
            #     continue

            # for chap in reversed(list_chap):
            for chap in list_chap:

                path_chap = path_title + '\\' + re.sub("[….?!]", "", chap[1])
                if not os.path.exists(path_chap):
                    os.makedirs(path_chap)
                ll = [file for file in os.listdir(path_chap)]
                # if len(ll) == len(list_jpg):
                # if str(len(ll) - 1) + ".jpg" in ll:

                if len([i for i in ll if i.endswith(".jpg")]) > 0 and len(
                        [i for i in ll if i.endswith(".jpg")]) - 1 == max(
                        [int(i.split('.')[0]) for i in ll if i.endswith(".jpg")]):
                    print('\r' + title + "--" + chap[1] + "  ---->未更新", end='')
                    z_title.append(title)
                    continue

                url = base_url + chap[0]
                reponse_jpg = get_html(url)
                xpath_jpg = '//*[@id="content"]/div[2]/div/div'
                list_jpg = [re.findall('data-original="(.*?)"', i)[0] for i in get_list(reponse_jpg, xpath_jpg)]

                for name, i in enumerate(list_jpg):
                    nameJpg = str(name) + '.jpg'
                    pathJpg = path_chap + '\\' + nameJpg
                    # save(i, pathJpg)
                    if nameJpg not in ll:
                        # t = threading.Thread(target=save, args=(i, pathJpg))  # target目标函数，args为参数
                        # t.start()
                        g_title.append(title)
                        pool.submit(save, i, pathJpg)
                        print('线程数：' + str(threading.active_count()) +' '+ title + '--' + chap[1] + '(' + str(
                            len(list_chap)) + '),' + ' 第' + str(name + 1) + '张' + '(' + str(
                            len(list_jpg)) + ')\n', end='')
        except Exception as result:
            err_id[id] = result
            continue
        #     print(re.sub("[….?!]","",chap[1])+' ---->线程数：', len(threading.enumerate()))
        #     if len(threading.enumerate())> 180:
        #         main()
        # print('当前总线程数：>>>>>', len(threading.enumerate()))


if __name__ == "__main__":
    main()
    pool.shutdown(True)
    g_title = list(set(g_title))
    z_title = list(set([i for i in z_title if i not in g_title]))

    print('\n', end='')
    print("已完结：", len(w_title), w_title)
    print('未更新：', len(z_title), z_title)
    print('已更新：', len(g_title), g_title)
    print("问题id：", err_id)
