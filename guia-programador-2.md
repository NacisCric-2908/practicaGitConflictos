# 👨‍💻 Guía Programador 2 — Clase de Git: merge, rebase y resolución de conflictos

> **Tu rol:** eres **Dev2**. Trabajas en tus propias ramas, subes tu código a GitHub y resuelves los conflictos que aparezcan cuando tu trabajo choca con el de Dev1 o con los cambios de `main`.
>
> **Proyecto:** *Mini Utilidades*, un programa pequeño en Python. Tu especialidad: **textos** (`textos.py`).
>
> **Tu estilo de resolución:** en la Parte 3 usarás **rebase**; en la Parte 4 usarás **merge**. (Dev1 hará lo contrario: así cada uno practica ambos.)

---

## 📌 Cómo leer esta guía

Cada paso tiene este formato:

- **🎯 Qué vamos a hacer** — la idea.
- **⌨️ Comando** — lo que escribes.
- **👀 Qué deberías ver** — salida aproximada de la terminal.
- **💡 Por qué** — el concepto detrás.

> ⚠️ **Los hashes cambian.** Códigos como `ab7e453` serán distintos en tu máquina. Fíjate en la *forma* de la salida, no en los números.

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
git config --global user.name "Dev Dos"
git config --global user.email "dev2@clase.com"
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

```bash
python main.py
```

👀 `Bienvenido a Mini Utilidades`

---

## 🌱 Parte 1 — Tu rama, tu archivo (sin conflictos)

**Situación:** tú creas `textos.py` en `feature/textos`; Dev1 crea `matematicas.py` en otra rama. No se tocan.

### 1.1 Crea tu rama

🎯 Nunca se trabaja directo en `main`. Cada tarea tiene su rama.

```bash
git switch -c feature/textos
```

👀

```
Switched to a new branch 'feature/textos'
```

💡 `-c` = *create*. Equivale a `git branch feature/textos` + `git switch feature/textos`.

### 1.2 Crea `textos.py`

```python
"""Utilidades para manejo de texto."""


def mayusculas(texto):
    return texto.upper()


def invertir(texto):
    return texto[::-1]
```

```bash
git status
```

👀

```
On branch feature/textos
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	textos.py

nothing added to commit but untracked files present (use "git add" to track)
```

### 1.3 Confirma el cambio (add + commit)

```bash
git add textos.py
git status -s
git commit -m "Agrega funciones mayusculas e invertir"
```

👀

```
A  textos.py

[feature/textos ab7e453] Agrega funciones mayusculas e invertir
 1 file changed, 9 insertions(+)
 create mode 100644 textos.py
```

💡 **Las tres zonas de Git:**

```
 Directorio de trabajo  ──git add──▶  Staging  ──git commit──▶  Repositorio local  ──git push──▶  GitHub
```

### 1.4 Sube tu rama

```bash
git push -u origin feature/textos
```

👀

```
To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/textos -> feature/textos
branch 'feature/textos' set up to track 'origin/feature/textos'.
```

💡 `-u` enlaza tu rama local con la remota. Después basta con `git push` y `git pull`.

```bash
git branch -vv
```

👀

```
* feature/textos ab7e453 [origin/feature/textos] Agrega funciones mayusculas e invertir
  main           eba20f0 [origin/main] Commit inicial: estructura base del proyecto
```

### 🚦 PE-2 — Avisa: «¡Subí mi rama!»

Espera a que DevOps avise el **PE-3**.

---

## ⚔️ Parte 2 — Mismo archivo, ramas distintas

**Situación:** tú y Dev1 editarán `main.py` **en las mismas líneas**, cada uno en su rama. El conflicto lo resolverá DevOps en `main`. Tu trabajo: partir de un `main` actualizado y subir tu rama.

### 2.1 Trae los metadatos con `fetch`

🎯 Ver qué pasó en GitHub **sin tocar tus archivos**.

