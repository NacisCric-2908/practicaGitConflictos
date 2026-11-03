# 👩‍💻 Guía Programador 1 — Clase de Git: merge, rebase y resolución de conflictos

> **Tu rol:** eres **Dev1**. Trabajas en tus propias ramas, subes tu código a GitHub y resuelves los conflictos que aparezcan cuando tu trabajo choca con el de Dev2 o con los cambios de `main`.
>
> **Proyecto:** *Mini Utilidades*, un programa pequeño en Python. Tu especialidad: **matemáticas** (`matematicas.py`).
>
> **Tu estilo de resolución:** en la Parte 3 usarás **merge**; en la Parte 4 usarás **rebase**. (Dev2 hará lo contrario: así cada uno practica ambos.)

---

## 📌 Cómo leer esta guía

Cada paso tiene este formato:

- **🎯 Qué vamos a hacer** — la idea.
- **⌨️ Comando** — lo que escribes.
- **👀 Qué deberías ver** — salida aproximada de la terminal.
- **💡 Por qué** — el concepto detrás.

> ⚠️ **Los hashes cambian.** Códigos como `5a59c61` serán distintos en tu máquina. Fíjate en la *forma* de la salida, no en los números.

### 🚦 Puntos de encuentro

Los tres roles trabajan a la vez. Cuando llegues a un **punto de encuentro**, **avisa en voz alta** y **espera** el aviso que indique la guía. Los números son iguales en las tres guías.

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
| **PE-12** | DevOps cambió `main` (¡hay que actualizarse!) |
| **PE-13** | Dev1 y Dev2 actualizaron sus ramas y subieron |

---

## 🧰 Parte 0 — Preparación

### 0.1 Configura tu identidad

🎯 Cada commit lleva tu nombre y correo.

```bash
git config --global user.name "Dev Uno"
git config --global user.email "dev1@clase.com"
git config --global init.defaultBranch main
git config --global pull.ff only
git config --global core.editor "nano"
```

💡 **Por qué:**
- `pull.ff only` → `git pull` solo funcionará si es un avance «limpio». Si hay divergencia, **se negará** y tú decidirás qué hacer (merge o rebase). Nada de sorpresas.
- `core.editor "nano"` → si Git abre un editor, será `nano` (guardar: `Ctrl+O`, `Enter`; salir: `Ctrl+X`). Si usas VS Code: `"code --wait"`.

> 🪟 **Windows:** puede salir `warning: LF will be replaced by CRLF`. Es inofensivo.

### 0.2 Espera el 🚦 PE-1 («`main` está publicado») y clona

```bash
git clone <URL-DEL-REPO> clase-git
cd clase-git
```

👀

```
Cloning into 'clase-git'...
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
Receiving objects: 100% (5/5), done.
```

### 0.3 Reconoce el terreno

```bash
ls
git log --oneline
git branch -a
git remote -v
```

👀

```
README.md  main.py

eba20f0 (HEAD -> main, origin/main, origin/HEAD) Commit inicial: estructura base del proyecto

* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

origin	https://github.com/<usuario>/clase-git.git (fetch)
origin	https://github.com/<usuario>/clase-git.git (push)
```

💡 `origin` es el **nombre** que Git le da al repositorio remoto. `origin/main` es tu copia local del estado de `main` en GitHub.

Prueba que funciona:

```bash
python main.py
```

👀 `Bienvenido a Mini Utilidades`

---

## 🌱 Parte 1 — Tu rama, tu archivo (sin conflictos)

**Situación:** tú creas `matematicas.py` en `feature/matematicas`; Dev2 crea `textos.py` en otra rama. No se tocan.

### 1.1 Crea tu rama

🎯 Nunca se trabaja directo en `main`. Cada tarea tiene su rama.

```bash
git switch -c feature/matematicas
```

👀

```
Switched to a new branch 'feature/matematicas'
```

💡 `-c` = *create*. Es equivalente a `git branch feature/matematicas` + `git switch feature/matematicas`.

### 1.2 Crea `matematicas.py`

```python
"""Operaciones matemáticas básicas."""


def suma(a, b):
    return a + b


def resta(a, b):
    return a - b
```

```bash
git status
```

👀

```
On branch feature/matematicas
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	matematicas.py

nothing added to commit but untracked files present (use "git add" to track)
```

### 1.3 Confirma el cambio (add + commit)

```bash
git add matematicas.py
git status -s
git commit -m "Agrega funciones suma y resta"
```

👀

```
A  matematicas.py

[feature/matematicas 5a59c61] Agrega funciones suma y resta
 1 file changed, 9 insertions(+)
 create mode 100644 matematicas.py
```

💡 **Las tres zonas de Git:**

```
 Directorio de trabajo  ──git add──▶  Staging  ──git commit──▶  Repositorio local  ──git push──▶  GitHub
```

