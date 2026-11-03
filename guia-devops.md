# 🛠️ Guía DevOps — Clase de Git: merge, rebase y resolución de conflictos

> **Tu rol:** eres el dueño de `main`. Los programadores (Dev1 y Dev2) trabajan en ramas; tú **integras** su trabajo, resuelves los conflictos que lleguen a `main` y mantienes el repositorio ordenado.
>
> **Proyecto:** *Mini Utilidades*, un programa pequeño en Python. Nadie necesita saber Python a fondo: lo importante es el flujo de Git.

---

## 📌 Cómo leer esta guía

Cada paso tiene este formato:

- **🎯 Qué vamos a hacer** — la idea.
- **⌨️ Comando** — lo que escribes.
- **👀 Qué deberías ver** — salida aproximada de la terminal.
- **💡 Por qué** — el concepto detrás.

> ⚠️ **Los hashes cambian.** Los códigos como `5a59c61` serán distintos en tu máquina. Lo importante es la *forma* de la salida, no los números.

### 🚦 Puntos de encuentro

Los tres roles trabajan al mismo tiempo, así que hay **puntos de encuentro** numerados. Cuando llegues a uno, **avisa en voz alta** (o en el chat) y **espera** el aviso que dice la guía antes de continuar. Los números son los mismos en las tres guías.

| Punto | Qué pasó |
|---|---|
| **PE-1** | DevOps publicó `main` |
| **PE-2** | Dev1 y Dev2 subieron sus ramas de la Parte 1 |
| **PE-3** | DevOps hizo el merge de la Parte 1 |
| **PE-4** | Dev1 y Dev2 subieron sus ramas de la Parte 2 |
| **PE-5** | DevOps resolvió el conflicto de la Parte 2 |
| **PE-6** | DevOps subió la rama compartida `feature/validaciones` |
| **PE-7** | Dev2 hizo `push` (Ronda A) |
| **PE-8** | Dev1 resolvió el conflicto y subió |
| **PE-9** | Dev1 hizo `push` primero (Ronda B) |
| **PE-10** | Dev2 resolvió con rebase y subió, y DevOps integró la rama en `main` |
| **PE-11** | Dev1 y Dev2 subieron sus ramas de la Parte 4 |
| **PE-12** | DevOps cambió `main` (¡los devs deben actualizarse!) |
| **PE-13** | Dev1 y Dev2 actualizaron sus ramas y subieron |

---

## 🧰 Parte 0 — Preparación (solo DevOps)

### 0.1 Verifica que Git esté instalado

🎯 Confirmar que tienes Git.

```bash
git --version
```

👀 Deberías ver algo como:

```
git version 2.43.0
```

### 0.2 Configura tu identidad

🎯 Cada commit lleva el nombre y correo de quien lo hizo. Sin esto, Git se queja.

```bash
git config --global user.name "DevOps"
git config --global user.email "devops@clase.com"
git config --global init.defaultBranch main
git config --global pull.ff only
git config --global core.editor "nano"
```

💡 **Por qué:**
- `init.defaultBranch main` → las ramas nuevas se llamarán `main` y no `master`.
- `pull.ff only` → `git pull` **se negará** a crear merges sorpresa. Solo avanza si es "limpio". Así aprendemos a decidir nosotros qué hacer.
- `core.editor "nano"` → si Git abre un editor (por ejemplo para un mensaje de merge), será `nano` y no `vim` (del que cuesta salir 😅). En nano: `Ctrl+O`, `Enter` para guardar y `Ctrl+X` para salir. *(Si usas VS Code: `"code --wait"`.)*

Verifica:

```bash
git config --global --list
```

👀 Debes ver tus valores `user.name`, `user.email`, etc.

> 🪟 **Windows:** puede aparecer `warning: LF will be replaced by CRLF`. Es inofensivo; ignóralo.

### 0.3 Clona el repositorio vacío

🎯 Traer a tu computador el repositorio que creó el profesor.

```bash
git clone <URL-DEL-REPO> clase-git
cd clase-git
```

👀 Como está vacío, verás una advertencia (es normal):

```
Cloning into 'clase-git'...
warning: You appear to have cloned an empty repository.
```

### 0.4 Crea los archivos iniciales

🎯 Tres archivos base: `README.md`, `main.py` y `.gitignore`.

**`README.md`**

```markdown
# Mini Utilidades

Proyecto de práctica para aprender Git en equipo.
```

**`main.py`**

```python
"""Programa principal de Mini Utilidades."""


def main():
    print("Bienvenido a Mini Utilidades")


if __name__ == "__main__":
    main()
```

**`.gitignore`**

```
__pycache__/
*.pyc
.venv/
.vscode/
```

Verifica que funciona:

```bash
python main.py
```

