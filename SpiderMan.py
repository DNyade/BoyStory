from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from URLManager import UrlManager
from DataOutput import DataOutput
import time

class SpiderMan():
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,url):
        # 从之前挂掉的地方继续
        # 如果文件为空则新url集合也为空
        self.manager.input_new_urls()

        #微博页的页码
        page = 1
        #爬取的微博数量计数
        count = 0

        while(page<=41):
            if self.manager.has_new_url():
                # 从url管理器获得新的评论url
                new_url = self.manager.get_new_url()
                # 输出保存当前的new_url
                self.manager.output_new_urls()
                count +=1
                print('准备爬取:'+new_url,'这是爬取的第%d条微博'%count)
                #初始化评论页页码
                cmtPage = 1
                while True:
                    try:
                        pg = self.downloader.comment_pg_download(new_url,cmtPage)
                        data = self.parser.CommentParser(url=new_url,html_cont=pg,page=cmtPage)
                        self.output.data_writer(data)

                        cmtPage +=1
                        # 防止新浪把我弄死多睡一会儿......
                        time.sleep(3)
                    except Exception:
                        # 当ctmPage超出后说明此条微博评论已经全部爬取完毕
                        break
            else:
                #下载新的一页
                print('准备爬取第%d页微博:'%page)
                pg = self.downloader.tweet_pg_download(url,page)
                #解析得到本页的评论url和数据
                data = self.parser.TweetParser(html_cont=pg,page=page)
                #本页url
                new_urls = data['URL']
                #循环添加url
                for new_url in new_urls:
                    self.manager.add_new_url(new_url)
                #存储数据
                self.output.data_writer(data)
                page +=1

        print('全部数据爬取完毕!')
if __name__ == '__main__':
    spider_man = SpiderMan()
    URL = "https://weibo.cn/u/6240904161"
    spider_man.crawl(URL)







