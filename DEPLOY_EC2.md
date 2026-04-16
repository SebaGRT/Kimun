# Despliegue de Kimun en una sola EC2 con Docker

Esta configuracion esta pensada para correr `Kimun` sin depender de RDS, S3 ni Nginx. La app usa:

- `SQLite` persistida en un volumen Docker
- `media/` persistido en un volumen Docker
- `gunicorn` como servidor de aplicacion
- `WhiteNoise` para servir archivos estaticos
- Django sirviendo `media/` directamente

## 1. Preparar la EC2

Instala Docker y Docker Compose Plugin en Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Cierra sesion y vuelve a entrar para aplicar el grupo `docker`.

## 2. Subir el proyecto

Clona o copia este repositorio a la instancia y entra a la carpeta `Kimun`.

## 3. Configurar variables

Copia el archivo de ejemplo:

```bash
cp .env.docker.example .env.docker
```

Edita estos valores:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

Si vas a entrar por IP publica, usa algo como:

```env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,12.34.56.78
DJANGO_CSRF_TRUSTED_ORIGINS=http://12.34.56.78:8000
```

## 4. Construir y levantar

```bash
docker compose up -d --build
```

La primera vez se ejecutaran automaticamente:

- `python manage.py migrate`
- `python manage.py collectstatic`

## 5. Crear superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

## 6. Abrir el puerto en AWS

En el Security Group de la EC2, abre:

- `TCP 8000` desde tu IP o desde internet si es una demo publica

## 7. Ver logs

```bash
docker compose logs -f web
```

## 8. Actualizar la app

```bash
docker compose down
docker compose up -d --build
```

## Notas importantes

- Esta version sirve para demo, pruebas internas o una primera puesta en marcha.
- `SQLite` funciona bien para poco trafico, pero no es ideal para alta concurrencia.
- Los archivos `media/` y la base de datos viven en volumenes Docker de la EC2. Si destruyes la instancia sin respaldarlos, se pierden.
- Si luego quieren pasar a produccion mas robusta, el siguiente paso natural es `RDS + S3 + ALB`.
