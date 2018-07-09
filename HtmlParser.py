import re
from bs4 import BeautifulSoup

class HtmlParser():

    def TweetParser(self,html_cont,page):
        if html_cont is None:
            print('微博页爬取失败!请检查Cookie!')
            return
        bs = BeautifulSoup(html_cont,'html.parser')
        cmt_urls = self._get_cmt_url(bs)

        like, repost, comment, date = self._get_zpzt(html_cont)
        ctt = self._get_context(bs)
        if page == 1:
            ctt = ctt[3:]

        if len(like) == len(ctt):
            print('微博页爬取信息正确!')
        else:
            print('微博页爬取信息缺失!')
            return

        basicData = []
        for i in range(len(like)):
            tempDic = {'LIKE': int(like[i]),
                       'REPOST': int(repost[i]),
                       'COMMENT': int(comment[i]),
                       'TIME': date[i],
                       'CONTEXT': ctt[i]}
            basicData.append(tempDic)

        return {'URL':cmt_urls,
                'TPdata':basicData}

    def _get_cmt_url(self,bs):
        '''
        获得某页所有微博的评论页URL
        :param bs:bs
        :return:set of new urls
        '''
        new_urls = set()
        links = bs.find_all('a',href=re.compile(r'https://weibo.cn/comment/\w+'))
        for link in links:
            new_url = link['href']
            pattern = re.compile(r'https://weibo.cn/comment/\w+(?=\?)')
            result = re.match(pattern,new_url).group()
            new_urls.add(result)
        return new_urls

    def _get_zpzt(self,html_cont):
        '''
        获得某页所有微博的转评赞数量及发布时间
        :param bs: bs
        :return: list*4
        '''
        like = re.findall(r'(?<=>赞\[)\d+(?=\]</a>)', html_cont)
        repost = re.findall(r'(?<=>转发\[)\d+', html_cont)
        comment = re.findall(r'(?<=>评论\[)\d+', html_cont)
        date = re.findall(r'\d+月\d+日\s\d+\S\d+|今天\s\d+\S\d+|\d{4}\S\d{2}\S\d{2}\s\d+\S\d+', html_cont)

        if len(like)==len(repost) & len(like)==len(comment) & len(like)==len(date):
            return like,repost,comment,date
        else:
            print('转评赞及时间爬取数量不等')
            return None

    def _get_context(self,bs):
        '''
        获得某页所有微博的内容
        :param bs:
        :return: list of context
        '''
        contextList = bs.findAll('span', {'class': 'ctt'})
        cttList = []
        for ctt in contextList:
            cttList.append(ctt.get_text())
        return cttList


    def CommentParser(self,url,html_cont,page):
        '''
        获得评论页的评论：评论地址、评论人ID、评论人ID域名、评论内容、评论时间
        :param bs: bs
        :return:list*4
        '''
        if html_cont is None:
            return

        # 解析评论域名
        pattern = re.compile(r'(?<=comment/)\w+')
        cmtSite = re.search(pattern=pattern,string=url).group()

        bs = BeautifulSoup(html_cont, 'html.parser')
        ID,IDSite,CMT,cmtTime = self._get_cmt(bs)
        # 去除第一个随机的三个热门ID
        if page == 1:
            ID = ID[3:]
            IDSite = IDSite[3:]
            CMT = CMT[3:]
            cmtTime = cmtTime[3:]

        if len(ID) == len(CMT) & len(ID) == len(cmtTime):
            print('评论页Page'+str(page)+'爬取信息正确!')
        else:
            print('评论页Page'+str(page)+'爬取信息错误!ID,Time,CMT不相等!')
            return

        basicData = []
        for i in range(len(ID)):
            tempDic = {'CMTSITE':cmtSite,
                       'ID': ID[i],
                       'IDSITE':IDSite[i],
                       'CMTCONTEXT': CMT[i],
                       'CMTTIME': cmtTime[i]}
            basicData.append(tempDic)

        return {'CPData':basicData}

    def _get_cmt(self,bs):
        '''
        获得评论页的评论人ID、域名、评论内容和评论时间
        :return:
        '''
        divs = bs.find_all('div', class_='c', id=re.compile(r'C_\w+'))
        new_IDs = []
        new_IDSites = []
        new_CMTs = []
        new_Times = []
        for div in divs:
            new_IDs.append(div.find('a').get_text())
            new_IDSites.append(div.find('a')['href'])
            new_CMTs.append(div.find('span', class_='ctt').get_text())
            time = div.find('span', class_='ct').get_text()
            pattern = re.compile(r'\d+月\d+日\s\d+\S\d+|今天\s\d+\S\d+|\d{4}\S\d{2}\S\d{2}\s\d+\S\d+')
            time = re.match(pattern,time).group()
            new_Times.append(time)

        return new_IDs,new_IDSites,new_CMTs,new_Times



    def _get_ID(self,bs):
        '''
        获得评论页的评论人ID和域名
        :param bs: bs
        :return:
        '''
        IDs = bs.find_all('a',href=re.compile(r'/u/\d+|^/\w+$'))
        # < a href = "/u/3090895917" > skye_May < / a >
        # < a href = "/xiaoxiaobaolan" > 南音若何 < / a >
        # 个性域名不满足一般ID的格式...
        new_IDs = []
        new_IDSites = []
        for ID in IDs:
            new_IDs.append(ID.get_text())
            new_IDSites.append(ID['href'])

        return new_IDs, new_IDSites

    def _get_comment(self,bs):
        '''
        获得评论页的评论
        :param bs:
        :return:
        '''
        CMTs = bs.find_all('span',class_='ctt')
        #< span class ="ctt" > 求官官补货！求官官补货！求官官补货！[祈祷][鲜花][鲜花][鲜花][鲜花][鲜花][鲜花]
        # < a href="/n/BOYSTORY_Official" > @ BOYSTORY_Official < / a > < / span >
        new_CMTs = []
        for cmt in CMTs:
            new_CMTs.append(cmt.get_text())
        new_CMTs = new_CMTs[4:]

        return new_CMTs

    def _get_time(self,bs):
        '''
        获得评论的时间
        :param bs:
        :return:
        '''
        Times = bs.find_all('span',class_='ct')
        new_Times = []
        for time in Times:
            new_time = time.get_text()
            ### 去除"来自网页"的影响
            pattern = re.compile(r'\d+月\d+日\s\d+\S\d+|今天\s\d+\S\d+|\d{4}\S\d{2}\S\d{2}\s\d+\S\d+')
            result = re.match(pattern, new_time).group()
            new_Times.append(result)
        new_Times = new_Times[4:]

        return new_Times











