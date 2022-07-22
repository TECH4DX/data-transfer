from opensearchpy import OpenSearch
from opensearchpy import helpers
import os


class SingletonOSClient(object):
    """
    Get the app in singleton mode to ensure that the app is unique throughout the project
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(SingletonOSClient, "_instance"):
            # 该脚本只在单线程模式下使用, 因此这里未加锁 (需注意多线程模式下无法保证该单例模式)。
            SingletonOSClient._instance = object.__new__(cls)
            SingletonOSClient.client = SingletonOSClient().get_client()
        return SingletonOSClient._instance

    def __init__(self):
        pass

    def get_client(self):
        """创建连接"""
        host = os.environ.get('OPEN_SEARCH_HOST', '')
        port = os.environ.get('OPEN_SEARCH_PORT', '')
        auth = (os.environ.get('OPEN_SEARCH_USER', ''),
                os.environ.get('OPEN_SEARCH_PASSWORD', ''))

        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=False,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=True,
            verify_certs=False
        )

        print("Connect to OpenSearch: ", client.ping())

        return client

    def query_all(self, field_name="origin", match_all=False):
        """查询索引全部内容"""
        if match_all:
            query = {
                "query": {
                    "match_all": {}
                }
            }
        else:
            query = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "wildcard": {
                                    field_name: {
                                        "value": "*mindspore*"
                                    }
                                }
                            },
                            {
                                "wildcard": {
                                    field_name: {
                                        "value": "*openeuler*"
                                    }
                                }
                            },
                            {
                                "wildcard": {
                                    field_name: {
                                        "value": "*opengauss*"
                                    }
                                }
                            }
                        ]
                    }
                }
            }

        return query

    def get_index_content(self, index_name):
        """查询索引全部内容"""

        # 根据不同index, 匹配不同query设置
        field_name = "origin"
        match_all = False
        if index_name == "contributors":
            field_name = 'tag'
        if index_name == 'mindspore_sigs' or index_name == 'opengauss_sigs':
            match_all = True

        response = helpers.scan(
            client=self.client, index=index_name, query=self.query_all(field_name, match_all))
        response = [record for record in response]
        return response

    @staticmethod
    def get_all_index():
        """
        静态方法, 因为目前all_index列表与OpenSearch实例无关, 后续如果使用get_client().indices.get('*'), 则需改为实例方法
        获取所有索引列表
        """
        # return get_client().indices.get('*')  # 该账户无超级管理员权限, AuthorizationException(403, 'security_exception', 'no permissions for [indices:admin/get] and User [name=DX2022, backend_roles=[], requestedTenant=null]')
        all_index = ['contributors',
                     'gitee_repo-raw',
                     'gitee_issues-enriched', 'gitee_issues-raw',
                     'gitee_pulls-enriched', 'gitee_pulls-raw',
                     'mindspore_sigs', 'opengauss_sigs'
                     ]
        return all_index


if __name__ == '__main__':
    pass
    # all_index = get_all_index()
    # for index in all_index:
    #     content = get_index_content(index)
    #     # 知道每一个index的mapping和content了, 就可以在es中根据mapping建立索引, 根据content导入数据
