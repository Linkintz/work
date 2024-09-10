
```python
import parsel  
import requests
```
语法使用
```python
url = 'http://www.baidu.com'
response = requests.get(url)
selector = parsel.Selector(response.text)
```
## CSS选择器
#### 语法简单介绍
```python
" * " 选择所有节点
" # container " 选择id为container的节点
" .container " 选择class包含container的节点
"li a " 选择 所有 li 下的所有 a 节点
“ul + p” 选择所有ul后面的第一个p元素
“#container > ul” 选择id为container的第一个ul节点
"a[class] " 选取所有有class属性的a元素
“a[href=“http://b.com”]” 含有href="http://b.com"的a元素
"a[href*=‘job’] " 包含job的a元素
"a[href^=‘https’] " 开头是https的a元素
“a[href$=‘cn’]” 结尾是cn的a元素
```
选择所有元素
```python
selector.css('*')
```
1、选择article元素
```python
html = selector.css('article')
# get(), getall() , extract_first(), extract() 都可以
```
2、选择id为container的元素
```python
selector.css('#container')
```
3、选择所有class包含container的元素
```python
selector.css('.container')
```
4、选取所有div下所有a元素
```python
selector.css('div a')
```
5、提取标签title列表
```python
title1 = selector.css('title').extract()
title2 = selector.css('title').extract_first()
```
6、提取标签p里的文本内容
```python
text = selector.css('p::text').extract()
```
7、提取标签div里的所有文本内容
```python
data = selector.css('div.post-content *::text').extract()
```
8、提取标签里的URL：标签名::attr(属性名)
```python
url = selector.css('div.post-content img::attr(src)').extract()
```
9、选取所有拥有title属性的a元素
```python
a = selector.css('a[title]').getall()
```
### 拓展语法
选取ul后面的第一个p元素
```python
selector.css('ul + p')
```
选取与ul相邻的所有p元素
```python
selector.css('ul ~ p')
```
选取下面第二个标签，如果是a的话则选取，不是则不取
```python
selector.css('a:nth-child(2)')
```
选取第偶数个a元素
```python
selector.css('a:nth-child(2n)')
```
选取第奇数个a元素
```python
selector.css('a:nth-child(2n+1)') 
```
选取class为multi-chosen的li的所有a元素
```python
selector.css('li.multi-chosen &gt; a') 
```
选取所有href属性为https://www.lagou.com/jobs/3537439.html的a元素
```python
selector.css('a[href=”https://www.lagou.com/jobs/3537439.html”]')
```
选取所有href属性值中包含www.lagou.com的a元素
```python
a[href*=”www.lagou.com”]
```
选取所有href属性值中以http开头的a元素
```python
a[href^=”http”] 
```
选取所有id为非content-container 的div
```python
div:not(#content-container)
```
## xpath选择器
```python
nodename  选择此节点的所有子节点
/         从当前节点选取直接子节点
//        从当前节点选取子孙节点
.          选取当前节点
...       选取当前节点的父节点
@         选取属性
```
实例
```python
import parsel
text = '''
<li class="li li-first">
<a href="link.html" img="jaxkbasjgglksjdlkjsdlkfjd.jpg">first item</a>
</li>
'''
sel = parsel.Selector(text)
#contains()方法，第一个参数传入属性名称，第二个参数传入属性值，只要此属性包含所传入的属性值，就可以完成匹配。
list1 = sel.xpath('//li[contains(@class,"li")]/a/text()').extract()
print(list1)   #['first item']
list2 = sel.xpath('//li/a/@img').extract()
print(list2)   #['jaxkbasjgglksjdlkjsdlkfjd.jpg']
list3 = sel.xpath('//li/a/@href').extract()
print(list3)   #['link.html']
```