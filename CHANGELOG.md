# Changelog

El historial de **decisiones** y **cambios** del proyecto, con su *por qué*.

- La entrada más reciente va **arriba**.
- Cada entrada es una *Decisión* (qué se eligió y por qué) o un *Cambio* (qué se
  consiguió en un paso).
- Las decisiones de partida no se repiten aquí: están en la tabla de la
  sección 4 de [CLAUDE.md](CLAUDE.md#4-decisiones-ya-tomadas).

---

## 2026-10-08

### Cambio · Paso 4: la hoja de estilos base
**Qué:** `web/styles.css` con el fondo de papel, el color de la tinta y las dos
tipografías (Georgia para los títulos, la letra del sistema para el resto),
enlazado desde `index.html`. Escrito a mano por Albert.
**Por qué:** separar el aspecto del contenido desde el principio. Los colores van
en variables para declararlos una sola vez.

### Decisión · Tipografías del sistema, sin Google Fonts
**Qué:** se usan las letras que ya tiene instalado el dispositivo.
**Por qué:** cargan al instante, no dependen de un servicio externo y no hay ningún
problema que justifique añadir una dependencia. Se revisa en el paso 20.

### Decisión · Nombres de fichero también en inglés
**Qué:** la regla de los nombres en inglés se amplía de las carpetas a los
ficheros (`styles.css`, `accounts.json`). El contenido sigue en castellano.
**Por qué:** Albert se siente más cómodo así, y una sola regla para carpetas y
ficheros evita mezclas.

### Cambio · Explicar en el README qué tipo de proyecto es
**Qué:** una sección nueva, "Sobre este proyecto", en el `README.md`.
**Por qué:** que quien llegue al repositorio sepa que es un proyecto de
aprendizaje, de contabilidad y de programación, y que está hecho con ayuda de
Claude.

## 2026-10-07

### Cambio · Paso 3: publicar en GitHub Pages
**Qué:** el repositorio se sube a GitHub como `contabilidad-pgc` (público) y la
web se publica con GitHub Pages.
**Por qué:** a partir de aquí cada mejora se puede ver publicada el mismo día y
compartir con un enlace.

### Decisión · Firmar los commits con el correo noreply de GitHub
**Qué:** git usa `202819105+AlbertSubirats@users.noreply.github.com` como correo,
y los dos primeros commits se rehicieron con `git rebase` para llevarlo.
**Por qué:** el repositorio es público y el correo de cada commit lo puede ver
cualquiera, incluidos los programas que buscan correos para enviar spam. Se hizo
antes del primer `push` porque reescribir commits ya publicados rompe la historia.

### Cambio · Paso 2: la primera página
**Qué:** `web/index.html` con un título y un párrafo. Escrita a mano por Albert.
**Por qué:** es la base sobre la que se construirá toda la web, y la página que
se publicará en el paso 3.

### Cambio · Paso 1: arrancar el repositorio
**Qué:** la carpeta pasa a ser un repositorio de git, con un `.gitignore` y un
`README.md`. Primer commit del proyecto.
**Por qué:** a partir de aquí cada paso queda guardado como una foto del proyecto
entero, y se puede volver a cualquiera de ellas.

### Decisión · Nombres de carpeta en inglés
**Qué:** las carpetas se llaman `sources/`, `data/`, `tools/`, `web/` y `docs/`.
Todo en minúscula y el changelog en la raíz. El contenido de los ficheros sigue en
castellano.
**Por qué:** es la costumbre en la mayoría de proyectos de software, y con una
regla única no hay que recordar excepciones. La minúscula evita errores al
publicar: Windows no distingue mayúsculas de minúsculas, pero GitHub sí.

### Decisión · Llevar un changelog
**Qué:** crear este fichero y actualizarlo al terminar cada paso.
**Por qué:** git dirá *qué* cambió en cada commit, pero no *por qué*. Este
fichero guarda las razones, para poder entenderlas meses después.