👀 `Bienvenido a Mini Utilidades`

> Si `python` no funciona, prueba con `python3`.

### 0.5 Mira el estado

```bash
git status
```

👀

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	README.md
	main.py

nothing added to commit but untracked files present (use "git add" to track)
```

💡 *Untracked* = Git ve los archivos pero aún no los sigue.

### 0.6 Primer commit y primer push

```bash
git add .
git commit -m "Commit inicial: estructura base del proyecto"
```

👀

```
[main (root-commit) eba20f0] Commit inicial: estructura base del proyecto
 3 files changed, 16 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 main.py
```

Asegúrate de que la rama se llame `main` y súbela:

```bash
git branch -M main
git push -u origin main
```

👀

```
To https://github.com/<usuario>/clase-git.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

💡 `-u` (upstream) enlaza tu `main` local con `origin/main`. Gracias a eso, luego `git status` te dice si vas adelante o atrás del remoto.

### 0.7 Invita a los programadores

En GitHub: **Settings → Collaborators → Add people** y agrega a Dev1 y Dev2. Compárteles la URL del repo.

### 🚦 PE-1 — «`main` ya está publicado»

**Avisa a Dev1 y Dev2.** Ellos pueden clonar. Mientras tanto, espera el **PE-2**.

---

## 🌱 Parte 1 — Dos ramas, archivos distintos (merge sencillo)

**Situación:** Dev1 crea `matematicas.py` en `feature/matematicas`. Dev2 crea `textos.py` en `feature/textos`. No se tocan entre sí → no habrá conflictos.

### 🚦 Espera el PE-2 («subimos nuestras ramas»)

### 1.1 Trae los metadatos del remoto con `fetch`

🎯 Descargar **información** de lo que hay en GitHub **sin modificar tu trabajo**.

```bash
git fetch
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/matematicas -> origin/feature/matematicas
 * [new branch]      feature/textos      -> origin/feature/textos
```

💡 **`fetch` vs `pull`** (¡el concepto más importante de la clase!):

| Comando | Qué hace | ¿Toca tus archivos? |
|---|---|---|
| `git fetch` | Descarga commits y ramas del remoto a las ramas `origin/*` | ❌ **No** |
| `git pull` | `fetch` **+** `merge` en tu rama actual | ✅ Sí (y puede dar conflictos) |

`fetch` es seguro: primero **miras**, luego **decides**.

### 1.2 Mira las ramas

```bash
git branch
```

👀 Solo tu rama local:

```
* main
```

```bash
git branch -a
```

👀 Ahora aparecen las remotas (`remotes/origin/...`):

```
* main
  remotes/origin/feature/matematicas
  remotes/origin/feature/textos
  remotes/origin/main
```

```bash
git branch -r -v
```

👀

```
  origin/feature/matematicas 5a59c61 Agrega funciones suma y resta
  origin/feature/textos      ab7e453 Agrega funciones mayusculas e invertir
  origin/main                eba20f0 Commit inicial: estructura base del proyecto
```

### 1.3 Inspecciona antes de integrar

🎯 ¿Qué trae cada rama que `main` no tiene?

```bash
git log --oneline main..origin/feature/matematicas
```

👀

```
5a59c61 Agrega funciones suma y resta
```

💡 La notación **`A..B`** significa: *«commits que están en B pero no en A»*.

```bash
git diff --stat main origin/feature/matematicas
git diff --name-status main origin/feature/textos
```

👀

```
 matematicas.py | 9 +++++++++
 1 file changed, 9 insertions(+)
A	textos.py
```

💡 `A` = archivo **añadido**. Otros códigos: `M` modificado, `D` eliminado.

### 1.4 Crea ramas locales a partir de las remotas

🎯 Tener una copia local de cada rama remota para poder revisarla.

**Forma corta** (Git detecta que existe `origin/feature/matematicas`):

```bash
git switch feature/matematicas
```

👀

```
branch 'feature/matematicas' set up to track 'origin/feature/matematicas'.
Switched to a new branch 'feature/matematicas'
```

**Forma explícita** (haz esta con la otra rama):

```bash
git switch -c feature/textos --track origin/feature/textos
```

👀

```
branch 'feature/textos' set up to track 'origin/feature/textos'.
Switched to a new branch 'feature/textos'
```

> 📜 **Forma antigua** (verás esto en tutoriales): `git checkout -b feature/textos origin/feature/textos`. Hace lo mismo.

Vuelve a `main` y revisa el mapa:

```bash
git switch main
git branch -vv
```

👀

```
  feature/matematicas 5a59c61 [origin/feature/matematicas] Agrega funciones suma y resta
  feature/textos      ab7e453 [origin/feature/textos] Agrega funciones mayusculas e invertir
* main                eba20f0 [origin/main] Commit inicial: estructura base del proyecto
```

