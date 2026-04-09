# ATHINA VSM — Guía Completa de la Aplicación de Value Stream Mapping

## Resumen Ejecutivo

ATHINA VSM es una aplicación web desarrollada por el equipo DevSecOps del proyecto ATHINA LOT1 para analizar y generar Value Stream Maps (mapas de flujo de valor) de manera automatizada. La herramienta permite a los equipos de desarrollo de software completar cuestionarios estructurados sobre sus procesos de trabajo, y luego utiliza inteligencia artificial (OpenAI o Azure OpenAI) para generar mapas visuales del flujo de valor con métricas de tiempo reales. También permite crear estos mapas manualmente desde el panel de administración.

La aplicación está construida con Django 5.1, PostgreSQL 16, y se ejecuta en contenedores Docker. Soporta dos idiomas (español e inglés) y usa Mermaid.js para renderizar diagramas interactivos, Bootstrap 5 para la interfaz, e Intro.js para tutoriales guiados.

Incluye un sistema completo de autenticación y autorización basado en roles por proyecto (viewer, editor, project_manager, admin), donde cada vista está protegida con `@login_required` y permisos granulares. También incorpora un módulo de **sugerencias de mejora con IA**: desde la visualización del VSM, los usuarios con rol de gestión pueden solicitar a la IA un análisis de mejora continua que identifica cuellos de botella, oportunidades de optimización y quick wins basados en las métricas reales del mapa.

---

## Qué es un Value Stream Map (VSM)

Un Value Stream Map es una herramienta visual de Lean Manufacturing adaptada al desarrollo de software. Muestra la secuencia completa de pasos que un equipo o conjunto de equipos sigue para entregar un producto o servicio, desde la solicitud inicial hasta la entrega final.

Cada paso del mapa incluye métricas clave como:
- **Tiempo de trabajo (Work Time)**: las horas reales de trabajo activo en un paso.
- **Tiempo de espera (Wait Time)**: las horas que el trabajo permanece inactivo antes de avanzar.
- **Factor de retrabajo (Loop Factor)**: la probabilidad de que ese paso necesite repetirse (por ejemplo, 0.3 significa que el 30% de las veces hay retrabajo).
- **Trabajo extra por retrabajo (Loop Work Extra)**: las horas adicionales que consume cada ciclo de retrabajo.
- **Personas involucradas (Num People)**: cuántas personas trabajan en ese paso.
- **Tipo de flujo (Flow Type)**: si el trabajo se "empuja" (push, asignado por un manager) o se "jala" (pull, el equipo lo toma de una cola).

El objetivo del VSM es identificar desperdicios (waste), cuellos de botella y oportunidades de mejora en el proceso de entrega.

### Fórmulas de cálculo

El sistema calcula automáticamente tres métricas derivadas para cada paso:

- **Loop Time** = Loop Factor × Loop Work Extra. Ejemplo: si hay 30% de retrabajo y cada ciclo cuesta 10 horas extra, el Loop Time es 3 horas.
- **Effective Work Time** = Work Time + Loop Time. El tiempo real de trabajo incluyendo retrabajo.
- **Total Time** = Effective Work Time + Wait Time. El tiempo completo que consume un paso.
- **Lead Time del VSM** = Suma de Total Time de todos los pasos. El tiempo total de punta a punta del flujo.

### Conceptos clave de VSM

| Término | Definición |
|---------|-----------|
| **Value Stream** | La secuencia de todos los pasos necesarios para entregar un producto o servicio |
| **Handoff** | El punto donde el trabajo se transfiere de una persona o equipo a otro |
| **Lead Time** | Tiempo total desde la solicitud hasta la entrega |
| **Process Time** | Tiempo real trabajando en una tarea, sin contar esperas |
| **Wait Time** | Tiempo que un elemento espera sin que nadie trabaje en él |
| **Waste (Muda)** | Cualquier actividad que consume recursos pero no crea valor para el cliente |
| **Bottleneck** | Una restricción que limita el rendimiento del sistema completo |
| **WIP** | Work in Progress: el número de elementos en los que se trabaja simultáneamente |
| **Push** | El trabajo es asignado o dirigido al equipo por un manager o sistema |
| **Pull** | El equipo coge el trabajo de una cola o backlog cuando tiene capacidad |

---

## Arquitectura Técnica de la Aplicación

### Stack tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | Django | 5.1 |
| Base de datos | PostgreSQL | 16 (Alpine) |
| Contenedores | Docker + Docker Compose | — |
| Frontend CSS | Bootstrap | 5.3.3 |
| Diagramas | Mermaid.js | 11 (ESM) |
| Tutorial guiado | Intro.js | 7.2.0 |
| Internacionalización | Django i18n | gettext .po/.mo |
| IA | OpenAI / Azure OpenAI SDK | — |

### Estructura de archivos principal

