import requests

class HtmlDownloader():
    def __init__(self):
        self.Cookie = "SUB=_2A252RbFkDeRhGeBP61IS8CfLyTWIHXVVyd8srDV6PUJbktANLXH6kW1NRZMdChrsv1k5ehpXyIsoUiHl9oe1tL9C; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFymv2Gq.WTIUsLTkcCalE05JpX5KzhUgL.Foqpeh50eh.Neo.2dJLoI7y1wg8.9-pfw5tt; SUHB=0BLo9ufWOXZgpy; SSOLoginState=1531035956; _T_WM=dd60ec8f5e81cb4688f6a303047054d2"
        self.User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit\
                           /537.36 (KHTML, like Gecko) Chrome\/66.0.3359.181 Safari/537.36"

        self.headers = {'User-Agent': self.User_Agent,'Cookie': self.Cookie}


    def tweet_pg_download(self, url, *args):
        '''
        下载微博页
        :param url: 微博页url
        :param args: 微博页页数
        :return:
        '''
        if url is None:
            return

        payload = {'page': str(args[0])}
        pg = requests.get(url, headers=self.headers, params=payload)
        if pg.status_code==200:
            pg.encoding = 'utf-8'
            return pg.text
        return None

    def comment_pg_download(self, url, *args):
        '''
        下载评论页
        :param url: 某条微博的评论页url
        :param args: 评论页页数
        :return:
        '''
        if url is None:
            return

        payload = {'uid':'6240904161','rl':'0','page':str(args[0])}
        pg = requests.get(url, headers=self.headers, params=payload)
        if pg.status_code==200:
            return pg.text
        return None