La `A` de `git status -s` significa *Added* (ya está en *staging*).

### 1.4 Sube tu rama a GitHub

```bash
git push -u origin feature/matematicas
```

👀

```
To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/matematicas -> feature/matematicas
branch 'feature/matematicas' set up to track 'origin/feature/matematicas'.
```

💡 `-u` enlaza tu rama local con la remota. Después basta con `git push` y `git pull` sin argumentos.

```bash
git branch -vv
```

👀

```
* feature/matematicas 5a59c61 [origin/feature/matematicas] Agrega funciones suma y resta
  main                eba20f0 [origin/main] Commit inicial: estructura base del proyecto
```

### 🚦 PE-2 — Avisa: «¡Subí mi rama!»

Espera a que DevOps avise el **PE-3** («hice el merge de la Parte 1»).

---

## ⚔️ Parte 2 — Mismo archivo, ramas distintas

**Situación:** tú y Dev2 editarán `main.py` **en las mismas líneas**, cada uno en su rama. El conflicto lo resolverá DevOps en `main`. Tu trabajo: partir de un `main` actualizado y subir tu rama.

### 2.1 Trae los metadatos del remoto con `fetch`

🎯 Ver qué pasó en GitHub **sin tocar tus archivos**.

```bash
git fetch
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/textos -> origin/feature/textos
   eba20f0..6fe928b  main           -> origin/main
```

💡 **`fetch` vs `pull`:**

| Comando | Qué hace | ¿Toca tus archivos? |
|---|---|---|
| `git fetch` | Descarga las novedades a las ramas `origin/*` | ❌ No |
| `git pull` | `fetch` **+** `merge` sobre la rama actual | ✅ Sí |

### 2.2 Mira el estado sin integrar nada

```bash
git status -sb
```

👀

```
## feature/matematicas...origin/feature/matematicas
```

💡 Tu rama no dice nada de `main`: `status` solo compara tu rama con **su** remota. Para ver `main` hay que mirar el grafo:

```bash
git log --oneline --graph --all --decorate
```

👀

```
*   6fe928b (origin/main, origin/HEAD) Merge feature/textos en main
|\
| * ab7e453 (origin/feature/textos) Agrega funciones mayusculas e invertir
* |   9bc3675 Merge feature/matematicas en main
|\ \
| |/
|/|
| * 5a59c61 (HEAD -> feature/matematicas, origin/feature/matematicas) Agrega funciones suma y resta
|/
* eba20f0 (main) Commit inicial: estructura base del proyecto
```

💡 Tu `main` **local** (`eba20f0`) se quedó atrás: `origin/main` ya tiene el merge de DevOps.

### 2.3 Actualiza tu `main` local

```bash
git switch main
git status
```

👀

```
Switched to branch 'main'
Your branch is behind 'origin/main' by 4 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
```

Antes de actualizar, **mira qué vas a recibir**:

```bash
git log --oneline main..origin/main
git diff --stat main origin/main
```

👀

```
6fe928b Merge feature/textos en main
9bc3675 Merge feature/matematicas en main
ab7e453 Agrega funciones mayusculas e invertir
5a59c61 Agrega funciones suma y resta

 matematicas.py | 9 +++++++++
 textos.py      | 9 +++++++++
 2 files changed, 18 insertions(+)
```

Ahora sí, actualiza:

```bash
git pull
```

👀

```
Updating eba20f0..6fe928b
Fast-forward
 matematicas.py | 9 +++++++++
 textos.py      | 9 +++++++++
 2 files changed, 18 insertions(+)
 create mode 100644 matematicas.py
 create mode 100644 textos.py
```

💡 **Fast-forward** = tu `main` no tenía nada propio, así que Git solo «avanzó el puntero». Sin merge, sin conflicto.

### 2.4 Crea tu nueva rama y edita `main.py`

```bash
git switch -c feature/menu-matematicas
```

Reemplaza **todo** `main.py` por:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta


def main():
    print("Bienvenido a Mini Utilidades")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))


if __name__ == "__main__":
    main()
```

Pruébalo y confirma:

```bash
python main.py
git add main.py
git commit -m "Agrega demo de matemáticas al programa principal"
git push -u origin feature/menu-matematicas
```

👀

```
Bienvenido a Mini Utilidades
Suma de 2 + 3 = 5
Resta de 5 - 1 = 4

[feature/menu-matematicas c16366d] Agrega demo de matemáticas al programa principal
 1 file changed, 4 insertions(+)