```
docs/vsm/app/
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile                  # Imagen del contenedor web
├── entrypoint.sh               # Script de inicialización (migraciones, collectstatic)
├── manage.py                   # Django management
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno
│
├── locale/es/LC_MESSAGES/      # Traducciones español
│   ├── django.po               # Archivo de traducciones fuente
│   └── django.mo               # Archivo compilado
│
├── vsm/                        # Aplicación Django principal
│   ├── models.py               # 9 modelos de datos
│   ├── views.py                # Vistas (controladores)
│   ├── forms.py                # Formularios dinámicos
│   ├── admin.py                # Panel de administración
│   ├── urls.py                 # Rutas URL
│   │
│   ├── fixtures/
│   │   └── questions_config.yaml   # 200+ preguntas precargadas
│   │
│   ├── management/commands/
│   │   ├── load_questions.py       # Cargador de preguntas desde YAML
│   │   ├── load_diagrams.py        # Cargador de diagramas
│   │   ├── load_vsm_seed.py        # Datos semilla de VSM
│   │   └── load_test_data.py       # Datos de prueba
│   │
│   ├── services/
│   │   └── ai_generator.py         # Generador de VSM con IA
│   │
│   ├── templates/vsm/
│   │   ├── base.html               # Template base con navbar y i18n
│   │   ├── index.html              # Página principal con diagrama
│   │   ├── form.html               # Formulario de cuestionario
│   │   ├── project_list.html       # Lista de proyectos
│   │   ├── project_detail.html     # Detalle de proyecto
│   │   ├── generate_vsm.html       # Generación IA
│   │   ├── vsm_map.html            # Visualización del VSM
│   │   ├── vsm_map_list.html       # Lista de VSMs
│   │   ├── response_list.html      # Lista de respuestas
│   │   ├── diagram_view.html       # Visor de diagramas Mermaid
│   │   └── thank_you.html          # Confirmación post-cuestionario
│   │
│   └── static/vsm/
│       └── style.css               # Estilos personalizados
│
└── vsm_project/                # Configuración Django
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

### Infraestructura Docker

La aplicación se ejecuta con Docker Compose con dos servicios:

1. **db**: PostgreSQL 16 Alpine, puerto 5433 externo → 5432 interno, con healthcheck automático y volumen persistente `pgdata`.
2. **web**: Aplicación Django, puerto 8000, monta el código fuente como volumen para desarrollo en vivo. Depende de que `db` esté healthy antes de arrancar.

El entrypoint ejecuta automáticamente las migraciones de base de datos y collectstatic al iniciar.

---

## Los 11 Modelos de Datos

La aplicación tiene 11 modelos Django que representan toda la estructura de datos:

### 1. AIConfiguration (Configuración de IA)

Modelo singleton (solo puede existir uno, forzado con pk=1) que almacena la configuración de la IA para generar VSMs automáticamente.

Campos: provider (openai o azure), api_key, endpoint, model_name, api_version, temperature, max_tokens, is_active. Soporta dos proveedores: OpenAI estándar y Azure OpenAI (requiere endpoint y api_version adicionales).

### 2. Category (Departamento)

Representa un equipo o departamento de la organización. Cada categoría tiene un conjunto de secciones y preguntas que forman su cuestionario.

Campos: name, slug (autogenerado), color (hexadecimal para la UI), order (posición), description.

La aplicación viene con 7 departamentos predefinidos:
- Developers: equipo de desarrollo backend y frontend
- QA / Testing: aseguramiento de calidad y pruebas
- UX / Design: experiencia de usuario y diseño de interfaces
- Data / Analytics: ingeniería de datos, ETL y analítica
- Agile / Scrum: scrum masters y coaches ágiles
- Management: product owners y gestión de programa
- DevOps / Platform: DevOps, SRE e ingeniería de plataforma

### 3. Section (Sección del cuestionario)

Cada departamento tiene secciones que agrupan preguntas temáticamente. Hay 7 secciones estándar por departamento:

- **Sección A — Team Identity**: define quién es el equipo, quiénes son sus clientes y proveedores internos.
- **Sección B — Process Steps**: describe los pasos concretos del proceso de trabajo del equipo, incluyendo tablas con métricas detalladas por tipo de trabajo (features, bug fixes, etc.).
- **Sección C — Handoffs & Dependencies**: mapea las entregas entre equipos, las dependencias, los cuellos de botella y los tiempos de espera en las transiciones.
- **Sección D — Pain Points & Waste**: identifica los problemas, el retrabajo, las causas de retraso y los desperdicios del proceso actual.
- **Sección E — Tools & Systems**: documenta las herramientas y sistemas que el equipo usa en cada paso de su proceso.
- **Sección F — Improvement Ideas**: recoge ideas de mejora, quick wins y cambios que el equipo propone para mejorar la entrega.
- **Sección G — VSM Metrics (for automated map generation)**: contiene las métricas cuantitativas que la IA necesita para generar el VSM automáticamente: tiempos de trabajo, tiempos de espera, porcentaje de retrabajo, número de personas, tipo de flujo (push/pull) y una tabla detallada por paso.

La Sección G es especial porque es la única que contiene datos numéricos estructurados. Sin ella, la IA no puede generar el VSM automáticamente. Las secciones A-F proporcionan contexto cualitativo valioso pero no datos cuantitativos directos.

Campos: category (FK), code (letra A-G), title, order.

### 4. Question (Pregunta)

Cada pregunta tiene un tipo que determina cómo se renderiza en el formulario y cómo se almacenan los datos. Existen 4 tipos:

**text**: Campo de texto corto de una línea. Se usa para nombres, números simples, porcentajes. Ejemplo: "Average work time in hours". No necesita opciones.

**textarea**: Área de texto multilínea. Se usa para descripciones, listas de pasos, explicaciones detalladas. Ejemplo: "Describe the steps for implementing a new feature". No necesita opciones.

**checklist**: Selección múltiple con checkboxes. Se usa para categorización, selección de opciones. Ejemplo: "What types of waste do you observe?" con opciones como "Waiting", "Rework", "Context switching". Requiere un campo options con una lista JSON de strings.

**table**: Tabla interactiva de filas y columnas. Se usa para datos estructurados con múltiples dimensiones. Ejemplo: una tabla con columnas "Step Name", "Work Time", "Wait Time", "Rework %". El usuario puede añadir filas dinámicamente con JavaScript. Los datos se almacenan como JSON (lista de diccionarios). Requiere un campo options con un objeto JSON que tenga la clave "columns" con la lista de nombres de columna.

Campos: section (FK), key (identificador único como "dev_a1"), label (texto de la pregunta), question_type, options (JSON, opcional), order.

### 5. Project (Proyecto)

Agrupa todo el trabajo de un análisis VSM: cuestionarios, respuestas, value streams y diagramas. Los usuarios se vinculan a proyectos a través del modelo ProjectMembership.

Campos: name, slug, description, color, members (M2M a User a través de ProjectMembership), created_at, updated_at.

### 6. ProjectMembership (Membresía de Proyecto)

Modelo intermedio (through) que vincula un usuario de Django con un proyecto y le asigna un rol específico. Garantiza restricción `unique_together` para que un usuario solo tenga un rol por proyecto.

Campos: project (FK a Project), user (FK a User), role (viewer, editor o project_manager).

Los superusuarios de Django obtienen automáticamente el rol "admin" virtual sin necesitar membresía explícita.

| Rol | Permisos |
|-----|----------|
| **viewer** | Ver proyecto, ver VSMs, ver respuestas |
| **editor** | Todo lo de viewer + rellenar/editar/eliminar cuestionarios |
| **project_manager** | Todo lo de editor + generar VSMs con IA, solicitar sugerencias de mejora, gestionar recursos del proyecto |
| **admin** (superuser) | Acceso total a todos los proyectos y funciones |

### 7. FormResponse (Respuesta de cuestionario)

Almacena una respuesta completa de un cuestionario. Un respondente llena el formulario de su departamento y todas sus respuestas se guardan como JSON en el campo "data", donde cada clave es el key de la pregunta y el valor es la respuesta.

Campos: category (FK), project (FK, opcional), respondent_name, respondent_role, data (JSON), submitted_at, updated_at.

Ejemplo de datos almacenados:
```json
{
  "dev_a1": "Core Development Team",
  "dev_a2": "5 developers",
  "dev_g1_work_time": "40",
  "dev_g2_wait_time": "8",
  "dev_g3_rework_pct": "20",
  "dev_g6_steps": [
    {"Step Name": "Planning", "Work Time (hours)": "2", "Wait Time (hours)": "4"},
    {"Step Name": "Development", "Work Time (hours)": "16", "Wait Time (hours)": "2"}
  ]
}
```

### 8. Diagram (Diagrama Mermaid)

Permite crear diagramas Mermaid personalizados asociados a proyectos: diagramas de arquitectura, flujos de secuencia, organigramas, etc.

Campos: project (FK, opcional), name, slug, description, mermaid_code (el código fuente del diagrama), is_default, created_at, updated_at.

### 9. ValueStream (Mapa de Flujo de Valor)

El modelo central del sistema. Representa un VSM completo con sus pasos y métricas. Tiene dos modos de creación: "manual" (el usuario crea cada paso desde el admin) o "ai" (la IA genera los pasos automáticamente a partir de las respuestas de los cuestionarios).

Campos: name, slug, project (FK), description, generation_method ("manual" o "ai"), ai_analysis (texto con el razonamiento de la IA), ai_suggestions (texto con sugerencias de mejora generadas por IA), source_responses (M2M a FormResponse), created_at, updated_at.

Propiedades calculadas: lead_time (suma de total_time de todos los pasos), total_work_time, total_wait_time.

### 10. ProcessStep (Paso del proceso)

Cada paso individual dentro de un ValueStream. Contiene todas las métricas de tiempo y flujo.

Campos: value_stream (FK), name, category (FK al departamento responsable), order (posición), row (0 = flujo principal, 1 = flujo secundario/paralelo), work_time, wait_time, loop_factor, loop_work_extra, num_people, flow_type ("push" o "pull"), description.

Propiedades calculadas: loop_time, effective_work_time, total_time.

---

## Sistema de Autenticación y Autorización

La aplicación implementa un sistema completo de control de acceso basado en roles por proyecto.

### Autenticación

- Todas las vistas están protegidas con el decorador `@login_required` de Django.
- La autenticación usa el sistema de usuarios estándar de Django (`django.contrib.auth`).
- El login se accede desde `/accounts/login/` con un formulario estilizado con Bootstrap.
- La barra de navegación muestra el nombre del usuario logueado y un botón de logout.
- Los superusuarios se crean con `python manage.py createsuperuser`.

### Autorización por roles

El acceso a los datos se controla a nivel de proyecto mediante el modelo `ProjectMembership`. El módulo `permissions.py` proporciona 5 funciones auxiliares:

| Función | Descripción | Roles permitidos |
|---------|-------------|------------------|
| `get_user_projects(user)` | Retorna los proyectos accesibles para el usuario | Cualquier rol / superuser ve todos |
| `get_user_role(user, project)` | Retorna el string del rol o None | — |
| `user_can_view(user, project)` | ¿Puede ver el proyecto? | viewer, editor, project_manager, admin |
| `user_can_edit(user, project)` | ¿Puede rellenar/editar cuestionarios? | editor, project_manager, admin |
| `user_can_manage(user, project)` | ¿Puede generar VSMs y gestionar? | project_manager, admin |

### Protección por vista

| Vista | Permiso requerido |
|-------|-------------------|
| index, vsm_map_list | Login (cualquier usuario) |
| project_list | Login (solo ve sus proyectos) |
| project_detail | `user_can_view` |
| form (cuestionario) | `user_can_edit` |
| response_list, response_edit, response_delete | `user_can_edit` |
| generate_vsm, save_vsm | `user_can_manage` |
| vsm_suggestions | `user_can_manage` + POST |
| vsm_map | `user_can_view` (del proyecto asociado) |

### Gestión de usuarios

Los usuarios y sus membresías se gestionan desde el panel de administración de Django:
- Admin → Users: crear/editar usuarios estándar.
- Admin → Project Memberships: asignar usuarios a proyectos con roles específicos.
- Los ProjectMemberships también aparecen como inline dentro de cada Project en el admin.

---

## Los Dos Flujos de Trabajo

La aplicación ofrece dos caminos distintos para crear un VSM:

### Flujo A: Cuestionarios + Inteligencia Artificial

Este es el flujo principal recomendado cuando se quiere analizar procesos reales de múltiples equipos.

**Paso 1 — Crear un proyecto**: Desde la web o el admin, se crea un proyecto que agrupa todo el análisis.

**Paso 2 — Los equipos rellenan cuestionarios**: Cada departamento tiene un cuestionario dedicado con 7 secciones (A-G). Los miembros del equipo acceden al proyecto, seleccionan su departamento y completan el formulario con datos reales de su proceso. El formulario se genera dinámicamente a partir de las preguntas almacenadas en la base de datos.

**Paso 3 — Revisar las respuestas**: El líder del proyecto verifica que hay suficientes respuestas de los departamentos relevantes. Puede ver un resumen por departamento con el conteo de respuestas. También puede editar o eliminar respuestas individuales.

**Paso 4 — Generar el VSM con IA**: La IA (GPT-4 o similar) recibe un prompt estructurado con todas las respuestas del proyecto. Analiza los datos cuantitativos (Sección G) y cualitativos (Secciones A-F) y genera un JSON con los pasos del proceso, métricas de tiempo, análisis de retrabajo y una explicación razonada del mapa propuesto.

**Paso 5 — Guardar el VSM**: El usuario revisa la vista previa del VSM generado, los pasos propuestos con sus tiempos y métricas, y el análisis escrito de la IA. Si está conforme, guarda el VSM en la base de datos.

**Paso 6 — Visualizar el mapa**: Se accede a la visualización interactiva del VSM que muestra cada paso como una tarjeta con métricas, flechas de flujo, indicadores de retrabajo, una tabla resumen por departamento y el lead time total.

**Paso 7 — Iterar y mejorar**: Se pueden recoger nuevas respuestas, regenerar el VSM y comparar versiones para medir la mejora continua.

### Flujo B: Creación Manual desde Admin

Este flujo es ideal cuando ya se conocen los datos del proceso o se quiere crear un VSM rápido sin necesidad de cuestionarios.

**Paso 1 — Crear departamentos**: Desde Admin → Categories, se crean los departamentos que participan en el flujo de valor (o se usan los 7 predefinidos).

**Paso 2 — Crear formularios (opcional)**: Si se quieren usar cuestionarios en el futuro, se configuran las secciones y preguntas para cada departamento.

**Paso 3 — Crear un proyecto**: Desde Admin → Projects, se crea el proyecto contenedor.

**Paso 4 — Crear el VSM manualmente**: Desde Admin → Value Streams, se crea un nuevo VSM con generation_method = "Manual". Se añaden los ProcessSteps directamente con los tiempos, factores de retrabajo, personas y tipo de flujo para cada paso.

---

## Interfaz de Usuario: Pantallas Principales

### Página Principal (index)

La página principal muestra:
- Un banner "ATHINA – Value Stream Mapping" con un botón de tutorial guiado.
- Un diagrama interactivo Mermaid con dos subgrafos: el flujo de cuestionarios (IA) en azul y el flujo admin (manual) en naranja. Ambos convergen en "Save VSM" → "Visualize" → "Iterate".
- Controles de zoom y pan para el diagrama (solo en escritorio).
- Una sección de pasos explicados para cada opción (A: IA con 7 pasos, B: Admin con 4 pasos).
- Tres tarjetas de navegación: Projects, Value Stream Maps, y Administration (enlace al admin de Django).

La página tiene dos versiones del diagrama: una horizontal (LR) para escritorio y una vertical (TD) para móvil, y solo renderiza la visible para optimizar rendimiento.

### Formulario de Cuestionario (form)

El formulario se genera dinámicamente basándose en las preguntas almacenadas en la base de datos para el departamento seleccionado. Muestra:
- Breadcrumb de navegación.
- Campos de nombre y rol del respondente.
- Secciones colapsables (A-G) con el color del departamento.
- Cada pregunta renderizada según su tipo: campos de texto, áreas de texto, checkboxes múltiples o tablas interactivas con filas añadibles.
- Las tablas permiten añadir filas dinámicamente con JavaScript y almacenan los datos como JSON en un campo oculto.

### Detalle de Proyecto (project_detail)

Muestra el dashboard de un proyecto con:
- Diagramas Mermaid del proyecto con zoom interactivo.
- Lista de Value Stream Maps generados.
- Tarjetas de departamentos con conteo de respuestas y enlaces para rellenar cuestionarios o ver respuestas existentes.
- Botón para generar VSM con IA.

### Generación de VSM con IA (generate_vsm)

Esta pantalla tiene tres estados:
1. **Vista previa**: muestra un resumen de las respuestas disponibles por departamento con barras de progreso. Si la IA no está configurada, muestra un aviso con enlace al admin. Incluye el botón "Generate VSM with AI".
2. **Generando**: el botón muestra un spinner mientras la IA procesa (puede tardar 10-30 segundos).
3. **Resultado**: muestra el VSM generado con los pasos propuestos, métricas por paso, y el análisis escrito de la IA. Incluye un botón para guardar el resultado.

### Visualización del VSM (vsm_map)

La pantalla más rica visualmente, que muestra:
- Los pasos del proceso como tarjetas conectadas por flechas.
- Cada tarjeta tiene el color del departamento, nombre del paso, métricas (work time, loop time, people, flow type) y una barra de tiempo inferior.
- Indicadores de retrabajo (badges rojos en las esquinas de las tarjetas con loop factor).
- Iconos de push/pull (círculos amarillos para push).
- Separación visual entre flujo principal (row 0) y flujo secundario (row 1).
- Una tabla resumen por departamento con: work time, loop time, wait time, porcentajes del lead time total.
- El lead time total destacado en grande.
- Una leyenda explicativa del diagrama.
- Si fue generado por IA, se muestra el análisis escrito de la IA.
- **Botón "Sugerir mejoras con IA"**: visible solo para usuarios con rol `project_manager` o `admin` y cuando la IA está configurada. Al pulsarlo, muestra un spinner de carga y envía un POST al endpoint `vsm_suggestions`. Las sugerencias generadas se guardan en el campo `ai_suggestions` del ValueStream y se renderizan como Markdown formateado (usando la librería `marked.js`) en una card informativa debajo de la tabla resumen.

### Visor de Diagramas Mermaid (diagram_view)

Pantalla de visor a pantalla completa para diagramas Mermaid personalizados con zoom, pan y controles de navegación. Soporta cualquier tipo de diagrama Mermaid: flowchart, sequenceDiagram, gantt, classDiagram, erDiagram, etc.

---

## Sistema de IA: Cómo Genera el VSM

### Proceso de generación

1. **Recopilación**: El sistema recoge todas las FormResponse del proyecto, organizadas por departamento. Para cada respuesta, extrae las contestaciones usando las claves de pregunta (keys) y las etiquetas originales.

2. **Construcción del prompt**: Se crea un prompt de sistema que define al modelo como un experto en Lean/Six-Sigma VSM. El prompt incluye las reglas de generación, el formato de salida esperado (JSON estricto), definiciones de campos y los slugs de categorías disponibles. El prompt de usuario incluye el nombre del proyecto, su descripción y todas las respuestas formateadas.

3. **Llamada al LLM**: Se usa el SDK de OpenAI (compatible con OpenAI y Azure OpenAI) con los parámetros configurados en AIConfiguration (temperature, max_tokens, modelo).

4. **Parseo y validación**: La respuesta del LLM se parsea como JSON (eliminando markdown fences si existen). Se validan los slugs de categorías contra la base de datos.

5. **Resultado**: Se retorna un diccionario con name, description, steps (lista de pasos con métricas), analysis (razonamiento de la IA) y response_ids (IDs de las respuestas usadas).

### Sugerencias de mejora con IA

Además de generar el VSM, la IA puede analizar un mapa existente y generar sugerencias de mejora continua. Este proceso se activa desde el botón "Sugerir mejoras con IA" en la pantalla de visualización del VSM.

**Proceso de generación de sugerencias:**

1. **Recopilación de datos**: Se recogen todos los ProcessSteps del VSM con sus métricas (work_time, wait_time, loop_factor, loop_work_extra, num_people, flow_type), se calculan totales y porcentajes.

2. **Prompt especializado**: Se usa un prompt de sistema que define al modelo como un experto en Lean/Six-Sigma y mejora continua de procesos de software. El prompt de usuario incluye el nombre del proyecto, las métricas resumen del VSM, el detalle paso a paso, y el análisis previo de la IA (si existe).

3. **Estructura de las sugerencias**: La IA genera un análisis estructurado en 6 secciones:
   - **Cuellos de botella identificados**: pasos con mayores tiempos de trabajo o espera.
   - **Reducción de tiempos de espera**: propuestas para eliminar esperas entre pasos.
   - **Eliminación de retrabajo**: estrategias para reducir los factores de loop.
   - **Optimización del flujo**: oportunidades para cambiar push → pull o consolidar pasos.
   - **Quick wins**: mejoras implementables en 1-2 sprints con alto impacto.
   - **Mejoras a largo plazo**: cambios estratégicos con mayor esfuerzo pero reducción significativa del Lead Time.

4. **Persistencia**: Las sugerencias se guardan en el campo `ai_suggestions` del ValueStream y persisten entre sesiones. Se pueden regenerar pulsando el botón nuevamente (sobreescribe las anteriores).

5. **Renderizado**: Las sugerencias se muestran formateadas como HTML a partir del Markdown usando la librería `marked.js` en el cliente, lo que permite negritas, listas numeradas y encabezados bien formateados.

### Prompt del sistema

El prompt del sistema instruye a la IA para que:
- Identifique los pasos principales del proceso a partir de las respuestas.
- Ordene los pasos en el flujo lógico de trabajo (upstream → downstream).
- Use dos filas: row 0 para el flujo principal y row 1 para flujos paralelos.
- Mapee cada paso al departamento correcto usando su slug.
- Extraiga tiempos realistas de las métricas cuantitativas (sección G) y las tablas de la sección B.
- Identifique bucles de retrabajo desde las descripciones de pain points y waste.
- Incluya un campo "analysis" con su razonamiento detallado.

### Configuración de la IA

Se configura desde Admin → AI Configuration (modelo singleton). Soporta dos proveedores:

**OpenAI estándar**: Solo necesita api_key y model_name (ej: gpt-4o). El endpoint se usa por defecto.

**Azure OpenAI**: Necesita api_key, endpoint (https://TU-RECURSO.openai.azure.com/), model_name (nombre del deployment) y api_version (ej: 2024-06-01).

Parámetros comunes: temperature (0.0-1.0, recomendado 0.3 para consistencia), max_tokens (recomendado 4000), is_active (checkbox para activar/desactivar).

---

## Panel de Administración de Django

El panel admin de Django está completamente configurado para gestionar todos los aspectos de la aplicación. Tiene 9 secciones registradas:

### AI Configuration
- Modelo singleton: solo permite una instancia.
- El campo api_key usa un PasswordInput para ocultar la clave.
- Fieldsets organizados: configuración del proveedor y parámetros del modelo.

### Categories (Departamentos)
- Lista con columnas: name, slug, color, order.
- Slug autogenerado del nombre.
- Inline de Sections: permite crear secciones directamente desde la vista de categoría.

### Sections (Secciones)
- Filtrable por categoría.
- Inline de Questions: permite crear preguntas directamente desde la vista de sección.

### Questions (Preguntas)
- Filtrable por sección y tipo de pregunta.
- Muestra key, label, question_type, order.
- El campo options acepta JSON para checklist y table.

### Projects (Proyectos)
- Slug autogenerado del nombre.
- Lista con name, slug, color, created_at.

### Form Responses (Respuestas)
- Lista con category, project, respondent_name, respondent_role, submitted_at.
- El campo data es JSON de solo lectura.
- Filtrable por categoría y proyecto.

### Project Memberships (Membresías)
- Gestión de membresías de usuarios por proyecto.
- Aparece también como inline dentro de cada Project.
- Campos: proyecto, usuario, rol (viewer / editor / project_manager).

### Value Streams (VSMs)
- Slug autogenerado del nombre.
- Fieldsets: datos generales y sección colapsable de IA (ai_analysis, ai_suggestions, source_responses).
- ai_analysis y ai_suggestions son campos readonly (solo se generan desde la aplicación).
- Inline de ProcessSteps: permite crear pasos directamente.
- Muestra generation_method (Manual o AI Generated).

### Process Steps (Pasos)
- Lista con todas las métricas editables inline: order, row, name, work_time, wait_time, loop_factor.
- list_editable para order, row, work_time, wait_time (edición rápida desde la lista).
- Filtrable por value_stream y category.

### Diagrams (Diagramas)
- Campo mermaid_code para el código fuente del diagrama.
- Checkbox is_default para marcar el diagrama principal del proyecto.

---

## Carga de Datos: El Sistema de Fixtures

### questions_config.yaml

El archivo `vsm/fixtures/questions_config.yaml` contiene más de 200 preguntas organizadas en 7 categorías × 7 secciones. Es el "blueprint" de todos los cuestionarios.

Estructura del YAML:
```yaml
categories:
  - name: "Developers"
    slug: "developers"
    color: "#2563eb"
    order: 1
    description: "Backend & frontend development"
    sections:
      - code: "A"
        title: "Team Identity"
        order: 1
        questions:
          - key: "dev_a1"
            label: "Team name and main responsibility"
            type: "text"
            order: 1
          - key: "dev_a2"
            label: "Describe your team composition"
            type: "textarea"
            order: 2
      - code: "G"
        title: "VSM Metrics (for automated map generation)"
        order: 7
        questions:
          - key: "dev_g1_work_time"
            label: "Average work time in hours"
            type: "text"
            order: 1
          - key: "dev_g6_steps"
            label: "Feature Process Metrics"
            type: "table"
            options:
              columns: ["Step Name", "Avg Duration (hours)", ...]
            order: 6