💡 Lo que está entre corchetes es la rama remota que sigue cada local.

### 1.5 Haz el merge de las dos ramas en `main`

🎯 Integrar el trabajo de ambos. Estás parado en `main`.

```bash
git merge --no-ff feature/matematicas -m "Merge feature/matematicas en main"
```

👀

```
Merge made by the 'ort' strategy.
 matematicas.py | 9 +++++++++
 1 file changed, 9 insertions(+)
 create mode 100644 matematicas.py
```

```bash
git merge --no-ff feature/textos -m "Merge feature/textos en main"
```

👀

```
Merge made by the 'ort' strategy.
 textos.py | 9 +++++++++
 1 file changed, 9 insertions(+)
 create mode 100644 textos.py
```

💡 **¿Qué es `--no-ff`?**

Como `main` no avanzó desde que Dev1 creó su rama, Git podría hacer un **fast-forward**: simplemente mover el puntero de `main` hacia adelante, sin dejar rastro de que existió una rama. Con `--no-ff` (*no fast-forward*) obligamos a Git a crear un **commit de merge**, así el historial muestra claramente qué se integró y cuándo.

Y `-m "..."` pone el mensaje directamente, para que no se abra ningún editor.

### 1.6 Mira el historial como grafo

```bash
git log --oneline --graph --decorate --all
```

👀

```
*   6fe928b (HEAD -> main) Merge feature/textos en main
|\
| * ab7e453 (origin/feature/textos, feature/textos) Agrega funciones mayusculas e invertir
* |   9bc3675 Merge feature/matematicas en main
|\ \
| |/
|/|
| * 5a59c61 (origin/feature/matematicas, feature/matematicas) Agrega funciones suma y resta
|/
* eba20f0 (origin/main) Commit inicial: estructura base del proyecto
```

💡 Cada `*` es un commit. Las líneas `|\` y `|/` muestran dónde se **separó** y dónde se **unió** el trabajo. Los nombres entre paréntesis son punteros (ramas) apuntando a ese commit.

Prueba que todo funciona y sube:

```bash
ls
git status
git push origin main
```

👀

```
README.md  main.py  matematicas.py  textos.py

On branch main
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean

To https://github.com/<usuario>/clase-git.git
   eba20f0..6fe928b  main -> main
```

💡 "Ahead by 4 commits" = 2 commits de los devs + 2 commits de merge.

### 🚦 PE-3 — «`main` ya tiene la Parte 1»

**Avisa a los devs.** Espera el **PE-4**.

---

## ⚔️ Parte 2 — Dos ramas, el mismo archivo (conflicto en `main`)

**Situación:** Dev1 (`feature/menu-matematicas`) y Dev2 (`feature/menu-textos`) editaron **las mismas líneas de `main.py`**. El primer merge entrará limpio; el segundo **chocará** y tú lo resolverás.

### 🚦 Espera el PE-4 («subimos las ramas de la Parte 2»)

### 2.1 Trae e inspecciona

```bash
git fetch
git branch -r
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/menu-matematicas -> origin/feature/menu-matematicas
 * [new branch]      feature/menu-textos      -> origin/feature/menu-textos

  origin/feature/matematicas
  origin/feature/menu-matematicas
  origin/feature/menu-textos
  origin/feature/textos
  origin/main
```

Mira qué hace cada rama sobre `main.py`:

```bash
git diff main origin/feature/menu-matematicas -- main.py
git diff main origin/feature/menu-textos -- main.py
```

💡 Los dos tocan **las mismas zonas** del archivo: ya puedes predecir el conflicto. Esa es la ventaja de hacer `fetch` primero.

### 2.2 Primer merge (entra limpio)

```bash
git switch main
git merge --no-ff origin/feature/menu-matematicas -m "Merge feature/menu-matematicas en main"
```

👀

```
Merge made by the 'ort' strategy.
 main.py | 4 ++++
 1 file changed, 4 insertions(+)
```

💡 Puedes hacer merge directamente de `origin/<rama>`, sin crear una rama local.

### 2.3 Segundo merge (¡conflicto!)

```bash
git merge --no-ff origin/feature/menu-textos -m "Merge feature/menu-textos en main"
```

👀

```
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts and then commit the result.
```

🎉 **¡Perfecto, esto es lo que queríamos ver!** No es un error: Git te dice «dos personas cambiaron lo mismo y no sé cuál elegir; decide tú».

### 2.4 Diagnostica

```bash
git status
```

👀

```
On branch main
Your branch is ahead of 'origin/main' by 2 commits.

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   main.py

