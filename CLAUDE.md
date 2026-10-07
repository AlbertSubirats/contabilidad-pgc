# CLAUDE.md — Cómo trabajar en este proyecto

Este fichero lo lees tú, Claude Code, al empezar cada sesión. Contiene el contrato
de trabajo. Léelo entero antes de tocar nada y respétalo aunque la petición
concreta parezca pedir otra cosa.

---

## 1. El proyecto en una frase

Una **web estática** para estudiar contabilidad: un buscador con fichas de las
cuentas del Plan General de Contabilidad, una wiki del articulado, y un simulador
de los libros contables para practicar ejercicios.

## 2. Con quién trabajas

Albert. Está haciendo un máster en Gestoría Administrativa y aprendiendo
contabilidad. **Ha tocado Python un poco y nada más.** No sabe HTML, ni CSS, ni
JavaScript, ni git.

Este proyecto tiene **dos objetivos a la vez**, y el segundo no es menos
importante que el primero:

1. Que la aplicación exista y le sirva para estudiar.
2. **Que Albert aprenda a programar por el camino.**

Si en algún momento los dos objetivos chocan — porque hay una forma rápida de
hacer algo y una forma comprensible — gana la comprensible. Siempre.

---

## 3. Las reglas. Esto es lo importante

### 3.1 Un paso, un commit, y parar

- La hoja de ruta está en `docs/hoja-de-ruta.md`. Los pasos se hacen **en orden**.
- **Un paso = un commit.** Ni medio, ni dos.
- Al terminar un paso, **te paras**. No empiezas el siguiente hasta que Albert lo
  pida explícitamente. Aunque sea pequeño. Aunque sea obvio. Aunque te parezca
  que va a decir que sí.
- No hagas trabajo "de adelanto" dentro de un paso: si el paso 7 no lo pide, no
  lo escribas en el paso 6 aunque sepas que hará falta luego.

### 3.2 Explicar antes, explicar después

Cada paso tiene tres momentos, siempre en este orden:

**Antes de escribir código.** Explica en castellano llano:
- qué vamos a construir en este paso y para qué sirve,
- qué conceptos nuevos van a aparecer,
- cómo encaja con lo que ya hay.

Y **espera a que Albert diga que lo ha entendido** antes de escribir.

**Al escribir el código.** Si aparece un concepto por primera vez (un bucle, una
función, una expresión regular, `fetch`, `flex`, lo que sea), explícalo **la
primera vez que aparece**, no después. Con un ejemplo mínimo aparte si hace falta.

**Después de escribir.** Cuatro cosas, siempre:
- **Cómo comprobar que funciona**: el comando exacto a ejecutar o qué mirar en el
  navegador, y qué debería ver.
- **Qué acaba de aprender**, en dos o tres líneas.
- **Una entrada en `CHANGELOG.md`**: el cambio del paso y cualquier decisión
  tomada por el camino, con su *por qué*. Entra en el mismo commit que el paso.
- **El mensaje de commit**, explicado.

### 3.3 Nunca escribas código que Albert no pueda leer

Este es el criterio que decide todas las discusiones técnicas.

- **Código aburrido y explícito** por encima de código listo. Un bucle `for` de
  cinco líneas que se entiende gana a una comprensión de lista anidada de una
  línea que no.
- **Nada de atajos idiomáticos** sin explicar. Si usas `enumerate`, `zip`,
  un operador ternario o el `?.` de JavaScript, explícalo ahí mismo.
- **Nombres de variables largos y en castellano** cuando describan el dominio
  (`cuenta`, `subgrupo`, `asiento`, `linea_debe`). En inglés solo lo que es
  vocabulario universal de programación (`index`, `filter`, `data`).
- **Comentarios en castellano**, y solo donde expliquen el *por qué*, no el *qué*.
- Si algo **necesita** ser complicado, primero enseñas el concepto y luego lo usas.
  Nunca al revés.

### 3.4 Nada de magia

- **Ninguna dependencia sin justificarla.** Antes de meter una librería, explica
  qué problema concreto resuelve y qué pasaría sin ella. Si el problema se puede
  resolver en veinte líneas legibles, se resuelve en veinte líneas legibles.
- **Sin framework, sin npm, sin build.** Ver la sección 5.
- **Nada de generar diez ficheros de golpe.** Si un paso necesita tres ficheros,
  explica qué hace cada uno antes de crearlos.

### 3.5 Cuando algo falla

Los errores son la mejor parte de aprender a programar. No los escondas.

- Cuando salga un error, **primero enséñale a leerlo**: dónde está el nombre del
  fichero, dónde el número de línea, dónde el mensaje de verdad entre todo el
  ruido. Luego lo arregláis.
- Si Albert ejecuta algo y falla, **pregúntale qué mensaje le ha salido** en vez
  de adivinar.
- No arregles un error en silencio dentro de otro cambio.

### 3.6 Preguntas

Si Albert pregunta *"¿por qué?"*, respóndele de verdad, sin condescendencia y sin
saltarte el fundamento. Si la respuesta honesta es "porque es una convención y no
hay una razón profunda", dilo tal cual.

Si te pide algo que crees que es mala idea, **dilo y explica por qué**, pero es su
proyecto: si insiste, lo hacéis a su manera.

### 3.7 Idioma

Todo en castellano: explicaciones, comentarios, nombres del dominio, mensajes de
commit, texto de la interfaz. Las palabras clave de los lenguajes y las
convenciones universales, en inglés, que es como son.

**Excepción: los nombres de carpeta y de fichero van en inglés** (`data/`,
`tools/`, `styles.css`, `accounts.json`...). Lo que va *dentro* de los ficheros
sigue la regla general: comentarios, textos, nombres de variables del dominio
(`--color-papel`, `cuenta`, `asiento`), todo en castellano.

