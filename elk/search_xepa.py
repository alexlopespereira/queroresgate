import json
import libgeohash as gh
import pandas as pd
from elasticsearch.helpers import bulk
try:
	from defs import es, ES_NOTIFICACAO_INDEX, ES_VACINEI_INDEX, ES_MENSAGENS_INDEX
except ModuleNotFoundError:
	from .defs import es, ES_NOTIFICACAO_INDEX, ES_VACINEI_INDEX, ES_MENSAGENS_INDEX
from elasticsearch_dsl import Search, Q
from datetime import datetime

from elk.send_email import send_email

RADIUS = "13km"  # TODO: mudar para 5km
BOUDING_BOX_BRASIL = {"top_left": "6.759092, -73.701466", "bottom_right": "-36.110702, -32.822774"}
PRECISION = 6

print(f"starting: {datetime.utcnow().isoformat()}")

def gendata():
    global records
    for r in records:
        r.update({"_id": f"{r['id']}", '_op_type': 'index', '_index': ES_MENSAGENS_INDEX})
        yield r


def get_counts(hashes, thresold, point):
    min_hash = None
    min_dist = thresold
    for k in hashes.keys():
        dist = gh.distance(k, point)
        if dist < min_dist:
            min_dist = dist
            min_hash = k
    if min_dist < thresold:
        return hashes[min_hash]['count'], min_hash
    else:
        return None


def send_emails(df_tasks, bucket_count):
    success = []
    for t in df_tasks.iterrows():
        orig = [float(f) for f in t[1]['location'].split(',')]
        currentgeohash = gh.encode(*orig, precision=PRECISION)
        filtered_buckets = dict(filter(lambda elem: elem[1]['vacina'] == t[1]['vacina'], bucket_count.items()))
        counts, min_hash = get_counts(filtered_buckets, int(RADIUS[:-2])*1000, currentgeohash)
        if counts is not None:
            ret = send_email(t[1]['email'], counts, t[1]['vacina'], f"https://www.google.com/maps/search/?api=1&query={t[1]['location']}")
            print(f"sent email to {t[1]['email']}, counts={counts}, vacina={t[1]['vacina']}")
            success.append(ret)
        else:
            success.append(False)
            print("error: get_counts(bucket_count, RADIUS, currentgeohash) is None")
    df_tasks['success'] = success


s = Search(using=es, index=ES_VACINEI_INDEX) \
    .filter('range', date={'gte': datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')}) \
    .filter('term', desperdicio=True) \
    .filter('geo_bounding_box', location=BOUDING_BOX_BRASIL)
s = s[:0]

records = []

s.aggs.bucket('per_geohash', 'geohash_grid', field='location', precision=PRECISION) \
    .pipeline('min_bucket_selector', 'bucket_selector', buckets_path={"count": "per_vacina._bucket_count"},
              script={"source": "params.count >= 3"}) \
    .bucket('per_vacina', 'terms', field='vacina')

response = s.execute()
results = {}
first = True
count_buckets = {}
for hit in response.aggregations.per_geohash.buckets:
    for h in hit.per_vacina.buckets:
        count_buckets[hit.key] = {'vacina': h.key, 'count': h.doc_count}
        if first:
            qf = Q('bool', must=Q('term', vacina=h.key), filter=Q('geo_distance', distance=RADIUS, location=hit.key, distance_type="plane"))
            first = False
        else:
            qf = qf | Q('bool', must=Q('term', vacina=h.key), filter=Q('geo_distance', distance=RADIUS, location=hit.key, distance_type="plane"))

if not first:
    s2 = Search(using=es, index=ES_NOTIFICACAO_INDEX)
    s2.query = qf
    response = s2.execute()
    to_notify = []
    for hit in response.hits.hits:
        mensagem = {'vacina': hit['_source']['vacina'], 'email': hit['_source']['email'], 'notification_type': 'email',
                  'date': datetime.utcnow().isoformat(), 'location': hit['_source']['location'],
                  'id': f"{hit['_source']['email']}_{hit['_source']['vacina']}_{datetime.utcnow().isoformat()}"}
        to_notify.append(mensagem)
    df_to_notify = pd.DataFrame(to_notify)
    s3 = Search(using=es, index=ES_MENSAGENS_INDEX) \
        .filter('range', date={'gte': datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')})

    response = s3.execute()
    notified = []
    for hit in response.hits.hits:
        notified.append(hit['_source'].to_dict())

    if notified:
        df_notified = pd.DataFrame(notified)
        df_diff = df_to_notify.merge(df_notified, how='outer', indicator=True, on=['email', 'vacina'],
                                     suffixes=['', '_y']).loc[lambda x: x['_merge'] == 'left_only']
        df_diff = df_diff[['vacina', 'email', 'notification_type', 'date', 'location', 'id']]
    else:
        df_diff = df_to_notify
    if not df_diff.empty:
        send_emails(df_diff, count_buckets)
        df_diff = df_diff[df_diff['success'] == True]
        records = df_diff[['vacina', 'email', 'notification_type', 'date', 'location', 'id']].to_dict('records')
        bulk(es, gendata())

print(f"finishing: {datetime.utcnow().isoformat()}")

