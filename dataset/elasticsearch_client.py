import json

from elasticsearch import Elasticsearch, helpers


def elasticsearch_config():
    return {
        'host': '/0aafb416713842b4921b1a2a1ced7925:dXMtZWFzdC0yLmF3cy5lbGFzdGljLWNsb3VkLmNvbTo0NDMkZjRlNWYxNjBmMWIxNDVjMDgyMGFmMjVjYzM3NjIxMDkkNmMzZGQ2NjI3MzM4NDk5YmI1ZmYyMjNiMTZkODUzZTA=',
        'username': 'elastic',
        'password': '8BFTuuzDdbXRCue5U0V87dq8',
        'index_name': 'metaphors'
    }


def get_client() -> Elasticsearch:
    c = elasticsearch_config()
    return Elasticsearch(cloud_id=c['host'],
                         basic_auth=(c['username'], c['password']))


def delete_metaphor_index():
    c = elasticsearch_config()
    client = get_client()
    print(client.indices.delete(index=c['index_name'], ignore_unavailable=True))


def create_metaphor_index():
    c = elasticsearch_config()
    index_name = c['index_name']
    with open('dataset/index_config.json', mode='r', encoding='utf_8') as json_file:
        config = json.load(json_file)

    client = get_client()
    print(client.indices.delete(index=index_name, ignore_unavailable=True))
    print(client.indices.create(index=index_name, settings=config['settings'], mappings=config['mappings']))


def tokenize_text(text, analyzer='plain'):
    c = elasticsearch_config()

    client = get_client()
    res = client.indices.analyze(index=c['index_name'], analyzer=analyzer, text=text)
    return res['tokens'], ' '.join([t['token'] for t in res['tokens']])


def bulk_insert_documents(docs):
    client = get_client()
    c = elasticsearch_config()
    return helpers.bulk(client=client, actions=docs, index=c['index_name'])


def insert_document(doc):
    client = get_client()
    c = elasticsearch_config()

    return client.index(index=c['index_name'], document=doc)


def search(query, size=100):
    client = get_client()
    c = elasticsearch_config()

    res = client.search(index=c['index_name'], query=query, size=size)

    if res['timed_out']:
        raise RuntimeError('Search request timed out.')
    return res['hits']
