from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "e7520055e0b2baf1bc8b3f4cbc94b12b" # Substitua pela sua chave da API de clima
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=pt&units=metric"

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "weather": None})

@app.post("/")
async def get_weather(request: Request, city: str = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL.format(city=city, api_key=API_KEY))
    
    if response.status_code == 200:
        weather_data = response.json()
        return templates.TemplateResponse("index.html", {"request": request, "weather": weather_data})
    
    return templates.TemplateResponse("index.html", {"request": request, "weather": None, "error": "Cidade não encontrada!"})