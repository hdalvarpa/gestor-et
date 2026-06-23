# Plan de Implementación (Rollout Plan)
## Sistema de Gestión de Expedientes (Gestor ET)

Este documento traza la hoja de ruta estratégica y técnica para llevar la aplicación desde su estado actual de desarrollo local (Localhost) hacia un entorno de producción real, seguro y accesible en internet para las Entidades Técnicas.

---

### Fase 1: Estabilización y Beta Interna (Local)
**Duración Estimada:** 1 - 2 Semanas
**Objetivo:** Asegurar que el núcleo de la aplicación esté libre de errores críticos antes de subirlo a la nube.

*   **1.1. Pruebas de Estrés Documental:** 
    *   Generar múltiples expedientes con nombres extremadamente largos, datos faltantes o caracteres especiales para garantizar que `reportlab` y `docxtpl` no se quiebren.
*   **1.2. Pulido de UI/UX:** 
    *   Verificación de la experiencia en dispositivos móviles/tablets (Responsividad del Modo Oscuro).
*   **1.3. Aprobación del MVP (Minimum Viable Product):** 
    *   Cerrar oficialmente la adición de nuevas características para enfocarse solo en el lanzamiento.

---

### Fase 2: Infraestructura y Servidor (Staging)
**Duración Estimada:** 2 Semanas
**Objetivo:** Preparar "la casa" en internet donde vivirá el Gestor ET.

*   **2.1. Selección de Servidor Cloud (VPS / PaaS):**
    *   *Recomendación:* Máquina Virtual Linux (Ubuntu 22.04 LTS) en proveedores como AWS, DigitalOcean, o un servicio gestionado como Render.
    *   *Recursos mínimos:* 2 vCPU, 2GB a 4GB de RAM (La manipulación de PDFs en RAM mediante `io.BytesIO` requiere memoria holgada).
*   **2.2. Migración de Base de Datos:**
    *   Migrar el archivo ligero actual `database.db` (SQLite) a un motor de base de datos robusto y concurrente como **PostgreSQL**.
    *   Configurar copias de seguridad automáticas (Backups diarios).
*   **2.3. Configuración del Servidor Web (Stack):**
    *   **Gunicorn**: Servidor de aplicaciones Python (WSGI) para reemplazar el servidor local de desarrollo de Flask.
    *   **Nginx**: Como proxy inverso para gestionar el tráfico de entrada, seguridad y compresión estática.
    *   Configuración de **Certificados SSL gratuitos (Let's Encrypt)** para forzar conexión segura **HTTPS** (indispensable al manejar DNIs e información confidencial).

---

### Fase 3: Despliegue Piloto y Capacitación (Pre-Launch)
**Duración Estimada:** 1 Semana
**Objetivo:** Probar el sistema con usuarios reales en un entorno controlado.

*   **3.1. Enlace de Dominio:** 
    *   Conectar la IP del servidor al dominio oficial (ej. `gestoret.com` o `portal.tuempresa.com`).
*   **3.2. Lanzamiento "Soft Launch":**
    *   Dar de alta a 1 o 2 Entidades Técnicas piloto en el sistema de producción.
*   **3.3. Sesión de Capacitación:**
    *   Crear un breve manual de usuario o un video explicativo apoyado en el documento *User Flow*.
    *   Explicar el correcto llenado del Mega-Formulario y cómo extraer descargas ZIP.

---

### Fase 4: Lanzamiento Oficial y Mantenimiento (Go-Live)
**Duración Estimada:** Permanente
**Objetivo:** Apertura global y soporte técnico activo.

*   **4.1. Creación Masiva de Credenciales:** 
    *   El Administrador genera desde su panel los usuarios y claves para todas las Entidades Técnicas.
*   **4.2. Monitoreo de Logs:** 
    *   Revisar los registros de Nginx y Flask semanalmente para identificar cuellos de botella (ej. Si la descarga del ZIP tarda más de 3 segundos).
*   **4.3. Implementación de Mejoras (V2.0):** 
    *   Posterior al primer mes, evaluar requerimientos adicionales como: Cuadros estadísticos en el Dashboard, exportación de la matriz completa a Excel, y filtros de búsqueda avanzada.

---

### Presupuesto Estimado de Operación Cloud (Mensual)
| Servicio | Descripción | Costo Aprox. |
| :--- | :--- | :--- |
| **Dominio Web** | Nombre público (`.com` o `.pe`) | $1 - $2 / mes |
| **Servidor (VPS)** | 2 vCPU, 2GB RAM, 50GB SSD (DigitalOcean / Linode) | $12 - $18 / mes |
| **Base de Datos** | PostgreSQL (Instalada en el mismo VPS) | $0 (Incluido) |
| **Certificado SSL** | Let's Encrypt | $0 (Gratis) |
| **Almacenamiento de Logos** | En la misma carpeta o Imgur/AWS S3 | $0 |
| **Total Mensual** | **Operación básica de alto rendimiento** | **$13 - $20 USD** |