no changes added to commit (use "git add" and/or "git commit -a")
```

💡 Lee las pistas: `both modified: main.py` te dice **qué archivo**; y `git merge --abort` es tu **salida de emergencia** para volver a antes del merge.

Lista solo los archivos en conflicto y los commits involucrados:

```bash
git diff --name-only --diff-filter=U
git log --oneline --merge
```

👀

```
main.py
f687312 Agrega demo de textos al programa principal
c16366d Agrega demo de matemáticas al programa principal
```

### 2.5 Abre `main.py` y entiende los marcadores

```python
"""Programa principal de Mini Utilidades."""

<<<<<<< HEAD
from matematicas import suma, resta
=======
from textos import mayusculas, invertir
>>>>>>> origin/feature/menu-textos


def main():
    print("Bienvenido a Mini Utilidades")
<<<<<<< HEAD
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
=======
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
>>>>>>> origin/feature/menu-textos


if __name__ == "__main__":
    main()
```

💡 **Cómo se lee un conflicto:**

```
<<<<<<< HEAD
   ... lo que hay en TU rama actual (main) ...
=======
   ... lo que viene de la rama que estás integrando ...
>>>>>>> origin/feature/menu-textos
```

Hay **dos conflictos** (dos bloques) en este archivo: los imports y el cuerpo de `main()`.

### 2.6 Resuelve: conserva lo de ambos

🎯 Decidir el resultado final. Aquí queremos **las dos cosas**. Borra **todos** los marcadores (`<<<<<<<`, `=======`, `>>>>>>>`) y deja:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta
from textos import mayusculas, invertir


def main():
    print("Bienvenido a Mini Utilidades")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))


if __name__ == "__main__":
    main()
```

> ⚠️ **Error clásico:** dejar un `<<<<<<<` olvidado. Python lanzará `SyntaxError`. Por eso **siempre se ejecuta el programa** antes de confirmar.

> 🛠️ **Con VS Code** verás botones sobre cada conflicto: *Accept Current Change*, *Accept Incoming Change*, *Accept Both Changes*. Útiles, pero revisa el resultado a mano.

Prueba:

```bash
python main.py
```

👀

```
Bienvenido a Mini Utilidades
Suma de 2 + 3 = 5
Resta de 5 - 1 = 4
En mayúsculas: HOLA
Invertido: aloh
```

### 2.7 Marca como resuelto y confirma

```bash
git add main.py
git status
```

👀

```
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   main.py
```

```bash
git commit -m "Merge feature/menu-textos en main (conflicto resuelto en main.py)"
git push origin main
git log --oneline --graph --decorate -6
```

👀

```
[main f7b4b30] Merge feature/menu-textos en main (conflicto resuelto en main.py)

To https://github.com/<usuario>/clase-git.git
   6fe928b..f7b4b30  main -> main

*   f7b4b30 (HEAD -> main, origin/main) Merge feature/menu-textos en main (conflicto resuelto en main.py)
|\
| * f687312 (origin/feature/menu-textos) Agrega demo de textos al programa principal
* |   e8d576c Merge feature/menu-matematicas en main
|\ \
| |/
|/|
| * c16366d (origin/feature/menu-matematicas) Agrega demo de matemáticas al programa principal
|/
*   6fe928b Merge feature/textos en main
```

💡 **El ciclo de un conflicto:** `merge` → conflicto → editar → **`add`** → **`commit`**. El `add` es tu forma de decirle a Git «este archivo ya está arreglado».

### 🚦 PE-5 — «Conflicto resuelto, `main` actualizado»

**Avisa a los devs.** Ellos mirarán el historial. Pasa a la Parte 3.

---

## 👥 Parte 3 — Dos personas, la misma rama, el mismo archivo

**Situación:** Esta vez los devs **comparten rama**. Tu trabajo aquí es: preparar el terreno, **observar** cómo se desarrolla y, al final, integrar.

### 3.1 Crea la rama compartida con un archivo base

```bash
git switch main
git switch -c feature/validaciones
```

👀 `Switched to a new branch 'feature/validaciones'`

Crea **`validaciones.py`**:

```python
"""Funciones de validación de datos."""


def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    pass
```

```bash
git add validaciones.py
git commit -m "Agrega esqueleto de validaciones"
git push -u origin feature/validaciones
```

👀

```
[feature/validaciones 2c6162b] Agrega esqueleto de validaciones
 1 file changed, 6 insertions(+)
 create mode 100644 validaciones.py

To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/validaciones -> feature/validaciones
branch 'feature/validaciones' set up to track 'origin/feature/validaciones'.
```

### 🚦 PE-6 — «Rama `feature/validaciones` publicada»

**Avisa a los devs.** Ellos crearán su copia local desde la remota. Ahora te toca **observar**.

### 3.2 Ronda A: observa el choque (Dev2 sube primero, Dev1 choca)