To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/menu-matematicas -> feature/menu-matematicas
branch 'feature/menu-matematicas' set up to track 'origin/feature/menu-matematicas'.
```

### 🚦 PE-4 — Avisa: «¡Subí `feature/menu-matematicas`!»

Ahora DevOps hará los merges y resolverá el conflicto. Espera el **PE-5**.

### 2.5 Mira cómo DevOps resolvió el conflicto

```bash
git fetch
git switch main
git pull
git log --oneline --graph --decorate -8
```

👀 Verás los dos merges (uno limpio y uno con el conflicto resuelto):

```
*   f7b4b30 (HEAD -> main, origin/main) Merge feature/menu-textos en main (conflicto resuelto en main.py)
|\
| * f687312 (origin/feature/menu-textos) Agrega demo de textos al programa principal
* |   e8d576c Merge feature/menu-matematicas en main
|\ \
| |/
|/|
| * c16366d (origin/feature/menu-matematicas, feature/menu-matematicas) Agrega demo de matemáticas al programa principal
|/
*   6fe928b Merge feature/textos en main
```

Y el programa ya combina el trabajo de ambos:

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

---

## 👥 Parte 3 — Misma rama, mismo archivo (¡dos rondas de choque!)

**Situación:** tú y Dev2 trabajan **en la misma rama remota** (`feature/validaciones`), en el mismo archivo.

- **Ronda A:** Dev2 sube primero → **tú** chocas → resuelves con **merge**.
- **Ronda B:** tú subes primero → Dev2 choca → él resuelve con **rebase**.

### 🚦 Espera el PE-6 («`feature/validaciones` publicada»)

### 3.1 Crea tu rama local a partir de la remota

🎯 La rama ya existe en GitHub; necesitas una copia local que la siga.

```bash
git fetch
git branch -a
```

👀 Aparece `remotes/origin/feature/validaciones`:

```
  feature/matematicas
* feature/menu-matematicas
  main
  remotes/origin/HEAD -> origin/main
  ...
  remotes/origin/feature/validaciones
  remotes/origin/main
```

```bash
git switch feature/validaciones
git branch -vv
```

👀

```
branch 'feature/validaciones' set up to track 'origin/feature/validaciones'.
Switched to a new branch 'feature/validaciones'

  feature/matematicas      5a59c61 [origin/feature/matematicas] Agrega funciones suma y resta
  feature/menu-matematicas c16366d [origin/feature/menu-matematicas] Agrega demo de matemáticas al programa principal
* feature/validaciones     2c6162b [origin/feature/validaciones] Agrega esqueleto de validaciones
  main                     6fe928b [origin/main: behind 4] Merge feature/textos en main
```

💡 Otras formas equivalentes de crear una local desde una remota:
`git switch -c feature/validaciones --track origin/feature/validaciones` o la antigua `git checkout -b feature/validaciones origin/feature/validaciones`.

El archivo base (creado por DevOps) es:

```python
"""Funciones de validación de datos."""


def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    pass
```

---

### 🅰️ Ronda A — Dev2 sube primero, tú chocas (resolución con MERGE)

#### 3.2 Haz tu cambio y confirma **sin hacer push**

Agrega **al final** de `validaciones.py` (deja dos líneas en blanco antes):

```python


def es_positivo(numero):
    """Devuelve True si el número es mayor que cero."""
    return numero > 0
```

```bash
git add validaciones.py
git commit -m "Agrega validación es_positivo"
```

👀

```
[feature/validaciones 39fb13a] Agrega validación es_positivo
 1 file changed, 5 insertions(+)
```

> ⛔ **No hagas `push` todavía.** Avisa: «tengo mi commit listo» y espera a que **Dev2 suba primero (🚦 PE-7)**.

#### 3.3 Intenta subir… ¡rechazado!

```bash
git push
```

👀

```
To https://github.com/<usuario>/clase-git.git
 ! [rejected]        feature/validaciones -> feature/validaciones (fetch first)
error: failed to push some refs to 'https://github.com/<usuario>/clase-git.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

💡 **Qué significa:** GitHub tiene un commit (el de Dev2) que tú no tienes. Git **no te deja sobrescribirlo**. Por defecto sugiere `git pull`, pero nosotros haremos las cosas por pasos: **primero mirar, luego decidir**.

#### 3.4 `fetch` y examina

```bash
git fetch
git status
```

👀

```
From https://github.com/<usuario>/clase-git
   2c6162b..00a9c0c  feature/validaciones -> origin/feature/validaciones

On branch feature/validaciones
Your branch and 'origin/feature/validaciones' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
```

💡 **`diverged`** = ambos tienen un commit que el otro no tiene. Hay que integrarlos.

Mira el mapa:

```bash
git log --oneline --graph --all --decorate -6
```

👀

```
* 39fb13a (HEAD -> feature/validaciones) Agrega validación es_positivo
| * 00a9c0c (origin/feature/validaciones) Agrega validación es_vacio
|/
* 2c6162b Agrega esqueleto de validaciones
```

