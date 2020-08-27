#!/usr/bin/env Python 
# -*- coding:utf-8 -*-
# autuor:DongBin
# time:2020/8/26

"""
Potplayer播放时系统总是提示“该站点安全证书的吊销凭证不可用”，可以ie浏览器的internet选项里关闭。
不想关闭的只要忍受一次提示然后点击是，之后播放会失效，再次在Potplayer里点击播放就可以了。但是重启Potplayer又会出现此问题。
------------思路设计----------
1、片名列表选择
2、列表信息获取
3、播放列表生成
"""
import requests, prettytable, re,codecs
from lxml import etree


def movie_playlist(link_html, name):
    first_epsoid_name =[]
    second_epsoid_name =[]
    first_epsoid_url = []
    second_epsoid_url = []
    # print("开始xpath")
    list_first_name = link_html.xpath('//div[@id="1"]/h3/span/text()')
    list_second_name = link_html.xpath('//div[@id="2"]/h3/span/text()')
    # 这个和name一起用来写文件
    # print("开始xpath")
    playlist_first = link_html.xpath('//div[@id="1"]/ul/li/text()')
    playlist_second = link_html.xpath('//div[@id="2"]/ul/li/text()')
    # print(playlist_first)
    for playlist in playlist_first:
        first_epsoid_name.append(playlist.split('$')[0])
        # print(epsoid_name)
        first_epsoid_url.append(playlist.split('$')[1])
    for playlist in playlist_second:
        second_epsoid_name.append(playlist.split('$')[0])
        # print(epsoid_name)
        second_epsoid_url.append(playlist.split('$')[1])
    playlist_head_first = "DAUMPLAYLIST\nplayname=%s\nplaytime=0\nsaveplaypos=0" % first_epsoid_url[0]
    playlist_head_second = "DAUMPLAYLIST\nplayname=%s\nplaytime=0\nsaveplaypos=0" % second_epsoid_url[0]
    # print(playlist_head
    for i, n, u, sn, su in zip(range(1, len(first_epsoid_url)+1), first_epsoid_name, first_epsoid_url,second_epsoid_name,second_epsoid_url):
        playlist_head_first = "\n".join([playlist_head_first, "%d*file*%s\n%d*title*%s\n%d*played*0" % (i, u, i, n, i)])
        playlist_head_second = "\n".join([playlist_head_second, "%d*file*%s\n%d*title*%s\n%d*played*0" % (i, su, i, sn, i)])

    # 写入第一个源的我播放列表
    with codecs.open('%s_%s.dpl' % (name, list_first_name[0]), 'w', encoding='utf8') as f:
        f.write(playlist_head_first)
    with codecs.open('%s_%s.dpl' % (name, list_second_name[0]), 'w', encoding='utf8') as f: # 写入第二个源的播放列表
        f.write(playlist_head_second)
    print('播放列表写入完成，请在请在程序目录下查看')


def movie_synopsis(links, names):
    link_choice = input("请按编号选择：")
    link_url = 'http://okzyw.com/'+links[int(link_choice)]
    link_response = requests.get(link_url)
    link_content = link_response.content.decode('utf8')
    link_html = etree.HTML(link_content)

    try:
        synopsis = link_html.xpath('//div[@class="vodplayinfo"]/text()')
        print("故事简介为："+synopsis[0])
    except():
        print("获取简介错误")

    back_or_not = input("输出播放列表请输入*y*,返回选择剧集请输入*n*：")
    if back_or_not == 'n':
        movie_synopsis(links, names)
    elif back_or_not == 'y':
        movie_playlist(link_html, names[int(link_choice)])


def movies_name(name):
    url = 'http://okzyw.com/index.php?m=vod-search-pg-1-wd-%s.html' % name
    response = requests.get(url)
    # print(response.text)
    response_content = response.content.decode('utf8')
    response_html = etree.HTML(response_content)
    # 先解析页数
    pages = response_html.xpath('//ul//div[@class="pages"]/text()')
    pages_re = re.findall(r'\d\/\d', str(pages))[0].split('/')[1]
    # print(type(pages_re))  # str类型
    names_full = []
    links_full = []  #创建几个空的列表类型用于合并
    types_full = []
    updates_full = []
    for i in range(1, int(pages_re)+1):
        urls = 'http://okzyw.com/index.php?m=vod-search-pg-%d-wd-%s.html' % (i, name)
        # print(urls)
        # continue
        page_response = requests.get(urls)  # 一开始这里的urls写成了url导致内容没有变化
        page_content = page_response.content.decode('utf8')
        page_html = etree.HTML(page_content)
        names = page_html.xpath('//div//span[@class="xing_vb4"]/a/text()')
        links = page_html.xpath('//div//span[@class="xing_vb4"]/a/@href')
        types = page_html.xpath('//div//span[@class="xing_vb5"]/text()')
        updates = page_html.xpath('//div//span[@class="xing_vb6"]/text()')
        # print(names)
        names_full.extend(names)
        links_full.extend(links)
        types_full.extend(types)
        updates_full.extend(updates)
    put = prettytable.PrettyTable()
    # print(names_full)
    put.field_names = ["编号", "名称", "类型", "更新时间"]
    for c, n, t, u in zip(range(len(names_full)),names_full, types_full, updates_full):
        put.add_row([c, n, t, u])

    print(put)

    movie_synopsis(links_full, names_full)




if __name__ == '__main__':
    while True:
        name = input("请搜索片名：")
        movies_name(name)
