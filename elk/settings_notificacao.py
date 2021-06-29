
body_settings_notificacao = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "email": {
        "type": "keyword"
      },
      "location": {
          "type": "geo_point"
      },
      "vacina":
      {
        "type": "keyword"
      },
      "date":
      {
        "type":   "date",
        "format": "date_optional_time"
      },
      "alerted_today":
      {
        "type":   "boolean",
        "null_value": False
      }
    }
  }
}
