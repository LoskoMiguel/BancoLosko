# BancoLosko (Proyecto de Prueba)

API REST para servicios bancarios desarrollada con FastAPI. Este es un proyecto de prueba con fines educativos y de demostración, no está destinado para uso en producción.

## Descripción

BancoLosko es una API REST que simula servicios bancarios básicos, implementada utilizando FastAPI y SQLAlchemy para la gestión de base de datos. Este proyecto fue creado como un ejercicio de aprendizaje y demostración de habilidades en el desarrollo de APIs con Python.

> **Nota**: Este es un proyecto de prueba y no debe utilizarse en un entorno de producción real. No implementa todas las medidas de seguridad necesarias para un sistema bancario real.

## Características

- Autenticación de usuarios
- Gestión de cuentas bancarias
- API RESTful con documentación automática
- Middleware CORS habilitado para integración con frontends

## Tecnologías Utilizadas

- FastAPI
- SQLAlchemy
- Python-Jose (JWT)
- BCrypt
- Uvicorn

## Requisitos

- Python 3.7+
- Entorno virtual (venv)
- Dependencias listadas en `requeriments.txt`

## Instalación

1. Clonar el repositorio
2. Crear y activar el entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate
```
3. Instalar dependencias:
```bash
pip install -r requeriments.txt
```

## Uso

Para iniciar el servidor en modo desarrollo:

```bash
uvicorn main:app --reload
```

El servidor se iniciará en `http://localhost:8000`

## Estructura del Proyecto

```
BancoLosko/
├── app/
│   ├── core/           # Configuraciones centrales
│   ├── database/       # Configuración de la base de datos
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routers/        # Rutas de la API
├── main.py            # Punto de entrada de la aplicación
├── requeriments.txt   # Dependencias del proyecto
└── README.md          # Documentación del proyecto
```

## Documentación API

Una vez que el servidor esté corriendo, puedes acceder a:
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`
