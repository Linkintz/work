# DWS

[TOC]

## 技巧类

### 通过建立临时表关联替代FOR内循环变量

~~~sql
create temp table tt_table as select v_bb;
FOR cour in select 字段 from t_emp a join tt_table b on a.字段=b.字段;
~~~

### 替换字符串中指定字段

#### 基本语法：

translate(string,from_str,to_str);

解释：返回将（所有出现的）from_str中的每个字符替换为to_str中的相应字符以后的string。TRANSLATE 是 REPLACE 所提供的功能的一个超集。如果 from_str 比 to_str 长，那么在 from_str 中而不在 to_str 中的额外字符将从 string 中被删除，因为它们没有相应的替换字符。to_str 不能为空。Oracle 将空字符串解释为 NULL，并且如果TRANSLATE 中的任何参数为NULL，那么结果也是 NULL。

常用的场景：

1. 将数字转换为9，其他的大写字母转换为X，然后返回。

   ``` sql
   SELECT TRANSLATE('2KRW229','0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ','9999999999XXXXXXXXXXXXXXXXXXXXXXXXXX')   "example"FROM DUAL; 
   ```

得到的结果是： 9XXX999

2. 将数字保留，其他的大写字母移除

``` sql
SELECT TRANSLATE('2KRW229','0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ','0123456789') "Translate example"FROM DUAL
```

得到的结果是： 2229

3. 字段处理是按照字符来处理的，不是按照字节来处理，如果to_str的字符数比from_str多的话，多出来的字符数也不会被用到，也不会报异常。

``` sql
SELECT TRANSLATE('我是中国人,我爱中国', '中国', 'China') "Translate example" FROM DUAL
```

执行结果：我是Ch人,我爱Ch

4. 如果from_string的字符数大于to_string，那么多出的字符会被移除，也就是ina三个字符会从char参数中移除，当然区分大小写啦

``` sql
SELECT TRANSLATE('I am Chinese, I love China', 'China', '中国') "Translate example" FROM DUAL
```

执行结果：I m 中国ese, I love 中国

5. 如果第二个参数是空字符串的话，整个返回null。

``` sql
 SELECT TRANSLATE('2KRW229','0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ','') "License"FROM DUAL
```

执行结果 是空

6. 在银行转账的时候经常看到很多字眼做了脱敏处理。

``` sql 
SELECT TRANSLATE('中国人',substr('中国人',1,length('中国人') - 1),rpad('*',length('中国人'),'*')) "License" FROM DUAL;
```

**执行结果**：**人

7. 去除字符串中数字

```sql
select replace(translate('abc1234def678add590a','0123456789',' '),' ','') from dual;
```

**执行结果**：abcdefadda

## 学习类

### 数据库模式使用

#### 方法一：

~~~sql
SET SEARCH_PATH TO myschema;
CREATE TABLE mytable (firstcol int);
~~~

#### 方法二：

~~~sql
CREATE TABLE myschema.mytable (firstcol int);
~~~

注：如果在创建对象时不指定schema，则会将对象创建在当前的schema下。查询当前schema的办法为：  

~~~sql
show search_path;
search_path
----------------
"$user",public
(1 row)
~~~

### 行存储和列存储的差异  

​		行存储是指将表按行存储到硬盘分区上，列存储是指将表按列存储到硬盘分区上。默认情况下，创建的表为行存储。一般情况下，如果表的字段比较多（大宽表），查询中涉及到的列不多的情况下，适合列存储。如果表的字段个数比较少，查询大部分字段，那么选择行存储比较好  。

| 存储模型 | 优点                                                         | 缺点                                                         | 使用场景                                                     |
| -------- | ------------------------------------------------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 行存     | 数据被保存在一起。 INSERT/ UPDATE容易。                      | 选择(Selection)时即使只涉及某几 列，所有数据也都会被读取。   | ● 点查询(返回记录少，基于索引的简单查询)。 <br />● 增、删、改操作较多的场景。 |
| 列存     | ● 查询时只有涉及到的列会被 读取。<br /> ● 投影(Projection)很高效。<br /> ● 任何列都能作为索引。 | ● 选择完成时，被选择的列要重新组 装。 <br />● INSERT/UPDATE比较麻烦。 | ● 统计分析类查询 (关联、分组操作较多的场景)。 <br />● 即席查询（查询条件不确定，行存表扫描难以使用索引）。 |