Cuando Dev2 avise **PE-7**, mira el remoto sin tocar nada:

```bash
git fetch
git log --oneline origin/feature/validaciones -3
```

👀

```
From https://github.com/<usuario>/clase-git
   2c6162b..00a9c0c  feature/validaciones -> origin/feature/validaciones

00a9c0c Agrega validación es_vacio
2c6162b Agrega esqueleto de validaciones
```

Cuando Dev1 resuelva y avise **PE-8**:

```bash
git fetch
git log --oneline --graph origin/feature/validaciones -5
```

👀 Un «diamante» → Dev1 resolvió con **merge**:

```
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
|\
| * 00a9c0c Agrega validación es_vacio
* | 39fb13a Agrega validación es_positivo
|/
* 2c6162b Agrega esqueleto de validaciones
```

### 3.3 Ronda B: observa el rebase (Dev1 sube primero, Dev2 choca)

Cuando Dev2 avise **PE-10**:

```bash
git fetch
git log --oneline --graph origin/feature/validaciones -7
```

👀 Arriba, una línea **recta** → Dev2 resolvió con **rebase**:

```
* 58470fe Implementa es_numero con isdigit()
* a07dabe Implementa es_numero con float()
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
|\
| * 00a9c0c Agrega validación es_vacio
* | 39fb13a Agrega validación es_positivo
|/
* 2c6162b Agrega esqueleto de validaciones
```

💡 **La comparación visual lo dice todo:**

| | Merge (Ronda A, Dev1) | Rebase (Ronda B, Dev2) |
|---|---|---|
| Historial | Con «diamante» y commit de merge | Línea recta |
| Commits | Se conservan tal cual | Se **reescriben** (hash nuevo) |
| Cuándo | Rama compartida / quieres conservar la historia real | Ramas **tuyas**, aún sin integrar |

### 3.4 Integra la rama en `main`

```bash
git switch main
git pull
git merge --no-ff origin/feature/validaciones -m "Merge feature/validaciones en main"
git push origin main
```

👀

```
Already up to date.
Merge made by the 'ort' strategy.
 validaciones.py | 22 ++++++++++++++++++++
 1 file changed, 22 insertions(+)
 create mode 100644 validaciones.py

To https://github.com/<usuario>/clase-git.git
   f7b4b30..e681a97  main -> main
```

Mira el historial «de alto nivel» (solo lo que pasó en `main`):

```bash
git log --first-parent --oneline -5
git log --merges --oneline
```

👀

```
e681a97 Merge feature/validaciones en main
f7b4b30 Merge feature/menu-textos en main (conflicto resuelto en main.py)
e8d576c Merge feature/menu-matematicas en main
6fe928b Merge feature/textos en main
9bc3675 Merge feature/matematicas en main
```

💡 `--first-parent` sigue solo la «línea principal» de `main` e ignora los commits internos de cada rama. Muy útil para ver el historial de **integraciones**.

### 🚦 PE-10 (parte DevOps) — «`main` ya tiene `validaciones.py`»

**Avisa a los devs.** Ahora ellos crearán nuevas ramas desde este `main`.

---

## 🔄 Parte 4 — `main` cambia mientras los devs trabajan

**Situación:** Dev1 (`feature/calculos`) y Dev2 (`feature/formato`) crean ramas y las suben. **Antes de que las integres, tú modificas `main`** en varios archivos. Ellos tendrán que **actualizar sus ramas** y arreglar los conflictos. Dev1 usará **rebase**; Dev2 usará **merge**.

### 🚦 Espera el PE-11 («subimos nuestras ramas de la Parte 4»)

> ⏱️ Es **muy importante** que esperes: tus cambios en `main` deben ocurrir **después** de que ellos crearon sus ramas. Así `main` se adelantó mientras ellos trabajaban, igual que en la vida real.

### 4.1 Prepara `main`

```bash
git fetch
git switch main
git status -sb
```

👀

```
## main...origin/main
```

### 4.2 Haz cambios en varios archivos (3 commits)

**Commit 1 — `main.py`:** reemplaza el archivo completo por:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta
from textos import mayusculas, invertir
from validaciones import es_numero


def main():
    print("=== Mini Utilidades v1.0 ===")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
    print("¿'42' es un número?", es_numero("42"))


if __name__ == "__main__":
    main()
```

```bash
git add main.py
git commit -m "Actualiza main.py: encabezado v1.0 y uso de es_numero"
```

**Commit 2 — `matematicas.py` y `textos.py`:**

`matematicas.py` completo:

```python
"""Operaciones matemáticas básicas."""


def suma(a, b):
    """Devuelve la suma de a y b."""
    return a + b


def resta(a, b):
    """Devuelve la resta de a y b."""
    return a - b


