# Kimun

Plataforma de capacitacion interna para la ONG ALUMCO, orientada a cursos, evaluaciones, certificados y seguimiento de avance para colaboradores.

Este repositorio queda preparado para dos escenarios:

- desarrollo local con SQLite
- despliegue simple en una sola instancia EC2 usando Docker

## Contenido

- [Resumen](#resumen)
- [Stack](#stack)
- [Modulos principales](#modulos-principales)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Ejecucion local sin Docker](#ejecucion-local-sin-docker)
- [Ejecucion con Docker](#ejecucion-con-docker)
- [Despliegue en una sola EC2](#despliegue-en-una-sola-ec2)
- [Variables de entorno](#variables-de-entorno)
- [Persistencia de datos](#persistencia-de-datos)
- [Comandos utiles](#comandos-utiles)
- [Solucion de problemas](#solucion-de-problemas)
- [Limitaciones actuales](#limitaciones-actuales)

## Resumen

Kimun incluye:

- gestion de usuarios con roles `admin`, `docente` y `colaborador`
- gestion de cursos, clases, materiales y categorias
- evaluaciones con correccion automatica
- certificados PDF con verificacion
- reportes y paneles de progreso
- calendario y anuncios

## Stack

- `Python 3.12` en la imagen Docker
- `Django 6.0.3`
- `SQLite` para desarrollo y despliegue simple
- `Gunicorn` como servidor de aplicacion
- `WhiteNoise` para servir archivos estaticos
- `WeasyPrint` para generacion de PDFs
- `django-ckeditor` para contenido enriquecido

## Modulos principales

- `usuarios`: autenticacion, perfiles, roles y recordatorios
- `cursos`: cursos, clases, materiales, categorias e inscripciones
- `evaluaciones`: pruebas, preguntas, alternativas e intentos
- `certificados`: emision, aprobacion, descarga y verificacion
- `reportes`: paneles y vistas de avance
- `calendario`: eventos y fechas relevantes
- `anuncios`: comunicados internos
- `tareas`: entregas y seguimiento

## Estructura del proyecto

```text
Kimun/
├── anuncios/
├── calendario/
├── certificados/
├── cursos/
├── evaluaciones/
├── kimun/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── reportes/
├── static/
├── tareas/
├── templates/
├── usuarios/
├── .env.docker
├── .env.docker.example
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── README.md
```

## Requisitos

### Para desarrollo local

- Python 3.10 o superior
- `pip`
- entorno virtual recomendado

### Para Docker

- Docker
- Docker Compose Plugin

### Para desplegar en EC2

- una instancia Ubuntu en AWS
- acceso SSH a la instancia
- Security Group con el puerto `8000` abierto segun tu caso

## Ejecucion local sin Docker

### 1. Entrar al proyecto

```bash
cd Kimun
```

### 2. Crear y activar entorno virtual

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

### 7. Acceder

- aplicacion: `http://127.0.0.1:8000`
- admin Django: `http://127.0.0.1:8000/admin`

## Ejecucion con Docker

La version Docker actual esta pensada para una instalacion simple:

- `SQLite` se guarda en un volumen Docker
- `media/` se guarda en otro volumen Docker
- los estaticos se recolectan automaticamente con `collectstatic`
- `gunicorn` atiende la aplicacion en el puerto `8000`

### 1. Revisar variables de entorno

El archivo base es `.env.docker`. Si quieres partir desde el ejemplo:

```bash
cp .env.docker.example .env.docker
```

Valores importantes:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

### 2. Construir y levantar

```bash
docker compose up -d --build
```

### 3. Crear superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

### 4. Ver logs

```bash
docker compose logs -f web
```

### 5. Bajar contenedores

```bash
docker compose down
```

## Despliegue en una sola EC2

Esta es la opcion mas simple para dejar el proyecto funcionando en AWS sin sumar mas servicios.

Arquitectura de esta modalidad:

- 1 instancia EC2
- 1 contenedor Docker para Django
- 1 volumen Docker para la base `SQLite`
- 1 volumen Docker para `media/`

No usa:

- RDS
- S3
- Nginx
- balanceador

### 1. Crear la instancia

Recomendacion base:

- Ubuntu Server 22.04 o 24.04
- tipo `t3.small` o `t3.micro` para demo ligera
- al menos 20 GB de almacenamiento

### 2. Configurar Security Group

Abre como minimo:

- `22/TCP` para SSH
- `8000/TCP` para acceder a la app

Si es solo para pruebas, idealmente limita el acceso de `8000` a tu propia IP.

### 3. Conectarte por SSH

Ejemplo:

```bash
ssh -i tu-llave.pem ubuntu@TU_IP_PUBLICA
```

### 4. Instalar Docker y Compose Plugin

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Cierra sesion y vuelve a entrar para que el grupo `docker` quede aplicado.

### 5. Subir o clonar el proyecto

Si usas `git`:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Kimun
```

Si prefieres copiarlo manualmente, sube la carpeta y entra a ella.

### 6. Configurar `.env.docker`

Puedes usar el archivo ya incluido o regenerarlo desde el ejemplo:

```bash
cp .env.docker.example .env.docker
```

Edita al menos estas variables:

```env
DJANGO_SECRET_KEY=una-clave-larga-y-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,TU_IP_PUBLICA
DJANGO_CSRF_TRUSTED_ORIGINS=http://TU_IP_PUBLICA:8000
SQLITE_PATH=/app/data/db.sqlite3
DJANGO_MEDIA_ROOT=/app/media
```

Si vas a usar dominio mas adelante:

```env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,TU_IP_PUBLICA,tudominio.com
DJANGO_CSRF_TRUSTED_ORIGINS=http://TU_IP_PUBLICA:8000,https://tudominio.com
```

### 7. Construir y levantar la aplicacion

```bash
docker compose up -d --build
```

En el primer arranque, el `entrypoint.sh` ejecuta automaticamente:

- `python manage.py migrate --noinput`
- `python manage.py collectstatic --noinput`

### 8. Crear el superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

### 9. Verificar que responde

```bash
docker compose logs -f web
```

Luego abre en el navegador:

```text
http://TU_IP_PUBLICA:8000
```

### 10. Actualizar el proyecto

Cada vez que cambies codigo:

```bash
docker compose down
docker compose up -d --build
```

Si actualizaste solo variables o quieres revisar el estado:

```bash
docker compose ps
docker compose logs -f web
```

## Variables de entorno

El proyecto usa estas variables relevantes para Docker y EC2:

| Variable | Uso | Ejemplo |
|---|---|---|
| `DJANGO_SECRET_KEY` | clave secreta de Django | `una-clave-larga-y-segura` |
| `DJANGO_DEBUG` | activa o desactiva debug | `False` |
| `DJANGO_ALLOWED_HOSTS` | hosts permitidos por Django | `localhost,127.0.0.1,12.34.56.78` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | origenes confiables para CSRF | `http://12.34.56.78:8000` |
| `SQLITE_PATH` | ruta interna del archivo SQLite | `/app/data/db.sqlite3` |
| `DJANGO_MEDIA_ROOT` | carpeta interna para media | `/app/media` |

## Persistencia de datos

En `docker-compose.yml` se definen dos volumenes:

- `kimun_data`: guarda la base SQLite
- `kimun_media`: guarda archivos subidos y PDFs

Eso significa:

- si reinicias el contenedor, los datos se conservan
- si haces `docker compose down`, los volumenes se mantienen
- si eliminas los volumenes manualmente, perderas la base y los archivos
- si destruyes la EC2 sin backup, perderas todo

## Comandos utiles

Levantar:

```bash
docker compose up -d --build
```

Ver contenedores:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f web
```

Entrar al contenedor:

```bash
docker compose exec web sh
```

Crear superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Ejecutar migraciones manualmente:

```bash
docker compose exec web python manage.py migrate
```

Recolectar estaticos manualmente:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

Apagar:

```bash
docker compose down
```

## Solucion de problemas

### La app no carga en la EC2

Revisa:

- que el contenedor este arriba con `docker compose ps`
- que el puerto `8000` este abierto en el Security Group
- que `DJANGO_ALLOWED_HOSTS` incluya la IP publica o dominio correctos

### Error `DisallowedHost`

Agrega la IP o dominio real a:

- `DJANGO_ALLOWED_HOSTS`

Despues reconstruye:

```bash
docker compose up -d --build
```

### Error de CSRF al iniciar sesion o enviar formularios

Agrega el origen real a:

- `DJANGO_CSRF_TRUSTED_ORIGINS`

Ejemplo:

```env
DJANGO_CSRF_TRUSTED_ORIGINS=http://12.34.56.78:8000
```

### Error al generar PDFs

La imagen Docker ya instala librerias del sistema necesarias para `WeasyPrint`. Si aun falla, revisa logs:

```bash
docker compose logs -f web
```

### Quiero reiniciar desde cero

Si realmente quieres borrar base y archivos persistidos:

```bash
docker compose down -v
```

Esto elimina volumenes y datos. Usalo con cuidado.

### Los cambios de codigo no aparecen

Reconstruye la imagen:

```bash
docker compose up -d --build
```

## Limitaciones actuales

Esta modalidad de despliegue es simple, pero tiene tradeoffs:

- `SQLite` no es ideal para alta concurrencia
- los archivos viven solo en esa instancia
- no hay balanceo ni alta disponibilidad
- no hay separacion entre app y base de datos

Para una siguiente etapa mas robusta, la evolucion natural seria:

- `RDS PostgreSQL`
- `S3` para media
- `ALB` o `Nginx`
- `ECS/Fargate` o una EC2 mas estructurada

## Notas finales

Archivos importantes de despliegue:

- [Dockerfile](D:/Universidad/Ing.%20software/Kimun/Dockerfile)
- [docker-compose.yml](D:/Universidad/Ing.%20software/Kimun/docker-compose.yml)
- [.env.docker.example](D:/Universidad/Ing.%20software/Kimun/.env.docker.example)
- [entrypoint.sh](D:/Universidad/Ing.%20software/Kimun/entrypoint.sh)
- [kimun/settings.py](D:/Universidad/Ing.%20software/Kimun/kimun/settings.py)
- [DEPLOY_EC2.md](D:/Universidad/Ing.%20software/Kimun/DEPLOY_EC2.md)

Si vas a usar este proyecto para una entrega o demo, esta configuracion ya te deja una ruta razonable y concreta para ponerlo en linea sin agregar infraestructura extra.