```bash
git fetch
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/matematicas -> origin/feature/matematicas
   eba20f0..6fe928b  main                -> origin/main
```

💡 **`fetch` vs `pull`:**

| Comando | Qué hace | ¿Toca tus archivos? |
|---|---|---|
| `git fetch` | Descarga las novedades a las ramas `origin/*` | ❌ No |
| `git pull` | `fetch` **+** `merge` sobre la rama actual | ✅ Sí |

### 2.2 Mira qué cambió antes de integrar

```bash
git log --oneline --graph --all --decorate
```

👀

```
*   6fe928b (origin/main, origin/HEAD) Merge feature/textos en main
|\
| * ab7e453 (HEAD -> feature/textos, origin/feature/textos) Agrega funciones mayusculas e invertir
* |   9bc3675 Merge feature/matematicas en main
|\ \
| |/
|/|
| * 5a59c61 (origin/feature/matematicas) Agrega funciones suma y resta
|/
* eba20f0 (main) Commit inicial: estructura base del proyecto
```

💡 DevOps ya integró nuestras ramas en `origin/main`. Tu `main` **local** (`eba20f0`) está atrasado.

```bash
git switch main
git log --oneline main..origin/main
git diff --stat main origin/main
```

👀

```
Switched to branch 'main'
Your branch is behind 'origin/main' by 4 commits, and can be fast-forwarded.

6fe928b Merge feature/textos en main
9bc3675 Merge feature/matematicas en main
ab7e453 Agrega funciones mayusculas e invertir
5a59c61 Agrega funciones suma y resta

 matematicas.py | 9 +++++++++
 textos.py      | 9 +++++++++
 2 files changed, 18 insertions(+)
```

💡 `A..B` = «commits que están en B y no en A».

### 2.3 Actualiza tu `main` local

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

💡 **Fast-forward** = tu `main` no tenía nada propio; Git solo avanzó el puntero. Sin merge ni conflicto.

### 2.4 Crea tu nueva rama y edita `main.py`

```bash
git switch -c feature/menu-textos
```

Reemplaza **todo** `main.py` por:

```python
"""Programa principal de Mini Utilidades."""

from textos import mayusculas, invertir


def main():
    print("Bienvenido a Mini Utilidades")
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))


if __name__ == "__main__":
    main()
```

```bash
python main.py
git add main.py
git commit -m "Agrega demo de textos al programa principal"
git push -u origin feature/menu-textos
```

👀

```
Bienvenido a Mini Utilidades
En mayúsculas: HOLA
Invertido: aloh

[feature/menu-textos f687312] Agrega demo de textos al programa principal
 1 file changed, 4 insertions(+)

To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/menu-textos -> feature/menu-textos
branch 'feature/menu-textos' set up to track 'origin/feature/menu-textos'.
```

### 🚦 PE-4 — Avisa: «¡Subí `feature/menu-textos`!»

DevOps hará los merges y resolverá el conflicto. Espera el **PE-5**.

### 2.5 Mira cómo DevOps resolvió el conflicto

```bash
git fetch
git switch main
git pull
git log --merges --oneline
```

👀

```
f7b4b30 Merge feature/menu-textos en main (conflicto resuelto en main.py)
e8d576c Merge feature/menu-matematicas en main
6fe928b Merge feature/textos en main
9bc3675 Merge feature/matematicas en main
```

```bash
python main.py
```

👀 Ahora el programa combina **tu trabajo y el de Dev1**:

```
Bienvenido a Mini Utilidades
Suma de 2 + 3 = 5
Resta de 5 - 1 = 4
En mayúsculas: HOLA
Invertido: aloh
```

---

## 👥 Parte 3 — Misma rama, mismo archivo (¡dos rondas de choque!)

**Situación:** tú y Dev1 trabajan **en la misma rama remota** (`feature/validaciones`), en el mismo archivo.

- **Ronda A:** tú subes primero → Dev1 choca → él resuelve con merge.
- **Ronda B:** Dev1 sube primero → **tú** chocas → resuelves con **rebase**.

