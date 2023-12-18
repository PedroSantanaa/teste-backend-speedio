from email.mime import base
import re
from fastapi import APIRouter,HTTPException
from models.siteInfo_model import SiteInfo
from config.database import collection_name
from schemas.schemas import serializer
from config.headers import headersNoAuth, headersAuth
import requests
from fastapi import status
import json

router=APIRouter()

#GET ROUTE /get_info já que o metodo GET é o mais apropriado para pegar dados do banco de dados
@router.get("/get_info/{url}")
async def get_info_GET(url: str):
  site= collection_name.find_one({"url":url})
  if site == None:
    raise HTTPException(status_code=404, detail="Site not found")
  return serializer(site)
  
#POST ROUTE /get_info já que o teste pede para que utilize o metodo POST para pegar dados do banco de dados
@router.post("/get_info")
async def get_info_POST(url: str):
  site= collection_name.find_one({"url":url})
  if site == None:
    raise HTTPException(status_code=404, detail="Site not found")
  return serializer(site)

#POST ROUTE /salve_info or /save_info já que o teste pede para que utilize o metodo POST para salvar dados no banco de dados
@router.post("/save_info")
async def save_info(url:str):
  noAuth_url=f'https://data.similarweb.com/api/v1/data?domain={url}'
  auth_url_demographic=f'https://pro.similarweb.com/widgetApi/DemographicSegments/Sectors/Table?from=2023%7C09%7C01&to=2023%7C11%7C30&country=999&webSource=Total&includeSubDomains=true&keys={url}'
  auth_url_similars= f'https://pro.similarweb.com/api/WebsiteOverview/getsimilarsites?key={url}&limit=5'
  responseNoAuth= requests.get(noAuth_url,headers=headersNoAuth)
  responseAuthDemographic = requests.get(auth_url_demographic,headers=headersAuth)
  responseAuthSimilarSites = requests.get(auth_url_similars,headers=headersAuth)
  if responseNoAuth.status_code == 200 and responseAuthDemographic.status_code == 200 and responseAuthSimilarSites.status_code == 200:
    dataNoAuth=json.loads(responseNoAuth.text)
    dataAuthDemographic=json.loads(responseAuthDemographic.text)
    dataAuthSimilarSites=json.loads(responseAuthSimilarSites.text)
    

    
    siteInfo: SiteInfo = {
      "url": url,
      "siteName":dataNoAuth['SiteName'],
      "classification": {"GlobalRank":dataNoAuth['GlobalRank']['Rank'] if dataNoAuth['GlobalRank']['Rank'] != None else 0 ,"CountryRank":dataNoAuth['CountryRank']['Rank'] if dataNoAuth['CountryRank']['Rank'] != None else 0
,"CategoryRank":int(dataNoAuth['CategoryRank']['Rank'] if dataNoAuth['CategoryRank']['Rank'] != None else 0)},
      "category": dataNoAuth['Category'],
      "average_visit_duration": str(float(dataNoAuth['Engagments']['TimeOnSite'])/60),
      "pages_per_visit": dataNoAuth['Engagments']['PagePerVisit'],
      "bounce_rate": str(float(dataNoAuth['Engagments']['BounceRate'])*100)+"%",
      "top_countries": dataNoAuth['TopCountryShares'],
      "gender_distribution": {"Male": str((1 - float(dataAuthDemographic[url].get('FemalesRatio', 0))) * 100) + '%' if dataAuthDemographic.get(url) and 'FemalesRatio' in dataAuthDemographic[url] else '',
    "Female": str(float(dataAuthDemographic[url].get('FemalesRatio', 0)) * 100) + '%' if dataAuthDemographic.get(url) and 'FemalesRatio' in dataAuthDemographic[url] else ''},
      "age_distribution": dataAuthDemographic[url].get('AgeRatios', {}) if dataAuthDemographic.get(url) else '',
      "competitors": dataAuthSimilarSites,
     
    }
    collection_name.insert_one(siteInfo)
    return status.HTTP_201_CREATED
  return status.HTTP_404_NOT_FOUND 