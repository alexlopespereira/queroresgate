from defs import es, ES_ALERTA_INDEX, ES_VACINEI_INDEX
from elasticsearch_dsl import Search
from datetime import datetime
import pprint
radius = 2220
pp = pprint.PrettyPrinter(indent=4)

s = Search()
s.aggs.bucket('tags', 'terms', field='category')\
    .metric('seller_qtt', 'cardinality', field='seller_code')\
    .pipeline('product_bucket_sort', 'bucket_sort', sort=[{'seller_qtt': 'desc'}])
print(s.to_dict())

s = Search(using=es, index=ES_VACINEI_INDEX)
        # \
        # .filter('range', date={'gte': datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')})\
        # .filter('term', desperdicio=True)\
        # .filter('geo_bounding_box', location={"top_left": "6.759092, -73.701466", "bottom_right": "-36.110702, -32.822774"})
# s = s[:0]
s.aggs.bucket('per_geohash', 'geohash_grid', field='location', precision=4)\
    .bucket('per_vacina', 'terms', field='vacina') \
    .metric('cnes_qtt', 'cardinality', field='seller_code') \
    .pipeline('min_bucket_selector', 'bucket_selector', buckets_path={"count": "per_vacina._bucket_count"},
              script={"source": "params.count > 1"})

print(s.to_dict())
response = s.execute()
results = {}
for hit in response.aggregations.per_geohash.buckets:
    print(hit)

# s = Search(using=es, index=ES_ALERTA_INDEX) \
#     .filter('geo_distance', distance='{0}m'.format(radius), geohome={"lat": point[0], "lon": point[1]})