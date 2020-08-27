# Python生成资源网播放列表

## 一、OK资源网

#### 1、URL

Request URL ：[http://okzyw.com/index.php?m=vod-search-pg-1-wd-聊斋.html](http://okzyw.com/index.php?m=vod-search-pg-1-wd-聊斋.html)

#### 2、请求类型

get

#### 3、信息收集

在搜索出来的内容里Xpath

+ 结果页数：/html/body/div[5]/ul[52]/li/div/text()[1]

+ 电影名称：//div//span[@class="xing_vb4"]/a/text()

  > 电影名称有个href属性是链接：/html/body/div[5]//li/span[2]/a/@href

+ 电影类型：/html/body/div[5]//li/span[@class="xing_vb5"]/text()
+ 更新时间：/html/body/div[5]//li/span[4]/text()

在点进去的相信内容里

+ 剧集简介：/html/body/div[5]/div[2]/div[2]/text()

+ 播放类型：

  > 播放类型1：//*[@id="1"]/h3/span
  >
  > 播放类型2：//*[@id="2"]/h3/span

+ 播放列表：

  > 类型1列表：//*[@id="1"]/ul//text()
  >
  > 类型2列表：//*[@id="1"]/ul//text()

#### 4、数据处理

播放链接样例：

第01集$https://sina.com-h-sina.com/share/d1942a3ab01eb59220e2b3a46e7ef09d

可以用$来拆分，左边为剧集，右边为播放链接，可以在剧集前面再加上剧名



## 二、遇到的问题

### 1、Xpath取文本问题

> Xpath取文本有两种，一种是/text()，另一种是//text()。
>
> /text()：表示当前里的文本
>
> //text()：表示当前目录及其下所有目录的文本

故：==需要确定好需要提取的文本是否就在这个目录下==