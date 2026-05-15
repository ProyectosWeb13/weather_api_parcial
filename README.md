Weather API – Parcial
API desarrollada en FastAPI que consume la API pública OpenWeather para obtener información del clima en tiempo real.
Este proyecto cumple con los requisitos del parcial: consumo de API externa, múltiples endpoints, manejo de errores y documentación.

🚀 Tecnologías utilizadas
Python
FastAPI
Uvicorn
HTTPX
python-dotenv
API pública: OpenWeather API

🔑 Configuración de la API Key
El proyecto usa variables de entorno, por eso debes crear un archivo .env
⚠ Este archivo NO va en GitHub (está en .gitignore).

📌 Cómo ejecutar el proyecto

1. Crear entorno virtual
python -m venv venv

2. Activar entorno virtual

Windows PowerShell:
venv\Scripts\activate

3. Instalar dependencias
pip install fastapi uvicorn httpx python-dotenv

4. Ejecutar API
uvicorn main:app --reload

5. Abrir documentación automática Swagger
http://127.0.0.1:8000/docs


Endpoints disponibles
1️⃣ GET /weather/{city}

Retorna información básica del clima.

{
  "ciudad": "bogota",
  "temperatura": 12.11,
  "humedad": 98,
  "descripcion": "algo de nubes"
}


2️⃣ GET /weather/details/{city}

Retorna información extendida del clima.

✔ Respuesta (ejemplo)
{
  "ciudad": "bogota",
  "sensacion_termica": 11.94,
  "viento_kmh": 9.65,
  "presion_hpa": 1019
}


3️⃣ GET /weather/full/{city}

Retorna un paquete completo mezclando datos simples + datos avanzados.

✔ Respuesta (ejemplo)
{
  "ciudad": "bogota",
  "temperatura": 12.11,
  "humedad": 98,
  "descripcion": "algo de nubes",
  "sensacion_termica": 11.94,
  "viento_kmh": 9.65,
  "presion_hpa": 1019
}


🧪 Evidencias

Las evidencias (capturas) están en la carpeta:

/evidencias

Incluyen:

Pruebas en Swagger
Respuestas JSON
Pruebas de los 3 endpoints


🔗 Repositorio del proyecto

https://github.com/ProyectosWeb13/weather_api_parcial

📚 Autor
Guillermo González – Universidad Americana