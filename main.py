import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import xml.dom

def get_html(link):
    req = requests.get(link)
    req.encoding = 'utf-8'
    return BeautifulSoup(req.text, 'lxml')


def get_attribute_Series(html):
    dic_attribute = {}
    for i in html.select('.infobox'):
        if len(i.select('.av_performer_cg_box')) > 0:
            if i.select('.av_performer_cg_box')[0].text.strip() == '----':
                dic_attribute['actor'] = None
            else:
                av_performer_list = [av_p.text for av_p in i.select('.av_performer_cg_box')]
                dic_attribute['actor'] = av_performer_list
        else:
            a = i.text.split('：')
            if a[0] == '番號':
                a[0] = 'num'
            elif a[0] == '發行時間':
                a[0] = 'releasedate'
            elif a[0] == '影片時長':
                a[0] = 'runtime'
                a[1] = int(a[1].split('分')[0])
            elif a[0] == '導演':
                a[0] = 'director'
            elif a[0] == '製作商':
                a[0] = 'maker'
            elif a[0] == '發行商':
                a[0] = 'studio'
            elif a[0] == '系列':
                a[0] = 'set'
            elif a[0] == '影片類別':
                a[0] = 'label'
                if len(a[1].split('、')) > 1:
                    a[1] = [x for x in a[1].split('、')]
            if a[1] =='----':
                a[1] = None
            dic_attribute[a[0]] = a[1]
    return pd.Series(dic_attribute)
def write_attribute_to_nfo(attritube):
    pass
soup = get_html('https://javbooks.com')
av_series = []
for i in soup.select('.Po_topic'):
    av_link = i.select('.Po_topic_title')[0].a['href']
    av_series.append(get_attribute_Series(get_html(av_link)))

df = pd.DataFrame(av_series)
df.to_csv('out.csv')
print(df)




