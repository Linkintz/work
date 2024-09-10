from wxzmh import ex_sql, hm2sr, check
import os, re

path = r'Z:\jpg'
# manga_id = [file.split("--")[-1] for file in os.listdir(path)]
manga_id = ['665']
base_url = 'https://wxzmh.top/'


def get_book(selector):
    infos = {}
    items = selector.css('.banner_detail_form')
    infos['book_name'] = items.css('.info h1::text').get()  # 获取标签下第二个标签的text
    infos['book_name1'] = items.css('.info p:nth-child(2)::text').get().replace('别名：', '')  # 获取标签下第二个标签的text
    infos['autor'] = re.sub("[….?!'<>]", "",items.css('.info p:nth-child(3)::text').get().replace('作者：', ''))  # 获取标签下第二个标签的text
    infos['status'] = items.css('.block span::text').get()  # 获取标签下第二个标签的text
    infos['area'] = items.css('.block.ticai a::text').get()  # 获取标签下第二个标签的text
    infos['upd_date'] = items.css('.tip span:nth-child(3)::text').get().replace('更新时间：', '')  # 获取标签下第二个标签的text
    infos['img_url'] = items.css('.cover img::attr(src)').get()  # 获取标签内属性值
    infos['label'] = ('|').join(items.css('.tip .block a::text').getall()[1:])  # 获取标签下第二个标签的text
    infos['content'] = items.css('.info p:nth-child(6)::text').get().replace('\\n', '').strip()
    # infos = (str(id), book_name, book_name1, autor, status, area, upd_date, img_url, label, content)
    return infos


def main(id):
    selector = hm2sr.get_html(base_url + "/book/" + id)
    infos = get_book(selector)
    sql = "select count(*) from jp_manga where mg_id ='"+ id + "'"
    is_exists = ex_sql.main(sql)[0][0]
    if is_exists == 0:
        sql = "insert into jp_manga values" + str((id,)+tuple(infos.values()))
        ex_sql.main(sql)
    else:
        sql = "update jp_manga set upd_date = '"+ infos['upd_date'] +"' where name||'--'||mg_id = '"+infos['book_name']+"--"+id +"'"
        ex_sql.main(sql)

    chapter = selector.css('.view-win-list.detail-list-select li a::text').getall()
    chapter_link = selector.css('.view-win-list.detail-list-select li a::attr(href)').getall()
    book_path = os.path.join(path,infos['book_name'])+'--'+id
    sql = "select count(*) from jp_chapter where mg_id ='"+ id + "'"
    pg_num = ex_sql.main(sql)[0][0]

    if not os.path.exists(book_path):
        print('该路径不存在，创建文件夹ing')
        os.makedirs(book_path)
    hm2sr.save(infos['img_url'], os.path.join(book_path, 'img.jpg'))  # 下载封面
    lo_num = len([i for i in os.listdir(book_path) if os.path.isdir(os.path.join(book_path,i))])
    print(infos['book_name'] + '--' + id + ' 共计 ' + str(len(chapter)) + ' 章,待同步 ' + str(len(chapter) - pg_num) + ' 章,待下载 ' + str(len(chapter) - lo_num) + ' 章')
    for i in range(pg_num,len(chapter)):
        sql = "insert into jp_chapter values" + str((id, infos['book_name'], str(i + 1), re.sub("[….?!<>]", "", chapter[i]), chapter_link[i]))
        ex_sql.main(sql)

    for i in range(lo_num,len(chapter)):
        hm2sr.main(os.path.join(book_path, re.sub("[….?!<>]", "", chapter[i])), base_url + chapter_link[i].lstrip('/'))
        # print(os.path.join(book_path,chapter[i]),base_url+chapter_link[i].lstrip('/'))



if __name__ == '__main__':
    check.check_exists()
    for id in manga_id:
        main(id)
    # check.check_date()