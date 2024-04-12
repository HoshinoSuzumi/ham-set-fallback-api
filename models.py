from ctypes import Union
from datetime import datetime
from pydantic import BaseModel, InstanceOf
from typing import Optional

class Observer(BaseModel):
  lat: float = 0.0
  lon: float = 0.0
  alt: float = 0.0

class SightingsRequest(BaseModel):
  tle0: str
  tle1: str
  tle2: str
  hours: int = 12
  elevation_threshold: int = 0
  observer: Observer = Observer()
  
class SightingDetail(BaseModel):
  time: Optional[datetime] = None
  lat: float = 0
  lon: float = 0
  elevation: float = 0
  azimuth: float = 0
  distance: float = 0

class Sighting(BaseModel):
  rise: SightingDetail = SightingDetail()
  culminate: SightingDetail = SightingDetail()
  set: SightingDetail = SightingDetail()
