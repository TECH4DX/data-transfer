# data-transfer installation guide

```bash
# Get the project
$ git clone https://github.com/TECH4DX/data-transfer.git
# Run the project to read data from the OpenSearch
$ ./run.sh read
# Run the project to write data to the ElasticSearch
$ ./run.sh write
```

```python3
# To run this project:
# Please set the variable values in advance in utils\open_search.py.
# OPEN_SEARCH_HOST: The host of the OpenSearch.
# OPEN_SEARCH_PORT: The port of the OpenSearch.
# OPEN_SEARCH_USER: Username.
# OPEN_SEARCH_PASSWORD: Password.
host = os.environ.get('OPEN_SEARCH_HOST', '')
port = os.environ.get('OPEN_SEARCH_PORT', '')
auth = (os.environ.get('OPEN_SEARCH_USER', ''),  os.environ.get('OPEN_SEARCH_PASSWORD', ''))

# Please set the variable values in advance utils\elastic_search.py.
# ELASTIC_SEARCH_HOST: The host of the ElasticSearch.
# ELASTIC_SEARCH_PORT: The port of the ElasticSearch.
# ELASTIC_SEARCH_USER: Username.
# ELASTIC_SEARCH_PASSWORD: Password.
host = os.environ.get('ELASTIC_SEARCH_HOST', '')
port = os.environ.get('ELASTIC_SEARCH_PORT', '')
auth = (os.environ.get('ELASTIC_SEARCH_USER', ''),  os.environ.get('ELASTIC_SEARCH_PASSWORD', ''))
```