def potencia(base, exponente):
    """Devuelve base elevada al exponente."""
    return base ** exponente
```

`textos.py` completo:

```python
"""Utilidades para manejo de texto."""


def mayusculas(texto):
    return texto.upper()


def invertir(texto):
    return texto[::-1]


def es_palindromo(texto):
    """Devuelve True si el texto se lee igual al derecho y al revés."""
    limpio = texto.replace(" ", "").lower()
    return limpio == limpio[::-1]
```

```bash
git add matematicas.py textos.py
git commit -m "Agrega potencia y es_palindromo; documenta suma y resta"
```

**Commit 3 — `README.md`:** agrega al final:

````markdown

## Cómo ejecutar

```bash
python main.py
```
````

```bash
git add README.md
git commit -m "Documenta cómo ejecutar el proyecto"
```

Prueba y sube:

```bash
python main.py
git push origin main
```

👀

```
=== Mini Utilidades v1.0 ===
Suma de 2 + 3 = 5
...
¿'42' es un número? True

To https://github.com/<usuario>/clase-git.git
   e681a97..7c30777  main -> main
```

> 🎯 **Lo que acabas de provocar:** `matematicas.py` y `textos.py` los editas al final del archivo (justo donde cada dev añadirá sus funciones), y `main.py` en el mismo sitio donde ellos agregan sus `print`. ¡Habrá choques!

### 🚦 PE-12 — «Cambié `main`, ¡actualícense!»

**Avisa a los devs.** Ellos harán `fetch`, verán que `main` avanzó y actualizarán sus ramas.

### 4.3 Mientras tanto: observa cómo divergieron

```bash
git fetch
git log --oneline --graph --all --decorate -10
```

👀

```
* 7c30777 (HEAD -> main, origin/main) Documenta cómo ejecutar el proyecto
* 555c57a Agrega potencia y es_palindromo; documenta suma y resta
* ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
| * c1407f1 (origin/feature/formato) Usa capitalizar y contar_palabras en el programa principal
| * 0191ee0 Agrega capitalizar y contar_palabras
|/
| * 71d1db5 (origin/feature/calculos) Usa multiplicar y dividir en el programa principal
| * b69dd7f Agrega multiplicar y dividir
|/
*   e681a97 Merge feature/validaciones en main
```

💡 Tres ramas **divergieron** desde el mismo commit (`e681a97`): `main` (3 commits tuyos), `feature/calculos` (2) y `feature/formato` (2).

Compara con la notación `A..B`:

```bash
git log --oneline origin/main..origin/feature/calculos
git log --oneline origin/feature/calculos..origin/main
```

👀

```
71d1db5 Usa multiplicar y dividir en el programa principal
b69dd7f Agrega multiplicar y dividir

7c30777 Documenta cómo ejecutar el proyecto
555c57a Agrega potencia y es_palindromo; documenta suma y resta
ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
```

💡 Primero: lo que Dev1 tiene y `main` no. Segundo: lo que `main` tiene y Dev1 no.

### 4.4 Cuando los devs ya actualizaron (PE-13): mira el cambio de Dev1

Dev1 hizo rebase y un push forzado. Verás esto en tu `fetch`:

```bash
git fetch
```

👀

```
From https://github.com/<usuario>/clase-git
 + 71d1db5...551a77c feature/calculos -> origin/feature/calculos  (forced update)
   c1407f1..c9aeeb7  feature/formato  -> origin/feature/formato
```

💡 El `+` y *forced update* significan que la historia de esa rama **fue reescrita** (hashes nuevos). Es normal tras un rebase y por eso solo se hace en ramas **propias**.

```bash
git log --oneline --graph --all --decorate -12
```

👀 `feature/calculos` quedó **encima** de `main` (línea recta) y `feature/formato` tiene un commit de merge que trajo `main`.

### 4.5 Integra `feature/calculos` (entra limpio)

```bash
git merge --no-ff origin/feature/calculos -m "Merge feature/calculos en main"
```

👀

```
Merge made by the 'ort' strategy.
 main.py        |  4 +++-
 matematicas.py | 10 ++++++++++
 2 files changed, 13 insertions(+), 1 deletion(-)
```

### 4.6 Integra `feature/formato` (¡un último conflicto!)

```bash
git merge --no-ff origin/feature/formato -m "Merge feature/formato en main"
```

👀

```
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts and then commit the result.
```

💡 **¿Por qué otra vez?** Dev2 se actualizó con `main` **antes** de que entrara el trabajo de Dev1. Cada uno modificó una línea de `import` distinta, pero **contigua** (Dev1 la de `matematicas`, Dev2 la de `textos`). Cuando los cambios están pegados, Git no puede separarlos y marca conflicto. Es completamente normal: el segundo en integrar siempre puede chocar con el primero.
> En un equipo real podrías pedirle a Dev2 que se actualice otra vez; aquí lo resuelves tú (¡practica!).

Abre `main.py`. Hay **un solo bloque** en conflicto, en los `import`:

```python
"""Programa principal de Mini Utilidades."""