### 🚦 Espera el PE-6 («`feature/validaciones` publicada»)

### 3.1 Crea tu rama local a partir de la remota

🎯 La rama ya existe en GitHub; necesitas una copia local que la siga.

```bash
git fetch
git branch -a
```

👀

```
* feature/menu-textos
  feature/textos
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

  feature/menu-textos  f687312 [origin/feature/menu-textos] Agrega demo de textos al programa principal
  feature/textos       ab7e453 [origin/feature/textos] Agrega funciones mayusculas e invertir
* feature/validaciones 2c6162b [origin/feature/validaciones] Agrega esqueleto de validaciones
  main                 6fe928b [origin/main: behind 4] Merge feature/textos en main
```

💡 Otras formas equivalentes: `git switch -c feature/validaciones --track origin/feature/validaciones` o la antigua `git checkout -b feature/validaciones origin/feature/validaciones`.

El archivo base (de DevOps):

```python
"""Funciones de validación de datos."""


def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    pass
```

---

### 🅰️ Ronda A — Tú subes primero (todo sale bien)

#### 3.2 Haz tu cambio, confirma y **sube**

Agrega **al final** de `validaciones.py` (con dos líneas en blanco antes):

```python


def es_vacio(texto):
    """Devuelve True si el texto está vacío o solo tiene espacios."""
    return texto.strip() == ""
```

```bash
git add validaciones.py
git commit -m "Agrega validación es_vacio"
git push
```

👀

```
[feature/validaciones 00a9c0c] Agrega validación es_vacio
 1 file changed, 5 insertions(+)

To https://github.com/<usuario>/clase-git.git
   2c6162b..00a9c0c  feature/validaciones -> feature/validaciones
```

💡 Subió sin problema porque el remoto no tenía nada nuevo que tú no conocieras: fue un avance limpio.

### 🚦 PE-7 — Avisa: «¡Ya subí!»

Dev1 intentará subir y chocará. Tú **espera** el **PE-8** («resolví y subí»).

#### 3.3 Ponte al día (cuando Dev1 avise)

Primero **mira** lo que llegó:

```bash
git fetch
git log --oneline HEAD..origin/feature/validaciones
git diff --stat HEAD origin/feature/validaciones
```

👀

```
From https://github.com/<usuario>/clase-git
   00a9c0c..90fe344  feature/validaciones -> origin/feature/validaciones

90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
39fb13a Agrega validación es_positivo

 validaciones.py | 5 +++++
 1 file changed, 5 insertions(+)
```

Ahora sí:

```bash
git pull
```

👀

```
Updating 00a9c0c..90fe344
Fast-forward
 validaciones.py | 5 +++++
 1 file changed, 5 insertions(+)
```

💡 Tú no tenías commits propios nuevos, así que es un **fast-forward**: el `pull` no puede dar conflicto. Ya estás sincronizado.

---

### 🅱️ Ronda B — Dev1 sube primero, tú chocas (resolución con REBASE)

**Ahora ambos modificarán la misma función (`es_numero`).**

#### 3.4 Implementa `es_numero` (con `isdigit`)

En `validaciones.py`, reemplaza el `pass` de `es_numero`:

```python
def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    return texto.isdigit()
```

```bash
git add validaciones.py
git commit -m "Implementa es_numero con isdigit()"
```

👀

```
[feature/validaciones 5a26e8f] Implementa es_numero con isdigit()
 1 file changed, 1 insertion(+), 1 deletion(-)
```

> ⛔ **No hagas push.** Avisa: «tengo mi commit listo» y espera a que **Dev1 suba primero (🚦 PE-9)**.

#### 3.5 Intenta subir… ¡rechazado!

```bash
git push
```

👀

```
To https://github.com/<usuario>/clase-git.git
 ! [rejected]        feature/validaciones -> feature/validaciones (fetch first)
error: failed to push some refs to 'https://github.com/<usuario>/clase-git.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. ...
```

