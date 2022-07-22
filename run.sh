# chmod +x ./run.sh
# ./run.sh

if test -z "$1"
then
  echo '请输出提交的内容！！命令执行格式是：./run.sh read (从OpenSearch读取index内容, 并写入JSON文件) or ./run.sh write (读取JSON文件, 并向ElasticSearch写入index内容)'
else
    python main.py "$1"
fi