💡 Una bifurcación en «Y»: los dos partieron de `2c6162b`.

Mira **qué trae** Dev2 y **qué cambió**:

```bash
git log --oneline HEAD..origin/feature/validaciones
git diff HEAD...origin/feature/validaciones
```

👀

```
00a9c0c Agrega validación es_vacio

diff --git a/validaciones.py b/validaciones.py
--- a/validaciones.py
+++ b/validaciones.py
@@ -4,3 +4,8 @@
 def es_numero(texto):
     """Devuelve True si el texto representa un número."""
     pass
+
+
+def es_vacio(texto):
+    """Devuelve True si el texto está vacío o solo tiene espacios."""
+    return texto.strip() == ""
```

💡 **Dos puntos vs tres puntos:**
- `A..B` → commits que están en B y no en A.
- `A...B` (en `diff`) → cambios que hizo **B desde el ancestro común**, ignorando lo que hizo A. Es lo que «traería» la otra rama.

#### 3.5 Integra con `merge`

```bash
git merge origin/feature/validaciones
```

👀

```
Auto-merging validaciones.py
CONFLICT (content): Merge conflict in validaciones.py
Automatic merge failed; fix conflicts and then commit the result.
```

Abre `validaciones.py`:

```python
"""Funciones de validación de datos."""


def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    pass


<<<<<<< HEAD
def es_positivo(numero):
    """Devuelve True si el número es mayor que cero."""
    return numero > 0
=======
def es_vacio(texto):
    """Devuelve True si el texto está vacío o solo tiene espacios."""
    return texto.strip() == ""
>>>>>>> origin/feature/validaciones
```

💡 **Cómo leerlo en un merge:**
- Entre `<<<<<<< HEAD` y `=======` → **tu** versión (la rama en la que estás).
- Entre `=======` y `>>>>>>>` → la versión **que viene** de la otra rama.

Aquí no es «cuál gana»: ambas funciones son válidas. **Conserva las dos.** Deja el archivo así:

```python
"""Funciones de validación de datos."""


def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    pass


def es_vacio(texto):
    """Devuelve True si el texto está vacío o solo tiene espacios."""
    return texto.strip() == ""


def es_positivo(numero):
    """Devuelve True si el número es mayor que cero."""
    return numero > 0
```

> ⚠️ Revisa que **no quede ningún** `<<<<<<<`, `=======` ni `>>>>>>>`. Búscalos con `Ctrl+F`.

#### 3.6 Cierra el merge y sube

```bash
git add validaciones.py
git commit -m "Merge origin/feature/validaciones: conserva es_vacio y es_positivo"
git push
```

👀

```
[feature/validaciones 90fe344] Merge origin/feature/validaciones: conserva es_vacio y es_positivo

To https://github.com/<usuario>/clase-git.git
   00a9c0c..90fe344  feature/validaciones -> feature/validaciones
```

```bash
git log --oneline --graph -5
```

👀 El «diamante» típico del merge:

```
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
|\
| * 00a9c0c Agrega validación es_vacio
* | 39fb13a Agrega validación es_positivo
|/
* 2c6162b Agrega esqueleto de validaciones
```

### 🚦 PE-8 — Avisa: «¡Resolví y subí!»

Dev2 hará un `git pull` para ponerse al día. Espera a que avise que está sincronizado.

---

### 🅱️ Ronda B — Tú subes primero, Dev2 choca

**Ahora los papeles se invierten:** ambos modificarán la **misma función** (`es_numero`). **Tú** subes primero.

#### 3.7 Implementa `es_numero` (con `float`)

En `validaciones.py`, reemplaza el cuerpo de `es_numero` (la línea `pass`) para que quede así:

```python
def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    try:
        float(texto)
        return True
    except ValueError:
        return False
```

Prueba rápida:

```bash
python -c "from validaciones import es_numero; print(es_numero('3.5'), es_numero('abc'))"
```

👀 `True False`

```bash
git add validaciones.py
git commit -m "Implementa es_numero con float()"
```

> 🤝 Avisa a Dev2: «yo voy a subir primero, ¿ya hiciste tu commit local?». Cuando ambos tengan su commit listo, **tú haces push**:

```bash
git push
```

👀

```
[feature/validaciones a07dabe] Implementa es_numero con float()
 1 file changed, 5 insertions(+), 1 deletion(-)

To https://github.com/<usuario>/clase-git.git
   90fe344..a07dabe  feature/validaciones -> feature/validaciones
```

### 🚦 PE-9 — Avisa: «¡Ya subí! Dev2, tu turno de chocar»

Dev2 resolverá con **rebase**. Mientras tanto, espera su aviso del **PE-10**.

#### 3.8 Mira el resultado (cuando Dev2 avise)

```bash
git fetch
git log --oneline --graph --decorate -7
```

