
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse  # ✅ Correção aqui!
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "e7520055e0b2baf1bc8b3f4cbc94b12b"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.get("/weather/{city}", response_class=HTMLResponse)
def get_weather(request: Request, city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao obter a previsão do tempo")

    data = response.json()
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "cidade": data["name"],
        "temperatura": data["main"]["temp"],
        "descricao": data["weather"][0]["description"].capitalize(),
        "umidade": data["main"]["humidity"],
        "vento": data["wind"]["speed"]
    })

