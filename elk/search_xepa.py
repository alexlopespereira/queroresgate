import json

import pandas as pd
from elasticsearch.helpers import bulk

from defs import es, ES_ALERTA_INDEX, ES_VACINEI_INDEX, ES_NOTIFICACOES_INDEX
from elasticsearch_dsl import Search, Q
from datetime import datetime

def gendata():
    global records
    for r in records:
        r.update({"_id": f"{r['id']}", '_op_type': 'index', '_index': ES_NOTIFICACOES_INDEX})
        yield r


RADIUS = "10km" #TODO: mudar para 5km
BOUDING_BOX_BRASIL = {"top_left": "6.759092, -73.701466", "bottom_right": "-36.110702, -32.822774"}

s = Search(using=es, index=ES_VACINEI_INDEX)\
        .filter('range', date={'gte': datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')})\
        .filter('term', desperdicio=True)\
        .filter('geo_bounding_box', location=BOUDING_BOX_BRASIL)
s = s[:0]

records = []

# TODO: mudar precision para 6
s.aggs.bucket('per_geohash', 'geohash_grid', field='location', precision=5)\
    .pipeline('min_bucket_selector', 'bucket_selector', buckets_path={"count": "per_vacina._bucket_count"},
              script={"source": "params.count >= 0"})\
    .bucket('per_vacina', 'terms', field='vacina')

response = s.execute()
results = {}
first = True
for hit in response.aggregations.per_geohash.buckets:
    for h in hit.per_vacina.buckets:
        if first:
            qf = Q('bool', must=Q('term', vacina=h.key), filter=Q('geo_distance', distance=RADIUS, location=hit.key, distance_type="plane"))
            first = False
        else:
            qf = qf | Q('bool', must=Q('term', vacina=h.key), filter=Q('geo_distance', distance=RADIUS, location=hit.key, distance_type="plane"))

if not first:
    s2 = Search(using=es, index=ES_ALERTA_INDEX)
    s2.query = qf
    response = s2.execute()
    to_notify = []
    for hit in response.hits.hits:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={hit['_source']['location']}"
        alerta = {'vacina': hit['_source']['vacina'], 'email': hit['_source']['email'], 'notification_type': 'email',
                  'date': datetime.utcnow().isoformat(), 'location': hit['_source']['location'],
                  'id': f"{hit['_source']['email']}_{hit['_source']['vacina']}_{datetime.utcnow().isoformat()}"}
        to_notify.append(alerta)
    df_to_notify = pd.DataFrame(to_notify)
    s3 = Search(using=es, index=ES_NOTIFICACOES_INDEX) \
        .filter('range', date={'gte': datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')})
    print(json.dumps(s3.to_dict()))
    response = s3.execute()
    notified = []
    for hit in response.hits.hits:
        notified.append(hit['_source'].to_dict())
    df_notified = pd.DataFrame(notified)
    df_diff = df_to_notify.merge(df_notified, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
    records = df_diff.to_dict('records')

    bulk(es, gendata())



# q1 = Q('bool', must=Q('term', vacina='pfizer'), filter=Q('geo_distance', distance=radius, location="6vjvv", distance_type="plane"))
# q2 = Q('bool', must=Q('term', vacina='jansen'), filter=Q('geo_distance', distance=radius, location="6vjvv", distance_type="plane"))
# print(q.to_dict())
#     .filter('geo_distance', distance='{0}m'.format(radius), geohome={"lat": point[0], "lon": point[1]})