```

### Comando load_questions

```bash
docker compose exec web python manage.py load_questions
```

Este comando lee el YAML y usa `update_or_create` para cada Category, Section y Question. Es **idempotente**: se puede ejecutar múltiples veces sin duplicar datos. Si se cambia el YAML, el comando actualiza los registros existentes que coincidan por key.

### Otros comandos de gestión

- `load_diagrams`: Carga diagramas Mermaid predefinidos.
- `load_vsm_seed`: Carga datos semilla de VSM para demostración.
- `load_test_data`: Carga datos de prueba completos.

---

## Internacionalización (i18n)

La aplicación soporta dos idiomas: inglés (por defecto) y español.

### Cómo funciona

- Todas las cadenas de texto en templates usan `{% trans "texto" %}` o `{% blocktrans %}`.
- Las traducciones están en `locale/es/LC_MESSAGES/django.po` (fuente editable) y `django.mo` (compilado).
- El selector de idioma está en la barra de navegación como un dropdown con banderas (🇪🇸 Español / 🇬🇧 English).
- El cambio de idioma usa el endpoint estándar de Django `set_language` con un formulario POST.
- Las URLs incluyen el prefijo de idioma: `/es/projects/`, `/en/projects/`.

### Para añadir traducciones

1. Marcar nuevas cadenas en templates con `{% trans %}`.
2. Ejecutar `python manage.py makemessages -l es`.
3. Editar `locale/es/LC_MESSAGES/django.po` con las traducciones.
4. Compilar: `python manage.py compilemessages`.
5. Reiniciar el contenedor Docker para que se carguen las nuevas traducciones.

---

## Contexto del Proyecto ATHINA

### La organización

ATHINA es un proyecto de desarrollo de software con múltiples equipos distribuidos. El proyecto tiene 4 entornos de despliegue en Azure:

| Entorno | Suscripción Azure | Región |
|---------|-------------------|--------|
| Development (dev) | az-intr-ath-dev01 | West Europe |
| Testing (test) | az-intr-ath-test01 | North Europe |
| UAT (uat) | az-intr-ath-uat01 | North Europe |
| Operations (ops) | az-intr-ath-ops01 | West Europe |

### Pipeline CI/CD actual

El pipeline de entrega actual sigue estos pasos:
```
Code Commit → Maven Build → Unit Tests → SonarQube Analysis → Docker Build
→ Qualys Security Scan → Push to ACR → Container App Deploy (Blue-Green)
→ Smoke Tests → Environment Promotion (dev → test → uat → acc → prd)
```

### Cadena de entrega entre equipos

La cadena de entrega sigue este flujo general:
1. El cliente final envía requisitos a Management.
2. Management prioriza con Agile/Scrum.
3. Agile refina el backlog y lo distribuye a los equipos de entrega.
4. Los equipos de entrega (Developers, QA, UX, Data) trabajan en paralelo.
5. DevOps/Platform provee infraestructura, pipelines y entornos a todos.
6. El Tech Lead (Felipe) revisa y coordina.
7. Management hace la revisión final.
8. Se entrega al cliente final.

### Relaciones cliente-proveedor entre equipos

| Equipo | Su cliente (a quién entrega) | Su proveedor (de quién recibe) |
|--------|------------------------------|-------------------------------|
| Management | Stakeholders / Cliente final | Todos los equipos |
| Agile / Scrum | Todos los equipos (backlog refinado) | Management, usuarios |
| Developers | Tech Lead | Agile (stories), UX (diseños), QA (defectos) |
| QA / Testing | Developers, Management | Developers (builds), Agile (criterios) |
| UX / Design | Developers, negocio | Negocio, usuarios |
| Data / Analytics | Negocio, Management | Developers (pipelines), negocio |
| DevOps / Platform | Todos los equipos | Developers, Management, Security |

---

## Instalación y Puesta en Marcha

### Requisitos previos

- Docker y Docker Compose instalados.
- (Opcional) API key de OpenAI o Azure OpenAI para generación con IA.

### Pasos de instalación

```bash
# 1. Navegar al directorio de la aplicación
cd docs/vsm/app