👀 ¡Línea recta arriba! El commit de Dev2 quedó **encima** del tuyo:

```
* 58470fe (origin/feature/validaciones) Implementa es_numero con isdigit()
* a07dabe (HEAD -> feature/validaciones) Implementa es_numero con float()
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
|\
| * 00a9c0c Agrega validación es_vacio
* | 39fb13a Agrega validación es_positivo
|/
* 2c6162b Agrega esqueleto de validaciones
```

```bash
git pull
```

👀

```
Updating a07dabe..58470fe
Fast-forward
 validaciones.py | 2 ++
 1 file changed, 2 insertions(+)
```

#### 3.9 Detective: ¿quién escribió cada línea?

```bash
git blame validaciones.py -L 4,12
```

👀

```
2c6162be (DevOps  2026-11-03 12:51:12 +0000  4) def es_numero(texto):
2c6162be (DevOps  2026-11-03 12:51:12 +0000  5)     """Devuelve True si el texto representa un número."""
58470feb (Dev Dos 2026-11-03 12:51:23 +0000  6)     if texto.strip() == "":
58470feb (Dev Dos 2026-11-03 12:51:23 +0000  7)         return False
a07dabe0 (Dev Uno 2026-11-03 12:51:23 +0000  8)     try:
a07dabe0 (Dev Uno 2026-11-03 12:51:23 +0000  9)         float(texto)
a07dabe0 (Dev Uno 2026-11-03 12:51:23 +0000 10)         return True
a07dabe0 (Dev Uno 2026-11-03 12:51:23 +0000 11)     except ValueError:
a07dabe0 (Dev Uno 2026-11-03 12:51:23 +0000 12)         return False
```

```bash
git log -p -1
```

👀 Muestra el último commit **con** su diff completo (el de Dev2: el chequeo de texto vacío).

💡 Resultado de la resolución de Dev2: **combinó** tu enfoque (`float`) con el suyo (rechazar vacíos).

### 🚦 Espera el aviso de DevOps: «`main` ya tiene `validaciones.py`» (parte final del PE-10)

---

## 🔄 Parte 4 — `main` cambia mientras trabajas (¡usarás REBASE!)

**Situación:** creas `feature/calculos` y la subes. DevOps **modifica `main`** en varios archivos. Tu rama queda «desactualizada» y habrá conflictos. La resolverás con **rebase**.

### 4.1 Parte de un `main` actualizado

```bash
git switch main
git pull
```

👀

```
Updating f7b4b30..e681a97
Fast-forward
 validaciones.py | 22 ++++++++++++++++++++++
 1 file changed, 22 insertions(+)
 create mode 100644 validaciones.py
```

### 4.2 Crea la rama y haz **dos commits**

```bash
git switch -c feature/calculos
```

**Commit 1 — `matematicas.py`:** agrega **al final**:

```python


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

```bash
git add matematicas.py
git commit -m "Agrega multiplicar y dividir"
```

**Commit 2 — `main.py`:** cambia el import de `matematicas` y agrega dos líneas al final de `main()`. El archivo completo queda:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta, multiplicar, dividir
from textos import mayusculas, invertir


def main():
    print("Bienvenido a Mini Utilidades")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
    print("Multiplicación 4 x 3 =", multiplicar(4, 3))
    print("División 10 / 2 =", dividir(10, 2))


if __name__ == "__main__":
    main()
```

```bash
python main.py
git add main.py
git commit -m "Usa multiplicar y dividir en el programa principal"
git push -u origin feature/calculos
```

👀

```
[feature/calculos b69dd7f] Agrega multiplicar y dividir
 1 file changed, 10 insertions(+)
[feature/calculos 71d1db5] Usa multiplicar y dividir en el programa principal
 1 file changed, 3 insertions(+), 1 deletion(-)

To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/calculos -> feature/calculos
branch 'feature/calculos' set up to track 'origin/feature/calculos'.
```

### 🚦 PE-11 — Avisa: «¡Subí `feature/calculos`!»

DevOps ahora cambiará `main`. Espera el **PE-12** («cambié `main`, ¡actualícense!»).

### 4.3 Detecta que `main` se movió

```bash
git fetch
git status -sb
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/formato -> origin/feature/formato
   e681a97..7c30777  main            -> origin/main

## feature/calculos...origin/feature/calculos
```

💡 El `status` sigue «limpio» porque compara contra **tu** remota. Para saber si `main` avanzó hay que preguntarle:

```bash
git log --oneline --graph --all --decorate -12
```

👀

