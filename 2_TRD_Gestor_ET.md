# Technical Requirements Document (TRD)
## Sistema de Gestión de Expedientes (Techo Propio)

### 1. Resumen de Arquitectura
El sistema opera bajo un patrón **MVC (Model-View-Controller)** simplificado, utilizando **Flask** (Python) como controlador principal, **Jinja2** para la renderización de las vistas en el servidor (SSR) y **SQLAlchemy** (ORM) para la capa del modelo de datos interactuando con una base de datos SQLite.

---

### 2. Estructura de Directorios

```text
gestor-et/
├── app.py                      # Controlador principal (Rutas, Core logic)
├── config.py                   # Configuraciones globales y variables de entorno
├── database.db                 # Base de datos SQLite local
├── FICHA DE INSCRIPCION.pdf    # PDF estático maestro para pypdf
├── FORMATO DE CONSTATACIÓN.docx # Word estático maestro para Constataciones
├── INFORME_TECNICO_MASTER.docx # Word estático maestro para Informes Técnicos
├── models/                     # Capa de Modelo (ORM)
│   ├── database.py             # Instancia de SQLAlchemy (db)
│   ├── conyuge.py              # Esquema de Cónyuge
│   ├── entidad_tecnica.py      # Esquema de Entidades
│   ├── ficha.py                # Esquema Padre (FichaInscripcion)
│   ├── jefe.py                 # Esquema Jefe de Familia
│   ├── predio.py               # Esquema Predio
│   └── usuario.py              # Esquema Usuarios
├── static/                     # Assets estáticos (CSS, JS, Logos de la web)
│   └── custom.css              # Reglas CSS específicas de UI
└── templates/                  # Capa de Vista (HTML/Jinja2)
    ├── admin_matriz.html       # Interfaz de Administrador (Acceso total)
    ├── base.html               # Layout base genérico/admin
    ├── base_usuario.html       # Layout base para el portal ET
    └── usuario_matriz.html     # Interfaz de Usuario Normal (Aislada por ET)
```

---

### 3. Esquema de Base de Datos (DB Schema)

El sistema utiliza `Flask-SQLAlchemy` con relaciones declarativas y Cascade Delete.

#### Relaciones Principales:
1. **`Usuario` (1) ➔ (N) `EntidadTecnica`**: A través de una tabla de asociación (relación Many-to-Many o asignaciones explícitas).
2. **`EntidadTecnica` (1) ➔ (N) `FichaInscripcion`**: Un administrador o ET inscribe expedientes que quedan vinculados a la ET responsable (`id_entidad_tecnica`).
3. **`FichaInscripcion` (1) ➔ (1) `Predio`, `Jefe`, `Conyuge`, `Constatacion`, `Informe`**: Relación `uselist=False`. La eliminación de la ficha gatilla `cascade="all, delete-orphan"`.
4. **`FichaInscripcion` (1) ➔ (N) `CargaFamiliar`, `FamiliarAdicional`**: Listas en cascada.

---

### 4. Algoritmos Core y Flujos de Renderizado

#### 4.1. Inyección y Fusión de PDF (Fichas de Inscripción)
- **Librerías**: `reportlab` y `pypdf`.
- **Flujo**: 
  1. Se obtienen los datos mediante ORM.
  2. Un bucle intercepta los valores nulos (`None`) y los transforma en cadenas vacías `""` para evitar fallos de renderizado en `reportlab`.
  3. `reportlab` dibuja texto en coordenadas absolutas (X,Y) y genera un PDF "Transparente" en memoria (`io.BytesIO()`).
  4. `pypdf` lee la plantilla maestra estática (`FICHA DE INSCRIPCION.pdf`) y superpone la capa transparente (`merge_page`).
  5. El resultado se vuelca al buffer y se sirve vía `send_file`.

#### 4.2. Inyección de Word Dinámico (Informes y Constataciones)
- **Librerías**: `docxtpl` (encapsulando `python-docx`).
- **Flujo**:
  1. Se arma un Diccionario (`contexto`) mapeando las variables (e.g. `contexto['DNIBENEFICIARIO'] = jefe.dni`).
  2. Inyección de Imagen Dinámica: La función `inject_logo(doc, contexto)` procesa `contexto['URL_LOGO']`, realiza un `requests.get`, convierte la imagen remota a un buffer binario y la inserta usando `InlineImage` de `docxtpl`.
  3. El motor renderiza el documento reemplazando los tags jinja integrados en el `.docx`.

#### 4.3. Procesamiento en Lote (Compositor de ZIP)
- Se utiliza `zipfile.ZipFile` apuntando a un buffer `io.BytesIO()`.
- Un array proveniente del Front-End (`?docs=ficha,informe,constatacion`) determina qué flujos (PDF y/o Word) se ejecutan. 
- Los retornos binarios en memoria se añaden al ZIP usando `zf.writestr('nombre.ext', buffer.getvalue())`.

---

### 5. Dependencias y Requisitos del Entorno (Requirements)

El entorno se gestiona mediante pip. Las dependencias críticas son:
- `Flask>=2.0.0`
- `Flask-SQLAlchemy`
- `Werkzeug` (Password hashing)
- `reportlab` (Creación de PDF programático)
- `pypdf` (Fusión de PDFs)
- `docxtpl` (Inyección de plantillas DOCX)
- `python-docx`
- `requests` (Fetch de logotipos remotos)
- `pandas` (Si se habilitan importaciones/exportaciones de Excel)

### 6. Control de Errores y Seguridad (Mitigación)

1. **Blindaje Multitenant**: En `app.py`, las funciones `/portal/matriz/editar/<id>` validan que la Entidad Técnica del usuario coincida con la Entidad Técnica de la Ficha (`if ficha.entidad_tecnica not in user_obj.entidades:`). Si falla, expulsa al usuario al dashboard.
2. **Silence Linter**: Importaciones dinámicas dentro de funciones incluyen marcadores especiales (`# pyrefly: ignore [missing-import]`) para mantener las extensiones del IDE limpias sin alterar el motor PVM.
3. **Timeout DB (`@app.errorhandler(500)`)**: Intercepta caídas de base de datos (`OperationalError`), realiza un `rollback()` forzoso e intenta redirigir de forma segura para no exponer el stack trace al usuario final.