### 执行计划



要了解执行计划，首先我们需要了解一个语句在数据库中从输入到输出的过程：

​	Sql query ——[> parser](https://bbs.huaweicloud.com/forum/thread-21245-1-1.html#)（分析器）——[> rewirte(](https://bbs.huaweicloud.com/forum/thread-21245-1-1.html#)查询重写)——[> ](https://bbs.huaweicloud.com/forum/thread-21245-1-1.html#)Optimize（优化器）——[> executor](https://bbs.huaweicloud.com/forum/thread-21245-1-1.html#)（执行器）——> query results

+ **parser（分析器）:查询分析器接收到语法分析树后，将其转换为以数据结构query表示的树形结构。**

+ **rewirte(查询重写)：依据数据库的规则系统，重写query结构，如将试图替换为该试图所代表的查询。**

+ **Optimize（优化器）：分为逻辑优化阶段和物理优化阶段，**其中：

  逻辑优化阶段：该阶段利用代数变换规则等价变换query：消除子查询，处理表达式，消除having子句，消除外连接，条件的上推下压等一系列等价变化，以获取最优的逻辑执行计划。

  物理优化阶段：该阶段考虑表的连接顺序、where条件的约束、计算各表的统计信息。在为逻辑执行计划的每个结点生成所有可能的执行路径时，通过代价估计的方法，计算各种可能路径的执行代价，并从中选择代价最小的作为当前结点的执行路径。

+ **executor（执行器）：形成执行计划，将得到的代价最小的物理执行路径等价的转换为物理执行计划并执行。**

  何为执行计划？简单来说就是对每个查询产生一个查询规划，规划好每一步的路径，执行时就按着计划执行。

  这里是一个简单的例子，只是用来显示执行计划输出会有些什么内容：

~~~sql
select * from emp;
~~~

![image-20211103111002186](C:\Users\Pactera\AppData\Roaming\Typora\typora-user-images\image-20211103111002186.png)

Cost中有2个值，前面的是启动代价，后面的值是总的代价：启动代价是只获取到第一个元组的代价，总代价是获取完所有元组的代价。Cost的估算方法：IO代价+CPU代价+网络代价。

#### 1   常见算子介绍：  

 详见附件：<img src="C:\Users\Pactera\AppData\Roaming\Typora\typora-user-images\image-20211103111133837.png" alt="image-20211103111133837"  />

#### 2   执行计划中表的连接方式： 

##### 2.1   嵌套连接(nested loop)  

​    对左边的关系里面找到的每条行都对右边关系进行一次扫描。这个策略容易实现，但是可能会很耗费时间。但是，如果右边的关系可以用索引扫描，那么这个可能就是个好策略。可以用来自左边关系的当前行的数值为键字进行对右边关系的索引扫描。

一般用在连接的表中有索引，并且索引选择性较好的时候；而在没有索引的情况下，嵌套连接的代价通常会很大。

eg:

create table tb1(a int,b int);
create table tb2(a int,b int);
explain (costs off) select * from tb2,tb1 where tb2.a > tb1.a; 
        QUERY PLAN       

\----------------------------------------

 Streaming (type: GATHER)

  Node/s: All datanodes

  -> Nested Loop

​     Join Filter: (tb2.a > tb1.a)

​     -> Streaming(type: BROADCAST)

​        Spawn on: All datanodes

​        -> Seq Scan on tb2

​     -> Materialize

​        -> Seq Scan on tb1

(9 rows)

##### 2.2   归并/排序连接(merge join)  

​    在连接开始之前，每个关系都对连接字段进行排序。然后对两个关系并发扫描，匹配的行就组合起来形成连接行。这种联合更有吸引力，因为每个关系都只用扫描一次。要求的排序步骤可以通过明确的排序步骤，或者是使用连接键字上的索引按照恰当的顺序扫描关系。

eg:` explain (costs off) select * from tb2,tb1 where tb2.a = tb1.a;`

Streaming (type: GATHER)

  Node/s: All datanodes

  -> Merge Join

​     Merge Cond: (tb2.a = tb1.a)

​     -> Sort

​        Sort Key: tb2.a

​        -> Seq Scan on tb2

​     -> Sort

​        Sort Key: tb1.a

​        -> Seq Scan on tb1

(10 rows)

归并连接的效率很高，只要时间复杂度是约是O(n)+O(m)的数量级，n,m是参与连接表的长度。但也有极端的情况，比如该列只有一个取值，那么每一条记录都是可连接的，则退变为嵌套连接，为O(n2)的复杂度。

另外，归并连接需要参与连接的两表都是排序好的，若表本身是无序的，那么对表本身进行排序也需要相应的开销。所以，最好是排序字段有索引，可以藉由索引获取有序表。不过话说回来，既然有索引，那么本身嵌套连接也是个不错的选择了。

##### 2.3   哈希连接(hash join)  

​    首先扫描右边的关系，并用连接的字段作为散列键字加载进入一个 Hash 表，然后扫描左边的关系，并将找到的每行用作散列键字来以定位表里匹配的行。

​    哈希连接通常使用在处理大数据集的场合，并且两表的数据量差别较大。
eg:`explain (costs off) select * from tb1, tb2 where tb1.a = tb2.a;`

​       QUERY PLAN      

\------------------------------------

 Streaming (type: GATHER)

  Node/s: All datanodes

  -> Hash Join

​     Hash Cond: (tb1.a = tb2.a)

​     -> Seq Scan on tb1

​     -> Hash

​        -> Seq Scan on tb2

(7 rows)

#### 3   计划中常见stream算子

##### 3.1   BROADCAST（广播）  

**Broadcast Stream** (1:N) – 由一个源节点将其数据发给N个目标节点；



![image.png](https://bbs-img.huaweicloud.com/data/attachment/forum/201907/19/161558vo4dpylmmgmau1xy.png)

##### 3.2   REDISTRIBUTE（重分布）  

**REDISTRIBUTE Stream** (N:N) – 每个源节点将其数据根据连接条件计算Hash值，根据重新计算的Hash值进行分布，发给对应的目标节点；

![image.png](https://bbs-img.huaweicloud.com/data/attachment/forum/201907/19/1616315hrnk11hk0aztlpf.png)

eg: `explain (costs off) select * from tb2,tb1 where tb2.a = tb1.b;`

​        QUERY PLAN        

\-------------------------------------------

 Streaming (type: GATHER)

  Node/s: All datanodes

  -> Hash Join

​     Hash Cond: (tb1.b = tb2.a)

​     -> Streaming(type: REDISTRIBUTE)

​        Spawn on: All datanodes

​        -> Seq Scan on tb1

​     -> Hash

​        -> Seq Scan on tb2

(9 rows)

##### 3.3   GATHER  

**Gather Stream** (N:1) – 每个源结点都将其数据发送给目标结点；

![image.png](https://bbs-img.huaweicloud.com/data/attachment/forum/201907/19/161653o532fjlzneyn7d6m.png)

常见注意点：

1. 一般来说小表broadcast ，大表重分布；broadcast之后每个dn均有一份表数据，无需再重分布；

2. 重分布是因为join条件不在分布列上，为了保证能够join到一起的数据都分布在相同的dn上，会做重分布，不论是重分布还是broadcast都是基于代价选择的；

举例：

~~~sql
create table t1(a int, b int , c int) with (orientation=column)distribute by hash(a,b);
create table t2(a int, b int , c int) with (orientation=column)distribute by hash(a,b);
~~~

t1、t2 分布列都是a,b

1）join列为分布列时，两表均不用重分布：

`explain select t1.a from t1 join t2 on t1.a=t2.a and t1.b=t2.b;`
id | operation | E-rows | E-costs | width
----+----------------------------------------+--------+----------------+-------
1 | -> Row Adapter | 288 | 20000000029.63 | 4
2 | -> Vector Streaming (type: GATHER) | 288 | 20000000029.63 | 4
3 | -> Vector Hash Join (4,5) | 288 | 20000000020.26 | 4
4 | -> CStore Scan on t1 | 240 | 10000000010.01 | 8
5 | -> CStore Scan on t2 | 240 | 10000000010.01 | 8
(5 rows)

2）join一个是分布列，一个不是分布列时，不是分布列的表需要重分布：

`explain select t1.a from t1 join t2 on t1.a=t2.a and t1.b=t2.c;`
id | operation | E-rows | E-costs | width
----+---------------------------------------------------+--------+----------------+-------
1 | -> Row Adapter | 288 | 20000000030.66 | 4
2 | -> Vector Streaming (type: GATHER) | 288 | 20000000030.66 | 4
3 | -> Vector Hash Join (4,5) | 288 | 20000000021.28 | 4
4 | -> CStore Scan on t1 | 240 | 10000000010.01 | 8
5 | -> Vector Streaming(type: REDISTRIBUTE) | 240 | 10000000011.03 | 8
6 | -> CStore Scan on t2 | 240 | 10000000010.01 | 8
(6 rows)

3）join 均不是分布列时，两表均需要重分布：

`explain select t1.a from t1 join t2 on t1.a=t2.a and t1.c=t2.c;`
id | operation | E-rows | E-costs | width
----+---------------------------------------------------+--------+----------------+-------
1 | -> Row Adapter | 288 | 20000000031.68 | 4
2 | -> Vector Streaming (type: GATHER) | 288 | 20000000031.68 | 4
3 | -> Vector Hash Join (4,6) | 288 | 20000000022.31 | 4
4 | -> Vector Streaming(type: REDISTRIBUTE) | 240 | 10000000011.03 | 8
5 | -> CStore Scan on t1 | 240 | 10000000010.01 | 8
6 | -> Vector Streaming(type: REDISTRIBUTE) | 240 | 10000000011.03 | 8
7 | -> CStore Scan on t2 | 240 | 10000000010.01 | 8
(7 rows)

4）相关子查询时，子查询的表必须做broadcast才能保证结果对，就是一个做了broadcast，另一个就啥也不用做：

explain select t1.a from t1 where t1.a in (select t2.a from t2 where t1.b=t2.b);
id | operation | E-rows | E-costs | width
----+---------------------------------------------------------+--------+----------------+-------
1 | -> Row Adapter | 120 | 60000001146.63 | 8
2 | -> Vector Streaming (type: GATHER) | 120 | 60000001146.63 | 8
3 | -> CStore Scan on t1 | 120 | 60000001142.71 | 8
4 | -> Row Adapter [3, SubPlan 1] | 5760 | 10000000054.48 | 8
5 | -> Vector Result | 5760 | 10000000054.48 | 8
6 | -> Vector Materialize | 5760 | 10000000054.48 | 8
7 | -> Vector Streaming(type: BROADCAST) | 5760 | 10000000053.28 | 8
8 | -> CStore Scan on t2 | 240 | 10000000010.01 | 8
(8 rows)

#### 4   Explain 常用参数介绍  

显示一个语句的执行计划。执行计划将显示SQL语句所引用的表会采用什么样的扫描方式，如：简单的顺序扫
描、索引扫描等。如果引用了多个表，执行计划还会显示用到的JOIN算法。执行计划的最关键的部分是语句的**预计执行开销**，这是计划生成器估算执行该语句将花费多长的时间。若指定了ANALYZE选项，则该语句会被执行，然后根据实际的运行结果显示统计数据，包括每个计划节点内时间总开销（毫秒为单位）和实际返回的总行数。这对于判断计划生成器的估计是否接近现实非常有用 。

注意事项：**在指定ANALYZE选项时，语句会被执行,分析INSERT，UPDATE， DELETE， CREATE TABLE AS或EXECUTE语句  （ROLLBACK)。**

##### 语法格式：

显示SQL语句的执行计划，支持多种选项，对选项顺序无要求。

`EXPLAIN [ ( option [, ...] ) ] statement;`
其中选项option子句的语法为。

~~~sql
ANALYZE [ boolean ] |
ANALYSE [ boolean ] |
VERBOSE [ boolean ] |
COSTS [ boolean ] |
CPU [ boolean ] |
DETAIL [ boolean ] |
NODES [ boolean ] |
NUM_NODES [ boolean ] |
BUFFERS [ boolean ] |
TIMING [ boolean ] |
PLAN [ boolean ] |
FORMAT { TEXT | XML | JSON | YAML }
~~~

● 显示SQL语句的执行计划，且要按顺序给出选项。
`EXPLAIN { [ { ANALYZE | ANALYSE } ] [ VERBOSE ] | PERFORMANCE } statement;`
● 显示复现SQL语句的执行计划所需的信息，通常用于定位问题。 STATS选项必须单独使用。
`EXPLAIN ( STATS [ boolean ] ) statement;  `

##### 参数介绍：

+ **statement** 	指定要分析的SQL语句。

+  **ANALYZE boolean | ANALYSE boolean**

  显示实际运行时间和其他统计数据。
  取值范围：
  – TRUE（缺省值）：显示实际运行时间和其他统计数据。
  – FALSE：不显示。
  
+ **VERBOSE boolean**
    显示有关计划的额外信息。
    取值范围：
    – TRUE（缺省值）：显示额外信息。
    – FALSE：不显示。
    
+ **COSTS boolean**
  包括每个规划节点的估计总成本，以及估计的行数和每行的宽度。
  取值范围：
  – TRUE（缺省值）：显示估计总成本和宽度。
  – FALSE：不显示。

+ **CPU boolean**
  打印CPU的使用情况的信息。
  取值范围：
  – TRUE（缺省值）：显示CPU的使用情况。
  – FALSE：不显示。

+  **DETAIL boolean**
  打印DN上的信息。
  取值范围：
  – TRUE（缺省值）：打印DN的信息。
  – FALSE：不打印。

+  **NODES boolean**
  打印query执行的节点信息。
  取值范围：
  – TRUE（缺省值）：打印执行的节点的信息。
  – FALSE：不打印。

+  **NUM_NODES boolean**
  打印执行中的节点的个数信息。
  取值范围：
  – TRUE（缺省值）：打印DN个数的信息。
  – FALSE：不打印。

+ **BUFFERS boolean**
  包括缓冲区的使用情况的信息。
  取值范围：
  – TRUE：显示缓冲区的使用情况。
  – FALSE（缺省值）：不显示。

+ **TIMING boolean**
  包括实际的启动时间和花费在输出节点上的时间信息。
  取值范围：
  – TRUE（缺省值）：显示启动时间和花费在输出节点上的时间信息。
  – FALSE：不显示。

+ **PLAN**
  是否将执行计划存储在plan_table中。当该选项开启时，会将执行计划存储在PLAN_TABLE中，不打印到当前屏幕，因此该选项为on时，不能与其他选项同时使用。
  取值范围：
  – ON（缺省值）：将执行计划存储在plan_table中，不打印到当前屏幕。执行
  成功返回EXPLAIN SUCCESS。
  – OFF：不存储执行计划，将执行计划打印到当前屏幕。

+ **FORMAT**

   指定输出格式。 

  取值范围： TEXT, XML, JSON和YAML。
  默认值： TEXT。

+ **PERFORMANCE**

   使用此选项时，即打印执行中的所有相关信息。 

+ **STATS boolean** 

  打印复现SQL语句的执行计划所需的信息，包括对象定义、统计信息、配置参数等，通常用于定位问题。
  取值范围：
  – TRUE（缺省值）：显示复现SQL语句的执行计划所需的信息。
  – FALSE：不显示。

### 存储过程

存储过程无法打印执行计划，只能先打桩先确定慢的sql，然后再单独执行慢sql的explain performance执行计划，打桩语句如下：

~~~sql 
raise info 'before insert table : % time: %', rd.name, clock_timestamp();
~~~

