import pymongo

class DataOutput():

    def data_writer(self,dict):
        '''
        存储数据到MongoDb:按照字典的key创建collection
        :param kwargs:
        :return:
        '''
        client = pymongo.MongoClient()
        db = client.BoyStory
        for key,value in dict.items():
            if key == 'URL':
                continue
            collection = db[key]
            data_id = collection.insert(value)
