import requests
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])



@app.get("/weather")
def weather():
  city = "oran"
  api_key = "b5d5197da4069b1f8225b1911f32c9ca"
  base_url =  "http://api.openweathermap.org/data/2.5/weather?" 
  url = base_url + "appid=" + api_key + "&q=" + str(city)
  response = requests.get(url)
  x = dict(response.json())
  if x["cod"] != "404":
    return JSONResponse(content=jsonable_encoder({"lat":dict(x["coord"])['lat'],"lon":dict(x["coord"])['lon']
    ,"description":dict(x["weather"][0])['description'],"icon":"https://openweathermap.org/img/wn/" + str(dict(x["weather"][0])['icon'] ) + "@2x.png",
    "temp":round(dict(x['main'])['temp']-273),"humidity":dict(x['main'])['humidity'],
    "wind":dict(x["wind"])["speed"] , "pressure" : dict(response.json())["main"]['pressure']}))
@app.get("/covid")
def covid():
  url = "https://api.corona-dz.live/country/latest"
  response = requests.get(url)
  x = dict(response.json())
  return JSONResponse(content=jsonable_encoder({'newConfirmed':x["newConfirmed"],
          'newRecovered': x['newRecovered'],
          'newDeaths':x['newDeaths']}))
@app.get('/forcast')
def forcast():
  url = "https://api.open-meteo.com/v1/forecast?latitude=35.69&longitude=-0.63&hourly=temperature_2m,relativehumidity_2m&windspeed_unit=ms&timezone=Europe%2FLondon"
  response = requests.get(url)
  x = dict(response.json())
  f = x["hourly"]
  f["city"] = "oran"
  return JSONResponse(content=jsonable_encoder(f))
@app.get('/salat')
def salat():
  import requests
  from datetime import date
  today = date.today()
  day = today.strftime("%d/%m/%Y")[:2]
  response = requests.get("http://api.aladhan.com/v1/calendar?latitude=35.6976541&longitude=-0.6337376&method=5&month=1&year=2022")
  for i in list(response.json()["data"]):
      if i["date"]["readable"][:2] == day:
          return JSONResponse(content=jsonable_encoder(i["timings"]))
