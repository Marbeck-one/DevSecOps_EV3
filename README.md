````markdown

# 🛡️ Guía de Despliegue y Ejecución - DevSecOps Evaluación 3



Esta guía detalla paso a paso cómo desplegar el entorno, configurar las herramientas y ejecutar el pipeline de seguridad, incluyendo las correcciones técnicas aplicadas durante la implementación.



## 👥 Integrantes

* **Rodrigo Martínez (Marbeck)**

* **Vincent Farenden**

* **Massimo Navarrete**



---



## 🚀 Fase 1: Levantamiento de Infraestructura



Sigue estos pasos en una terminal de **Kali Linux**.



### 1. Clonar el Repositorio

```bash

git clone [https://github.com/Marbeck-one/DevSecOps_EV3.git](https://github.com/Marbeck-one/DevSecOps_EV3.git)

cd DevSecOps_EV3

````



### 2\. Preparar el Entorno Docker



Es crítico dar permisos al socket de Docker para que Jenkins pueda lanzar contenedores hermanos (Siblings).



```bash

# Dar permisos al socket (Necesario en Kali)

sudo chmod 666 /var/run/docker.sock



# Levantar todos los servicios (Jenkins, App, Prometheus, Grafana)

docker-compose up -d --build

```



-----



## ⚙️ Fase 2: Configuración de Jenkins (El Cerebro)



### 1\. Desbloquear Jenkins



1.  Accede en tu navegador a: `http://localhost:8080`.

2.  Para obtener la contraseña inicial, ejecuta en tu terminal:

    ```bash

    docker exec parcial3-jenkins-1 cat /var/jenkins_home/secrets/initialAdminPassword

    ```

3.  Pega la clave y selecciona **"Install suggested plugins"**.

4.  Crea tu usuario administrador (ej: `admin` / `admin`).



### 2\. 🔧 CRÍTICO: Preparar el Contenedor de Jenkins



Por defecto, el contenedor de Jenkins no trae Python ni Docker instalados. Para que el pipeline funcione, aplicamos este **Fix Técnico**:



Ejecuta estos comandos en tu terminal de Kali:



```bash

# 1. Instalar Python3, Pip y Cliente Docker dentro de Jenkins

docker exec -u 0 -it parcial3-jenkins-1 apt-get update

docker exec -u 0 -it parcial3-jenkins-1 apt-get install -y python3 python3-pip docker.io



# 2. Reforzar permisos del socket

docker exec -u 0 -it parcial3-jenkins-1 chmod 666 /var/run/docker.sock

```



### 3\. Crear el Pipeline



1.  En Jenkins, ve a **Nueva Tarea** -\> Escribe "Pipeline\_DevSecOps" -\> Selecciona **Pipeline** -\> OK.

2.  Baja a la sección **Pipeline**.

3.  En **Definition**, elige **Pipeline script from SCM**.

4.  En **SCM**, elige **Git**.

5.  **Repository URL:** `https://github.com/Marbeck-one/DevSecOps_EV3.git`

    *(Si da error de credenciales, puedes usar la opción "Pipeline script" y pegar el contenido del archivo `Jenkinsfile` manualmente).*

6.  Asegúrate que la rama sea `*/main`.

7.  Click en **Guardar**.



-----



## 📊 Fase 3: Configuración de Monitorización (Grafana)



1.  Accede a `http://localhost:3000` (Credenciales: `admin` / `admin`).

2.  Ve a **Connections** -\> **Data Sources** -\> **Add data source**.

3.  Selecciona **Prometheus**.

      * **Connection URL:** `http://prometheus:9090`

      * Click en **Save & Test**.

4.  Ve a **Dashboards** -\> **Create** -\> **Import**.

      * Ingresa el ID **9688** (Dashboard oficial de Flask Prometheus).

      * Selecciona el Data Source que creaste.

      * Click en **Import**.



-----



## ▶️ Fase 4: Ejecución del Pipeline (CI/CD)



1.  Ve a tu tarea en Jenkins.

2.  Haz click en **Construir ahora (Build Now)**.

3.  El sistema ejecutará automáticamente:

      * **Setup:** Instalación de dependencias (`flask`, `safety`, `bandit`).

      * **SAST:** Análisis de código con **Bandit**.

      * **SCA:** Revisión de librerías con **Safety**.

      * **Build:** Creación de la imagen Docker de la App.

      * **DAST:** Ataque automatizado con **OWASP ZAP** (Imagen `zaproxy/zap-stable`).

      * **Doc:** Generación de documentación con `pydoc`.



### 📂 Evidencias Generadas



Al finalizar, podrás descargar desde el "Workspace" de Jenkins:



  * `zap_report.html` (Reporte de vulnerabilidades dinámicas).

  * `bandit_report.json` (Reporte de código estático).

  * `safety_report.txt` (Reporte de dependencias).



-----



## 🛠️ Resumen de Cambios y Fixes (Trazabilidad)



Para lograr el despliegue exitoso se realizaron las siguientes modificaciones al plan original:



  * **Infraestructura:** Se corrigió el montaje de `prometheus.yml` en el `docker-compose.yml`.

  * **Jenkins:** Se inyectaron herramientas (Python/Docker) manualmente en el contenedor.

  * **Pipeline:**

      * Se actualizó la imagen de ZAP a `zaproxy/zap-stable` por deprecación de la antigua.

      * Se añadió el flag `--user 0` en Docker para evitar errores de permisos de escritura.

      * Se cambió la llamada de `pydoc` a `python3 -m pydoc`.

  * **GitHub:** Se implementó autenticación vía Token (Classic) para la gestión del repositorio.



<!-- end list -->



````