💡 GitHub tiene un commit de Dev1 que tú no tienes. Git no te deja sobrescribirlo.

#### 3.6 `fetch` y examina

```bash
git fetch
git status -sb
git log --oneline --graph --all --decorate -5
```

👀

```
From https://github.com/<usuario>/clase-git
   90fe344..a07dabe  feature/validaciones -> origin/feature/validaciones

## feature/validaciones...origin/feature/validaciones [ahead 1, behind 1]

* 5a26e8f (HEAD -> feature/validaciones) Implementa es_numero con isdigit()
| * a07dabe (origin/feature/validaciones) Implementa es_numero con float()
|/
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
```

💡 `[ahead 1, behind 1]`: tienes 1 commit que el remoto no tiene y viceversa → **divergieron**.

#### 3.7 Integra con `rebase`

🎯 Quitar temporalmente **tu** commit, avanzar tu rama hasta lo que tiene el remoto y volver a aplicar tu commit encima.

```
ANTES                                  DESPUÉS DEL REBASE
 90fe344──a07dabe  (origin, Dev1)       90fe344──a07dabe──5a26e8f'  (tú)
        \                                         (origin)
         5a26e8f   (tú)
```

```bash
git rebase origin/feature/validaciones
```

👀

```
Rebasing (1/1)
Auto-merging validaciones.py
CONFLICT (content): Merge conflict in validaciones.py
error: could not apply 5a26e8f... Implementa es_numero con isdigit()
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply 5a26e8f... Implementa es_numero con isdigit()
```

```bash
git status
```

👀

```
interactive rebase in progress; onto a07dabe
Last command done (1 command done):
   pick 5a26e8f Implementa es_numero con isdigit()
No commands remaining.
You are currently rebasing branch 'feature/validaciones' on 'a07dabe'.
  (fix conflicts and then run "git rebase --continue")
  ...
Unmerged paths:
	both modified:   validaciones.py
```

Abre `validaciones.py`:

```python
def es_numero(texto):
    """Devuelve True si el texto representa un número."""
<<<<<<< HEAD
    try:
        float(texto)
        return True
    except ValueError:
        return False
=======
    return texto.isdigit()
>>>>>>> 5a26e8f (Implementa es_numero con isdigit())
```

> 🔄 **¡OJO! En un rebase los lados están «invertidos» respecto al merge:**
>
> | Marcador | En un **merge** | En un **rebase** |
> |---|---|---|
> | `<<<<<<< HEAD` | **Tu** trabajo | El trabajo **del remoto (Dev1)**: la base sobre la que se reproduce |
> | `>>>>>>> <commit>` | Lo de la otra rama | **Tu** commit que se está reproduciendo |
>
> Aquí `HEAD` es la versión de **Dev1** (`float`) y tu commit es el «entrante» (`isdigit`).

**¿Cuál gana?** Piensa en el código: `isdigit()` **falla** con `"3.5"` y con `"-2"`, así que la versión de Dev1 (`float`) es más completa. Pero tu idea también aporta algo: rechazar **explícitamente** el texto vacío o de solo espacios (justo lo que ya valida `es_vacio`). **Combina las dos ideas.** Deja:

```python
def es_numero(texto):
    """Devuelve True si el texto representa un número."""
    if texto.strip() == "":
        return False
    try:
        float(texto)
        return True
    except ValueError:
        return False
```

> ⚠️ **Trampa frecuente:** si resuelves dejando **exactamente** el código de Dev1 (sin aportar nada tuyo), tu commit queda **vacío** y Git lo **descarta** en silencio al continuar el rebase. No es un error, pero tu trabajo «desaparece». Por eso conviene que tu resolución aporte algo.

Prueba, marca como resuelto y continúa:

```bash
python -c "from validaciones import es_numero; print(es_numero('3.5'), es_numero('abc'), es_numero(''))"
git add validaciones.py
git rebase --continue
```

