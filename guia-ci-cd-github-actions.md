# Guía básica de CI/CD con GitHub Actions (Python)

> Objetivo: entender **dónde** vive un pipeline, **dónde** se ejecuta, **qué lenguaje** usa, **cómo** se estructura y **qué hace** cada paso. Con un ejemplo completo de CI en Python y un CD real que publica en GitHub Pages.

---

## Índice

1. [¿Qué es CI/CD?](#1-qué-es-cicd)
2. [Dónde se guarda](#2-dónde-se-guarda)
3. [Dónde se ejecuta](#3-dónde-se-ejecuta)
4. [Qué hace cada uno: CI vs CD](#4-qué-hace-cada-uno-ci-vs-cd)
5. [El lenguaje: YAML](#5-el-lenguaje-yaml)
6. [Estructura de un workflow](#6-estructura-de-un-workflow)
7. [El proyecto de ejemplo](#7-el-proyecto-de-ejemplo)
8. [Ejemplo de CI explicado parte por parte](#8-ejemplo-de-ci-explicado-parte-por-parte)
9. [CD con GitHub Pages](#9-cd-con-github-pages)
10. [Permisos, secrets y environments](#10-permisos-secrets-y-environments)
11. [Errores comunes](#11-errores-comunes)
12. [Glosario y siguientes pasos](#12-glosario-y-siguientes-pasos)

---

## 1. ¿Qué es CI/CD?

| Sigla | Significado | Idea en una frase |
|-------|-------------|-------------------|
| **CI** | Integración Continua | Cada vez que alguien sube código, se **verifica automáticamente** (instalar, lint, tests). |
| **CD** | Entrega / Despliegue Continuo | Si la verificación pasa, el código se **entrega o despliega automáticamente** a un entorno. |

Sin CI/CD el flujo es: "en mi máquina funciona" → subo → alguien lo prueba a mano → alguien lo despliega a mano.
Con CI/CD ese flujo lo hace un robot, **siempre igual**, en cada cambio.

```
 git push ──► CI (¿está bien el código?) ──► CD (publícalo / despliégalo)
```

**Delivery vs Deployment** (el segundo "CD" tiene dos sabores):

- **Continuous Delivery**: el código queda *listo* para desplegar, pero una persona aprueba con un botón.
- **Continuous Deployment**: se despliega solo, sin aprobación humana.

En la guía usaremos **Continuous Deployment**: cada merge a `main` con el CI en verde se publica solo en GitHub Pages. En la sección 10 verás cómo añadir una aprobación manual si algún día la necesitas.

---

## 2. Dónde se guarda

Los pipelines de GitHub Actions se llaman **workflows** y son **archivos dentro de tu propio repositorio**:

```
mi-proyecto/
├── .github/
│   └── workflows/
│       ├── ci.yml        ← pipeline de integración
│       └── cd.yml        ← pipeline de despliegue
├── app/
├── tests/
└── requirements.txt
```

Reglas importantes:

- La carpeta debe llamarse **exactamente** `.github/workflows/` (con el punto al inicio) y estar en la **raíz** del repo.
- Cada archivo `.yml` o `.yaml` ahí dentro es un workflow independiente. Puedes tener los que quieras.
- Como es código en el repo, **se versiona con git**: puedes hacer PRs, revisar cambios y volver atrás igual que con cualquier archivo.
- GitHub los detecta solo, no hay que "registrarlos" en ningún lado. Haces push y aparecen en la pestaña **Actions** del repositorio.
- Solo se ejecuta la versión del workflow que esté en la rama sobre la que ocurre el evento.

---

## 3. Dónde se ejecuta

Un workflow **no corre en tu computador ni en el servidor de tu app**. Corre en una máquina llamada **runner**.

### Runners alojados por GitHub (los de por defecto)

Cuando escribes `runs-on: ubuntu-latest`, GitHub:

1. Levanta una **máquina virtual nueva y limpia** (Ubuntu en este caso; también hay `windows-latest` y `macos-latest`).
2. Ejecuta ahí tus pasos.
3. **Destruye la máquina** al terminar.

Consecuencias que conviene tener claras:

- **Todo empieza desde cero** en cada ejecución: no hay tus librerías, ni tu código, ni nada. Por eso el primer paso casi siempre es `checkout` (descargar el repo) y luego instalar dependencias.
- **Nada persiste** entre ejecuciones (salvo que uses *cache* o *artifacts*).
- Es gratis dentro de ciertos minutos mensuales (en repos públicos es ilimitado; en privados hay una cuota según tu plan).

### Runners propios (self-hosted)

Puedes registrar tu propia máquina (un servidor, una VM, una Raspberry) con `runs-on: self-hosted`. Útil cuando necesitas acceso a una red privada o hardware especial, pero tú te encargas de mantenerla. Para empezar, olvídalo.

### Cuándo se ejecuta: los eventos (`on:`)

El workflow se dispara por **eventos**. Los más usados:

| Evento | Cuándo se dispara |
|--------|-------------------|
| `push` | Alguien sube commits a una rama |
| `pull_request` | Se abre o actualiza un PR |
| `workflow_dispatch` | Botón manual "Run workflow" en la pestaña Actions |
| `schedule` | Cron (ej: todos los días a las 3 AM) |
| `release` / tags | Cuando creas una release o subes un tag `v1.0.0` |
| `workflow_call` | Otro workflow lo invoca (reutilización) |

---

## 4. Qué hace cada uno: CI vs CD

| | **CI** | **CD** |
|---|--------|--------|
| **Pregunta que responde** | ¿Este código está sano? | ¿Cómo lo llevo a donde corre de verdad? |
| **Se dispara con** | Cada `push` y cada `pull_request` | Merge a `main`, un tag de versión o un botón manual |
| **Qué hace** | Instala dependencias, linter, tests, cobertura, build de prueba | Construye lo que se va a publicar, lo despliega y verifica que quedó vivo |
| **Resultado** | ✅ / ❌ en el commit o PR | Una versión corriendo en un entorno |
| **Si falla** | Se bloquea el merge | Se detiene el despliegue (o se hace rollback) |
| **Necesita credenciales** | Casi nunca | Depende del destino: con GitHub Pages no; con una VM o nube sí (claves, tokens) → se guardan como *secrets* |

**La conexión entre ambos:** el CD solo debería ejecutarse si el CI pasó. Nunca despliegues código que no pasó los tests.

---

## 5. El lenguaje: YAML

Los workflows se escriben en **YAML**. No es un lenguaje de programación: es un formato de **datos** (como JSON pero más legible). Describes *qué* quieres que pase; GitHub se encarga del *cómo*.

Lo mínimo que hay que saber de YAML:

```yaml
# Esto es un comentario

clave: valor                 # pares clave: valor (OJO al espacio después de los dos puntos)
texto: "con comillas"        # las comillas son opcionales casi siempre
numero: 3.12                 # cuidado: 3.10 se leería como 3.1 → escribe "3.10"
booleano: true

objeto:                      # la indentación (2 espacios) define la jerarquía
  hijo: 1
  otro_hijo: 2

lista:                       # las listas usan guion
  - uno
  - dos

lista_de_objetos:
  - name: Paso 1
    run: echo hola
  - name: Paso 2
    run: echo adios

script_multilinea: |         # el "|" conserva los saltos de línea
  echo linea 1
  echo linea 2
```

**Dos errores clásicos de YAML:**

1. Usar **tabulaciones** en lugar de espacios → error. Usa siempre espacios (2 por nivel).
2. Indentación inconsistente → el workflow no carga o hace algo distinto a lo que querías.

Dentro de los pasos `run:` escribes **comandos de shell normales** (bash en Linux), los mismos que escribirías en tu terminal.

---

## 6. Estructura de un workflow

Jerarquía, de lo más grande a lo más pequeño:

```
Workflow  (un archivo .yml)
 └── on:       qué eventos lo disparan
 └── jobs:     uno o varios trabajos
      └── job
           ├── runs-on:   en qué máquina corre
           ├── needs:     (opcional) de qué otro job depende
           └── steps:     lista ordenada de pasos
                └── step  →  `uses:` (una acción ya hecha)  ó  `run:` (un comando tuyo)
```

Conceptos clave:

- **Workflow**: el archivo completo.
- **Event (`on`)**: el disparador.
- **Job**: un grupo de pasos que corre **en una misma máquina**. Por defecto los jobs corren **en paralelo**, cada uno en su propia VM. Con `needs:` los encadenas.
- **Step**: una tarea individual, se ejecuta **en orden** dentro del job.
- **Action (`uses:`)**: un paso empaquetado y reutilizable hecho por GitHub o la comunidad (ej: `actions/checkout@v4`). Es como importar una librería.
- **`run:`**: un comando de shell que escribes tú.

Esqueleto vacío para tener en mente:

```yaml
name: Nombre visible en la pestaña Actions

on:
  push:
    branches: [main]

jobs:
  mi-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Decir hola
        run: echo "Hola desde el runner"
```

---

## 7. El proyecto de ejemplo

Un proyecto Python mínimo, pero con todo lo que un CI necesita: dependencias en `requirements.txt`, código, tests y un linter.

```
mi-proyecto/
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
├── app/
│   ├── __init__.py
│   └── calc.py
├── tests/
│   └── test_calc.py
├── scripts/
│   └── build_site.py     ← lo añadiremos en el CD (sección 9)
├── pytest.ini
└── requirements.txt
```

**`pytest.ini`** (le dice a pytest que busque tu código desde la raíz del proyecto)

```ini
[pytest]
pythonpath = .
testpaths = tests
```

**`requirements.txt`**

```txt
pytest==8.3.3
pytest-cov==5.0.0
ruff==0.7.0
```

**`app/__init__.py`**: vacío.

**`app/calc.py`**

```python
def sumar(a: float, b: float) -> float:
    return a + b


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

**`tests/test_calc.py`**

```python
import pytest

from app.calc import dividir, sumar


def test_sumar():
    assert sumar(2, 3) == 5


def test_dividir():
    assert dividir(10, 2) == 5


def test_dividir_entre_cero():
    with pytest.raises(ValueError):
        dividir(1, 0)
```

Esto mismo lo corres en tu máquina con `pip install -r requirements.txt`, `ruff check .` y `pytest`. **El CI es repetir exactamente eso, pero automáticamente y en una máquina limpia.**

---

## 8. Ejemplo de CI explicado parte por parte

Archivo: **`.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_call:          # permite que cd.yml reutilice este workflow

jobs:
  test:
    name: Lint y tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - name: Descargar el código
        uses: actions/checkout@v4

      - name: Instalar Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Linter (ruff)
        run: ruff check .

      - name: Correr tests con cobertura
        run: pytest --cov=app --cov-report=term-missing --cov-report=xml

      - name: Guardar reporte de cobertura
        if: matrix.python-version == '3.12'
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
```

### Parte por parte

#### `name: CI`
Nombre que verás en la pestaña **Actions** y en los checks de los PRs.

#### `on:` (el disparador)

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_call:
```

- Corre cuando hay **push a `main`**.
- Corre cuando se **abre/actualiza un PR hacia `main`** (esto es lo que te permite ver ✅/❌ *antes* de hacer merge).
- `workflow_call` lo deja "invocable" desde otro workflow; lo usaremos en el CD para no duplicar los tests.

#### `jobs:` → `test:`
Definimos un único job llamado `test`. `name:` es solo la etiqueta visible; `${{ ... }}` es la sintaxis de **expresiones** para insertar valores (aquí la versión de Python de la matriz).

#### `runs-on: ubuntu-latest`
La máquina virtual limpia donde se ejecuta todo.

#### `strategy.matrix` (probar en varias versiones)

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.11", "3.12"]
```

GitHub crea **una ejecución del job por cada valor**: una con Python 3.11 y otra con 3.12, en paralelo. Así compruebas que tu código funciona en ambas.
`fail-fast: false` evita que, si una falla, cancele las demás: así ves el resultado de todas.
Las versiones van entre comillas para que `3.10` no se convierta en `3.1`.

#### Steps (los pasos, en orden)

**1. `actions/checkout@v4`**: descarga el código del repo al runner. Sin esto, la máquina está vacía.

**2. `actions/setup-python@v5`**: instala la versión de Python pedida. El parámetro `cache: pip` guarda las librerías descargadas entre ejecuciones (usa el hash de `requirements.txt` como llave), así las siguientes corridas son más rápidas.

**3. Instalar dependencias** (aquí entra tu `requirements.txt`):

```yaml
run: |
  python -m pip install --upgrade pip
  pip install -r requirements.txt
```

El `|` permite varias líneas de shell en un mismo paso. Es literalmente lo que harías a mano.

**4. Linter**: `ruff check .` revisa estilo y errores obvios. Si encuentra problemas, devuelve código de salida distinto de 0.

**5. Tests con cobertura**: `pytest --cov=app ...` corre los tests y mide qué porcentaje de `app/` se ejecutó.

> **Regla de oro de Actions:** un paso **falla si su comando devuelve un código de salida distinto de 0**. Un test que falla, un linter que se queja o un `pip` que no encuentra un paquete → el paso se pone en ❌ → los pasos siguientes se saltan → el job falla → el commit/PR queda en rojo.

**6. Subir el reporte como artefacto**

```yaml
if: matrix.python-version == '3.12'
uses: actions/upload-artifact@v4
```

- `if:` ejecuta el paso solo si se cumple la condición (aquí, solo en la corrida de 3.12 para no subirlo dos veces).
- Un **artifact** es un archivo que sobrevive al runner: puedes descargarlo desde la pestaña Actions después de que la VM se destruyó.

### Qué ves cuando corre

1. Haces push o abres un PR.
2. Pestaña **Actions** → aparece la ejecución con un job por cada versión de Python.
3. Entras y ves el log de cada paso en tiempo real.
4. Resultado: ✅ verde o ❌ rojo, visible también en el PR.

### Bonus: obligar a que el CI pase antes de hacer merge

En GitHub: **Settings → Branches → Add branch protection rule** → rama `main` → activar **Require status checks to pass before merging** → elegir el check `Lint y tests`. Ahora nadie puede mezclar código roto.

---

## 9. CD con GitHub Pages

### 9.1 Por qué en Vercel o en local "no hace falta tanto"

Si has desplegado en local o en Vercel y no necesitaste escribir nada de esto, es porque **alguien más ya te daba el CD hecho**:

| Dónde desplegabas | Qué pasaba realmente |
|-------------------|----------------------|
| **Local** (`python app.py`, `npm run dev`) | Tú eres el pipeline. No hay empaquetado ni verificación. Funciona porque la máquina es la tuya y ya tiene todo instalado. |
| **Vercel / Netlify / Render** | Conectas el repo y *ellos* vigilan cada push, hacen el build, publican y te dan una URL. **Eso es CD**, solo que escondido en su plataforma. |
| **GitHub Pages con Actions** | Lo mismo que Vercel, pero **tú escribes el pipeline** y ves cada fase. Por eso es ideal para aprender CD sin complicarse: no hay servidores, ni SSH, ni secrets. |

Un CD tiene siempre las mismas fases, las veas o no:

```
1. DISPARO      ¿Cuándo despliego?            (merge a main, tag, botón manual)
2. VERIFICAR    ¿El código está sano?         (reusar el CI)
3. CONSTRUIR    Generar lo que se va a publicar (carpeta site/)
4. ENTREGAR     Subirlo al destino            (upload-pages-artifact)
5. ACTIVAR      Ponerlo en línea              (deploy-pages)
6. COMPROBAR    ¿Responde la URL?             (curl)
7. REVERTIR     Si algo sale mal, volver a una versión anterior
```

### 9.2 Qué es GitHub Pages y qué vamos a publicar

**GitHub Pages** es un hosting **gratuito de sitios estáticos** (HTML, CSS, JS, imágenes) que vive en una URL como:

```
https://<tu-usuario>.github.io/<nombre-del-repo>/
```

Ten presente sus límites, porque definen qué tiene sentido desplegar ahí:

- Es **estático**: no ejecuta Python en el servidor. Publica archivos ya generados.
- En repos públicos es gratis; en repos privados depende de tu plan.
- El sitio publicado es **público** (aunque el repo sea privado en planes que lo permiten, revisa la configuración de visibilidad).

Como nuestro proyecto es Python, el patrón natural es: **Python genera el sitio durante el CD y Pages lo publica**. En la guía publicaremos dos cosas:

1. Un **reporte de cobertura de tests** en HTML (lo genera `pytest-cov`).
2. Una **página principal** (`index.html`) que genera un script nuestro, con el commit y la fecha del despliegue.

Así el CD se conecta directamente con el CI: cada merge a `main` que pase los tests deja publicado su reporte en línea. Más adelante podrías cambiar ese contenido por documentación (MkDocs, Sphinx), un dashboard estático o cualquier sitio.

### 9.3 Configuración previa (una sola vez)

En GitHub: **Settings → Pages → Build and deployment → Source: `GitHub Actions`**.

Eso es todo. Al hacerlo, GitHub crea automáticamente un *environment* llamado `github-pages` que verás en **Settings → Environments**.

### 9.4 El script que genera el sitio

Añade **`scripts/build_site.py`**:

```python
"""Genera la página principal que se publicará en GitHub Pages."""

import os
from datetime import datetime, timezone
from pathlib import Path

SITE = Path("site")
SITE.mkdir(exist_ok=True)

sha = os.getenv("GITHUB_SHA", "local")[:7]
rama = os.getenv("GITHUB_REF_NAME", "local")
fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Mi proyecto</title>
</head>
<body>
  <h1>Mi proyecto</h1>
  <p>Desplegado automáticamente con GitHub Actions.</p>
  <ul>
    <li>Rama: <code>{rama}</code></li>
    <li>Commit: <code>{sha}</code></li>
    <li>Fecha: {fecha}</li>
  </ul>
  <p><a href="coverage/index.html">Ver reporte de cobertura</a></p>
</body>
</html>
"""

(SITE / "index.html").write_text(html, encoding="utf-8")
print(f"Sitio generado en {SITE}/index.html (commit {sha})")
```

Qué hace: crea la carpeta `site/` y escribe un `index.html` con los datos del despliegue. `GITHUB_SHA` y `GITHUB_REF_NAME` son variables que GitHub inyecta solo en el runner; en tu máquina valen `local`.

La estructura final de lo que se publica será:

```
site/
├── index.html          ← lo genera scripts/build_site.py
└── coverage/           ← lo genera pytest --cov-report=html:site/coverage
    └── index.html
```

### 9.5 El workflow de CD

Archivo: **`.github/workflows/cd.yml`**

```yaml
name: CD

on:
  push:
    branches: [main]      # cada merge a main intenta desplegar
  workflow_dispatch:      # o manualmente desde la pestaña Actions

# Permisos mínimos que necesita Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Evita dos despliegues simultáneos
concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  # 1) Reutilizamos el CI completo: si falla, no se despliega nada
  ci:
    uses: ./.github/workflows/ci.yml

  # 2) Construir el sitio
  build:
    needs: ci
    runs-on: ubuntu-latest
    steps:
      - name: Descargar el código
        uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Generar reporte de cobertura (HTML)
        run: pytest --cov=app --cov-report=html:site/coverage

      - name: Generar página principal
        run: python scripts/build_site.py

      - name: Configurar Pages
        uses: actions/configure-pages@v5

      - name: Empaquetar el sitio
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  # 3) Publicar
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Publicar en GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

      - name: Comprobar que el sitio responde
        run: |
          curl --fail --silent --show-error \
               --retry 5 --retry-delay 5 --retry-all-errors \
               "${{ steps.deployment.outputs.page_url }}" > /dev/null
          echo "El sitio responde en ${{ steps.deployment.outputs.page_url }}"
```

### 9.6 Explicación parte por parte

**`on: push: branches: [main]`**
El CI corre en cada push y PR; el CD solo cuando el código **llega a `main`** (normalmente al hacer merge de un PR). Así el flujo queda: PR → CI en verde → merge → CD publica. `workflow_dispatch` añade el botón manual **Run workflow**, útil para republicar sin cambiar código.

**`permissions:`**
Cada ejecución recibe un token temporal (`GITHUB_TOKEN`). Aquí le decimos exactamente qué puede hacer:

| Permiso | Para qué |
|---------|----------|
| `contents: read` | Leer el código del repo (checkout) |
| `pages: write` | Publicar en Pages |
| `id-token: write` | Que `deploy-pages` verifique que el despliegue viene de este workflow (OIDC) |

Es el **principio de mínimo privilegio**: el pipeline solo puede lo imprescindible. Y fíjate que **no hay ningún secret**: GitHub ya conoce tu repo y Pages, así que la autenticación es automática. Esa es la razón principal por la que Pages es el mejor primer CD.

**`concurrency`**
Si haces dos merges seguidos, no queremos dos despliegues pisándose. Con `group: pages` se encolan. `cancel-in-progress: false` deja terminar el que está en curso en vez de cancelarlo a medias.

**Job `ci` con `uses: ./.github/workflows/ci.yml`**
Llama al workflow de CI completo como un bloque reutilizable (por eso le dejamos `workflow_call` en la sección 8). **Si el CI falla, `needs: ci` impide que `build` y `deploy` corran.** Esta es la conexión CI → CD: nunca se publica código que no pasó los tests.

> Nota: en un push a `main` el CI corre dos veces (la suya propia y la que invoca el CD). Para empezar es inocuo; más adelante puedes quitar `push` del `ci.yml` y dejar el CI solo para PRs.

**Job `build` (construir)**
Es el mismo patrón del CI (checkout → Python → dependencias) pero con un objetivo distinto: en vez de *verificar*, *producir* algo:

1. `pytest --cov-report=html:site/coverage` genera el reporte navegable dentro de `site/coverage/`.
2. `python scripts/build_site.py` crea `site/index.html`.
3. `configure-pages` prepara los metadatos que Pages necesita.
4. `upload-pages-artifact` toma la carpeta `site/` y la empaqueta como un **artifact** especial de Pages.

**Por qué `build` y `deploy` son jobs separados:** cada job corre en una VM distinta y limpia. Lo construido en `build` solo llega a `deploy` a través del artifact. Además, separar permite que *solo* el job `deploy` quede asociado al environment y a sus reglas de protección.

**Job `deploy` (publicar)**

```yaml
environment:
  name: github-pages
  url: ${{ steps.deployment.outputs.page_url }}
```

- `environment: github-pages` registra el despliegue en la pestaña **Deployments** del repo, con su historial.
- `url:` muestra un botón "View deployment" en la ejecución, apuntando al sitio publicado.
- `actions/deploy-pages@v4` toma el artifact y lo pone en línea. Devuelve `page_url` como *output*, y por eso el paso lleva `id: deployment`, para que otros pasos puedan leerlo con `steps.deployment.outputs.page_url`.

**Paso "Comprobar que el sitio responde"**
Es la fase de verificación post-despliegue (el *health check*). `curl --fail` devuelve error si la respuesta no es 2xx, y `--retry` da unos segundos por si Pages tarda en propagar. Si falla, el job queda en rojo y te enteras de que algo pasó, en vez de descubrirlo cuando alguien te avise.

### 9.7 Probarlo en tu máquina antes de subirlo

Todo lo que el CD hace en `build` lo puedes reproducir en local:

```bash
pip install -r requirements.txt
pytest --cov=app --cov-report=html:site/coverage
python scripts/build_site.py
python -m http.server 8000 --directory site
```

Abre `http://localhost:8000` y verás exactamente lo que se publicará. Si funciona aquí, funcionará en el runner: es el mismo comando.

### 9.8 Primer despliegue paso a paso

1. Sube el proyecto a GitHub con `ci.yml` y `cd.yml` en `.github/workflows/`.
2. Activa **Settings → Pages → Source: GitHub Actions**.
3. Haz push a `main` (o usa **Actions → CD → Run workflow**).
4. Entra a la pestaña **Actions** y observa la cadena `ci → build → deploy`.
5. Al terminar, en el job `deploy` aparece la URL. Ábrela: ese es tu sitio en línea.
6. **Rompe algo a propósito**: cambia un test para que falle, haz push y comprueba que el CD **no despliega** y el sitio sigue mostrando la versión anterior. Eso es CI/CD funcionando.

### 9.9 Revertir (rollback)

Pages publica lo que le entregó el último despliegue exitoso. Para volver atrás tienes dos opciones:

- **Revertir el commit** (`git revert <sha>` y push a `main`): el CD vuelve a correr y publica el estado anterior. Es la forma limpia y deja rastro en el historial.
- **Re-ejecutar un despliegue antiguo**: en **Actions**, abre la ejecución exitosa anterior y pulsa **Re-run all jobs**.

### 9.10 Siguientes variantes del mismo patrón

La estructura del workflow no cambia; solo cambia **qué se construye** y **a dónde se entrega**:

| Quiero publicar... | Cambia la fase "construir" por... |
|--------------------|-----------------------------------|
| Documentación del proyecto | `pip install mkdocs` + `mkdocs build -d site` |
| Un sitio estático generado con Python | Tu script que escribe en `site/` (Pelican, Jinja2, etc.) |
| Un reporte o dashboard de datos | Un script que lee datos y escribe HTML en `site/` |

Y cuando quieras salir de Pages hacia una nube real, cambia la fase "entregar":

| Destino | Entrega con... |
|---------|----------------|
| VM / VPS | `scp` + `ssh` + reiniciar el servicio (credenciales en *secrets*) |
| Docker | `docker build` + `docker push` a un registry (GHCR, Docker Hub) |
| AWS / GCP / Azure | Acciones oficiales de cada proveedor (`configure-aws-credentials`, `deploy-cloudrun`, `azure/webapps-deploy`...) |
| Vercel | `vercel deploy --prod --token ${{ secrets.VERCEL_TOKEN }}` |

---

## 10. Permisos, secrets y environments

El CD de Pages no necesitó ningún secret, pero en cuanto despliegues a otro lugar los necesitarás. Conviene entender las tres piezas.

### Permisos (`permissions:`)

Controlan lo que el `GITHUB_TOKEN` automático puede hacer en tu repo. Declara siempre el mínimo necesario, como hicimos en el CD. Puedes ponerlos a nivel de workflow (como arriba) o de job.

### Secrets y variables

Nunca escribas contraseñas, tokens ni llaves dentro del YAML (el repo puede ser leído por mucha gente y queda en el historial de git).

**Dónde se crean:** *Settings → Secrets and variables → Actions* (para todo el repo) o dentro de un *Environment* (solo para ese entorno).

**Cómo se usan:**

```yaml
- name: Desplegar
  env:
    TOKEN: ${{ secrets.MI_TOKEN }}
    HOST: ${{ vars.SERVER_HOST }}          # vars = no secretos (visibles)
  run: ./mi-script-de-despliegue.sh
```

| Tipo | Se usa para | Visible en logs |
|------|-------------|-----------------|
| `secrets.X` | Tokens, llaves, contraseñas | No (GitHub lo enmascara como `***`) |
| `vars.X` | Configuración no sensible (URLs, nombres) | Sí |
| `github.*` / `GITHUB_*` | Datos del evento (rama, tag, autor, SHA) | Sí |

### Environments

Un *environment* es un destino con nombre (`github-pages`, `staging`, `production`...) que ofrece:

1. **Reglas de protección**: por ejemplo, *Required reviewers* para que una persona apruebe antes de desplegar, o limitar qué ramas pueden desplegar (para `github-pages` suele venir restringido a `main`).
2. **Secrets propios** por entorno (la clave de staging no sirve para producción).
3. **Historial de despliegues** en la pestaña *Deployments*.

Si más adelante quieres un flujo con aprobación, basta con añadir *Required reviewers* al environment: el job `deploy` quedará en pausa hasta que alguien pulse **Approve**. Eso convierte tu *Continuous Deployment* en *Continuous Delivery*.

Buenas prácticas:

- Usa **un secret distinto por entorno** y con los **mínimos permisos**.
- Los workflows de un PR que viene de un *fork* **no reciben secrets** (es una protección intencional).

---

## 11. Errores comunes

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| El workflow no aparece en Actions | Carpeta mal nombrada o no está en la rama correcta | Debe ser `.github/workflows/` en la raíz y estar en la rama que disparó el evento |
| "Invalid workflow file" | Error de indentación o tabulaciones | Revisa los espacios; valida el YAML en un editor con soporte YAML |
| `No such file: requirements.txt` | Olvidaste `actions/checkout` | Siempre `checkout` como primer paso |
| `ModuleNotFoundError: app` en los tests | Python no encuentra tu paquete | Crea `pytest.ini` con `pythonpath = .` (sección 7), ejecuta desde la raíz y asegúrate de tener `app/__init__.py` |
| Funciona en local pero falla en CI | Versiones distintas o dependencias sin fijar | Fija versiones en `requirements.txt` (`paquete==x.y.z`) |
| El deploy falla con "Pages not enabled" o error 404 | Pages no está activado con Actions como fuente | **Settings → Pages → Source: GitHub Actions** |
| Python `3.10` se instala como `3.1` | Número sin comillas en YAML | Escribe `"3.10"` |
| `deploy` falla por permisos (`Resource not accessible by integration`) | Faltan `pages: write` o `id-token: write` | Decláralos en `permissions:` del `cd.yml` |
| El sitio se publica pero muestra la versión vieja | Caché del navegador o despliegue aún propagándose | Espera unos segundos y recarga con Ctrl+Shift+R; confirma en Actions que el deploy terminó |
| La página principal carga pero los estilos o enlaces rotos | Rutas absolutas (`/coverage/...`) en un sitio que vive en `/<repo>/` | Usa rutas relativas (`coverage/index.html`) |
| El CD no se dispara al hacer merge | El workflow no está en `main` o la rama no es `main` | Verifica `on.push.branches` y que `cd.yml` exista en esa rama |
| Un paso en rojo pero "no veo el error" | El log del paso está colapsado | Expande el paso; para depurar añade `run: env` o `run: ls -la` temporalmente |

---

## 12. Glosario y siguientes pasos

**Glosario rápido**

- **Workflow**: archivo YAML con un pipeline completo.
- **Event**: lo que dispara el workflow (`push`, `pull_request`, tag...).
- **Job**: conjunto de pasos que corre en una misma máquina.
- **Step**: una tarea individual (`uses:` o `run:`).
- **Action**: paso reutilizable de terceros (`actions/checkout`).
- **Runner**: la máquina que ejecuta el job.
- **Artifact**: archivo que persiste después de que termina el job.
- **Cache**: datos reutilizables entre ejecuciones (dependencias).
- **Matrix**: ejecutar el mismo job con varias combinaciones (versiones, sistemas).
- **Environment**: destino de despliegue con reglas, secrets y aprobaciones propias.
- **Secret**: valor cifrado e inyectado en tiempo de ejecución.
- **GitHub Pages**: hosting estático gratuito de GitHub; publica una carpeta de archivos HTML/CSS/JS.
- **Health check**: verificación automática de que lo desplegado está vivo.
- **Rollback**: volver a la versión anterior si algo sale mal.

**Orden sugerido para practicar**

1. Crea un repo con el proyecto de ejemplo y sube **solo `ci.yml`**. Mira la pestaña Actions. Rompe un test a propósito y observa el ❌.
2. Activa la **protección de rama** para exigir el CI antes de hacer merge.
3. Agrega `scripts/build_site.py` y **pruébalo en local** (sección 9.7).
4. Activa **Settings → Pages → Source: GitHub Actions**, sube `cd.yml` y haz merge a `main`. Abre la URL publicada.
5. Rompe un test a propósito y comprueba que el CD **no despliega**. Luego revierte el commit para practicar el rollback.
6. Cuando te sientas cómodo, cambia el contenido de `site/` por documentación (MkDocs) o prueba otro destino (VM por SSH, Docker, Vercel desde Actions).

**Para seguir aprendiendo**

- Documentación oficial: <https://docs.github.com/es/actions>
- Marketplace de actions: <https://github.com/marketplace?type=actions>
- Probar workflows en local: [`act`](https://github.com/nektos/act)

---

*Resumen de una línea:* **CI = "¿está sano el código?" en cada cambio; CD = "construye lo que se publica, llévalo a donde vive y verifica que funciona", todo descrito en archivos YAML dentro de `.github/workflows/` y ejecutado en máquinas temporales de GitHub.**
