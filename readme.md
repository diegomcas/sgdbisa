# Instrucciones para preparar el entorno de ejecución del sistema.
## Requerimientos
Su sistema debe tener instalado:
- Python > 3.8 https://www.python.org/downloads/
- PostgreSQL > 12.0 https://www.postgresql.org/download/
- git https://git-scm.com/downloads

### Una vez tenga instalado Python en sus sistema es recomendable actualizar la utilidad Pip:
$ python -m pip install --upgrade pip

### Una vez instalado GIT en sus sistema, clonar el repositorio remoto:
- Cambiar el directorio de trabajo actual a la ubicación en donde quieres clonar el directorio remoto.
-Ejecutar el siguiente comando
$ git clone https://github.com/diegomcas/sgdbisa.git

### Con el repositorio remoto clonado en su repositorio local, dentro del directorio de trabajo ejecutar el comando:
$ pip install -r requirements.txt

Con lo que usted instala el Framework Django y otras bibliotecas requeridas por el sistema.

# Instalación de PostGIS en PostgreSQL
- Instale la versión para sus sistema operativo que puede obtenerla desde https://postgis.net/install/

## Creando la base de datos, agregando el usuario y activando las extensión PostGIS en la misma.
- Una vez instalado PostgreSQL en sus sistema ejecute el comando psql:
$ psql -U 'Usuario postgresql'
 Se le solicitará la contraseña para dicho usuario.
 
- Cree la base de datos con el siguiente comando:
postgres=# CREATE DATABASE sgdbisa
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            LC_COLLATE = 'Spanish_Argentina.1252'
            LC_CTYPE = 'Spanish_Argentina.1252'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;

COMMENT ON DATABASE sgdbisa
    IS 'Sistema de Gestión de Documentos BISA';

-Una vez dentro de psql ingrese:
postgres=# CREATE USER sgdbisauser WITH PASSWORD 'THPrNr13ToP';
postgres=# GRANT ALL PRIVILEGES ON DATABASE sgdbisa to sgdbisauser;

# Conectando Django con PostgreSQL
- Desde el directorio de trabajo donde se clonó el repositorio (identificable puesto que se encuentra el archivo manage.py), ejecute el siguiente comando:
$ python manage.py makemigrations
$ python manage.py migrate

# Ejecutando el servidor de pruebas de Django:
- Desde el directorio de trabajo ejecute el siguiente comando:
$ python manage.py runserver

- Ahora puede abrir su navegador e ingresar la url:
http://127.0.0.1:8000/

Se mostrará la versión web del sitio.

# Para utilizar la aplicación en autocad siga los siguientes pasos:
- Abra autocad
- Ingrese en el menú herramientas / opciones (tools / options) y en la pestaña archivos (files) agregue la ruta donde se encuentra el proyecto descargado.
- Ingrese al menú herramientas / AutoLISP / Cargar Aplicación y seleccione el archivo .lsp, presione cargar