👀

```
True False False

Successfully rebased and updated refs/heads/feature/validaciones.
```

> ✏️ Si se abre un editor pidiendo confirmar el mensaje, guarda y cierra. *(El mensaje dirá «con isdigit()» aunque ya no lo uses; en un equipo real lo corregirías con `git commit --amend`.)*

> 🆘 **¿Te enredaste?** `git rebase --abort` te devuelve al estado previo al rebase.

```bash
git status -sb
git log --oneline --graph -5
```

👀 Una línea **recta**; tu commit tiene un hash nuevo:

```
## feature/validaciones...origin/feature/validaciones [ahead 1]

* 58470fe Implementa es_numero con isdigit()
* a07dabe Implementa es_numero con float()
*   90fe344 Merge origin/feature/validaciones: conserva es_vacio y es_positivo
|\
| * 00a9c0c Agrega validación es_vacio
```

#### 3.8 Sube (esta vez sin forzar)

```bash
git push
```

👀

```
To https://github.com/<usuario>/clase-git.git
   a07dabe..58470fe  feature/validaciones -> feature/validaciones
```

💡 **¿Por qué no necesité `--force`?** Porque tu commit ahora está **encima** de lo que ya tenía el remoto (`a07dabe`). Para GitHub es un avance normal (fast-forward). Solo se fuerza cuando reescribes commits que **ya estaban subidos** (¡lo verá Dev1 en la Parte 4!).

### 🚦 PE-10 — Avisa: «¡Resolví con rebase y subí!»

DevOps integrará la rama en `main`. Espera su aviso: «`main` ya tiene `validaciones.py`».

---

## 🔄 Parte 4 — `main` cambia mientras trabajas (¡usarás MERGE!)

**Situación:** creas `feature/formato` y la subes. DevOps **modifica `main`** en varios archivos. Tu rama queda desactualizada y habrá conflictos en **dos archivos**. Los resolverás con **merge**.

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
git switch -c feature/formato
```

**Commit 1 — `textos.py`:** agrega **al final**:

```python


def capitalizar(texto):
    return texto.capitalize()


def contar_palabras(texto):
    return len(texto.split())
```

```bash
git add textos.py
git commit -m "Agrega capitalizar y contar_palabras"
```

**Commit 2 — `main.py`:** cambia el import de `textos`, decora el saludo y agrega 2 líneas al final de `main()`. El archivo completo queda:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta
from textos import mayusculas, invertir, capitalizar, contar_palabras


def main():
    print("Bienvenido a Mini Utilidades 🐍")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
    print("Capitalizado:", capitalizar("hola mundo"))
    print("Palabras:", contar_palabras("hola mundo cruel"))


if __name__ == "__main__":
    main()
```

```bash
python main.py
git add main.py
git commit -m "Usa capitalizar y contar_palabras en el programa principal"
git push -u origin feature/formato
```

👀

```
[feature/formato 0191ee0] Agrega capitalizar y contar_palabras
 1 file changed, 8 insertions(+)
[feature/formato c1407f1] Usa capitalizar y contar_palabras en el programa principal
 1 file changed, 4 insertions(+), 2 deletions(-)

To https://github.com/<usuario>/clase-git.git
 * [new branch]      feature/formato -> feature/formato
branch 'feature/formato' set up to track 'origin/feature/formato'.
```

### 🚦 PE-11 — Avisa: «¡Subí `feature/formato`!»

DevOps cambiará `main` ahora. Espera el **PE-12**.

### 4.3 Detecta que `main` se movió

```bash
git fetch
git status -sb
```

👀

```
From https://github.com/<usuario>/clase-git
 * [new branch]      feature/calculos -> origin/feature/calculos
   e681a97..7c30777  main             -> origin/main

## feature/formato...origin/feature/formato
```

💡 El `status` dice «limpio» porque compara con **tu** remota. Para saber si `main` avanzó:

```bash
git log --oneline HEAD..origin/main
git diff --stat HEAD...origin/main
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
```

💡 DevOps tocó `main.py` y `textos.py` (¡tu archivo!), además de `README.md` y `matematicas.py`. Habrá choques en los dos primeros.

> 💼 **Bonus (stash):** ¿y si tuvieras cambios **sin confirmar** justo ahora? Git podría negarse a mezclar. Mira la sección 5.3.

### 4.4 Merge: «trae `main` hacia mi rama»

```bash
git merge origin/main
```

👀

```
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Auto-merging textos.py
CONFLICT (content): Merge conflict in textos.py
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
git status
```

👀

```
On branch feature/formato
Your branch is up to date with 'origin/feature/formato'.

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Changes to be committed:
	modified:   README.md
	modified:   matematicas.py

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   main.py
	both modified:   textos.py
```

💡 **Lee el status con calma:**
- `Changes to be committed` → archivos que Git **fusionó solo** (`README.md`, `matematicas.py`: nadie más los tocó donde tú los tocaste). No requieren acción.
- `Unmerged paths` → solo **esos dos** necesitan tu decisión.

> 🆘 Salida de emergencia: `git merge --abort` (vuelve a antes del merge).

#### Conflicto 1: `textos.py`

```python
<<<<<<< HEAD
def capitalizar(texto):
    return texto.capitalize()


def contar_palabras(texto):
    return len(texto.split())
=======
def es_palindromo(texto):
    """Devuelve True si el texto se lee igual al derecho y al revés."""
    limpio = texto.replace(" ", "").lower()
    return limpio == limpio[::-1]
>>>>>>> origin/main
```

💡 En un **merge**, `HEAD` = tu rama (tus funciones) y el otro lado = `origin/main` (la `es_palindromo` de DevOps). Conserva ambas:

```python
def capitalizar(texto):
    return texto.capitalize()


def contar_palabras(texto):
    return len(texto.split())


def es_palindromo(texto):
    """Devuelve True si el texto se lee igual al derecho y al revés."""
    limpio = texto.replace(" ", "").lower()
    return limpio == limpio[::-1]
```

#### Conflicto 2: `main.py` (¡dos bloques!)

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta
<<<<<<< HEAD
from textos import mayusculas, invertir, capitalizar, contar_palabras


def main():
    print("Bienvenido a Mini Utilidades 🐍")
=======
from textos import mayusculas, invertir
from validaciones import es_numero


def main():
    print("=== Mini Utilidades v1.0 ===")
>>>>>>> origin/main
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))
<<<<<<< HEAD
    print("Capitalizado:", capitalizar("hola mundo"))
    print("Palabras:", contar_palabras("hola mundo cruel"))
=======
    print("¿'42' es un número?", es_numero("42"))
>>>>>>> origin/main


if __name__ == "__main__":
    main()
```

Aquí **no basta con «quedarte con uno»**. Hay que **construir** el resultado correcto:

- **Imports:** tu línea de `textos` (con `capitalizar, contar_palabras`) **+** el `import` de `validaciones` de DevOps.
- **Saludo:** DevOps cambió el encabezado a `v1.0`; tú lo habías decorado con 🐍. Decidimos **respetar el de DevOps** (es el nombre oficial).
- **Final de `main()`:** conserva las líneas de ambos.

Resultado:

```python
"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta
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


if __name__ == "__main__":
    main()
```

```bash
python main.py
```

👀

```
=== Mini Utilidades v1.0 ===
Suma de 2 + 3 = 5
Resta de 5 - 1 = 4
En mayúsculas: HOLA
Invertido: aloh
Capitalizado: Hola mundo
Palabras: 3
¿'42' es un número? True
```

> 🔎 Antes de continuar, busca que no queden marcadores:
> ```bash
> git grep -nE "^(<<<<<<<|=======|>>>>>>>)" -- '*.py'
> ```
> Si no imprime nada, ¡estás limpio! (Si imprime líneas, te falta quitar algún marcador.)

#### Cierra el merge y sube

```bash
git add main.py textos.py
git status
git commit -m "Merge origin/main en feature/formato (conflictos resueltos)"
git push
```

👀

```
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   README.md
	modified:   main.py
	modified:   matematicas.py
	modified:   textos.py