# 2. Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 3. Levantar los contenedores
docker compose up -d

# 4. Crear superusuario
docker compose exec web python manage.py createsuperuser

# 5. Cargar las preguntas predefinidas
docker compose exec web python manage.py load_questions

# 6. (Opcional) Cargar datos de ejemplo
docker compose exec web python manage.py load_test_data

# 7. Acceder a la aplicación
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

---

## Ejemplo Completo: De Cero a VSM

### Escenario: Mapear el proceso de entrega de features

**Paso 1**: Acceder a http://localhost:8000 y hacer clic en "Projects".

**Paso 2**: Crear un proyecto "Release 3.0 Analysis" con descripción "Análisis del flujo de entrega para la versión 3.0".

**Paso 3**: Dentro del proyecto, el equipo de Developers hace clic en su departamento y rellena el cuestionario. En la Sección G introduce: work_time=40, wait_time=8, rework_pct=20, people=3, flow=pull.

**Paso 4**: El equipo de QA hace lo mismo con sus datos: work_time=16, wait_time=4, rework_pct=15, people=2.

**Paso 5**: DevOps rellena su cuestionario: work_time=2, wait_time=2, rework_pct=10, people=1.

**Paso 6**: El líder del proyecto va a "Generate VSM with AI". Ve el resumen: 1 respuesta de Developers, 1 de QA, 1 de DevOps. Hace clic en "Generate".

