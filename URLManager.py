class UrlManager():
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_url_size()!=0

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self,url):
        '''
        将新的URL添加到未爬取的URL集合中
        :param url: 单个URL
        :return:
        '''
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def new_url_size(self):
        '''
        获取未爬取URL集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已经爬取URL集合的大小
        :return:
        '''
        return len(self.old_urls)

    def output_new_urls(self):
        '''
        为了防止爬虫由于各种原因挂掉，需要记录某一页中未被爬取的微博地址
        这样挂掉之后就可以继续了，不需要重新开始或去重的操作！！
        :return:
        '''
        txtName = 'newUrls.txt'
        f = open(txtName, 'w')
        # 每次清空重新写数据
        for url in self.new_urls:
            f.write(url+'\n')
        f.close()

    def input_new_urls(self):
        '''
        读取之前挂掉时保存的url
        :return:
        '''
        txtName = 'newUrls.txt'
        f = open(txtName,'r')
        sourceInLines = f.readlines()
        f.close()

        # 定义一个空列表，用来存储结果
        urls = []
        for line in sourceInLines:
            # 去掉每行最后的换行符'\n'
            temp = line.strip('\n')
            urls.append(temp)
        self.new_urls = set(urls)