[feature/formato c9aeeb7] Merge origin/main en feature/formato (conflictos resueltos)

To https://github.com/<usuario>/clase-git.git
   c1407f1..c9aeeb7  feature/formato -> feature/formato
```

```bash
git log --oneline --graph -8
```

👀 El «diamante» del merge:

```
*   c9aeeb7 Merge origin/main en feature/formato (conflictos resueltos)
|\
| * 7c30777 Documenta cómo ejecutar el proyecto
| * 555c57a Agrega potencia y es_palindromo; documenta suma y resta
| * ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
* | c1407f1 Usa capitalizar y contar_palabras en el programa principal
* | 0191ee0 Agrega capitalizar y contar_palabras
|/
*   e681a97 Merge feature/validaciones en main
```

💡 Un solo `commit` resolvió **todo**; y el `push` fue normal (sin `--force`) porque no reescribiste nada.

### 🚦 PE-13 — Avisa: «¡Actualicé mi rama con merge y la subí!»

Espera: DevOps integrará ambas ramas.

### 4.5 Compara con Dev1

```bash
git fetch
git log --oneline --graph --all --decorate -14
```

| | **Merge** (tú) | **Rebase** (Dev1) |
|---|---|---|
| Historial | Con commit de merge (diamante) | Lineal, limpio |
| Commits | Intactos | Reescritos (hash nuevos) |
| Resolución | Todo de una vez | Commit por commit |
| Subida | `push` normal | `push --force-with-lease` |
| Riesgo | Bajo | Alto si la rama es compartida |

---

## 🔍 Parte 5 — Historial, stash y limpieza

### 5.1 Explora el historial

Cuando DevOps haya integrado todo:

```bash
git fetch --prune
git switch main
git pull
```

```bash
git log --author="Dev Dos" --oneline     # solo mis commits
git log -S"es_palindromo" --oneline      # ¿cuándo apareció esta palabra?
git shortlog -sn --no-merges HEAD        # commits por persona
git show --stat HEAD                     # detalle del último commit
git log --first-parent --oneline -6      # solo la «línea principal» de main
git log --merges --oneline               # solo los merges
```

👀 Ejemplos de salidas:

```
555c57a Agrega potencia y es_palindromo; documenta suma y resta

     6	Dev Dos
     6	Dev Uno
     5	DevOps

fe369df Merge feature/formato en main (conflicto en main.py resuelto)
ef7cf75 Merge feature/calculos en main
7c30777 Documenta cómo ejecutar el proyecto
555c57a Agrega potencia y es_palindromo; documenta suma y resta
ebd9dfc Actualiza main.py: encabezado v1.0 y uso de es_numero
e681a97 Merge feature/validaciones en main
```

💡 `-S"texto"` («pickaxe») encuentra el commit que **añadió o quitó** esa palabra. Oro puro para investigar bugs.

### 5.2 Mira qué cambió en un archivo (`diff` y `restore`)

```bash
echo "x" >> main.py
git diff
```

👀

```
diff --git a/main.py b/main.py
--- a/main.py
+++ b/main.py
@@ -22,3 +22,4 @@ def main():
 
 if __name__ == "__main__":
     main()
+x
```

Descarta el cambio:

```bash
git restore main.py
git status -sb
```

👀 `## main...origin/main` (limpio otra vez).

### 5.3 Bonus: `git stash` («guarda mis cambios en un cajón»)

🎯 Tienes cambios a medias y necesitas cambiar de rama o traer cosas nuevas **sin hacer commit**.

