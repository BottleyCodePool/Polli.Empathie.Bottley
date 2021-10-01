from elasticsearch import Elasticsearch

def connect():
    """
    Connect to ElasticSearch with environment credentials
    """
    ### Connect to Elasticsearch ###
    try:
        esClient = Elasticsearch(hosts=["0.0.0.0"])
    except Exception as e:
        print('[ERROR][elasticsearchConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    if esClient.ping() != True:
        print('[ERROR][elasticsearchConnector]: ElasticSearch "connect" error')
        return False
    return esClient
