from pydantic import BaseModel

class SiteInfo(BaseModel):
    url: str
    siteName: str
    classification: dict
    category: str
    average_visit_duration: str
    pages_per_visit: float
    bounce_rate: str
    top_countries: list
    gender_distribution: dict
    age_distribution: dict
    competitors: list
    keywords: list

    
    