<<<<<<< HEAD
from matematicas import suma, resta, multiplicar, dividir
from textos import mayusculas, invertir
=======
from matematicas import suma, resta
from textos import mayusculas, invertir, capitalizar, contar_palabras
>>>>>>> origin/feature/formato
from validaciones import es_numero
```

💡 Las líneas `print(...)` **no** chocaron: Dev1 agregó las suyas al final de `main()` y Dev2 las suyas en el medio, así que Git las combinó solo.

Aquí hay que **construir** la línea correcta, tomando lo mejor de cada lado: `multiplicar, dividir` (Dev1) y `capitalizar, contar_palabras` (Dev2). Resuelve para que el archivo completo quede así:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta, multiplicar, dividir
from textos import mayusculas, invertir, capitalizar, contar_palabras
from validaciones import es_numero


def main():
    print("=== Mini Utilidades v1.0 ===")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
    print("Capitalizado:", capitalizar("hola mundo"))
    print("Palabras:", contar_palabras("hola mundo cruel"))
    print("¿'42' es un número?", es_numero("42"))
    print("Multiplicación 4 x 3 =", multiplicar(4, 3))
    print("División 10 / 2 =", dividir(10, 2))


if __name__ == "__main__":
    main()
```

> 🔎 Si te quedas con un solo lado del conflicto, `python main.py` fallará con `NameError` (falta alguna función importada). **Por eso siempre se prueba antes de confirmar.**

```bash
python main.py
git add main.py
git commit -m "Merge feature/formato en main (conflicto en main.py resuelto)"
git push origin main
```

👀

```
=== Mini Utilidades v1.0 ===
...
División 10 / 2 = 5.0
[main fe369df] Merge feature/formato en main (conflicto en main.py resuelto)

To https://github.com/<usuario>/clase-git.git
   7c30777..fe369df  main -> main
```

### 4.7 Etiqueta la versión (tag)

🎯 Marcar este momento como la versión 1.0.

```bash
git tag -a v1.0 -m "Primera versión de Mini Utilidades"
git push origin v1.0
git tag
```

👀

```
To https://github.com/<usuario>/clase-git.git
 * [new tag]         v1.0 -> v1.0
v1.0
```

### 4.8 Contempla el resultado final

```bash
git log --oneline --graph --decorate -14
```

👀

```
*   fe369df (HEAD -> main, tag: v1.0, origin/main) Merge feature/formato en main (conflicto en main.py resuelto)
|\
| *   c9aeeb7 (origin/feature/formato) Merge origin/main en feature/formato (conflictos resueltos)
| |\
| * | c1407f1 Usa capitalizar y contar_palabras en el programa principal
| * | 0191ee0 Agrega capitalizar y contar_palabras
* | |   ef7cf75 Merge feature/calculos en main
|\ \ \
| |_|/
|/| |
| * | 551a77c (origin/feature/calculos) Usa multiplicar y dividir en el programa principal
| * | 0d15d8f Agrega multiplicar y dividir
|/ /
* | 7c30777 Documenta cómo ejecutar el proyecto
* | 555c57a Agrega potencia y es_palindromo; documenta suma y resta
* | ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
|/
*   e681a97 Merge feature/validaciones en main
```

💡 Compara las dos ramas de los devs: la de Dev1 (rebase) es una **línea recta** que sale de `main`; la de Dev2 (merge) lleva un **diamante** que trae `main` hacia su rama.

---

## 🔍 Parte 5 — Explorar el historial y limpiar

### 5.1 Herramientas de historial

```bash
git log --oneline -5                 # resumen
git log --stat -2                    # con archivos tocados
git log --author="Dev Dos" --oneline # commits de una persona
git log -S"es_palindromo" --oneline  # ¿cuándo apareció esta palabra?
git shortlog -sn --no-merges HEAD    # commits por persona
git show --stat HEAD                 # detalle de un commit
git show v1.0                        # detalle de la etiqueta
```

👀 Por ejemplo, `-S` encuentra el commit que **introdujo** el texto:

```
555c57a Agrega potencia y es_palindromo; documenta suma y resta
```

Y el conteo por persona:

```
     6	Dev Dos
     6	Dev Uno
     5	DevOps
```

### 5.2 La red de seguridad: `reflog`

```bash
git reflog -5
```

👀

