# Sistema de Gestión de Usuarios

## Descripción

Aplicación modular desarrollada en Python para gestionar usuarios desde consola. Permite registrar, listar y buscar usuarios, aplicando validaciones y manejo de errores.

## Tecnologías utilizadas

* Python
* venv
* pip
* python-dotenv
* Git y GitHub
* Visual Studio Code

## Estructura

```text
sistema_usuarios/
├── app/
│   ├── usuarios/
│   │   ├── gestor.py
│   │   └── validaciones.py
│   └── config/
│       └── settings.py
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Entorno virtual

Crear:

```bash
python -m venv venv
```

Activar en Windows:

```bash
venv\Scripts\activate
```

## Dependencias

Instalar:

```bash
pip install python-dotenv
```

Generar:

```bash
pip freeze > requirements.txt
```

## Variables de entorno

Archivo `.env`:

```env
APP_NAME=Sistema Usuarios
APP_VERSION=1.0
ADMIN_USER=admin
```

Estas variables son cargadas desde `settings.py` utilizando `python-dotenv`.

## Modularización

* **gestor.py:** registra, lista y busca usuarios.
* **validaciones.py:** valida nombres y edades.
* **settings.py:** carga las variables de entorno.
* **main.py:** contiene el menú principal y ejecuta el sistema.

## Ejecución

```bash
python main.py
```

## Funcionalidades

El sistema permite registrar usuarios, listar usuarios, buscar por nombre, validar datos y manejar errores mediante excepciones.

## Ventajas

La modularización permite tener un código organizado y fácil de mantener. El entorno virtual aísla las dependencias del proyecto y las variables de entorno permiten separar la configuración del código.

## Evidencias

Se incluyen capturas de:

* Creación y activación del entorno virtual.
* Instalación de dependencias.
* Ejecución del sistema.
* Uso de variables de entorno.
* Registro, listado y búsqueda de usuarios.

## Reflexión

Este proyecto permitió comprender la importancia de modularizar el código, aislar las dependencias con entornos virtuales y utilizar variables de entorno para manejar las configuraciones de manera más segura.
