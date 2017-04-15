import re
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')#win�ı�����gbk����ҳ��utf-8�����ⲻƥ��

class spider(object):
    def __init__(self):
        print u'��ʼ��ȡ���ݡ���'

    def getsource(self,url):
        html=requests.get(url)
        return html.text

    def changepage(self,url,total_page):
        page_group=[]
        for i in range(1, total_page+1):
            link = re.sub("\d+","%s"%i,url,re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self,source):
        everyclass=re.findall('<li id=".*?</li>',source,re.S)
        return everyclass

    def getinfo(self,eachclass):
        info={}
        info['title']=re.search('title="(.*?)"',eachclass,re.S).group(1)
        info['content']=re.search('<p(.*?)>(.*?)</p>',eachclass,re.S).group(1)
        timeandlevel=re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        return info

    def saveinfo(self,classinfo):
        f=open('info.txt','a')
        for each in classinfo:
            f.write('title:'+each['title']+'\n')
            f.write('content:' + each['content'] + '\n')
            f.write('classtime:' + each['classtime'] + '\n')
            f.write('classlevel:' + each['classlevel'] + '\n')
            f.write('\n\n')
        f.close()

if __name__=='__main__':

    classinfo=[]
    url='http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider=spider()
    all_links=jikespider.changepage(url,20)
    for link in all_links:
        print u'���ڴ���ҳ�棺'+link
        html =jikespider.getsource(link)
        everyclass=jikespider.geteveryclass(html)
        for each in everyclass:
            info=jikespider.getinfo(each)
            classinfo.append(info)
        jikespider.saveinfo(classinfo)
