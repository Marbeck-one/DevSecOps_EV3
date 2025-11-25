================================================================================
BITÁCORA DE IMPLEMENTACIÓN DEVSECOPS - EVALUACIÓN 3
================================================================================
Fecha: 25 Noviembre 2025
Entorno: Kali Linux
Tecnologías: Docker, Jenkins, Flask, Bandit, Safety, OWASP ZAP, Grafana.

1. PREPARACIÓN DEL CÓDIGO (SEGURIDAD - IL 3.1)
--------------------------------------------------------------------------------
- Se analizó 'vulnerable_flask_app.py'.
- VULNERABILIDADES DETECTADAS:
  * SQL Injection en login (concatenación de cadenas).
  * XSS/SSTI en renderizado de templates (uso de render_template_string).
- CORRECCIONES APLICADAS:
  * Creación de 'app/secure_app.py'.
  * Uso de consultas parametrizadas (SQLite '?').
  * Implementación de templates HTML separados para mitigar SSTI.
  * Agregado de 'prometheus-flask-exporter' para monitorización.

2. INFRAESTRUCTURA (DOCKER)
--------------------------------------------------------------------------------
- Creación de Dockerfile para la app Python.
- Creación de docker-compose.yml orquestando: Jenkins, WebApp, Prometheus, Grafana.
- ERROR CRÍTICO 1: Docker montó 'prometheus.yml' como un directorio en lugar de un archivo.
  * Causa: El archivo local tenía un error de tipeo ('prometeus.yml').
  * Solución: Se eliminó el directorio erróneo, se renombró el archivo correctamente y se reconstruyó el contenedor.

3. CONFIGURACIÓN CI/CD (JENKINS)
--------------------------------------------------------------------------------
- Despliegue en puerto 8080.
- Obtención de contraseña inicial mediante 'docker exec'.
- Instalación de plugins sugeridos + Docker Pipeline.
- PREPARACIÓN DEL ENTORNO JENKINS:
  * El contenedor oficial de Jenkins no trae Python ni Docker instalados.
  * Solución: Se ejecutaron comandos 'apt-get install python3-pip docker.io' dentro del contenedor.
  * Se otorgaron permisos al socket de Docker (chmod 666 /var/run/docker.sock).

4. EVOLUCIÓN DEL PIPELINE (ERRORES Y SOLUCIONES)
--------------------------------------------------------------------------------
- ERROR 1: "requirements.txt not found".
  * Causa: Jenkins no tenía los archivos porque no se usó un repo remoto inicialmente.
  * Solución: Se utilizó 'docker cp' para mover la carpeta 'app' local al workspace de Jenkins manualmente.

- ERROR 2: "pydoc not found".
  * Solución: Se cambió la llamada a 'python3 -m pydoc'.

- ERROR 3: OWASP ZAP "repository does not exist".
  * Causa: La imagen 'owasp/zap2docker-stable' fue renombrada/deprecada.
  * Solución: Se actualizó el script para usar 'zaproxy/zap-stable'.

- ERROR 4: Fallos de permisos al escribir reportes ZAP.
  * Solución: Se agregó el flag '--user 0' (root) en el comando docker run de ZAP dentro del pipeline.

5. RESULTADO FINAL
--------------------------------------------------------------------------------
- Pipeline ejecutado exitosamente (Estado: SUCCESS).
- Generación de artefactos:
  * zap_report.html (DAST)
  * bandit_report.json (SAST)
  * safety_report.txt (SCA)
  * Documentación pydoc.
- Monitorización activa en Grafana (Puerto 3000).
