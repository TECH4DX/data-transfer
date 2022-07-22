from db.open_search import SingletonOSClient
from db.elastic_search import SingletonESClient

from collections import defaultdict

import json


def read_json(filename):
    """读取json文件"""
    with open(filename, "r") as f:
        hashmap = json.load(f)
        return hashmap


def write_json(filename, hashmap):
    """写入json文件"""
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(hashmap))


def read_opensearch(all_index = SingletonOSClient.get_all_index()):
    """从OpenSearch中读取索引的内容"""
    for i, index in enumerate(all_index):
        print('当前进度为: {}, {}/{}'.format(index, i + 1, len(all_index)))
        hashmap = defaultdict()
        hashmap[index] = SingletonOSClient().get_index_content(index)  # 从OpenSearch中获取每一个index的内容
        write_json('./data/' + index + ".json", hashmap)


def write_elasticsearch(all_index = SingletonOSClient.get_all_index()):
    """向ElasticSearch中写入索引的内容"""
    for index in all_index:
        hashmap = read_json('./data/' + index + ".json")
        content = hashmap[index]
        start = 0 # 由于大量写入，可能存在写入中断，灵活控制起始定位
        step = 100 # bulk每次批量写入step条数据
        for i in range(start, len(content), step):
            print('{}: total: {}, from {} to {}.'.format(index, len(content), i, min(i + step, len(content))))
            sub_content = content[i: min(i + step, len(content))]
            SingletonESClient().put_index(sub_content)  # 将该index的sub内容写入到ElasticSearch中