```
fe369df HEAD@{0}: commit (merge): Merge feature/formato en main (conflicto en main.py resuelto)
ef7cf75 HEAD@{1}: merge origin/feature/calculos: Merge made by the 'ort' strategy.
7c30777 HEAD@{2}: pull: Fast-forward
...
```

💡 `reflog` guarda **todos los movimientos de HEAD**, incluso los que ya no aparecen en `log`. Si crees que «perdiste» algo tras un reset o rebase, aquí lo encuentras: `git reset --hard HEAD@{2}`.

### 5.3 Limpia las ramas ya integradas

```bash
git branch --merged
```

👀 Las ramas que ya están dentro de `main`:

```
  feature/matematicas
  feature/textos
  feature/validaciones
* main
```

Borra las **locales**:

```bash
git branch -d feature/matematicas feature/textos feature/validaciones
```

👀

```
Deleted branch feature/matematicas (was 5a59c61).
Deleted branch feature/textos (was ab7e453).
Deleted branch feature/validaciones (was 2c6162b).
```

Borra las **remotas** de las partes anteriores:

```bash
git push origin --delete feature/matematicas feature/textos feature/menu-matematicas feature/menu-textos feature/validaciones
```

👀

```
To https://github.com/<usuario>/clase-git.git
 - [deleted]         feature/matematicas
 - [deleted]         feature/textos
 ...
```

Y limpia las referencias fantasma que quedan localmente:

```bash
git fetch --prune
git branch -r
```

👀

```
  origin/feature/calculos
  origin/feature/formato
  origin/main
```

> ✅ `-d` (minúscula) **solo borra si ya está integrada** (es seguro). `-D` (mayúscula) borra **a la fuerza**: úsala con cuidado.

Cuando los devs terminen su limpieza, borra también `feature/calculos` y `feature/formato` del remoto.

---

## 🆘 «Me equivoqué»: tabla de rescate

| Situación | Comando | Efecto |
|---|---|---|
| Estoy en medio de un merge y me enredé | `git merge --abort` | Vuelve al estado **antes** del merge |
| Estoy en medio de un rebase y me enredé | `git rebase --abort` | Vuelve al estado antes del rebase |
| Edité un archivo y quiero descartar los cambios | `git restore archivo.py` | ⚠️ Pierdes lo no confirmado |
| Hice `git add` de algo que no quería | `git restore --staged archivo.py` | Lo saca del *staging* |
| Quiero deshacer un commit **ya subido** | `git revert <hash>` | Crea un commit que lo deshace (seguro) |
| Quiero ver cómo estaba un archivo antes | `git show <hash>:archivo.py` | Lo muestra sin cambiar nada |
| «Perdí» commits | `git reflog` y luego `git reset --hard <hash>` | Recupera el estado de ese punto |
| Tengo cambios sin commit y necesito cambiar de rama | `git stash` / `git stash pop` | Los guarda y luego los recupera |
| El `push` es rechazado | `git fetch` y luego `merge` o `rebase` | Integra lo remoto primero |

---

## 🧾 Resumen de comandos que usaste

| Comando | Para qué |
|---|---|
| `git clone <url>` | Copiar un repo remoto |
| `git fetch` | Traer metadatos del remoto **sin** tocar tu trabajo |
| `git branch -a` / `-r` / `-vv` | Ver ramas locales, remotas y su seguimiento |
| `git switch <rama>` | Cambiar de rama (crea la local si existe en el remoto) |
| `git switch -c <rama> --track origin/<rama>` | Crear rama local desde una remota |
| `git log --oneline --graph --decorate --all` | Ver el historial como grafo |
| `git log A..B` | Commits que están en B y no en A |
| `git diff --stat A B` | Resumen de diferencias entre ramas |
| `git merge --no-ff <rama>` | Integrar dejando commit de merge |
| `git add` + `git commit` | Cerrar la resolución de un conflicto |
| `git tag -a v1.0 -m "..."` | Marcar una versión |
| `git push origin --delete <rama>` | Borrar una rama remota |
| `git fetch --prune` | Limpiar referencias remotas ya borradas |

---

## ✅ Checklist final del DevOps

- [ ] Hice el commit inicial y publiqué `main`
- [ ] Usé `fetch` e inspeccioné con `log A..B` y `diff` **antes** de integrar
- [ ] Creé ramas locales a partir de remotas
- [ ] Hice un merge limpio con `--no-ff`
- [ ] Resolví un conflicto en `main` (marcadores → editar → `add` → `commit`)
- [ ] Publiqué la rama compartida y observé merge vs rebase en el grafo
- [ ] Cambié `main` mientras los devs trabajaban
- [ ] Integré las dos ramas finales y resolví el último conflicto
- [ ] Creé el tag `v1.0`
- [ ] Limpié las ramas viejas

🎉 **¡Buen trabajo, DevOps!**