**Paso 7**: La IA genera un VSM con 6-8 pasos: Requirements → Design → Development → Code Review → Testing → Deployment → Monitoring. Cada paso tiene métricas calculadas a partir de las respuestas.

**Paso 8**: El usuario revisa, y si está de acuerdo, guarda el VSM.

**Paso 9**: Accede a la visualización interactiva donde ve el lead time total, los cuellos de botella (pasos con más wait time) y los puntos de retrabajo (pasos con alto loop factor).

---

## Glosario Completo

| Término | Definición en ATHINA VSM |
|---------|--------------------------|
| **Category** | Departamento o equipo (Developers, QA, etc.) |
| **Section** | Sección del cuestionario (A-G) |
| **Question** | Pregunta individual con tipo y opciones |
| **Project** | Contenedor de análisis que agrupa todo |
| **FormResponse** | Respuesta completa de un cuestionario |
| **ValueStream** | El mapa de flujo de valor completo |
| **ProcessStep** | Un paso individual del mapa con métricas |
| **Diagram** | Diagrama Mermaid personalizado |
| **AIConfiguration** | Configuración de la IA (singleton) |
| **Key** | Identificador único de pregunta (ej: dev_a1) |
| **Slug** | Identificador URL-friendly autogenerado |
| **Work Time** | Tiempo de trabajo real (horas) |
| **Wait Time** | Tiempo de espera antes de un paso (horas) |
| **Loop Factor** | Probabilidad de retrabajo (0 a 1) |
| **Loop Work Extra** | Horas extra por ciclo de retrabajo |
| **Lead Time** | Tiempo total de punta a punta |
| **Push** | Trabajo asignado por un manager |
| **Pull** | Trabajo tomado de una cola por el equipo |
| **Row 0** | Flujo principal del mapa |
| **Row 1** | Flujo secundario o paralelo |
| **Mermaid** | Librería JavaScript para diagramas |
| **Fixture** | Datos predefinidos cargables con comandos Django |
| **ProjectMembership** | Vinculación usuario-proyecto con rol asignado |
| **Role (viewer)** | Rol con permisos solo de lectura sobre un proyecto |
| **Role (editor)** | Rol que permite rellenar y editar cuestionarios |
| **Role (project_manager)** | Rol que permite generar VSMs y solicitar sugerencias IA |
| **Role (admin)** | Superusuario Django con acceso total |
| **AI Suggestions** | Sugerencias de mejora generadas por IA basadas en métricas del VSM |
| **permissions.py** | Módulo de funciones auxiliares para verificación de permisos |
| **@login_required** | Decorador Django que protege vistas requiriendo autenticación |
| **marked.js** | Librería JavaScript para renderizar Markdown como HTML |

---

*Documento preparado para importar en NotebookLM — Proyecto ATHINA LOT1, DevSecOps Team*
*Cubre la totalidad de la aplicación ATHINA VSM: arquitectura, modelos, flujos de trabajo, interfaz, IA, autenticación, autorización por roles, sugerencias IA, administración e instalación.*