```
* 7c30777 (origin/main, origin/HEAD) Documenta cómo ejecutar el proyecto
* 555c57a Agrega potencia y es_palindromo; documenta suma y resta
* ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
| * 71d1db5 (HEAD -> feature/calculos, origin/feature/calculos) Usa multiplicar y dividir en el programa principal
| * b69dd7f Agrega multiplicar y dividir
|/
| * c1407f1 (origin/feature/formato) Usa capitalizar y contar_palabras en el programa principal
| * 0191ee0 Agrega capitalizar y contar_palabras
|/
*   e681a97 Merge feature/validaciones en main
```

Pregunta con precisión:

```bash
git log --oneline HEAD..origin/main      # lo que main tiene y yo no
git diff --stat HEAD...origin/main       # qué archivos cambió main desde que salí de ahí
git merge-base HEAD origin/main          # el punto donde nos separamos
```

👀

```
7c30777 Documenta cómo ejecutar el proyecto
555c57a Agrega potencia y es_palindromo; documenta suma y resta
ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero

 README.md      | 6 ++++++
 main.py        | 4 +++-
 matematicas.py | 7 +++++++
 textos.py      | 6 ++++++
 4 files changed, 22 insertions(+), 1 deletion(-)

e681a97a88181baaf621eeefb231083a4b617b15
```

💡 DevOps tocó `main.py` **y** `matematicas.py` (¡tu archivo!). Prepárate: habrá conflictos.

### 4.4 Rebase: «reescribe mi trabajo encima de `main`»

🎯 Imagina que sacas tus 2 commits, actualizas la base a `origin/main` y los «vuelves a poner» uno por uno.

```
ANTES                                 DESPUÉS DEL REBASE
        A───B  (feature/calculos)             A'──B'  (feature/calculos)
       /                                     /
 ●────●────C───D───E  (main)          ●────●────C───D───E  (main)
```

```bash
git rebase origin/main
```

👀 **Primer choque**: Git empieza a reproducir tu primer commit y se detiene.

```
Rebasing (1/2)
Auto-merging matematicas.py
CONFLICT (content): Merge conflict in matematicas.py
error: could not apply b69dd7f... Agrega multiplicar y dividir
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply b69dd7f... Agrega multiplicar y dividir
```

```bash
git status
```

👀

```
interactive rebase in progress; onto 7c30777
Last command done (1 command done):
   pick b69dd7f Agrega multiplicar y dividir
Next command to do (1 remaining command):
   pick 71d1db5 Usa multiplicar y dividir en el programa principal
  (use "git rebase --edit-todo" to view and edit)
You are currently rebasing branch 'feature/calculos' on '7c30777'.
  (fix conflicts and then run "git rebase --continue")
  ...
Unmerged paths:
	both modified:   matematicas.py
```

💡 Fíjate: Git te dice **en qué commit** está (1 de 2) y qué falta.

Abre `matematicas.py`, al final:

```python
<<<<<<< HEAD
def potencia(base, exponente):
    """Devuelve base elevada al exponente."""
    return base ** exponente
=======
def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
>>>>>>> b69dd7f (Agrega multiplicar y dividir)
```

> 🔄 **¡OJO! En un rebase los lados están «invertidos» respecto al merge:**
>
> | Marcador | En un **merge** | En un **rebase** |
> |---|---|---|
> | `<<<<<<< HEAD` | **Tu** trabajo | El trabajo **de `main`** (la base sobre la que se reproduce) |
> | `>>>>>>> <commit>` | Lo de la otra rama | **Tu** commit que se está reproduciendo |
>
> Razón: durante un rebase Git primero se «coloca» en `main` y luego aplica tus commits encima, uno por uno. Tu commit es el «entrante».

Conserva **ambas** funciones. El final del archivo debe quedar:

```python
def resta(a, b):
    """Devuelve la resta de a y b."""
    return a - b


def potencia(base, exponente):
    """Devuelve base elevada al exponente."""
    return base ** exponente


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

```bash
python -c "import matematicas"
git add matematicas.py
git rebase --continue
```

> ✏️ Si se abre un editor pidiendo confirmar el mensaje, guarda y cierra sin cambiar nada.

👀 **Segundo choque**: pasó el commit 1; ahora se detiene en el 2.

```
[detached HEAD 0d15d8f] Agrega multiplicar y dividir
 1 file changed, 10 insertions(+)
Rebasing (2/2)
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
error: could not apply 71d1db5... Usa multiplicar y dividir en el programa principal
```

💡 **Cada commit se reproduce por separado**, por eso un rebase puede pedirte resolver varias veces. (Un merge lo habría resuelto todo de una sola vez.)

Abre `main.py`. El `import` se fusionó solo; el conflicto está al final de `main()`:

```python
    print("Invertido:", invertir("hola"))
<<<<<<< HEAD
    print("¿'42' es un número?", es_numero("42"))
=======
    print("Multiplicación 4 x 3 =", multiplicar(4, 3))
    print("División 10 / 2 =", dividir(10, 2))
