import pandas as pd
from pymongo import MongoClient
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
import re

def MongoConnecter(database,clction):
    '''
    从数据库获取表输出为DataFrame格式
    :param database:
    :param clction:
    :return:
    '''
    client = MongoClient()
    db = client[database]
    collection = db[clction]
    data = pd.DataFrame(list(collection.find()))
    return data

def plotZPZ(data):
    '''
    绘制转评赞的曲线图
    :param data:
    :return:
    '''
    data.plot(y=['LIKE','COMMENT','REPOST'],figsize=(12,6))
    plt.show()

def time_adder(data):
    '''
    在DataFrame中添加表示时间的列
    :param data:
    :return:
    '''
    data2 = data.copy()
    #添加列
    for index, row in data.iterrows():
        data2.loc[index, 'YEAR'] = int(index.year)
        data2.loc[index, 'MONTH'] = index.month
        data2.loc[index, 'DAY'] = index.day
        data2.loc[index, 'HOUR'] = index.hour
        data2.loc[index, 'MINUTE'] = index.minute
    #转换数据格式为int
    data2[['YEAR','MONTH','DAY','HOUR','MINUTE']] = \
        data2[['YEAR','MONTH','DAY','HOUR','MINUTE']].astype('int64')
    return data2


def plotTweetFreq(data, year):
    '''
    绘制发博频率柱状图,以月为单位.
    :param data:
    :param year:
    :return:
    '''
    taData = time_adder(data)
    Data = taData[taData.YEAR == year]
    freq = Data['MONTH'].value_counts()

    MONTH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for m in MONTH:
        if m not in freq.index.tolist():
            freq[m] = 0

    freq = freq.sort_index()
    freq.plot(kind='bar', figsize=(12, 6))
    plt.xlabel('Month')  # 横轴标题
    plt.ylabel('Tweets')  # 纵轴标题
    plt.show()

def plotTweetTimeFreq(data):
    Data = time_adder(data)
    freq = Data['HOUR'].value_counts()
    freq = freq.sort_index()
    #转换0点为24点
    Index = freq.index.tolist()
    Index[0] = 24
    freq.index = Index
    freq = freq.sort_index()
    freq.plot(kind='bar', figsize=(12, 6))
    plt.xlabel('HOUR')  # 横轴标题
    plt.ylabel('Tweets')  # 纵轴标题
    plt.show()

def name_counter(data,name):
    '''
    通过计数评论中出现名字的次数来代表个人关注度
    :return:
    '''
    # 遍历数据库 去匹配姓名

    if name == '贾涵予':
        pattern = re.compile(r'贾涵予|涵予|队长|老大|贾宝|jhy')
    elif name == '李梓豪':
        pattern = re.compile(r'李梓豪|梓豪|爷|棋棋|棋哥|lzh')
    elif name == '贺鑫隆':
        pattern = re.compile(r'贺鑫隆|鑫隆|隆隆|恐龙|贺撩撩|隆哥|hxl')
    elif name == '于泽宇':
        pattern = re.compile(r'于泽宇|泽宇|甜豆|甜宇|小宇|yzy')
    elif name == '苟明睿':
        pattern = re.compile(r'苟明睿|明睿|狗狗|苟苟|睿睿|gmr')
    elif name == '任书漾':
        pattern = re.compile(r'任书漾|书漾|漾漾|忙内|rsy')
    else:
        print('人名输入错误!')
        return
    count = 0
    context = []
    for index, row in data['CMTCONTEXT'].iteritems():
        if re.search(pattern, row):
            count += 1
            context.append(row)
    return count, context





if __name__ == '__main__':

    TPdata = MongoConnecter(database='BoyStory2018-07-10',clction='TPData')

    #转换时间格式
    TPdata['TIME'] = pd.to_datetime(TPdata['TIME'])
    #设置索引
    TPdata.set_index('TIME',inplace=True,drop=False)

    # 绘制转评赞数量图
    # 发现异常值 查看
    # 清洗掉四张单曲发布的微博
    # 绘制转评赞数量图
    # 统计发博时间
    ## 绘制发博月频柱状图
    ## 绘制发博小时频柱状图
    # 分析微博内容：微博分类

    #让我来思考一下CPdata可以干啥
    # 评论内容方面
    # 1.统计一下六个孩子的关注度 -->用正则匹配就可以了
    # 2.情感分析 -->不知道咋做
    # 评论用户方面
    # 1.继续去爬用户的信息 -->关注书

    CPData = MongoConnecter(database='BoyStory2018-07-10',clction='CPData')
    count = [0 for i in range(6)]
    context = [0 for i in range(6)]
    count[0], context[0] = name_counter(data=CPData,name='贾涵予')
    count[1], context[1] = name_counter(data=CPData,name='李梓豪')
    count[2], context[2] = name_counter(data=CPData,name='贺鑫隆')
    count[3], context[3] = name_counter(data=CPData,name='于泽宇')
    count[4], context[4] = name_counter(data=CPData,name='苟明睿')
    count[5], context[5] = name_counter(data=CPData,name='任书漾')
    print(count)









