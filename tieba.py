#coding=utf-8
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def towrite(contentdict):
    f.writelines(u'回帖时间：'+str(contentdict['topic_reply_time'])+'\n')
    f.writelines(u'回帖内容：' + unicode(contentdict['topic_reply_content']) + '\n')
    f.writelines(u'回帖人：' + contentdict['user_name'] + '\n\n')


def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')#这里得到许多个回帖
    items = {}
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot', '')) #这里得到一个回帖的内容
        author = reply_info['author']['user_name']
        content = each.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0]
        reply_time = reply_info['content']['date']
        print content
        print reply_time
        print author
        items['user_name'] = author
        items['topic_reply_content'] = content
        items['topic_reply_time'] = reply_time
        towrite(items)

if __name__ == '__main__':
    pool = ThreadPool(4)
    f = open('content.txt', 'a')
    page = []
    for i in range(1,20):
        newpage = 'http://tieba.baidu.com/p/5061243572?pn='+str(i)
        page.append(newpage)

    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()


