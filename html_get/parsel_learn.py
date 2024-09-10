import requests
import parsel
import test

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'}
    html = requests.get(url=url, headers=headers).text
    # print(requests.get(url=url, headers=headers).status_code)
    return html


def sel_html(html):
    return parsel.Selector(html)


def str_get(src):
    for i in ['\\n', '', '\xa0', '\xa0/\xa0']:
        src = src.replace(i, '').strip()
    return src.strip('/')


def main(url):
    html = get_html(url)
    selector = sel_html(html)
    items = selector.css('.grid_view li')
    infos = []
    for i, item in enumerate(items[0:1]):
        info = [item.css('.item em::text').get(),
                item.css('.hd span::text').get(),
                item.css('.hd span:nth-child(2)::text').get(),
                item.css('.hd span:nth-child(3)::text').get(),
                item.css('.star span:nth-child(2)::text').get(),
                item.css('.star span:nth-child(4)::text').get(),
                item.css('.bd p::text').getall()[0],
                item.css('.bd p::text').getall()[1],
                item.css('.quote span::text').get(),  # src
                item.css('.hd a::attr(href)').get()]  # link

        html_detail = get_html(info[-1])
        selector_dateail = sel_html(html_detail).css('.related-info')
        info.append(selector_dateail.css('.short span::text').get())  # content
        # for dd in selector_dateail.css('.short span::text').getall():
        #     # print(dd)
        #     info.append(dd)

        info_list = [str_get(val) if val is not None else '' for val in info]
        infos.append(tuple(info_list))

    for i in infos:
        print(str(i))


if __name__ == '__main__':
    for i in range(1):
        main('https://movie.douban.com/top250?start=' + str(25 * i) + '&filter=')