>>>>>>> 71d1db5 (Usa multiplicar y dividir en el programa principal)
```

Conserva todo (quita solo los marcadores):

```python
    print("Invertido:", invertir("hola"))
    print("¿'42' es un número?", es_numero("42"))
    print("Multiplicación 4 x 3 =", multiplicar(4, 3))
    print("División 10 / 2 =", dividir(10, 2))
```

```bash
python main.py
git add main.py
git rebase --continue
```

👀

```
[detached HEAD 551a77c] Usa multiplicar y dividir en el programa principal
 1 file changed, 3 insertions(+), 1 deletion(-)
Successfully rebased and updated refs/heads/feature/calculos.
```

🎉 **¡Rebase completado!** Revisa el resultado:

```bash
python main.py
git log --oneline --graph -7
```

👀 Línea **recta**: tus 2 commits quedaron encima de los de `main`, con **hashes nuevos**.

```
* 551a77c Usa multiplicar y dividir en el programa principal
* 0d15d8f Agrega multiplicar y dividir
* 7c30777 Documenta cómo ejecutar el proyecto
* 555c57a Agrega potencia y es_palindromo; documenta suma y resta
* ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
*   e681a97 Merge feature/validaciones en main
|\
```

> 🆘 **¿Te enredaste en medio del rebase?** `git rebase --abort` te devuelve a como estabas antes de empezar. Sin consecuencias.

### 4.5 Sube… y descubre el `push --force-with-lease`

```bash
git push
```

👀 **Rechazado**, aunque acabas de actualizar:

```
To https://github.com/<usuario>/clase-git.git
 ! [rejected]        feature/calculos -> feature/calculos (non-fast-forward)
error: failed to push some refs to 'https://github.com/<usuario>/clase-git.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. ...
```

💡 **¿Por qué?** Tu rama **ya estaba** en GitHub con los commits viejos (`b69dd7f`, `71d1db5`). Tras el rebase tienes commits **nuevos** (`0d15d8f`, `551a77c`) con la misma intención pero distinto hash. Para Git son historias distintas y piensa que vas a «perder» commits.

Como **esta rama es solo tuya** y sabes lo que hiciste, puedes sobrescribirla con seguridad:

```bash
git push --force-with-lease
```

👀

```
To https://github.com/<usuario>/clase-git.git
 + 71d1db5...551a77c feature/calculos -> feature/calculos (forced update)
```

```bash
git status -sb
```

👀

```
## feature/calculos...origin/feature/calculos
```

💡 **`--force-with-lease` vs `--force`:**
- `--force` sobrescribe **sin preguntar**, aunque alguien más haya subido algo.
- `--force-with-lease` solo sobrescribe si el remoto **sigue como tú lo viste**; si alguien subió algo nuevo, falla y te protege. **Prefiérelo siempre.**

> 🏆 **LA REGLA DE ORO DEL REBASE**
>
> **Nunca** hagas rebase (ni `push --force`) de commits que **otras personas ya usan**: `main`, o una rama compartida como `feature/validaciones`.
> Rebase = reescribir historia. Solo en ramas **tuyas**.

### 🚦 PE-13 — Avisa: «¡Actualicé mi rama con rebase y la subí!»

Espera: DevOps integrará ambas ramas en `main`.

### 4.6 Compara con Dev2

Cuando ambos hayan terminado:

```bash
git fetch
git log --oneline --graph --all --decorate -14
```

💡 Tu rama es una línea **recta** que sale de `main`. La de Dev2 lleva un **diamante** (merge de `main` dentro de su rama). Ambos resolvieron el mismo problema con resultados de historial distintos:

| | **Rebase** (tú) | **Merge** (Dev2) |
|---|---|---|
| Historial | Lineal, limpio | Con commit de merge |
| Commits | Reescritos (hash nuevos) | Intactos |
| Resolución | Commit por commit | Todo de una vez |
| Subida | `push --force-with-lease` | `push` normal |
| Riesgo | Alto si la rama es compartida | Bajo |

---

## 🧹 Parte 5 — Historial y limpieza

### 5.1 La red de seguridad: `reflog`

```bash
git reflog -8
```

👀

```
551a77c HEAD@{3}: rebase (finish): returning to refs/heads/feature/calculos
551a77c HEAD@{4}: rebase (continue): Usa multiplicar y dividir en el programa principal
0d15d8f HEAD@{5}: rebase (continue): Agrega multiplicar y dividir
7c30777 HEAD@{6}: rebase (start): checkout origin/main
71d1db5 HEAD@{7}: commit: Usa multiplicar y dividir en el programa principal
```

💡 `reflog` guarda cada movimiento de `HEAD`. Tu commit **original** `71d1db5` sigue ahí: si el rebase hubiera salido mal, podrías volver con `git reset --hard 71d1db5`.

### 5.2 Limpia las ramas integradas

Cuando DevOps avise que ya integró todo:

```bash
git fetch --prune
git switch main
git pull
git branch -vv
```

👀

```
From https://github.com/<usuario>/clase-git
 - [deleted]         (none)     -> origin/feature/matematicas
 - [deleted]         (none)     -> origin/feature/textos
   7c30777..fe369df  main       -> origin/main
 * [new tag]         v1.0       -> v1.0

