import pymongo

class DataOutput():

    def data_writer(self,dict,date):
        '''
        存储数据到MongoDb:按照字典的key创建collection,按照抓取起始日期创建表
        :param kwargs:
        :return:
        '''
        client = pymongo.MongoClient()
        name = 'BoyStory'+date
        db = client[name]
        for key,value in dict.items():
            if key == 'URL':
                continue
            collection = db[key]
            data_id = collection.insert(value)
