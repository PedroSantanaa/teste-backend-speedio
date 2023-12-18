from email.mime import base
import re
from fastapi import APIRouter,HTTPException
from models.siteInfo_model import SiteInfo
from config.database import collection_name
from schemas.schemas import serializerList
import requests
from fastapi import status

router=APIRouter()

#GET ROUTE /get_info já que o metodo GET é o mais apropriado para pegar dados do banco de dados
@router.get("/get_info/{url}")
async def get_info(url: str):
  site= collection_name.find_one({"url":url})
  if site == None:
    raise HTTPException(status_code=404, detail="Site not found")
  return serializerList(collection_name.find_one({"url":url}))
  
#POST ROUTE /get_info já que o teste pede para que utilize o metodo POST para pegar dados do banco de dados
@router.post("/get_info")
async def get_info(url: str):
  return serializerList(collection_name.find_one({"url":url}))

#POST ROUTE /salve_info or /save_info já que o teste pede para que utilize o metodo POST para salvar dados no banco de dados
@router.post("/save_info")
async def save_info(url:str):
  noAuth_url=f'https://data.similarweb.com/api/v1/data?domain={url}'
  headers = {
    "authority":"data.similarweb.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.7",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.similarweb.com/pt/",
    "Cookie": "sgID=abe5a1cf-bef8-4921-8bfa-47a97bacdcd9; _abck=A582A26C0564C37D005C7EF867ADA5D7~0~YAAQkgopF7FZhlmMAQAAIsq/fAsyItlnOI/7QdaDtKjn2iggpPjFYKa3liUCkCLDBdrOZSFt2b8hgKG1HFqHpSF8x8i+sYsSC+q6jZL2tz+mqNFIiULSvLes/4BSGxgzQhD9MK7Teg7BTpMNDhc3zAIwOub3S5AEyEL6pzjR/h3sNeP9Gol1gLj7YbcV7u7IjInh5Ih8cALhkFNlxxUan9xvMtKLcrRk/OHPXP0wy96hhC7CNfX92GNFJEdtYhdKcTBOLg5B7q63xyCKM3veTx+TES0/u9+dbeEMCq+m2iPrf+jRY7o1bnrmaFDaJSvWuDBlnZZGxH/kKgcNt4Q3MZWzCvfxWZ6a3Zj65ghTSfDZ647W/dQ+k/Sn7iZoN9nuwxnUpyQXcWBnaR5k8Hrq/8+Ou7MI+r55skZzrjc=~-1~-1~-1; bm_sz=9CA73B7E2D28A3A8A4D12150D4432B80~YAAQkgopF7JZhlmMAQAAIsq/fBYObeNwPzvakwXzzXfjb4Lmv/ruU8WP7/DKSFoEmvyWASuhZsgR5830YDo1nmjpX6Mt6YxNP5Q3EONJDqG80sY+tUe2GGBmYXuXi/oZPf53OXjs4CBOA3+joGRMvGtW3lw70d8mz4pQGyCJ/BzEJPmrxoF4hEstrEx+BUO7EwGsnmeMyx9HP4p0iPA4Wu+r0+8r4koqGHSMywrTksqMw+SEXqgxsdGXSuUaqSrQRCGa7dk04puEs2VIp4AekrV+jZVWvyvU/z6qkl6YuWS3lz9x0kLY~3749441~3749958; ak_bmsc=ECEB86F9B8E379F14EA60A6B4EC7B82B~000000000000000000000000000000~YAAQx81YaPP3W0eMAQAAmSLWfBbdW1xVKayAt2NxBGtIaXbbj3SBArK7n/lNp3UBW3n1lQzw5ShP/7W/cGv8Zt9rrxQvMZIKqs6ZBZ8wzGnsz24AYWqgnMkyidH/OE6FVKfQZBkIilJvGJKj6NFg0N7rUTUNEcRrMvh/Nl0JbLofI/bC3yMBD4VH6779edmvOGndXVTCoXcmsa0MkbG3kSvod1Syzs3FA0Loozc+0EdR6DOuqXNCHNP1LdaRsWxVRV6O48FG8CABCohDIdmrmwBSFnKWx+j3ccQN6FYiohnLyfaDZ4cl34F1m6UXnnwK2xzcR4+M7YM9vs+s8jGyvUhq0X8dFUX4pRhE4SYXn9H7b+yKZpQiLM2ywHWJzBLv68q2+jfm8NYZMKN8+mYL; bm_sv=2C7868208EA2A59355D9D9F57CB46B46~YAAQx81YaJ39W0eMAQAAX1fWfBar7FlFJFDJltiTCkYtspDFQ4zF9ISj47NcuuFbrlUJUE9FO9+a0R8th6rhPbE5dl1p+48AglH9UWEt5qYdn30uvA1wwNYx4U3JocigNVSqFjK32mMjg5CbKtulCLVaxEz9m0nv3mx6Tl+RjlN+sh8LR2oSAi6d9gBTn6S+6KP4v6bzaKjX3P+aQivp2XGWz26OO9HmLXWqcXtvKUBVEfgYNdGx6PLjB/nrIWDGRDUCBw==~1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }
  response= requests.get(noAuth_url,headers=headers)
  if response.status_code == 200:
    
  # collection_name.insert_one(dict(siteInfo))
  # return serializerList(collection_name.find_one({"url":siteInfo.url}))