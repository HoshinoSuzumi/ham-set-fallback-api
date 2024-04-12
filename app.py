from skyfield.api import EarthSatellite, wgs84, load, utc
from datetime import datetime, timedelta, UTC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import *
from utils import *
import uvicorn
import pytz

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:3000",
    "https://ham.c5r.app",
    "https://ham-dev.c5r.app",
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

ts = load.timescale()
bjtz = pytz.timezone('Asia/Shanghai')

@app.post('/sat/sightings', response_model=list[Sighting])
async def sat_sightings(param: SightingsRequest):
  satellite = EarthSatellite(param.tle1, param.tle2, param.tle0, ts)
  observer = wgs84.latlon(param.observer.lat, param.observer.lon, param.observer.alt)
  
  
  utc_now = datetime.now(UTC).replace(tzinfo=utc)
  t0 = ts.utc(utc_now)
  t1 = t0 + timedelta(hours=param.hours)
  passes = satellite.find_events(observer, t0, t1)
  
  sightings: list[Sighting] = []
  
  index = -1
  for time, event, i in zip(passes[0], passes[1], range(len(passes[0]))):
    if index == -1 and event != 0:
      continue
    if event == 0:
      if index == -1:
        index = 0
      rise_time = time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(bjtz)
      sightings.append(Sighting(rise=SightingDetail(time=rise_time, **get_sat_observe_detail(satellite, observer, time))))
    elif event == 1:
      culminate_time = time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(bjtz)
      sightings[index].culminate = SightingDetail(time=culminate_time, **get_sat_observe_detail(satellite, observer, time))
    elif event == 2:
      set_time = time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(bjtz)
      sightings[index].set = SightingDetail(time=set_time, **get_sat_observe_detail(satellite, observer, time))
      index += 1
  
  filtered_sightings = [sighting for sighting in sightings if sighting.culminate.elevation >= param.elevation_threshold]
  
  return filtered_sightings
  

if __name__ == '__main__':
  uvicorn.run(app, port=5000, log_level="info")