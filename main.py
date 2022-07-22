from utils.utils import read_opensearch, write_elasticsearch

import urllib3
urllib3.disable_warnings()  # 在未启用证书验证的情况下向 HTTPS URL 发出请求时会发生警告，disable_warnings可禁用警告

import sys

if __name__ == '__main__':
    # IS_READ = False # 控制从OpenSearch读取或者向ElasticSearch写入
    IS_READ = True if sys.argv[1] == 'read' else False # 通过run.sh脚本, 控制从OpenSearch读取或者向ElasticSearch写入
    if IS_READ:
        # 从OpenSearch中读取数据并写入JSON文件. 使用JSON文件当做缓存, 原因是数据量太大, 蓝云内存会崩溃.
        read_opensearch()
    else:
        # 从JSON文件读取数据，并写入到ElasticSearch
        write_elasticsearch()
