
def serializer(siteInfo) -> dict:
  return{
    "id":str(siteInfo["_id"]),
    "url":siteInfo["url"],
    "classification":siteInfo["classification"],
    "category":siteInfo["category"],
    "ranking_change":siteInfo["ranking_change"],
    "average_visit_duration":siteInfo["average_visit_duration"],
    "pages_per_visit":siteInfo["pages_per_visit"],
    "bounce_rate":siteInfo["bounce_rate"],
    "top_countries":siteInfo["top_countries"],
    "gender_distribution":siteInfo["gender_distribution"],
    "age_distribution":siteInfo["age_distribution"],
    "competitors":siteInfo["competitors"],
    "keywords":siteInfo["keywords"],
  }

def serializerList(sitesInfo) -> list:
  return[serializer(siteInfo) for siteInfo in sitesInfo if siteInfo != None]
  