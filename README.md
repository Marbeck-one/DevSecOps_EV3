# Evaluación 3: Implementación de Pipeline DevSecOps

Este proyecto consiste en la implementación de un ciclo de vida de desarrollo seguro (DevSecOps) para una aplicación web basada en Flask. El objetivo es demostrar la integración de pruebas de seguridad automatizadas (SAST, DAST), gestión de dependencias y monitorización en un entorno CI/CD.

## 👥 Integrantes
* **Nombre:** RODRIGO MARTINEZ(MARBECK) , VINCENT FARENDEN, MASSIMO NAVARRETE
* **Asignatura:** Ciberseguridad en Desarrollo (OCY1102)

## 🏗️ Arquitectura del Proyecto

El entorno se despliega utilizando **Docker Compose** y consta de los siguientes servicios:

* **WebApp:** Aplicación Python Flask (securizada).
* **Jenkins:** Servidor de automatización CI/CD.
* **Prometheus:** Base de datos de series temporales para monitorización.
* **Grafana:** Dashboard para visualización de métricas.

## 🔒 Pipeline de Seguridad (CI/CD)

El pipeline de Jenkins (`Jenkinsfile`) ejecuta las siguientes etapas:

1.  **Checkout & Setup:** Instalación de dependencias y herramientas de seguridad.
2.  **SAST (Static Application Security Testing):** Análisis de código estático con **Bandit** para detectar vulnerabilidades en Python.
3.  **SCA (Software Composition Analysis):** Revisión de librerías vulnerables usando **Safety**.
4.  **Build & Deploy Test:** Despliegue efímero de la aplicación en un entorno de pruebas aislado.
5.  **DAST (Dynamic Application Security Testing):** Escaneo dinámico de la aplicación en ejecución utilizando **OWASP ZAP**.
6.  **Documentación:** Generación automática de documentación técnica con `pydoc`.

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python 3.9
* **Orquestación:** Docker & Docker Compose
* **CI/CD:** Jenkins
* **Seguridad:** Bandit, Safety, OWASP ZAP (Dockerizada)
* **Monitorización:** Prometheus, Grafana, prometheus-flask-exporter

## 🚀 Despliegue

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPO>
   cd parcial3
