# UI/UX Design Brief
## Sistema de Gestión de Expedientes (Gestor ET - Techo Propio)

### 1. Visión y Sensación (Look & Feel)
La plataforma web persigue una **estética "Premium", técnica y enfocada al trabajo prolongado**. Debido a que las Entidades Técnicas pasarán horas capturando datos, se ha optado por una **Interfaz Nativa en Modo Oscuro (Dark Theme)**. Esto reduce significativamente la fatiga visual, resalta el contenido más importante a través del contraste y proyecta un aura de seguridad, tecnología y confidencialidad.

---

### 2. Paleta de Colores y Acentos (Color System)

La paleta se apoya en el ecosistema de **Bootstrap 5**, modificado para entornos de baja luminosidad (Dark Mode):

*   **Fondo Base (Background)**: Gris profundo (`#212529` a `#121212`). Simula el modo oscuro nativo de sistemas operativos.
*   **Superficies Elevadas (Tarjetas, Modales, Acordeones)**: Tonos grises más claros (`#2b2b2b` o clases `.bg-secondary` / `.bg-dark bg-gradient`). Permite distinguir niveles de profundidad.
*   **Texto Principal**: Blanco mate y gris claro (`.text-light`, `.text-muted`) para un contraste de alta legibilidad que no encandila.
*   **Acentos Funcionales (Botones e Iconos)**:
    *   🔵 **Primary (Azul Técnico)**: Utilizado para guardado de formularios y descarga de *Informes Técnicos*. Denota acción oficial.
    *   🔴 **Danger (Rojo Cardenal)**: Utilizado para la descarga de *Fichas de Inscripción (PDF)* y botones de borrado. Atrapa la atención inmediatamente.
    *   🟢 **Success (Verde Esmeralda)**: Utilizado exclusivamente para el *Empaquetado Múltiple (ZIP)*. Transmite culminación o éxito total.
    *   🌐 **Info (Cian)**: Utilizado para el *Formato de Constatación*.

---

### 3. Tipografía y Jerarquía Visual

*   **Fuente Principal**: Pila de fuentes del sistema de Bootstrap (System UI, `-apple-system`, `BlinkMacSystemFont`, `"Segoe UI"`, `Roboto`, `"Helvetica Neue"`, `Arial`, `sans-serif`).
    *   *Razón*: Utilizar tipografías nativas del sistema operativo asegura tiempos de carga nulos y un aspecto familiar para los ingenieros o digitadores que usan Windows/macOS.
*   **Jerarquía**: 
    *   Títulos (`H1`, `H2`): Gruesos y en color blanco sólido.
    *   Cuerpo del formulario: Tamaño estándar (`1rem`).
    *   Etiquetas de ayuda e inputs: Texto de menor tamaño y apagado (`.text-muted`, `.small`) para no estorbar el recorrido visual principal.

---

### 4. Patrones de Diseño (UI Components)

Para resolver el principal desafío arquitectónico (capturar docenas de campos de datos de una sola vez sin abrumar al usuario), se emplearon las siguientes soluciones:

#### A. Reducción de Carga Cognitiva (Acordeones)
El "Mega-Formulario" de inscripción está empaquetado en **Acordeones Colapsables**. En lugar de ver 50 inputs en una pantalla infinita, el usuario ve 5 barras horizontales limpias (Predio, Jefe de Familia, etc.). A medida que el usuario hace clic, se revela el contexto pertinente y se oculta lo demás.

#### B. Menús Ocultos Intuitivos (Rows Colapsables)
En la tabla o *Matriz* de usuarios, en lugar de empujar botones en una columna extremadamente ancha horizontal, la matriz cuenta con un ícono de flecha (`chevron-down`). Al hacer clic en la fila de un cliente, la tabla **se expande verticalmente** relevando un "cajón secreto" inferior con todos los botones de descarga coloridos y ordenados.

#### C. Modales Preventivos (El Cajón de Descarga ZIP)
En lugar de descargar archivos a ciegas, operaciones pesadas (como generar ZIPs) abren un *Modal Oscuro en Pantalla Completa Parcial*.
*   Fuerza al usuario a concentrarse solo en seleccionar una **Fecha** y los **Checkboxes** de sus documentos.
*   Evita falsos clics.

---

### 5. Micro-Interacciones (Motion & Feedback)

*   **Feedback Inmediato (Toasts / Alertas)**: Cada acción (crear, actualizar, errar un login, descargar un ZIP corrupto) emite una barra o alerta en la parte superior del formulario indicando Éxito (Verde) o Fallo (Rojo).
*   **Hover States (Sombras Flotantes)**: 
    *   Los botones de descarga tienen sombras ligeras (`.shadow-sm`) que reaccionan al posicionar el cursor sobre ellos.
    *   El icono de expansión en la matriz de expedientes (`chevron`) tiene una transición suave CSS de rotación `0.3s ease` cuando la fila se abre.
    *   Las tarjetas del Portal (`.card`) se elevan simulando relieve 3D al pasar el ratón.

---

### 6. Accesibilidad (a11y) e Iconografía

*   **Iconografía**: Se utiliza extensivamente la librería `Bootstrap Icons`. Cada botón de texto va invariablemente acompañado de un icono representativo (`bi-file-pdf`, `bi-file-word`, `bi-file-zip`). Esto acelera el reconocimiento cognitivo.
*   **Espaciado**: Los inputs del formulario de inscripción tienen márgenes amplios (`.mb-3` y `.mb-4`) evitando el síndrome de *clic erróneo* y garantizando que se visualicen bien tanto en monitores de PC como en Tablets.
