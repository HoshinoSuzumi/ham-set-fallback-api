from skyfield.api import wgs84

def get_sat_observe_detail(sat, observer, t):
  geocentric = sat.at(t)
  lat, lon = wgs84.latlon_of(geocentric)
  
  diff = sat - observer
  topocentric = diff.at(t)
  alt, az, distance = topocentric.altaz()
  return {
    'lat': lat.degrees,
    'lon': lon.degrees,
    'elevation': 0 if round(alt.degrees, 1) in [0.0, -0.0] else round(alt.degrees, 1),
    'azimuth': 0 if round(az.degrees, 1) in [0.0, -0.0] else round(az.degrees, 1),
    'distance': round(distance.km, 1)
  }