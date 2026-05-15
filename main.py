import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# 1. Cargar variables del archivo .env
load_dotenv()

# 2. Crear la aplicación FastAPI
app = FastAPI(title="Weather API - Parcial")

# 3. Leer la API KEY del archivo .env
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 4. URLs base de OpenWeather
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"



#  ENDPOINT 0 - Inicio

@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}



#  ENDPOINT 1 - Clima Básico

@app.get("/weather/{city}")
async def weather(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Falta API KEY en .env")

    async with httpx.AsyncClient() as client:

        # GEO: Buscar lat/lon
        geo_response = await client.get(
            GEOCODING_URL,
            params={"q": city, "limit": 1, "appid": API_KEY}
        )

        if geo_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando geocoding")

        geo_data = geo_response.json()

        if not geo_data:
            raise HTTPException(status_code=404, detail="Ciudad no encontrada")

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # CLIMA ACTUAL
        weather_response = await client.get(
            WEATHER_URL,
            params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "es"}
        )

        if weather_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando clima")

        weather_data = weather_response.json()

        return {
            "ciudad": city,
            "temperatura": weather_data["main"]["temp"],
            "humedad": weather_data["main"]["humidity"],
            "descripcion": weather_data["weather"][0]["description"]
        }



#  ENDPOINT 2 - Detalles del Clima

@app.get("/weather/details/{city}")
async def weather_details(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Falta API KEY en .env")

    async with httpx.AsyncClient() as client:
        geo_response = await client.get(
            GEOCODING_URL,
            params={"q": city, "limit": 1, "appid": API_KEY}
        )

        if geo_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando geocoding")

        geo_data = geo_response.json()
        if not geo_data:
            raise HTTPException(status_code=404, detail="Ciudad no encontrada")

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_response = await client.get(
            WEATHER_URL,
            params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "es"}
        )

        if weather_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando clima")

        weather_data = weather_response.json()

        return {
            "ciudad": city,
            "sensacion_termica": weather_data["main"]["feels_like"],
            "viento_kmh": round(weather_data["wind"]["speed"] * 3.6, 2),
            "presion_hpa": weather_data["main"]["pressure"]
        }



#  ENDPOINT 3 - Temp mínima y máxima

@app.get("/weather/minmax/{city}")
async def weather_minmax(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Falta API KEY en .env")

    async with httpx.AsyncClient() as client:
        geo_response = await client.get(
            GEOCODING_URL,
            params={"q": city, "limit": 1, "appid": API_KEY}
        )

        if geo_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando geocoding")

        geo_data = geo_response.json()
        if not geo_data:
            raise HTTPException(status_code=404, detail="Ciudad no encontrada")

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        weather_response = await client.get(
            WEATHER_URL,
            params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "es"}
        )

        if weather_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando clima")

        data = weather_response.json()

        return {
            "ciudad": city,
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"]
        }



#  ENDPOINT 4 - Pronóstico 3 horas

@app.get("/weather/forecast/{city}")
async def weather_forecast(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Falta API KEY en .env")

    async with httpx.AsyncClient() as client:

        # GEO
        geo = await client.get(GEOCODING_URL, params={"q": city, "limit": 1, "appid": API_KEY})
        if geo.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando geocoding")

        geo_data = geo.json()
        if not geo_data:
            raise HTTPException(status_code=404, detail="Ciudad no encontrada")

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # FORECAST
        forecast = await client.get(
            FORECAST_URL,
            params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "es"}
        )

        if forecast.status_code != 200:
            raise HTTPException(status_code=502, detail="Error consultando pronóstico")

        forecast_data = forecast.json()

        proximo = forecast_data["list"][0]

        return {
            "ciudad": city,
            "clima_en_3_horas": proximo["weather"][0]["description"],
            "temperatura_en_3_horas": proximo["main"]["temp"]
        }