import os
from wxzmh import ex_sql as ex, hm2sr as hm
import time

url_base ='https://wxzmh.top/'
path = r'Z:\jpg'
list_info  = [file.split("--") for file in os.listdir(path)]



def check_book(url_base):
    num = 0
    for name,id in list_info:
        num += 1
        url = url_base+'search?keyword='+name
        selector = hm.get_html(url)
        id_list = selector.css('.mh-item-detali h2 a::attr(href)').getall()
        name_list = selector.css('.mh-item-detali h2 a::attr(title)').getall()
        for i,name_new in enumerate(name_list):
            if set(name_new).issuperset(set(list(name))):
                print(num,name,id,'  ',name_list[i],id_list[i].split('/')[-1])
                if id != id_list[i].split('/')[-1] or name != name_list[i]:
                    os.rename(os.path.join(path,name+'--'+id),os.path.join(path,name_list[i]+'--'+id_list[i].split('/')[-1]))
                    print(name_list[i]+' 已重命名！')
                break


def check_exists():
    list_id = [i[1] for i in list_info]
    sql = 'select mg_id,name from jp_manga where mg_id not in ' + str(tuple(list_id))
    del_list = ex.main(sql)
    num = 0
    for id,name in del_list:
        sql = "select count(*) from jp_chapter where mg_id ='" + id + "'"
        num = ex.main(sql)[0][0]
        print('预计删除书籍：'+id + '--' + name + ' 共计 ' +str(num)+ ' 章节')
    if num > 0:
        sql = 'delete from jp_manga where mg_id in ' + str(tuple([i[0] for i in del_list])+('Null',))
        ex.main(sql)
        sql = 'delete from jp_chapter where mg_id  in ' + str(tuple([i[0] for i in del_list])+('Null',))
        ex.main(sql)
        print('数据库已完成删除！')
    else:
        print('无数据需删除！')


def check_date():
    for file in os.listdir(path):
        print(file)
        ct = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getctime(os.path.join(path,file))))
        sql = "update jp_manga set create_date = '"+ct +"' where regexp_replace(name||'--'||mg_id,'[….?!<>]','') = '"+file +"'"
        print(sql)
        ex.main(sql)
        chap_path = os.path.join(path,file)
        for chapter in os.listdir(chap_path):
            ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(os.path.join(chap_path, chapter))))
            sql = "update jp_chapter set create_date = '" + ct + "' where regexp_replace(mg_name||'--'||mg_id,'[….?!<>]','') = '" + file + "' and regexp_replace(cp_name,'[….?!]','') = '" + chapter + "'"
            print(sql)
            ex.main(sql)


def main():
    check_exists()

if __name__ == '__main__':
    main()