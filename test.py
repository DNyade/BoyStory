import requests
import re
from bs4 import BeautifulSoup

url = 'https://weibo.cn/comment/Glsx3bC2d'
Cookie = "_T_WM=73adda7bb6e38819b0f820194620355e; SCF=AuRwN3mfFDIATy2carqwQiBbqV9VUMRzjvbpnoG6ioCaGUH8Z5a1vEbH-E7mJ2qgT4KK1BewVHkQBNONabFa2VM.; SUB=_2A252RLOtDeRhGeBP61IS8CfLyTWIHXVVxt3lrDV6PUJbktAKLWbTkW1NRZMdCk6DX4-225lFHjU3uHih--TE75K4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFymv2Gq.WTIUsLTkcCalE05JpX5KzhUgL.Foqpeh50eh.Neo.2dJLoI7y1wg8.9-pfw5tt; SUHB=0idrrD5Pp1F776; SSOLoginState=1530971133"
User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit\
                           /537.36 (KHTML, like Gecko) Chrome\/66.0.3359.181 Safari/537.36"

headers = {'User-Agent': User_Agent, 'Cookie': Cookie}
payload = {'uid': '6240904161', 'rl': '0','page':'1'}
pg = requests.get(url, headers=headers, params=payload)
bs = BeautifulSoup(pg.text,'html.parser')
print(bs.prettify())
Divs = bs.find_all('div',class_='c',id=re.compile(r'C_\w+'))
for div in Divs:
    id = div.find('a').get_text()
    idsite = div.find('a')['href']
    cmt = div.find('span',class_='ctt').get_text()
    time = div.find('span',class_='ct').get_text()

    print('1')


#pattern = re.compile(r'/u/\d+|^/\w+$')
#IDs = re.findall(pattern=pattern,string=Divs)
new_ID = []
'''
IDs = Divs.find_all('a',href=re.compile(r'/u/\d+|^/\w+$'))
newID = []
new_IDSites = []
for ID in IDs:
    newID.append(ID.get_text())
    new_IDSites.append(ID['href'])
print(new_IDSites)


CMTs = bs.find_all('span', class_='ctt')
new_CMTs = []
for cmt in CMTs:
    new_CMTs.append(cmt.get_text())
print(new_CMTs)

Times = bs.find_all('span',class_='ct')
new_Times = []
for time in Times:
    newtime = time.get_text()
    pattern = re.compile(r'\d+月\d+日\s\d+\S\d+|今天\s\d+\S\d+|\d{4}\S\d{2}\S\d{2}\s\d+\S\d+')
    result = re.match(pattern,newtime).group()
    new_Times.append(result)
print(new_Times)

'''


