from pydantic import BaseModel

class SiteInfo(BaseModel):
    url: str
    classification: str
    category: str
    ranking_change: float
    average_visit_duration: str
    pages_per_visit: float
    bounce_rate: float
    top_countries: list
    gender_distribution: dict
    age_distribution: dict
    competitors: list
    keywords: list

    
    