Updating e681a97..fe369df
Fast-forward
 ...

  feature/calculos         551a77c [origin/feature/calculos] Usa multiplicar y dividir en el programa principal
  feature/matematicas      5a59c61 [origin/feature/matematicas: gone] Agrega funciones suma y resta
  feature/menu-matematicas c16366d [origin/feature/menu-matematicas] Agrega demo de matemáticas al programa principal
  feature/validaciones     58470fe [origin/feature/validaciones] Implementa es_numero con isdigit()
* main                     fe369df [origin/main] Merge feature/formato en main (conflicto en main.py resuelto)
```

💡 `: gone` indica que la rama remota **ya no existe** (fue borrada). Bórralas localmente:

```bash
git branch -d feature/matematicas feature/menu-matematicas feature/calculos feature/validaciones
```

👀

```
Deleted branch feature/matematicas (was 5a59c61).
Deleted branch feature/menu-matematicas (was c16366d).
Deleted branch feature/calculos (was 551a77c).
Deleted branch feature/validaciones (was 58470fe).
```

> ✅ `-d` solo borra ramas **ya integradas** (seguro). `-D` fuerza el borrado: úsalo solo si estás seguro.

---

## 🆘 «Me equivoqué»: tabla de rescate

| Situación | Comando | Efecto |
|---|---|---|
| Me enredé en un merge | `git merge --abort` | Vuelve a antes del merge |
| Me enredé en un rebase | `git rebase --abort` | Vuelve a antes del rebase |
| En un rebase, ese commit ya no me hace falta | `git rebase --skip` | Descarta ese commit |
| Quiero descartar cambios sin confirmar en un archivo | `git restore archivo.py` | ⚠️ Pierdes esos cambios |
| Hice `git add` por error | `git restore --staged archivo.py` | Lo saca del staging |
| Mi último commit tiene mal el mensaje (y no lo subí) | `git commit --amend -m "nuevo mensaje"` | Reescribe el último commit |
| Quiero deshacer un commit **ya subido** | `git revert <hash>` | Crea un commit que lo anula (seguro) |
| «Perdí» commits | `git reflog` → `git reset --hard <hash>` | Recupera ese punto |
| Push rechazado | `git fetch` → `merge` o `rebase` | Integra lo remoto primero |

---

## 🧾 Resumen de comandos que usaste

| Comando | Para qué |
|---|---|
| `git clone <url>` | Copiar un repo |
| `git switch -c <rama>` | Crear y cambiar de rama |
| `git add` / `git commit -m` | Preparar y confirmar cambios |
| `git push -u origin <rama>` | Subir una rama por primera vez |
| `git fetch` | Traer metadatos **sin** modificar tu trabajo |
| `git pull` | `fetch` + `merge` (solo si es avance limpio) |
| `git switch <rama>` | Crear local desde remota (si existe `origin/<rama>`) |
| `git log --oneline --graph --all --decorate` | Ver el grafo de historia |
| `git log A..B` / `git diff A...B` | Qué tiene B que A no |
| `git merge <rama>` | Integrar ramas (con commit de merge) |
| `git rebase <rama>` | Reproducir tus commits encima de otra base |
| `git rebase --continue / --abort / --skip` | Controlar un rebase en curso |
| `git push --force-with-lease` | Forzar push **de forma segura** tras un rebase |
| `git blame <archivo>` | Quién escribió cada línea |
| `git reflog` | Historial de movimientos de HEAD |
| `git branch -vv` / `-d` | Ver seguimiento / borrar rama integrada |

---

## ✅ Checklist final de Dev1

- [ ] Creé una rama, un commit y la subí con `push -u`
- [ ] Usé `fetch` y entendí la diferencia con `pull`
- [ ] Actualicé mi `main` con fast-forward
- [ ] Creé una rama local desde una remota
- [ ] Sufrí un `push` rechazado y lo resolví con **merge**
- [ ] Leí marcadores de conflicto (`HEAD` = yo, en un merge)
- [ ] Actualicé mi rama con **rebase** resolviendo 2 conflictos
- [ ] Entendí que en rebase `HEAD` = la base, y mi commit es el «entrante»
- [ ] Usé `push --force-with-lease` y sé por qué solo en ramas propias
- [ ] Limpié mis ramas

🎉 **¡Buen trabajo, Dev1!**