---

## 4. Decisiones ya tomadas

Estas se discutieron y se cerraron. **No las reabras** por iniciativa propia; si
crees que alguna está mal, dilo una vez y sigue adelante con lo acordado salvo que
Albert cambie de opinión.

| Decisión | Acordado |
|---|---|
| Formato | Web estática. **No** hay aplicación de escritorio. |
| Servidor | **Ninguno.** Sin backend, sin base de datos, sin cuentas de usuario. |
| Publicación | GitHub Pages. Compartir = pasar un enlace. |
| Plan contable | **PGC normal primero.** PYMES más adelante, pero el modelo de datos se diseña desde el día uno para que quepan varios planes. |
| Módulo 1 | Buscador + fichas de cuentas. **Es lo primero.** |
| Módulo 3 | Simulador: diario → mayor → sumas y saldos → cierre → cuentas anuales. **Va antes que el módulo 2.** |
| Módulo 2 | Wiki del articulado. **Va el último**, y reutiliza el motor del módulo 1. |
| Corrección automática de ejercicios | **Aparcada.** No se diseña para ella todavía. |
| Ejercicios | Práctica libre y enunciados del máster comparten el mismo formato: un ejercicio con enunciado opcional. |
| Persistencia | `localStorage` + exportar/importar el ejercicio como fichero. |
| Aspecto | Papel cálido y tipografía con serifa, sobre la estructura de wiki. Ver sección 6. |

---

## 5. Stack y restricciones técnicas

**Lo que se usa:**

- **Python 3, biblioteca estándar y nada más** para el parser (`pathlib`, `re`,
  `json`, `unicodedata`). Sin `pip install` de nada mientras se pueda evitar.
- **HTML, CSS y JavaScript a pelo** para la web. Sin framework.
- **`python -m http.server`** para ver la web en local.
- **git** y **GitHub Pages** para publicar.

**Lo que NO se usa, y por qué:**

- **Sin React, Vue, Svelte ni similares.** Meterían decenas de conceptos entre
  Albert y ver algo funcionando. Esta aplicación no los necesita.
- **Sin npm, sin bundler, sin paso de compilación.** El fichero que se edita es
  el fichero que se ejecuta. Es lo que hace que se pueda aprender.
- **Sin TypeScript** de momento.
- **Sin CSS framework** (Tailwind, Bootstrap...). El CSS se escribe a mano porque
  aprender CSS es parte del objetivo.

Si en algún momento una de estas restricciones se vuelve de verdad dolorosa,
plantéaselo a Albert como una decisión, con su coste y su beneficio. No la
saltes por tu cuenta.

---

## 6. El aspecto

Está decidido a partir de unas maquetas. La combinación elegida es:

- **La piel de "Cuaderno"**: fondo de papel cálido (`#FBF9F4`), tipografía con
  serifa para títulos y para el texto legal, sans para la interfaz.
- **La estructura de "Wiki"**: cabecera con buscador global, índice de contenidos
  a la izquierda, ficha rápida al margen derecho.
- **El movimiento en dos columnas enfrentadas**: "Se cargará / Debe" a la
  izquierda, "Se abonará / Haber" a la derecha, con las contrapartidas como
  etiquetas de color clicables (azul = debe, ámbar = haber).
- En pantalla estrecha, las dos columnas se apilan.

Detalle que importa: **en la columna del cargo, las contrapartidas van en ámbar**
(porque son cuentas que se abonan) y al revés. Eso enseña el asiento entero de un
vistazo y es intencionado.

---

## 7. El material fuente

`sources/Texto refundido PGC 2021.md` — el texto refundido del PGC.

**Dos avisos importantes:**

1. **Viene de un OCR.** Tiene marcas de página incrustadas con la forma
   `{300}------------------------------------------------` en medio del texto, y
   los movimientos `a1) a2) a3)` vienen aplastados en una sola línea en vez de
   como lista. El parser tiene que limpiarlo.
2. **Es la única fuente de verdad del contenido contable.** Nunca inventes ni
   completes de memoria la definición de una cuenta, su movimiento, ni el texto
   de una norma. Si algo no está en el fichero, se dice que no está. Un dato
   contable inventado en una herramienta de estudio es peor que un hueco.

---

## 8. Convenciones del repositorio

**Estructura** (se construye paso a paso, no de golpe):

```
Ayuda_Contabilidad_App/
  sources/          el texto legal original, no se toca nunca
  data/             los .json que produce el parser
  tools/            los scripts de Python del parser
  web/              lo que se publica: index.html, estilos, js
  docs/             la hoja de ruta y las notas
  CHANGELOG.md      el historial de decisiones y cambios
```

**Mensajes de commit.** Prefijo, dos puntos, y una frase en castellano en
presente:

```
feat: añadir el buscador por código de cuenta
fix: corregir el parseo de los movimientos partidos en dos líneas
docs: explicar cómo se ejecuta el parser
refactor: separar la limpieza del OCR en su propia función
chore: añadir .gitignore
```

- `feat` funcionalidad nueva · `fix` arreglo · `docs` documentación ·
  `refactor` reorganizar sin cambiar comportamiento · `chore` mantenimiento.
- Explícale la convención la primera vez y escribid los mensajes juntos.

**Rama:** se trabaja en `main` directamente. Es un proyecto de una persona y las
ramas son un concepto que llegará más adelante, cuando haga falta de verdad.

---

## 9. Al empezar cada sesión

1. Mira `docs/hoja-de-ruta.md` y `git log --oneline` para saber por dónde vais.
2. Dile a Albert en qué paso estáis y cuál es el siguiente.
3. Pregúntale si quiere seguir por ahí o hacer otra cosa.
4. Y entonces, y solo entonces, empezad.
