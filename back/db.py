import pymongo
import redis
from loguru import logger


# 封装操作，用于打印操作信息
class MongoClient():
    def __init__(self, database_name: str='tpcosmo', collection_name='test'):
        # 连接mongo客户端
        self.mongo_client = pymongo.MongoClient("mongodb://White:klx5596688@8.222.210.54:27071/admin")[database_name][collection_name]
        # 存储参数
        self.database_name = database_name
        self.collection_name = collection_name

    # 插入数据
    def insert_data(self, data: dict or list):
        logger.debug(f"正在进行插入操作: {self.database_name}|{self.collection_name} -> {data}")
        # many
        if type(data) == list:
            self.mongo_client.insert_many(data)
            logger.debug(f"插入数据库多条 {self.database_name}|{self.collection_name} —> {len(data)}|{data}")
        # one
        elif type(data) == dict:
            logger.debug(f"插入数据库单条 {self.database_name}|{self.collection_name} —> {len(data)}|{data}")
            self.mongo_client.insert_one(data)
        # erro
        else:
            logger.error(f"插入mongo数据库出错 -> 传入参数有误: {type(data)}|{data}")

    # 查询数据
    def find(self, filter: dict, only_one: bool=False, is_last: bool=False):
        if is_last:
            sort_param = [("_id", -1)]
        else:
            sort_param = None
        logger.debug(f"正在进行查询操作: {self.database_name}|{self.collection_name} -> {filter}")
        if only_one:
            r = self.mongo_client.find_one(filter, sort=sort_param)
        else:
            r = self.mongo_client.find(filter, sort=sort_param)
            r = list(r)
        logger.debug(f"查询到数据结果: {len(r) if r else ''}|{r}")
        return r

    # 更新数据
    def update_data(self, filter: dict, update: dict, update_many=False, upsert=False, costumed=False):
        """

        :param filter:
        :param update:
        :param update_many:
        :param upsert:
        :param costumed: 自定义
        :return:
        """
        logger.debug(f"正在进行更新操作: {self.database_name}|{self.collection_name} -> {filter}|{update}")
        if not costumed:
            update = {
                '$set': update
            }

        # print('update:', update)
        if update_many:
            r = self.mongo_client.update_many(filter, update, upsert=upsert)
        else:
            r = self.mongo_client.update_one(filter, update, upsert=upsert)

        r = (r.matched_count, r.modified_count)
        logger.debug(f"更新结果: (匹配, 更新)|{r}")
        return r

    # 聚合语句
    def aggregate(self, pipeline: list):
        r = self.mongo_client.aggregate(pipeline)
        logger.debug(f"pipleine执行结果: {r}")
        return r


# class redis_client():
#     def __init__(self):
#         self.redis_client = redis.Redis(host='8.222.210.54', password='Klx5596688')
#
#     def hset(self):
#         pass
#
#     def hget(self):
#         pass


# mongo_client = pymongo.MongoClient("mongodb://White:klx5596688@8.222.210.54:27071/admin")
# r = MongoClient(collection_name='user_base_info').find({'openid': 'oB4qP6eXuFoEEz_61EGXlDrR9LlQ'}, only_one=True)
# print(r)


#
# mongo_client['test']['test'].insert_one({'key': '1'})
# r = mongo_client['test']['test'].find()
# print(r)
# print(list(r))
# r = mongo_client['test']['test'].find_one()
# print(r)
# print(list(r))


mongo_client = pymongo.MongoClient("mongodb://White:klx5596688@8.222.210.54:27071/admin")
# r = MongoClient(database_name='test', collection_name='test').update_data({'key': 'value'}, {'key': 1})
# print(r)

redis_client = redis.Redis(host='8.222.210.54', password='Klx5596688')
