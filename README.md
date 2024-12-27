# 🏦 BancoLosko (Proyecto de Prueba)

<div align="center">

![Banner](https://img.shields.io/badge/Status-En%20Desarrollo-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Latest-red)

</div>

## 🚀 Descripción

BancoLosko es una innovadora API REST que simula servicios bancarios, diseñada como un sistema moderno y eficiente. Este proyecto forma parte de un ecosistema más amplio, integrándose perfectamente con el sistema de [CajaRegistradora](https://github.com/LoskoMiguel/CajaRegistradora) para proporcionar una solución completa de gestión financiera.

> 💡 **Nota**: Este es un proyecto de prueba desarrollado con fines educativos y de demostración. No está destinado para uso en producción.

## ✨ Características Principales

- 🔐 **Autenticación Segura**
- 💳 **Gestión de Cuentas**
- 🔄 **Integración**

## 🛠️ Tecnologías Utilizadas

- ⚡ FastAPI - Framework moderno y rápido
- 🗃️ SQLAlchemy - ORM potente y flexible
- 🔑 Python-Jose (JWT) - Autenticación segura
- 🔒 BCrypt - Encriptación robusta
- 🚀 Uvicorn - Servidor ASGI de alto rendimiento

## 📋 Requisitos Previos

- Python 3.7+
- Entorno virtual (venv)
- Dependencias listadas en `requeriments.txt`

## 🚀 Guía de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/LoskoMiguel/BancoLosko
cd BancoLosko
```

2. **Crear y activar el entorno virtual**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requeriments.txt
```

## 💻 Uso

**Iniciar el servidor en modo desarrollo:**
```bash
uvicorn main:app --reload
```

🌐 El servidor estará disponible en `http://localhost:8000`

## 📁 Estructura del Proyecto

```
BancoLosko/
├── 📂 app/
│   ├── 📂 core/           # Configuraciones centrales
│   ├── 📂 database/       # Configuración de la base de datos
│   ├── 📂 models/         # Modelos de SQLAlchemy
│   ├── 📂 routers/        # Rutas de la API
├── 📜 main.py            # Punto de entrada de la aplicación
├── 📝 requeriments.txt   # Dependencias del proyecto
└── 📖 README.md          # Documentación del proyecto
```

## 📚 Documentación API

Una vez que el servidor esté corriendo, accede a:
- 📘 **Swagger UI**: `http://localhost:8000/docs`
- 📗 **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Integración con CajaRegistradora

Este proyecto está diseñado para trabajar en conjunto con el sistema de [CajaRegistradora](https://github.com/LoskoMiguel/CajaRegistradora)

## 👥 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, no dudes en:

1. 🍴 Hacer un Fork del proyecto
2. 🔧 Crear una nueva rama
3. 📝 Realizar tus cambios
4. 📫 Enviar un Pull Request
