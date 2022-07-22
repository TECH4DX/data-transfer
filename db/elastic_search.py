from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os


class SingletonESClient(object):
    """
    Get the app in singleton mode to ensure that the app is unique throughout the project
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(SingletonESClient, "_instance"):
            SingletonESClient._instance = object.__new__(cls)  # 该脚本只在单线程模式下使用，因此这里未加锁 (需注意多线程模式下无法保证该单例模式)。
            SingletonESClient.client = SingletonESClient.get_client(SingletonESClient)  #
        return SingletonESClient._instance

    def __init__(self):
        pass

    def get_client(self):
        """创建连接"""
        host = os.environ.get('ELASTIC_SEARCH_HOST', '')
        port = os.environ.get('ELASTIC_SEARCH_PORT', '')
        auth = (os.environ.get('ELASTIC_SEARCH_USER', ''), os.environ.get('ELASTIC_SEARCH_PASSWORD', ''))

        client = Elasticsearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=auth,
            timeout=60000
        )

        print("Connect to ElasticSearch: ", client.ping())

        return client

    def query_all(self):
        """查询索引全部内容"""
        query = {
            "query": {
                "match_all": {}
            }
        }

        return query

    def get_index_content(self, index_name):
        """查询索引全部内容"""
        response = helpers.scan(client=self.client, index=index_name, query=self.query_all())
        response = [record for record in response]
        return response

    def get_all_index(self):
        """获取所有索引列表"""
        client = self.client
        all_index = client.indices.get('*')
        return all_index

    def put_index(self, content):
        """创建索引"""
        helpers.bulk(client=self.client, actions=content)

    def delete_index(self, index):
        """删除索引"""
        self.client.indices.delete(index)


if __name__ == '__main__':
    print(SingletonESClient().get_all_index().keys())
    # SingletonESClient().delete_index('gitee_issues-enriched')
    print(SingletonESClient().get_all_index().keys())
