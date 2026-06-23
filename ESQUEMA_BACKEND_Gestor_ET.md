# Esquema del Backend
## Sistema de Gestión de Expedientes (Gestor ET - Techo Propio)

Este documento expone la anatomía del servidor escrito en **Python/Flask**. Detalla cómo se procesa la información, la estructura de enrutamiento y los motores principales que dan vida a la plataforma.

---

### 1. El Núcleo (app.py)
El archivo `app.py` es el controlador principal (Controller) del patrón MVC. Alberga más de 2000 líneas de código (con refactorizaciones modulares a los esquemas DB). Se levanta sobre la librería `Flask` para gestionar las peticiones HTTP.

#### Principales Librerías Involucradas:
*   **Flask / Werkzeug**: Manejo de rutas, renderización HTML (SSR) y hashing de contraseñas.
*   **SQLAlchemy**: El ORM (Object-Relational Mapper) que traduce Python puro a consultas SQL bajo el capó.
*   **ReportLab & PyPDF**: Para dibujar texto en coordenadas cartesianas (X, Y) y fusionarlo con plantillas estáticas de PDF.
*   **DocxTemplate (docxtpl)**: Para parsear e inyectar etiquetas Jinja en archivos `.docx`.
*   **io.BytesIO**: Gestión de flujos binarios en Memoria RAM para evitar escribir y borrar archivos basura en el disco duro del servidor.

---

### 2. Capa de Seguridad (Middlewares de Autenticación)

El Backend implementa seguridad de sesión (Cookies cifradas) gestionada nativamente por Flask `session`. 
Para evitar que usuarios sin permiso accedan a rutas críticas, se implementan dos "Decoradores" a lo largo de todo el código:

1.  **`@login_admin_requerido`**: Envoltorio que comprueba si `session.get('rol') == 'admin'`. Si no es administrador, intercepta la petición y lo expulsa al login de admin.
2.  **`@login_usuario_requerido`**: Envoltorio que comprueba si `session.get('rol') == 'user'`. Protege el ecosistema del Portal aislado.

Adicionalmente, en las rutas de edición (ej. `/portal/matriz/editar/<id>`), el backend hace una validación manual (Tenant Isolation): *¿La entidad técnica dueña de esta ficha pertenece realmente a la lista de entidades asignadas a este usuario activo?* Si la respuesta es negativa, la solicitud es rechazada.

---

### 3. Mapa de Rutas (Endpoints)

El servidor divide su tráfico en tres grandes ramas lógicas:

#### A. Autenticación
*   `GET /` ➔ Redirección al portal principal.
*   `GET/POST /login_admin` ➔ Entrada superusuario.
*   `GET/POST /login_usuario` ➔ Entrada de digitadores de la ET.
*   `GET /logout_admin` | `GET /logout_usuario` ➔ Destrucción de sesión.

#### B. Rama Administrativa (Super-Admin)
*   `GET /dashboard` ➔ Panel de estadísticas y atajos.
*   `GET/POST /entidades` ➔ CRUD de Empresas Constructoras (Entidades Técnicas).
*   `GET/POST /usuarios` ➔ CRUD de usuarios del sistema y asignación de contraseñas hash.
*   `GET/POST /fichas/...` ➔ Control total y visualización de toda la base de datos de expedientes a nivel global.

#### C. Rama Portal (Digitadores ET)
*   `GET /portal/entidades` ➔ Visualiza las tarjetas de entidades a las que pertenece el usuario.
*   `GET /portal/matriz/<id_entidad>` ➔ Matriz de datos asilada.
*   `GET/POST /portal/matriz/crear` ➔ Ingesta de datos de los 5 acordeones (Guarda Predio, Jefe, Cónyuge, etc.).

---

### 4. Capa del Modelo (ORM - Database)

Todos los esquemas de base de datos se alojan de forma limpia en la carpeta `/models/`. 

*   `models.database.py`: Instancia el objeto `db`.
*   `models.usuario.py`: Tabla `usuarios`. Relacionado Many-to-Many con la tabla `entidades_tecnicas`.
*   `models.ficha.py`: Es el corazón del sistema (`fichas_inscripcion`). Posee claves primarias que son foráneas para el resto de entidades.
*   `models.predio.py`, `models.jefe.py`, etc: Tablas hijas. Tienen relación `One-to-One` usando `uselist=False` en SQLAlchemy, de tal manera que si llamas a `Ficha.jefe.dni` tienes acceso directo. La eliminación de `Ficha` gatilla `cascade="all, delete-orphan"` purgando todo el árbol de datos huérfanos.

---

### 5. Motores de Descarga y Procesamiento Binario

El gran logro del backend es la carencia de archivos estáticos basura. **Todo se procesa en memoria RAM**.

#### Motor PDF (`_generar_pdf_interno`)
1.  Se extrae la `FichaInscripcion` y todos sus hijos (Jefe, Predio, etc) de la base de datos.
2.  **Saneamiento (BugFix):** Un iterador recorre las clases limpiando todos los `None` y pasándolos a `""`. Esto previene el mortal `AttributeError` interno de ReportLab al intentar decodificar Nulls.
3.  `crear_pdf_datos(...)`: Levanta un `canvas` transparente y ejecuta más de 100 comandos `drawString(X, Y, texto)`.
4.  Se superpone el PDF estático de fondo con la plantilla transparente usando `PyPDF`. 
5.  Se devuelve el chorro de bytes (Buffer).

#### Motor DOCX (`_descargar_informe_interno`)
1.  `get_contexto_documentos(id_ficha, fecha)`: Función masiva que traduce el objeto SQLAlchemy complejo en un simple "Diccionario" de Python (`contexto['DNIBENEFICIARIO'] = '12345678'`). Maneja la lógica condicional booleana (traduce un `True` de base de datos a una cadena `'X'` visual).
2.  `inject_logo(doc, contexto)`: Captura la `URL` de la imagen asociada a la Entidad de turno, realiza una petición HTTPS externa, convierte la imagen a Bytes y la inyecta al contexto como objeto `InlineImage` de `docxtpl`.
3.  Se ejecuta `render()` y el archivo se guarda en memoria RAM.

#### Motor ZIP (`_descargar_todo_zip_interno`)
Reutiliza las lógicas del PDF y del DOCX. Recibe un arreglo (Array) indicando qué documentos se requieren y empaqueta los chorros de bytes (`zf.writestr()`) en un nuevo flujo binario comprimido con el algoritmo `ZIP_DEFLATED`.