```bash
echo "# nota temporal" >> README.md
git status -s
git stash
git status -s
git stash list
```

👀

```
 M README.md

Saved working directory and index state WIP on main: fe369df Merge feature/formato en main (conflicto en main.py resuelto)

stash@{0}: WIP on main: fe369df Merge feature/formato en main (conflicto en main.py resuelto)
```

El segundo `git status -s` no imprime nada: el directorio quedó **limpio**. Ahora ya puedes cambiar de rama, hacer `pull`, etc. Para recuperar tus cambios:

```bash
git stash pop
git restore README.md      # (solo para limpiar el ejemplo)
```

👀

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
	modified:   README.md
```

### 5.4 Limpia tus ramas

```bash
git branch -vv
git branch -d feature/textos feature/menu-textos feature/validaciones feature/formato
```

👀

```
Deleted branch feature/textos (was ab7e453).
Deleted branch feature/menu-textos (was f687312).
Deleted branch feature/validaciones (was 58470fe).
Deleted branch feature/formato (was c9aeeb7).
```

> ✅ `-d` solo borra ramas **ya integradas** (seguro). `-D` fuerza el borrado: úsalo solo si estás seguro.

---

## 🆘 «Me equivoqué»: tabla de rescate

| Situación | Comando | Efecto |
|---|---|---|
| Me enredé en un merge | `git merge --abort` | Vuelve a antes del merge |
| Me enredé en un rebase | `git rebase --abort` | Vuelve a antes del rebase |
| En un rebase, mi commit quedó vacío | `git rebase --skip` (o `--continue`) | Git lo descarta |
| Descartar cambios sin confirmar en un archivo | `git restore archivo.py` | ⚠️ Pierdes esos cambios |
| Hice `git add` por error | `git restore --staged archivo.py` | Lo saca del staging |
| El mensaje de mi último commit está mal (y no lo subí) | `git commit --amend -m "nuevo mensaje"` | Reescribe el último commit |
| Quiero deshacer un commit **ya subido** | `git revert <hash>` | Crea un commit que lo anula (seguro) |
| «Perdí» commits | `git reflog` → `git reset --hard <hash>` | Recupera ese punto |
| Tengo cambios a medias y necesito cambiar de rama | `git stash` / `git stash pop` | Los guarda y los recupera |
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
| `git pull` | `fetch` + `merge` (con `pull.ff only`: solo avance limpio) |
| `git switch <rama>` | Crear local desde remota (si existe `origin/<rama>`) |
| `git log --oneline --graph --all --decorate` | Ver el grafo de historia |
| `git log A..B` / `git diff A...B` | Qué tiene B que A no |
| `git rebase <rama>` | Reproducir tus commits encima de otra base |
| `git rebase --continue / --abort / --skip` | Controlar un rebase en curso |
| `git merge <rama>` | Integrar ramas (con commit de merge) |
| `git merge --abort` | Cancelar un merge en conflicto |
| `git stash` / `git stash pop` | Guardar y recuperar cambios a medias |
| `git log -S"texto"` / `--author` | Buscar en el historial |
| `git branch -d` | Borrar rama integrada |

---

## ✅ Checklist final de Dev2

- [ ] Creé una rama, un commit y la subí con `push -u`
- [ ] Usé `fetch` y entendí la diferencia con `pull`
- [ ] Actualicé mi `main` con fast-forward
- [ ] Creé una rama local desde una remota
- [ ] Hice `push` primero y me puse al día con un `pull` limpio
- [ ] Sufrí un `push` rechazado y lo resolví con **rebase**
- [ ] Entendí que en rebase `HEAD` = la base, y mi commit es el «entrante»
- [ ] Sé por qué esta vez **no** necesité `--force`
- [ ] Actualicé mi rama con **merge** resolviendo conflictos en 2 archivos
- [ ] Usé `stash`, `log -S` y `shortlog`
- [ ] Limpié mis ramas

🎉 **¡Buen trabajo, Dev2!**
