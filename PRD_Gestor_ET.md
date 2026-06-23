# Product Requirements Document (PRD)
## Sistema de Gestión de Expedientes (Techo Propio)

### 1. Visión y Objetivo del Producto
Desarrollar una plataforma web centralizada e intuitiva que permita a las **Entidades Técnicas (ET)** y a los **Administradores** registrar, editar, gestionar y exportar expedientes (fichas) de posibles beneficiarios (Jefes de Familia). 
El objetivo principal es **automatizar y acelerar** la generación de documentos oficiales (Ficha de Inscripción en PDF, Informes Técnicos en Word y Formatos de Constatación en Word) evitando errores de digitación y garantizando un control estricto de roles y privacidad entre entidades.

---

### 2. Roles y Permisos

#### A. Administrador (Super-Admin)
- **Acceso Total**: Visualización y gestión de *todas* las Entidades Técnicas y *todas* las Fichas de Inscripción.
- **Gestión de Entidades**: Capacidad para crear, editar y eliminar cuentas de Entidades Técnicas (asignando usuarios y contraseñas).
- **Gestión Global de Beneficiarios**: Capacidad para registrar, editar y dar de baja beneficiarios a nombre de cualquier ET.
- **Generación de Documentos**: Puede generar y descargar documentos individuales o empaquetados en ZIP de cualquier beneficiario.

#### B. Entidad Técnica (Usuario Portal)
- **Acceso Aislado**: Cada sesión está vinculada exclusivamente a su propia Entidad. Solo puede ver a sus propios beneficiarios.
- **Creación y Edición Autónoma**: Capacidad de registrar y editar a sus propios beneficiarios sin depender del Administrador.
- **Generación de Documentos**: Capacidad de descargar sus propios expedientes técnicos (PDF/Word/ZIP) pre-rellenados y con los logotipos dinámicos de su propia entidad.
- **Seguridad Perimetral**: No tiene acceso a listados maestros ni puede interactuar (vía inyección de URL) con beneficiarios de otras ETs.

---

### 3. Requisitos Funcionales (Core Features)

#### 3.1. Autenticación y Seguridad
- Inicio de sesión con Usuario y Contraseña encriptada (`werkzeug.security`).
- Rutas protegidas (`@login_usuario_requerido` y `@login_admin_requerido`).
- Desconexión segura.

#### 3.2. Gestión del Beneficiario (Mega-Formulario)
El formulario de captura de datos consolida 6 bloques lógicos en un solo paso (con opciones dinámicas):
1. **Entidad Técnica a Cargo**: Asignación automática para usuarios normales; selección desplegable para Administradores.
2. **Datos del Predio**: Ubicación (Distrito, Provincia, Manzana, Lote, Partida Registral).
3. **Jefe de Familia**: Datos personales, DNI, ingresos, grado de instrucción, discapacidad y ocupación.
4. **Cónyuge** (Opcional): Datos personales y laborales.
5. **Cargas Familiares y Adicionales**: Generación de listas dinámicas (Nombres, vínculos, DNI).
6. **Constatación e Informe Técnico**: Medidas de linderos (Frente, Derecha, Izquierda, Fondo) y cuenta de servicios (Agua/Saneamiento).
7. **Contacto**: Teléfono y correo electrónico.

#### 3.3. Motor de Generación Documental Automática
- **Fichas de Inscripción (PDF)**: Generación por coordenadas `X/Y` usando la biblioteca `reportlab` sobre una plantilla PDF. Resiliencia ante valores vacíos/nulos de la base de datos.
- **Informes Técnicos y Constataciones (Word)**: Inserción de variables usando `docxtpl` con llaves `{{ variable }}`. Inserción dinámica de logotipos de las ET (usando un link de la BD a una imagen alojada).
- **Descargas Agrupadas (ZIP)**: Modal unificado que solicita la "Fecha de Emisión de los Documentos", con validación estricta de seleccionar al menos dos documentos para empaquetarlos al vuelo en un archivo `ZIP`.

#### 3.4. Interfaces de Usuario (UI/UX)
- Interfaz en **Modo Oscuro** (Dark Theme) apoyada por Bootstrap 5 y CSS personalizado, dando una sensación premium y técnica.
- Modales nativos (Visualización de Fichas) y vistas tipo "Acordeón" para no saturar al usuario con tablas largas.

---

### 4. Stack Tecnológico

| Componente | Tecnología / Librería |
| :--- | :--- |
| **Backend / Framework** | Python 3 + Flask |
| **Base de Datos** | SQLite (con `Flask-SQLAlchemy`) |
| **Frontend UI** | HTML5, CSS3, JavaScript Vanilla, Bootstrap 5, Bootstrap Icons |
| **Manipulación de Documentos** | `reportlab` (PDF), `pypdf` (Merge), `docxtpl` / `python-docx` (Word) |

---

### 5. Estructura de Datos (Modelos Base)

- **Usuarios**: Id, username, password_hash, rol (admin/user).
- **Entidad Técnica**: Razón Social, RUC, URL de Logo.
- **FichaInscripcion**: Eje central. Relaciona 1:1 con Predio, Jefe, Conyuge, Constatacion, Informe y 1:N con Cargas y Adicionales.
- **Predio, Jefe, Conyuge**: Almacenan el detalle de los datos primarios.
- **CargaFamiliar, FamiliarAdicional**: Tablas relacionadas a la ficha mediante llave foránea.

---

### 6. Historial de Resoluciones Críticas (Decisiones de Arquitectura)

1. **Aislamiento de Plantillas (Separation of Concerns)**: Se optó por tener un `admin_matriz.html` y un `usuario_matriz.html` separados para asegurar que la inyección de código y botones no contamine las rutas de permisos entre Administrador y ET.
2. **Gestión de Errores Silenciosos de ReportLab**: Se diseñó una función inyectora de variables seguras para convertir datos nulos en *strings vacíos* antes de inyectarlos en el PDF, evitando colapsos del servidor.
3. **Descargas Masivas Ponderadas**: Para evitar que la selección del ZIP descargara archivos redundantes, se trasladó la condición del Front-End a la generación del Backend (Validación Front y validación de Arrays en el Back).
4. **Plantilla Maestra de Word**: Se eliminaron dependencias a múltiples plantillas hardcodeadas por ET, utilizando únicamente `INFORME_TECNICO_MASTER.docx` para un código más limpio y fácil de mantener.

---

### 7. Futuras Mejoras (Roadmap Propuesto)
1. *Búsqueda y Filtros:* (P. ej., buscar DNI o filtrar Fichas por Rango de Fechas).
2. *Estadísticas / Dashboard:* Gráficos de Beneficiarios registrados por mes.
3. *Respaldos Automáticos:* Exportación de toda la Base de Datos a un archivo SQL/Excel.
