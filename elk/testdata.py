from elasticsearch.helpers import bulk
from datetime import datetime
from defs import es, ES_ALERTA_INDEX, ES_VACINEI_INDEX
from elasticsearch_dsl import Search
import pandas as pd
import json
records = []
index = None

def create_vacinei_json(file):
    s = Search(using=es, index=ES_VACINEI_INDEX)
    response = s.execute()
    result = []
    for hit in response.hits.hits:
        hit['_source']['id'] = hit['_source']['e-mail']
        hit['_source']['email'] = hit['_source']['e-mail']
        del hit['_source']['@timestamp']
        del hit['_source']['e-mail']
        result.append(hit['_source'].to_dict())

    df = pd.DataFrame(data=result)
    df.to_json(file, orient="records")


def create_alerta_json(file):
    s = Search(using=es, index=ES_ALERTA_INDEX)
    response = s.execute()
    result = []
    for hit in response.hits.hits:
        alerta = {"email": hit['_source']['email'], "location": hit['_source']['location'], "vacina": hit['_source']['vacina'],
                  "id": hit['_id'], "date": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')} #, "alerted_today": False
        result.append(alerta)

    df = pd.DataFrame(data=result)
    df.to_json(file, orient="records")

def gendata_vacinei():
    global records
    for r in records:
        doc = {"doc": r, "_id": r['id'], '_op_type': 'update', 'doc_as_upsert': True, '_index': ES_VACINEI_INDEX}
        yield doc

def gendata():
    global records
    global index
    for r in records:
        doc = {"doc": r, "_id": r['id'], '_op_type': 'update', 'doc_as_upsert': True, '_index': index}
        yield doc

def index_vacinei(file):
    global records
    with open(file) as json_file:
        records = json.load(json_file)
        for r in records:
            r['date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z') #datetime.strptime(r['date'], "%b %d, %Y, %H:%M:%S.%f") #datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            r['data_vacinacao'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')# datetime.strptime(r['data_vacinacao'], "%b %d, %Y, %H:%M:%S.%f") #datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            loc = r['location'].split(',')
            r['location'] = ','.join(loc[::-1])

        bulk(es, gendata_vacinei())

def index_generic(file, curr_index):
    global records
    global index
    index = curr_index
    with open(file) as json_file:
        records = json.load(json_file)
        bulk(es, gendata())

# index_json("./testdata.json")
file_alertas = "./testdata_alertas.json"
# create_alerta_json(file_alertas)
index_generic(file_alertas, ES_ALERTA_INDEX)
