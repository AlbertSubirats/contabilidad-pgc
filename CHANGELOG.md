# Changelog

El historial de **decisiones** y **cambios** del proyecto, con su *por qué*.

- La entrada más reciente va **arriba**.
- Cada entrada es una *Decisión* (qué se eligió y por qué) o un *Cambio* (qué se
  consiguió en un paso).
- Las decisiones de partida no se repiten aquí: están en la tabla de la
  sección 4 de [CLAUDE.md](CLAUDE.md#4-decisiones-ya-tomadas).

---

## 2026-10-15

### Cambio · Paso 20·5: el título de la ficha y las zonas, como en la maqueta A
**Qué:** en `app.js`, el título de la ficha se arma con dos `<span>`: el
código (`codigo-titulo`) y el nombre (`nombre-titulo`), separados por un
espacio en vez del "·". En `styles.css`, el código va 1,3 veces más grande y
en negrita, con cifras alineadas (`lining-nums`: las de Georgia, si no, suben
y bajan como letras), y el nombre en un marrón oscuro nuevo,
`--color-tinta-marron`. Otro color nuevo, `--color-papel-claro`, para la
cabecera, el árbol y las cajas de la ficha rápida: la ficha se queda en el
papel de fondo, un poco más oscuro, y las zonas se distinguen. El árbol mide
siempre el alto de la ventana, para que su fondo llegue hasta abajo.
Comprobado en el navegador a 1440 píxeles con la 430. Escrito por Claude, a
petición de Albert.
**Por qué:** idea de Albert, al comparar con la maqueta A: el código es lo
que se busca y lo que se recuerda, y con todas las zonas del mismo color la
página parecía una sola mancha.

### Decisión · Un marrón para el nombre que no es el del Haber
**Qué:** el nombre de la cuenta va en `#6B4A35`, más oscuro y más rojizo que
el ámbar del Haber (`#8A5A14`).
**Por qué:** el ámbar quiere decir Haber en esta web; un título en ese color
diría algo que no es. Lo pidió Albert ("un tono más marroncete").

### Cambio · Paso 19 bis: abrir el árbol desde un botón en el móvil
**Qué:** un `<button>` "☰ Cuadro de cuentas" en la cabecera, al lado del
nombre, que solo se ve por debajo de 64em. Al pulsarlo, `app.js` pone la
clase `abierto` al árbol (`classList.add`) y el CSS lo enseña entre la
cabecera y la ficha; el botón pasa a "✕ Cerrar el cuadro" y su
`aria-expanded`, a `"true"`. Se vuelve a cerrar con el mismo botón o al
elegir una cuenta del árbol (escuchando el clic, con `evento.target.closest("a")`
para no cerrarlo al pulsar un triángulo). La cabecera del móvil pasa a dos
columnas: el nombre y el botón arriba, el buscador debajo
(`grid-column: 1 / -1`). Comprobado en el navegador: a 375 píxeles el botón
abre el árbol, un triángulo no lo cierra, elegir el 10 lo cierra y abre su
ficha; a 1440, el botón no se ve, el árbol está en su columna y el buscador
sigue centrado. Escrito por Claude, a petición de Albert.
**Por qué:** desde el paso 19, en el móvil solo se llegaba a las cuentas con
el buscador y los enlaces. Idea de Albert (él lo pensó como un gesto con el
dedo; se cambió por un botón, ver la decisión del paso 19).

### Decisión · El árbol se abre en su sitio, no flotando encima
**Qué:** al abrirlo, el árbol empuja la ficha hacia abajo, en vez de flotar
por encima de ella como un panel que entra por el lado.
**Por qué:** un panel flotante pide `position: fixed`, un fondo que tape la
ficha, su propio botón de cerrar y cuidar quién queda encima de quién. Así
son dos reglas de CSS. Como el árbol se cierra al elegir una cuenta, la ficha
vuelve a quedar arriba. Si con el uso se echa en falta el panel, se cambia.

### Cambio · Paso 20·4: el nombre de la web, la tipografía de la maqueta A y el foco visible
**Qué:** la cabecera lleva el nombre "Cuentas PGC" (con serifa, enlace al
inicio) y el buscador; en ancho, una rejilla `1fr minmax(0, 32em) 1fr`
deja el buscador en el centro, y en el móvil van uno encima del otro. La
pestaña también se llama "Cuentas PGC". El título de la ficha pasa a ser el
`<h1>`, sus apartados `<h2>` y las columnas del movimiento `<h3>` (antes
`<h2>`, `<h3>` y `<h4>`). La ficha toma la tipografía de la maqueta A:
Georgia en los títulos y en el texto de la norma (definición y
presentación), con líneas de 40em como mucho y más aire entre ellas; la
presentación, en un recuadro con barra; la ficha entera, de 64em como mucho.
Una regla `:focus-visible` para toda la web dibuja un recuadro en el color de
enlace en lo que tenga el foco del teclado. Comprobado en el navegador a 1440
y 375 píxeles: un solo `<h1>` ("430 · Clientes"), el buscador centrado en
ancho, el nombre encima en el móvil sin salirse nada, y pulsar el nombre
quita la ficha y las marcas del árbol. Escrito por Claude, a petición de Albert.
**Por qué:** cierra el paso 20: la página se había quedado sin título
principal en el paso 19, el CLAUDE.md pide serifa para los títulos y el texto
legal, y el foco visible tenía reglas sueltas y distintas en cada sitio.

### Decisión · "Cuentas PGC", y el `<h1>` es el título de la ficha
**Qué:** la web se llama "Cuentas PGC", como en la maqueta A. El nombre es un
enlace normal; el `<h1>` es el título de la ficha.
**Por qué:** el título principal de cada página es lo que cambia de una a
otra, la cuenta, como en la Wikipedia. Si llega el simulador, el nombre se
podrá revisar. Lo decidió Albert.

### Decisión · Georgia, sin fuentes de Google
**Qué:** la serifa es Georgia, que viene instalada en todos los ordenadores.
**Por qué:** las fuentes de la maqueta son de Google Fonts: se parecerían
más, pero la web tendría que pedírselas a Google cada vez que se abre. Una
dependencia externa que no hace falta (sección 3.4 de CLAUDE.md).

### Decisión · La portada, para más adelante
**Qué:** sin cuenta elegida, el centro de la página sigue vacío.
**Por qué:** qué se enseña ahí (bienvenida, cómo se usa...) es un diseño
propio, no pulido. Queda apuntado en la hoja de ruta.

### Cambio · Paso 20·3 bis: hacer más legible el árbol
**Qué:** la columna del árbol pasa de 18em a 22em y su letra, a 0,9. Las
líneas de un mismo nombre van más juntas (`line-height: 1.3`) y entre una
cuenta y la siguiente hay más aire. Los subgrupos y las cuentas cuelgan de
una línea guía fina a la izquierda (`border-left`), con menos sangría que
antes. Los subgrupos se enseñan con la inicial en mayúscula
(`text-transform: lowercase` y `::first-letter`); en `app.js`, las clases
`titulo-subgrupo` y `nombre-arbol` para que el CSS los encuentre. Al pasar el
ratón, la fila entera se oscurece. Comprobado en el navegador con la 403:
"40 Proveedores" en vez de "40 PROVEEDORES", la 401 en dos líneas en vez de
tres. Escrito por Claude, a petición de Albert.
**Por qué:** Albert lo encontraba difícil de leer: con 288 píxeles y la
sangría de cada nivel, los nombres ocupaban tres líneas, y el espacio entre
las líneas de un nombre era el mismo que entre dos cuentas.

### Decisión · Aire y línea guía, no una cajita por cuenta
**Qué:** de las tres maneras que se compararon (como estaba, aire con línea
guía, una caja por cuenta), la segunda.
**Por qué:** una caja por cuenta gasta ancho en una columna que ya va justa
y, con casi mil cuentas, convierte el árbol en una cuadrícula. Tampoco filas
alternas de color: con nombres de una, dos o tres líneas se vería
desordenado. Lo decidió Albert ("muchísimo más agradable a la vista").

### Decisión · Los subgrupos, en minúsculas solo en el árbol
**Qué:** el árbol enseña "Proveedores" donde el BOE escribe "PROVEEDORES".
**Por qué:** las mayúsculas se leen peor y ocupan más. Es solo el aspecto:
el JSON no cambia, y la ficha, las migas y la ficha rápida siguen poniéndolo
tal como se publicó (sección 7 de CLAUDE.md). Lo decidió Albert.

### Decisión · El árbol más ancho, a costa de la ficha en pantallas justas
**Qué:** con el árbol a 22em, en una pantalla de 1024 píxeles (el mínimo
para las tres columnas) a la ficha le quedan unos 370 píxeles, antes 450.
**Por qué:** en pantallas de ordenador normales (1280 o más) la ficha va
sobrada. Si se queda corta en alguna, se mira en el paso 20·4.

### Cambio · Paso 20·3: el árbol como en la maqueta A
**Qué:** en `app.js`, `crearEnlaceDelArbol` pone el código y el nombre de
cada línea en dos `<span>`, y los grupos llevan la clase `titulo-grupo`.
Nuevas `marcarEnArbol` y `quitarMarcasDelArbol`: al abrir una ficha, el
árbol se despliega por su rama (subiendo por los padres, como las migas),
marca la cuenta con la clase `actual` y su grupo y subgrupo con `en-camino`,
y se desplaza hasta ella si no se ve. En `styles.css`: "Cuadro de cuentas"
pequeño y en mayúsculas; el triángulo propio con `summary::before`, pequeño
y en gris, que apunta abajo con la caja abierta (`details[open]`); cada línea
en una rejilla (código en gris con `tabular-nums`, nombre al lado); los
grupos con serifa; el camino en el color de enlace y la cuenta abierta con
fondo y barra (`box-shadow: inset`). Comprobado en el navegador: la 430
abre el 4 y el 43 y se resalta; la 642 abre el 6 y el 64 y el árbol baja
hasta ella; con la 4300 (subcuenta, no está en el árbol) se marca el camino
hasta la 430; con `#9999` o sin `#` no queda nada marcado. Escrito por
Claude, a petición de Albert.
**Por qué:** idea de Albert: el árbol de la maqueta A se lee mejor, y al
llegar a una cuenta desde el buscador o un enlace, el árbol dice dónde está.

### Decisión · El árbol abre, pero no cierra
**Qué:** al abrir una ficha se despliega su rama, pero las cajas que ya
estaban abiertas se quedan como estaban.
**Por qué:** cerrar las demás borraría lo que el usuario haya abierto a mano.
La maqueta A enseña solo la rama de la cuenta, pero es un dibujo de un
momento; si con el uso el árbol se llena de cajas abiertas, se puede cambiar.

### Decisión · El triángulo, dibujado por la página
**Qué:** se quita el triángulo del navegador y se pone uno propio con
`::before`.
**Por qué:** el del navegador no se puede hacer más pequeño ni pintar de gris
de forma fiable en todos los navegadores, y al partir el paso 20 se acordó
dejarlo, pero discreto. Sigue siendo el que pliega (paso 17): el nombre
lleva a la ficha.

### Cambio · Paso 20·2: las migas de pan en color de enlace
**Qué:** un color nuevo en `:root`, `--color-enlace` (#2A6B7C, azul
petróleo), y los enlaces de las migas en ese color. La cuenta en la que
estás y los separadores siguen en gris, porque no llevan a ningún sitio.
Comprobado en el navegador con la 430: "Grupo 4" y "Subgrupo 43" en el color
de enlace, "›" y "430" en gris. Contraste con el papel, 5,7 a 1 (el mínimo
para leer bien un texto es 4,5). Escrito por Claude, a petición de Albert.
**Por qué:** idea de Albert, para mejorar el aspecto: en gris, las migas no
parecían enlaces.

### Decisión · Un azul petróleo, no el azul del Debe
**Qué:** el color de enlace es un azul verdoso, a propósito distinto del
`--color-debe`.
**Por qué:** en esta web, el azul del movimiento quiere decir Debe; si las
migas lo usaran, dejaría de querer decir solo eso. De momento solo lo usan
las migas; el camino del árbol lo usará en el paso 20·3. Lo decidió Albert.

### Cambio · Paso 20·1: el buscador como en la maqueta B
**Qué:** en `index.html`, la caja es un `div.caja-busqueda` con tres cosas en
fila (flex): una lupa dibujada en SVG, el input sin borde y un contador
("19 resultados"). Los resultados van en un `#desplegable-buscador` con el
título "Cuentas" encima de la lista; ahora es el desplegable, y no la lista,
lo que se esconde y se enseña. En `app.js`, `crearResultado` pone el código y
el nombre en dos `<span>` (el árbol sigue con `crearElementoDeCuenta`) y
`pintarContador` escribe el número, en singular si es uno. En `styles.css`,
cada fila es una rejilla de dos columnas (código en 4em, nombre en lo que
sobra) y el primer resultado va resaltado (`:first-child`), porque es el que
abre Enter. La caja enseña dónde está el foco con `:focus-within`.
Comprobado en el navegador a 1280 y 375 píxeles: "clientes" da 19
resultados con los nombres alineados, "zzz" da 0 con su aviso, la caja
vacía esconde el desplegable y el contador, Enter sigue funcionando y en el
móvil no se sale nada por la derecha. Escrito por Claude, a petición de Albert.
**Por qué:** idea de Albert: la lista se lee mejor con los códigos en su
columna, y el resaltado dice qué abre Enter.

### Decisión · Del buscador de la maqueta B, la forma y no los colores
**Qué:** se toman la lupa, el contador, el título del desplegable, las dos
columnas y el resaltado del primero. No se toman el blanco y el azul de la
maqueta B (manda la piel de papel de la A) ni el apartado "En el articulado",
que es de la fase 5. El resaltado va en el color de la tinta y no en azul,
que en esta web quiere decir Debe.
**Por qué:** lo dice la sección 6 de CLAUDE.md: de la B, solo la estructura.

### Decisión · Sin etiqueta visible, con aria-label
**Qué:** el texto "Buscar cuenta" de encima de la caja se quita; el input
lleva `aria-label="Buscar cuenta"` y la lupa, `aria-hidden="true"`.
**Por qué:** en la maqueta B no hay etiqueta a la vista; la lupa y el texto
de ejemplo ya dicen para qué es la caja. El lector de pantalla sigue
teniendo el nombre gracias a `aria-label`.

### Decisión · Los resultados, todavía por orden de código
**Qué:** "clientes" da primero el subgrupo 43 y luego la 430, así que Enter
abre el 43.
**Por qué:** ordenar por lo bien que coincide cada nombre (como en la
maqueta B, con la 430 la primera) es un cambio de lógica y no de aspecto, y
no estaba en el paso. Queda como idea si Albert la echa en falta.

### Cambio · Paso 19 quater: Enter abre el primer resultado
**Qué:** nueva función `abrirPrimerResultado` en `app.js`, que escucha el
evento `keydown` de la caja del buscador. Si la tecla (`evento.key`) es
Enter, busca el primer enlace de la lista con `querySelector("a")`, cierra el
buscador y cambia la URL a su `#código`, como si se hubiera pulsado. No hace
nada si la lista está escondida o no hay resultados. Comprobado en el
navegador: "clien" + Enter abre el 43; "572" + Enter abre la 572; con la
caja vacía o con "zzz", Enter no cambia nada; otra tecla tampoco. Escrito
por Claude, a petición de Albert.
**Por qué:** idea de Albert: buscar y abrir sin soltar el teclado.

### Decisión · Con la lista escondida, Enter no hace nada
**Qué:** antes de buscar el primer enlace se mira si la lista está escondida.
**Por qué:** `cerrarBuscador` esconde la lista pero no la vacía. Sin esa
comprobación, Enter con la caja vacía abriría el primer resultado de la
búsqueda anterior.

### Decisión · El paso 20 se parte en cuatro
**Qué:** 20·1 el buscador como en la maqueta B, 20·2 las migas en color de
enlace, 20·3 el árbol como en la maqueta A, 20·4 el resto del pulido.
**Por qué:** son las peticiones de Albert de aspecto, y cada una se
comprueba por separado. Las migas no irán en el azul del Debe sino en un
color de enlace propio: en esta web, el azul del movimiento quiere decir
Debe. En el árbol se queda el triángulo, más discreto, porque es el que
pliega (paso 17). Lo decidió Albert.

### Cambio · Paso 19 ter: la ficha rápida como en la maqueta D
**Qué:** la ficha rápida se reparte en dos cajas (`.caja`), "Ficha rápida" y
"Contrapartidas", con borde redondeado y el título en una franja de papel
más oscuro (`--color-papel-oscuro`), con serifa. Las contrapartidas van solo
con el número, en cajitas una al lado de la otra (`flex-wrap: wrap`), bajo
"De los cargos" y "De los abonos" en el color de su lado; las cajitas, con
los colores cruzados de siempre. El nombre de cada una sale al dejar el
ratón encima (atributo `title`). Comprobado en el navegador con la 430: los
12 números con su nombre en el `title` y los colores cruzados. Escrito por
Claude, a petición de Albert.
**Por qué:** idea de Albert: con los nombres al lado, la lista era larga, y
los números en cajitas se leen de un vistazo, como en la maqueta D.

### Decisión · El nombre, con title y no con un recuadro propio
**Qué:** el nombre de la contrapartida lo enseña el navegador con el
atributo `title`.
**Por qué:** es una línea en `app.js`, sin CSS ni JavaScript nuevos. Lo malo:
el recuadro lo dibuja el navegador, tarda un segundo y no funciona con el
dedo; como en el móvil la ficha rápida no se ve, no importa. Un recuadro con
la estética de la web, si hace falta, en el paso 20. Lo decidió Albert.

### Decisión · De la maqueta D, solo las cajas y las contrapartidas
**Qué:** "De los cargos" y "De los abonos" en vez del "Al cargo" y "Al abono"
de la maqueta, y las dos franjas del mismo color de papel (en la maqueta, la
de contrapartidas es azul). Balance, norma aplicable, fuente y el botón "Usar
en un asiento" no se toman.
**Por qué:** "Al cargo" se puede leer como "las cuentas que se cargan", que
es justo al revés: son las contrapartidas de los cargos. El azul, en esta
web, quiere decir debe, y una franja azul lo mezclaría. Lo demás, como se
decidió en el paso 18: no está en los datos o es de otro módulo.

### Cambio · Paso 19: adaptar la interfaz a pantallas estrechas
**Qué:** `index.html` lleva la etiqueta `<meta name="viewport">`, y
`styles.css` pasa a diseñarse primero para pantalla estrecha: la base es
una sola columna, y lo de pantalla ancha va en media queries
(`@media (min-width: ...)`). Desde 64em (1024 píxeles): la rejilla de tres
columnas, el `sticky` de los márgenes, y el árbol y la ficha rápida, que por
debajo se esconden. Desde 40em (640 píxeles): el movimiento en dos columnas
enfrentadas; por debajo, el Debe y debajo el Haber. La cabecera se queda solo
con el buscador, centrado. Comprobado en el navegador a 375, 768 y 1280
píxeles: sin desbordarse a lo ancho, y en ancho, la ficha rápida sigue
escondida sin cuenta elegida. Albert escribió los trozos 1 a 3 (viewport,
rejilla y `sticky`); Claude, del 4 al 6 y los comentarios.
**Por qué:** en el móvil los dos márgenes ya ocupaban más que la pantalla, y
sin la línea del viewport el móvil encogía la página entera. Se empieza por
lo estrecho porque una zona debajo de otra es lo que hace el HTML sin CSS: lo
complicado se añade cuando hay sitio, en vez de deshacerlo.

### Decisión · En el móvil, sin árbol; el botón, en un paso 19 bis
**Qué:** por debajo de 64em el árbol se esconde y a las cuentas se llega con
el buscador y los enlaces. Un botón "☰ Cuadro de cuentas" que lo abra por
encima de la ficha queda para el paso 19 bis.
**Por qué:** Albert propuso abrirlo deslizando el dedo. Se descartó: el gesto
desde el borde ya es "atrás" en el móvil, no se ve que exista y pide mucho
JavaScript nuevo. El botón es lo habitual y se entiende solo, pero no estaba
en el paso 19. Lo decidió Albert.

### Decisión · En el móvil, sin ficha rápida
**Qué:** por debajo de 64em la ficha rápida no se ve.
**Por qué:** repite lo que ya dice la ficha. Lo decidió Albert. Para que se
vuelva a ver en ancho sin pisar el atributo `hidden` (`display` manda sobre
él, como pasó con la lista del buscador), hay una regla
`.columna-ficha-rapida[hidden]`.

### Decisión · Dos puntos de corte: 40em y 64em
**Qué:** 64em para las tres columnas y 40em para el movimiento en dos
columnas. En una tablet, la ficha va a todo lo ancho con el Debe y el Haber
enfrentados.
**Por qué:** por debajo de 64em, la ficha no cabe entre dos márgenes de
18em; por debajo de 40em, cada columna del movimiento se queda en un puñado
de palabras por línea. Las condiciones de `@media` no admiten variables CSS,
así que 64em sale escrito en tres sitios: los comentarios lo avisan.

### Decisión · La cabecera, solo con el buscador
**Qué:** se quitan el título "Ayuda Contabilidad" y el subtítulo; el
buscador queda centrado. El nombre sigue en la pestaña (`<title>`).
**Por qué:** a Albert le sobraban, y en el móvil apretaban el buscador hasta
dejarlo inútil. Cómo presentar la web con buena información se verá más
adelante. Queda pendiente para el paso 20: la página ya no tiene `<h1>`, y
los lectores de pantalla lo usan para orientarse. Lo decidió Albert.

## 2026-10-14

### Cambio · Paso 18: repartir la página en árbol, ficha y ficha rápida
**Qué:** `index.html` se ordena en zonas con significado (`<header>`,
`<aside>`, `<main>`) y `styles.css` las coloca con CSS grid: la cabecera
arriba y debajo tres columnas, el árbol, la ficha y la ficha rápida
(`grid-template-areas`). Los dos márgenes son `position: sticky` y no se van
al bajar por la ficha. Nuevo en `app.js`: `pintarMigas` (sube por los
`padre` con un `while`), `pintarFichaRapida` con `anadirDato` (una lista
`<dl>`) y `pintarContrapartidas`. El buscador pasa a la cabecera y enseña los
resultados en una lista desplegable (`position: absolute`), que se esconde
con la caja vacía y se cierra al pulsar un resultado (`cerrarBuscador`); si
nada coincide, lo dice. La lista de las 915 cuentas ya no se pinta al
cargar. Comprobado en el navegador: grupo, subgrupo, cuenta, subcuenta,
`#9999` y sin `#`, buscar "clien" y pulsar la 436, buscar "zzz", sin errores
en la consola. Escrito por Claude, trozo a trozo; comprobado también por Albert.
**Por qué:** con todo apilado en una columna, para ver la ficha había que
saltar arriba. Ahora el árbol, la ficha y sus datos se ven a la vez.

### Decisión · A la izquierda, el árbol y no el índice de la ficha
**Qué:** la columna izquierda es el cuadro de cuentas (maqueta A), no el
índice de contenidos de la ficha (maqueta B).
**Por qué:** la ficha tiene tres apartados y cabe en una pantalla; un índice
no ayudaría. El árbol dice dónde está la cuenta dentro del PGC. Lo decidió Albert.

### Decisión · La ficha rápida, solo con lo que está en los datos
**Qué:** plan, nivel, grupo, subgrupo y las contrapartidas con su nombre. El
grupo y el subgrupo salen de la primera y las dos primeras cifras del código.
**Por qué:** "Naturaleza", la línea del balance y la norma aplicable de la
maqueta B no están en el JSON, y deducirlas sería inventar contenido
contable (sección 7 de CLAUDE.md). La línea del balance llegará en el paso
30 y la norma en la fase 5. Lo decidió Albert.

### Decisión · El buscador, con lista desplegable
**Qué:** los resultados caen bajo la caja, flotando por encima de la ficha,
como en la maqueta B. Se cierran al pulsar un resultado escuchando el clic,
no el cambio de URL.
**Por qué:** la lista desplegable no quita el árbol de su sitio mientras se
busca. El clic, porque pulsar la cuenta que ya está abierta no cambia la URL
y la lista se habría quedado abierta. No se cierra con Escape ni al pulsar
fuera: se dejó para más adelante si hace falta. Lo decidió Albert, sabiendo
que era la opción más larga.

### Decisión · De lo que dibujan las maquetas, solo las migas de pan
**Qué:** "Grupo 4 › Subgrupo 43 › 430" encima del título, con los antepasados
como enlaces. "Ver también", "Vecinas", "Mostrar los movimientos restantes" y
el menú "Cuadro · Normas · Diario" se quedan fuera.
**Por qué:** las migas salen de los datos y orientan. "Ver también" no está en
el JSON, "Vecinas" ya las enseña el árbol, y el menú es para módulos que aún
no existen. Lo decidió Albert.

### Decisión · Se quita la etiqueta del grupo de debajo del título
**Qué:** la etiqueta "Grupo 4 · Acreedores y deudores..." del paso 15
desaparece; queda solo la del nivel ("Cuenta").
**Por qué:** con las migas y la ficha rápida, el grupo salía tres veces. Lo
decidió Albert.

### Decisión · El commit no se llama como decía la hoja de ruta
**Qué:** `feat: repartir la página en árbol, ficha y ficha rápida` en lugar
de `feat: añadir el índice y el panel lateral de la ficha`.
**Por qué:** al final no hay índice de la ficha; el nombre viejo describiría
algo que no está en el commit.

### Cambio · Paso 17 bis: convertir en enlaces las remisiones del texto
**Qué:** el parser busca en la definición y la presentación las remisiones a
otras cuentas (`PATRON_REMISION`) y las guarda en dos campos nuevos,
`remisiones_definicion` y `remisiones_presentacion`. La web las convierte en
enlaces dentro del texto: `crearFraseConContrapartidas` pasa a ser
`crearTextoConEnlaces(texto, codigos, clase)` y la usan los movimientos y los
párrafos. `verify.py` gana el apartado 7. Resultado: 460 remisiones en 199
cuentas; en la 101, "análogo al señalado para la cuenta 100" enlaza con la
100, y en la 109 el "artículo 170" se queda como texto. Comprobado en el
navegador. Idea de Albert; escrito por Claude, trozo a trozo.
**Por qué:** la ficha remite a menudo a otras cuentas, y poder seguir la
remisión con un clic es la mitad del valor de una wiki.

### Decisión · Una remisión es una palabra clave seguida de una lista de números
**Qué:** `r"\b(cuentas?|subgrupos?|grupos?) ([\d ,/yoó]+)"`: "cuenta",
"subgrupo" o "grupo" (con o sin "s") y luego todo lo que sean cifras,
espacios, comas, barras, "y", "o" u "ó". De esa lista se quedan los números
que son una cuenta que existe.
**Por qué:** con la regla de las contrapartidas (todo número que sea una
cuenta), "artículo 239" enlazaría con la 239. Mirar la palabra de delante deja
fuera los 32 números que no son remisiones (artículos, la Ley 46/1998, las
"b1)" de los derivados, los "1." de la 490) y atrapa las listas ("130, 131 ó
132", "35y 36", "300/309"). Se probó también un patrón con grupos anidados:
daba exactamente lo mismo, párrafo a párrafo, y se eligió el que se lee de un
vistazo.

### Decisión · Las remisiones se guardan como una lista por apartado
**Qué:** como las contrapartidas: una lista de códigos para la definición y
otra para la presentación, y la web enlaza los números del texto que están en
ella.
**Por qué:** se comprobó que en ningún párrafo el mismo número es una vez
remisión y otra no (el caso dudoso, la 529, dice "subgrupo 14" las dos
veces). Si un día pasara, el apartado 7 de `verify.py` no lo vería; habría
que guardar las remisiones párrafo a párrafo.

### Decisión · Las remisiones, como enlaces discretos y no en cajita
**Qué:** clase `remision`: el número en el color del texto, con un subrayado
fino y gris separado de las letras, que se oscurece y engorda al pasar el
ratón o al llegar con el teclado.
**Por qué:** las contrapartidas van en cajitas de color porque enseñan el
asiento (Debe/Haber); una remisión no tiene lado, y hay párrafos con cinco o
seis remisiones que en cajitas se leerían peor. Lo decidió Albert.

### Decisión · "salvo la 499" se queda sin enlace
**Qué:** en la presentación del 49, el 499 no se toma como remisión.
**Por qué:** delante dice "la", no "cuenta". Aceptar "la" como palabra clave
colaría números que no son cuentas ("la Ley 46/1998"). Es un solo caso, sale en
el apartado 7 de `verify.py` y el texto se lee igual. Lo decidió Albert.

### Decisión · `verify.py` lista los números que no son remisión
**Qué:** apartado 7: los números de la definición y la presentación que son
el código de una cuenta pero no se han tomado como remisión. Hoy salen 33.
**Por qué:** si la regla se estropea o el BOE cambia una frase, aparecerá ahí
un número que debería ser enlace. Lo decidió Albert.

### Cambio · Paso 17: navegar entre cuentas por la URL
**Qué:** las contrapartidas, las cuentas de la lista y del árbol, y los
títulos de grupos y subgrupos del árbol son enlaces (`<a href="#430">`), que
fabrica `crearEnlaceACuenta`. Un enlace solo cambia el hash de la URL; el
enrutador, `mostrarCuentaDeLaUrl`, se entera por el evento `hashchange` y
enseña la ficha, y también se llama al cargar la página, después de que
llegue el JSON. Comprobado en el navegador: el enlace directo a `#430` abre su
ficha, de la 430 se llega a la 436 pulsando su contrapartida, "atrás" vuelve a
la 430, sin `#` la página queda como al entrar, y sin errores en la consola.
Escrito por Claude, trozo a trozo, a petición de Albert.
**Por qué:** la ficha enseña el asiento entero; ahora se puede recorrer. La URL
hace que "atrás" funcione y que se pueda compartir el enlace a una cuenta.

### Decisión · Un solo camino para abrir una ficha: la URL
**Qué:** nada llama a `mostrarFicha` directamente salvo el enrutador. Los
clics cambian la URL y la URL decide.
**Por qué:** así un clic, el botón "atrás" y un enlace compartido van por el
mismo camino y no pueden comportarse distinto. Además, las cuentas pasan de un
`click` en el `<li>` a enlaces de verdad, que se pueden usar con el teclado
(Tab y Enter) y abrir en otra pestaña: era lo que el paso 15 dejó apuntado
como provisional. El desplazamiento hasta la ficha (`scrollIntoView`) sigue
hasta el paso 18.

### Decisión · En el árbol, el título es el enlace y el triángulo pliega
**Qué:** el texto del `<summary>` de cada grupo y subgrupo es un enlace a su
ficha. Para plegar y desplegar queda el triángulo.
**Por qué:** era el pendiente del paso 17 en la hoja de ruta. Se compararon un
enlace aparte "ficha" junto al título, el título como enlace, y no hacer
nada. Albert eligió el título como enlace, la opción más limpia. Se comprobó
que pulsar un enlace dentro de un `<summary>` sigue el enlace sin plegar la
caja, así que no hace falta código para evitarlo.

### Decisión · Un enlace a una cuenta que no existe enseña un aviso
**Qué:** con `#9999` (o `#hola`), la ficha se esconde y sale "No hay ninguna
cuenta con el código «9999» en el PGC.", con el estilo de los demás avisos.
**Por qué:** lo pidió Albert, en vez de no hacer nada: un enlace roto tiene
que decir que lo está. El código se pasa por `decodeURIComponent` para que el
aviso enseñe lo que se escribió ("é" y no "%C3%A9"). Al probarlo apareció un
fallo: con un "%" suelto (`#50%`) `decodeURIComponent` lanza un `URIError` y
el enrutador se cortaba sin enseñar nada. Se arregla con `try`/`catch`: si no
se puede decodificar, se usa el texto tal cual.

### Decisión · Las remisiones del texto, en un paso propio (17 bis)
**Qué:** la idea de Albert de que "análogo al señalado para la cuenta 100"
también sea un enlace se apunta en la hoja de ruta como paso 17 bis.
**Por qué:** de los 448 números de las definiciones y presentaciones que
coinciden con una cuenta, unos 15 no son remisiones ("artículo 170",
"artículos 239 a 243", "Ley 46/1998"). Con la regla de las contrapartidas,
"artículo 239" enlazaría con la 239. Hace falta una regla que mire la palabra
de delante, calculada en el parser y verificada: es un paso por sí misma. Lo
decidió Albert.

### Problema conocido · Pulsar la cuenta que ya se está viendo no hace nada
**Qué:** si se está viendo la 430 y se pulsa otra vez su enlace (por ejemplo,
en la lista, más abajo), la URL no cambia, no hay `hashchange` y la página no
sube hasta la ficha.
**Por qué se deja:** es menor, y desaparece en el paso 18, cuando la ficha vaya
al lado de la lista y deje de hacer falta subir.

### Cambio · Paso 1b·6: usar las etiquetas del BOE en el movimiento
**Qué:** la web lee ya los datos del BOE. `pintarMovimientos` pinta la
etiqueta que trae cada movimiento ("a1", "b3", o la "a" sola de la 761), y si
no la trae, el movimiento es la frase de entrada: va sin número y a todo el
ancho. Desaparecen el contador, el parámetro de la letra y la regla de la
minúscula. Se retiran el texto del OCR, el PDF del que salía, el parser viejo
y `compare.py`; `parser_boe.py` pasa a llamarse `parser.py` y
`accounts_boe.json`, `accounts.json`. `verify.py` y `check_chart.py` se
adaptan, y el README y la sección 7 de `CLAUDE.md` dicen ya que la fuente es
el BOE. Comprobado en el navegador: la 430 y la 640 se ven como antes, la 400
con su numeración del PGC, y sin errores en la consola. Escrito por Claude a
petición de Albert; los borrados y renombrados los hizo Albert con `git rm` y
`git mv`.
**Por qué:** cierra la fase 1 bis. La web ya no reconstruye nada que la
fuente traiga escrito.

### Decisión · La web deja de deducir la etiqueta por la columna
**Qué:** la etiqueta de un movimiento sale siempre del dato, nunca de la
columna en la que está.
**Por qué:** al preparar el paso apareció un error que no sabíamos que
teníamos: la web ponía siempre "a" en el Debe y "b" en el Haber, pero en las
cuentas de pasivo y de ingresos el PGC pone los cargos en `b)`. En la 400
Proveedores enseñaba "a1, a2..." donde la ley dice "b1, b2...". Le pasaba a
164 movimientos de cargo. Sustituye la decisión del paso 16 sobre las frases
en minúscula: aquella regla era una forma de adivinar lo que ahora dice el
dato.

### Decisión · Los ficheros recuperan sus nombres de siempre
**Qué:** `tools/parser_boe.py` → `tools/parser.py` y `data/accounts_boe.json`
→ `data/accounts.json`. La web no cambia la ruta del `fetch`.
**Por qué:** el "_boe" solo tenía sentido mientras convivían los dos parsers y
los dos JSON. Git lo cuenta como una modificación de `parser.py` y de
`accounts.json`, porque los nombres siguen existiendo con otro contenido. Lo
decidió Albert.

### Decisión · El PDF de `sources/` se retira también
**Qué:** `sources/PLAN_GENERAL_DE_CONTABILIDAD_accesible.pdf` sale del
repositorio.
**Por qué:** era el documento del que salía el texto del OCR y no lo usaba
ningún programa. La sección 7 de `CLAUDE.md` dice que la única fuente es el
BOE, y otra copia del PGC en `sources/` invitaría a confusión. Sigue en el
historial de git. Lo decidió Albert.

### Decisión · `verify.py` se adapta en vez de retirarse
**Qué:** lee el texto de los movimientos con `textos_de_los_movimientos`, y la
regla de los nombres en mayúsculas mira solo los subgrupos.
**Por qué:** sus comprobaciones siguen sirviendo, pero con el formato nuevo se
rompía (`TypeError: ... got 'dict'`). Los nombres de los grupos van en
minúscula en el BOE, y la regla vieja daba nueve avisos falsos. Ahora salen
dos textos sospechosos, los párrafos numerados de la 490 ("1. Cuando la
empresa..."), que son de verdad. `compare.py` se retira porque ya no hay dos
JSON que comparar; queda en el historial.

### Cambio · Paso 1b·5: comparar los datos del BOE con los del texto refundido
**Qué:** `tools/compare.py`, nuevo, compara cuenta a cuenta `accounts.json`
(OCR) con `accounts_boe.json` (BOE) y clasifica cada cuenta: ficha idéntica,
mismo texto en otro apartado, casi igual (enseña las palabras que cambian, con
`difflib`), ficha nueva, ficha que desaparece y diferencias grandes (enseña
los párrafos que solo están en un lado). Se revisó el informe entero con
Albert. Resultado, después del arreglo de la 673: los 915 códigos coinciden,
698 fichas son idénticas y las otras 217 tienen explicación. Escrito por
Claude, trozo a trozo, a petición de Albert.
**Por qué:** el verificador del paso 1b·3 cruzaba el BOE consigo mismo; el
OCR se equivoca de otra manera, así que donde coinciden la confianza es alta y
donde no, hay que saber quién falla.

### Decisión · Lo que dice la comparación: en ninguna diferencia acierta el OCR
**Qué:** las diferencias se explican así: nombres (decisiones del 1b·3); texto
que cambia de apartado por las presentaciones nuevas y los párrafos
separados, y "Con carácter general, su movimiento es el siguiente:", que el
parser viejo tiraba (decisiones del 1b·4); fallos de lectura del OCR
(comillas, guiones, "dé" por "de"); fichas que el OCR colgó de otra cuenta al
perder el título (la 642 en la 641, la 669 en la 668, la 627 y la 628 en la
626, la 798 en la 797, el grupo 7 en la 699, la 440 y la 441 en el 44 y la
446); títulos de cuatro cifras que el OCR colgaba de la cuenta de tres (1110,
2550, 5580, 6510, 7510, 7950-7957, 8300); intervalos (230/237, 580/584,
585/589, 700/705, 710/713); párrafos que el OCR pegaba al último movimiento
("c) Si los valores se clasifican...", "2. Cuando la empresa cifre..."); tres
cuentas con movimientos nuevos (761, 774, 802); los derivados de cobertura; y
la 113, donde el texto vigente dice "cuenta 6301" y el refundido "subgrupo
6301".
**Por qué:** era lo que pedía la hoja de ruta: que cada diferencia tuviera
explicación. Ninguna es un dato que el OCR tuviera bien y el BOE no.

### Decisión · Cuatro erratas más del BOE que se respetan
**Qué:** "registra)" por "registral" (100), "vin culado" (135), "cuentas de
subgrupo 57" (171) y "cargados en factura los proveedores" (400) se quedan
tal como se publicaron.
**Por qué:** no cambian el sentido. Es la regla de la sección 7 de `CLAUDE.md`.

### Decisión · Fe de erratas de los títulos: "6733/5734/5735"
**Qué:** `parser_boe.py` tiene una fe de erratas de títulos de ficha, con la
misma idea que la del cuadro, y avisa si el BOE la corrige. Corrige
"6733/5734/5735" por "6733/6734/6735".
**Por qué:** la 5734 y la 5735 no existen, así que el título no se reconocía:
la 6733, la 6734 y la 6735 se quedaban sin ficha y su texto acababa en la 673.
El índice del subgrupo 67 y el texto refundido dan "6733/6734/6735". Al
corregirlo, las cuatro cuentas pasan a ser idénticas a las del OCR (`git diff
data/accounts_boe.json` enseña justo ese cambio). Lo destapó la comparación y
lo decidió Albert. Va en el commit de este paso porque es el "caso nuevo que
arreglar" que la hoja de ruta preveía.

### Decisión · Las 833, 834, 836 y 838 se quedan como están
**Qué:** su "b) Al cierre del ejercicio, se cargará..." sigue en la
definición (el problema conocido del paso 1b·4).
**Por qué:** la comparación enseña que el OCR lo hacía peor: pegaba esa frase
al último movimiento de la otra columna. En la definición no se pierde nada, y
atraparlo obligaría a aflojar la regla de las cabeceras. Lo decidió Albert.

### Decisión · El texto del OCR se retira en el paso 1b·6
**Qué:** `sources/Texto refundido PGC 2021.md` y `parser.py` se retiran,
pero en el paso 1b·6, cuando la web pase al JSON del BOE. Se actualizan la
sección 7 de `CLAUDE.md` y el paso 1b·6 de la hoja de ruta.
**Por qué:** la comparación no encontró nada que el OCR tuviera bien y el BOE
no. Retirarlo ya dejaría `accounts.json`, que es el que usa la web, sin nadie
que lo pueda regenerar. Lo decidió Albert.

### Cambio · Paso 1b·4: extraer las fichas del BOE con sus etiquetas originales
**Qué:** `parser_boe.py` lee la quinta parte con la máquina de estados del
paso 8, adaptada, y añade a cada cuenta su definición, su presentación, sus
movimientos y sus contrapartidas. Cada movimiento es ahora
`{"etiqueta": "a1", "texto": "..."}`, con `"etiqueta": null` cuando es el
texto que va detrás de la cabecera ("b) Se abonará por las enajenaciones...").
Lo guarda en `data/accounts_boe.json`. La 430 sale con a1-a3 y b1-b9 y sus 11
contrapartidas de siempre; la 642 tiene su propia ficha. De las 421 cuentas de
tres cifras, 358 tienen definición, 110 presentación y 254 movimientos en
columnas (en el `accounts.json` del OCR son 330, 95 y 240). `boe_reader.py` gana
`contenido_del_bloque` (párrafos y tablas en su orden), y `parrafos_del_bloque`
y `filas_de_las_tablas` se apoyan ahora en él y en `filas_de_la_tabla`.
Escrito por Claude, trozo a trozo, a petición de Albert, después de probar las
reglas en un prototipo.
**Por qué:** completa el parser nuevo. El BOE simplifica la máquina de
estados: el índice de cada subgrupo es una tabla (ya no hay que adivinar
rachas de títulos), cada párrafo viene entero (sobra la regla de la
minúscula) y las etiquetas vienen escritas.

### Decisión · El JSON del BOE va en un fichero aparte hasta el paso 1b·6
**Qué:** `parser_boe.py` escribe `data/accounts_boe.json`; `data/accounts.json`
lo sigue generando `parser.py`.
**Por qué:** los movimientos cambian de forma y la web no se adapta hasta el
1b·6. Sobrescribir `accounts.json` rompería la web, también la publicada en
cuanto se hiciera `push`. Además, en el 1b·5 hacen falta los dos ficheros para
compararlos.

### Decisión · Una frase de presentación dice en qué parte del balance figura
**Qué:** un párrafo es presentación si dice "figurar(á/án) en el activo /
pasivo / patrimonio / epígrafe". Además de las 95 que empiezan por
"Figurará", entran 50 nuevas: "Las cuentas de este subgrupo figurarán en el
pasivo corriente del balance", "Estas cuentas figurarán...", "La parte... que
tenga vencimiento a corto deberá figurar en el pasivo corriente...".
**Por qué:** es el pendiente que la hoja de ruta pedía resolver aquí. Mirar
dónde figura, y no solo la palabra, deja fuera las definiciones que usan el
verbo ("En esta cuenta figurarán todos aquellos elementos de transporte...").
Se revisaron una a una; el único caso discutible es una cuenta hipotética
("...creará la correspondiente cuenta en el grupo 2 que figurará en el
activo no corriente"). Lo decidió Albert.

### Decisión · Los párrafos que mezclan dos cosas se separan, sin tocar el texto
**Qué:** un párrafo con ". Figurará" en medio se parte en dos justo ahí
(definición y presentación). La frase "Su movimiento es el siguiente:" se
quita cuando va sola o al final de un párrafo. "Con carácter general, su
movimiento es el siguiente:" (37) se queda entera en la definición.
**Por qué:** si un párrafo mezclado va entero a un apartado, el otro dice
"sin definición" o "sin presentación", y es falso (la 556). El parser viejo
tiraba entero todo párrafo que acabara en "su movimiento es el siguiente:", y
con él "Corresponde a las empresas individuales", una presentación y el
matiz de "con carácter general". Partir y quitar una frase fija no inventa
nada. Lo decidió Albert.

### Decisión · En los títulos, dos códigos son un intervalo y tres o más, una lista
**Qué:** "700/705" es de la 700 a la 705 (también la 701 a la 704), y
"710/713" y "230/237" igual. "600/601/602/607" es una lista: la 606 no entra.
"230/237" se acepta aunque no lleve nombre, y "2403/2404" aunque no lleve
punto.
**Por qué:** es la notación del PGC ("Las cuentas 300/309"), y el texto lo
confirma: la ficha 710/713 habla de los subgrupos 33 a 36, es decir, de
cuatro cuentas. Con dos códigos seguidos ("570/571") da igual. Resuelve el
pendiente de la 230/237 del paso 8. Lo decidió Albert.

### Decisión · Los derivados de cobertura guardan su movimiento en la definición
**Qué:** la 1768, la 2553, la 5593 y la 5598 no tienen columnas: su
movimiento se queda en la definición, párrafo a párrafo, tal cual.
**Por qué:** es un movimiento en dos niveles con una condición ("b) Cuando el
derivado se utilice como instrumento de cobertura...: b1) Se cargará: i)...
ii)..."). En dos columnas planas se perdería la condición y los movimientos
parecerían valer siempre. Es la regla del paso 8: lo que no se puede repartir
sin inventar, a la definición. Pintar los dos niveles sería una mejora de la
web, a hablar aparte. Lo decidió Albert. Cierra el problema conocido de las
etiquetas `i) ii)` del paso 9.

### Decisión · La etiqueta de un movimiento tiene que encajar con su cabecera
**Qué:** bajo una cabecera con letra ("b) Se abonará:") solo son movimientos
las etiquetas de esa letra con número (`b1)`, `b2)`...). Bajo una cabecera sin
letra ("Se abonará:") valen `a)`, `b)`... y `a1)`, `a2)`...
**Por qué:** lo destapó el prototipo. La 761 numera sus abonos `a)`, `b)` bajo
un "Se abonará:" sin letra, y la 640 numera `a1)`... bajo un "Se cargará por
el importe íntegro...:" sin letra. Aceptar cualquier etiqueta colaría como
movimiento párrafos como "c) Si las participaciones se clasifican...", que
van detrás de los `b1) b2)` y hablan de cargo y abono a la vez.

### Problema conocido · Cuatro abonos y cargos con el verbo en medio de la frase
**Qué:** en la 833, la 834, la 836 y la 838, el segundo movimiento es "b) Al
cierre del ejercicio, se cargará con abono a la cuenta 137." Como el verbo no
va al principio, no se reconoce como cabecera y el párrafo va a la
definición.
**Por qué se deja:** para atraparlo habría que aflojar la regla de las
cabeceras, y entonces se colarían frases de definición como "Cuando se
produzca..., se cargará...". En la definición no se pierde nada. Se revisa en
el paso 1b·5.

### Cambio · Paso 1b·3: extraer el cuadro de cuentas del BOE
**Qué:** `tools/parser_boe.py`, nuevo, saca grupos, subgrupos, cuentas y
subcuentas de las tablas de la cuarta parte del BOE, con la misma forma de
dato de siempre. Los grupos salen de los dos primeros párrafos de cada bloque
(`grupo1`...`grupo9`), y el resto de las filas de su tabla: la primera celda
con texto es el código y la siguiente, el nombre. Resultado: 9 grupos, 78
subgrupos, 421 cuentas y 407 subcuentas, los mismos 915 códigos y los mismos
padres que el JSON del texto refundido. `tools/boe_reader.py` gana
`filas_de_las_tablas` y `version_vigente`, `texto_del_parrafo` pasa a
llamarse `texto_del_elemento` (ahora también lee celdas), y su prueba va
dentro de `if __name__ == "__main__":` para que no salga al importarlo.
Escrito por Claude, trozo a trozo, a petición de Albert.
**Por qué:** es la primera mitad del parser nuevo. Todavía no escribe JSON:
lo hará en el paso 1b·4, con las fichas.

### Decisión · Un verificador del cuadro que lo cruza con el resto del BOE
**Qué:** `tools/check_chart.py`, nuevo, imprime un informe con seis
apartados: códigos de las tablas que no llegan al cuadro (leídos por otro
camino que el parser), grupos y subgrupos vacíos, códigos repetidos o sin
padre, fichas de la quinta parte sin cuenta en el cuadro, códigos citados en
los modelos de cuentas anuales ("(6655)") sin cuenta en el cuadro, y nombres
que la ficha escribe distinto que el cuadro. Para que pueda pedir el cuadro,
`parser_boe.py` lo construye ahora en `extraer_cuadro_de_cuentas(raiz)` y su
resumen va dentro de `if __name__ == "__main__":`. Hoy los cinco primeros
apartados salen a cero, y el sexto lista nueve nombres que la propia ley
escribe de dos maneras ("Beneficio transferido (gestor)" en el cuadro,
"Beneficio transferido" en la ficha).
**Por qué:** lo pidió Albert al ver que el fallo del `<tbody>` se encontró
por casualidad: no sabíamos si había más. Un verificador solo vale si es
capaz de fallar, así que se probó reproduciendo los dos fallos reales: con
`findall` salen 761 códigos perdidos y 7 grupos vacíos; sin la fe de erratas,
los apartados 4, 5 y 6 encuentran, cada uno por su lado, los seis errores de
la tabla del BOE. Es un informe para leer, como `verify.py`, y no pruebas
automáticas (`unittest`): el sexto apartado no es un sí o un no. Su límite:
una cuenta que faltara a la vez en el cuadro, en las fichas y en los modelos
no la vería; para eso está la comparación con el texto refundido (paso 1b·5).

### Decisión · Un parser nuevo en vez de cambiar `parser.py`
**Qué:** `parser.py` no se toca y sigue generando `data/accounts.json`. Las
cuatro funciones que sirven igual (`nivel_de_cuenta`, `padre_de_cuenta`,
`crear_cuenta`, `codigo_de_la_cuenta`) se copian al fichero nuevo.
**Por qué:** se pensó en sacar de `parser.py` solo el cuadro del BOE y seguir
leyendo las fichas del Markdown, pero las fichas se reconocen comparando la
primera palabra del título con el nombre del cuadro, y el BOE escribe
`«Rappels»` donde el OCR escribía `"Rappels"`: varias fichas dejarían de
encontrarse. Además, `parser.py` hará falta en el paso 1b·5 para comparar. Las
funciones se copian en vez de importarse porque `parser.py` ejecuta todo su
proceso al importarlo, y es un fichero que se va a retirar.

### Decisión · El nivel se toma de las cifras y la columna lo confirma
**Qué:** el nivel de cada cuenta sale, como siempre, del número de cifras del
código. La columna en la que la tabla pone el código (0 para 2 cifras, 1 para
3...) se usa como segunda opinión: si no coinciden, sale un aviso.
**Por qué:** las cifras son la regla del propio PGC, y ya funcionaba. La
columna es una fuente independiente: que las dos digan lo mismo en las 902
filas da confianza, y si un día no coinciden, la tabla tiene algo raro.

### Decisión · Fe de erratas del cuadro de cuentas del BOE
**Qué:** `parser_boe.py` corrige dos nombres (500 y 501) y añade cuatro
cuentas que la tabla del BOE no trae (502, 1141, 6655 y 6656). Cada
corrección lleva al lado de dónde sale el dato bueno, y el programa avisa si
el BOE la corrige un día.
**Por qué:** la tabla de la cuarta parte del BOE tiene errores de contenido en
todas sus versiones: pega los nombres de la 500 y la 501, llama 501 a la 502,
y no trae la 1141, la 6655 ni la 6656. Las fichas de la quinta parte del
mismo BOE dan la 500, la 501, la 502 y la 1141 bien, y el texto refundido trae
la 6655 y la 6656 (que el BOE cita en la cuenta de pérdidas y ganancias).
Reproducir la tabla tal cual sería fiel al BOE, pero en una herramienta de
estudio una cuenta que falta es un dato falso que parece verdadero. Así no se
inventa nada: cada dato sale del propio texto legal. Lo decidió Albert. Las
dos cuentas añadidas desde el texto refundido llevan «», como sus vecinas en
el BOE.

### Decisión · Las erratas tipográficas del BOE se respetan; los puntos finales, no
**Qué:** "DETERIOROY", "DONACIONESY" y "ACTIVOSY" (cuatro subgrupos) quedan
tal como se publicaron. En cambio, a los ocho nombres de cuenta que el BOE
termina en punto se les quita, como al resto.
**Por qué:** las palabras pegadas no cambian el sentido, y la regla de la
sección 7 de `CLAUDE.md` es reproducir la norma como se publicó. Los puntos
finales son una inconsistencia de formato (los demás 900 nombres no lo
llevan) que se vería en el título de la ficha. Lo decidió Albert. Los nombres
de los grupos quedan como los escribe el BOE, en minúscula ("Financiación
básica"); el OCR los daba en mayúsculas.

### Decisión · Las filas de las tablas se buscan con `iter`, no con `findall`
**Qué:** `filas_de_las_tablas` recorre las filas con `tabla.iter("tr")`.
**Por qué:** en siete de las nueve tablas (todas menos las de los grupos 3 y
4) las filas van dentro de un `<tbody>`, que en HTML es opcional. Con
`findall("tr")` esos grupos salían sin cuentas y sin dar ningún error; lo
destapó la fe de erratas al no encontrar la 500. No hay tablas dentro de
tablas, así que `iter` no puede colar filas de otra.

### Cambio · Paso 1b·2: leer los bloques del XML del BOE
**Qué:** `tools/boe_reader.py` encuentra un bloque de `sources/boe/texto.xml`
por su `id`, se queda con su última versión y devuelve sus párrafos como texto
limpio, sin notas del BOE ni párrafos vacíos. Al final lleva una prueba con el
bloque `grupo4-2`: salen 401 párrafos, entre ellos "430. Clientes", y ninguna
nota. Lo escribió Claude, trozo a trozo, a petición de Albert.
**Por qué:** es la pieza de la que tirarán los pasos 1b·3 y 1b·4. Va en un
fichero aparte porque `parser.py` sigue leyendo el Markdown hasta el 1b·3.

### Decisión · Las notas del BOE quedan fuera por la estructura del XML
**Qué:** se leen solo los `<p>` hijos directos de la versión. El filtro por
clase (`nota_pie`, `nota_pie_2`) se deja de reserva, con un comentario que lo
explica.
**Por qué:** al probar se vio que las 168 notas del texto van todas dentro de
`<blockquote>` (73 en total), y que esos `<blockquote>` no contienen nada más.
Así que el filtro no estaba quitando nada: las notas desaparecían porque
`findall("p")` no entra en el `<blockquote>`. Se mantiene por si una versión
futura del BOE cambia esa forma, y la prueba de "notas coladas" lo vigila.

### Decisión · Los párrafos de las tablas no se leen en este paso
**Qué:** `parrafos_del_bloque` no entra en las `<table>`.
**Por qué:** el cuadro de cuentas de la cuarta parte va entero en tablas, y
leerlo es justo el paso 1b·3. Mezclarlo aquí sería trabajo de adelanto.

### Cambio · Paso 1b·1: descargar el texto del PGC desde el BOE
**Qué:** `tools/download_boe.py` pide a la API de datos abiertos del BOE el
índice y el texto completo de `BOE-A-2007-19884` y los guarda tal cual en
`sources/boe/indice.xml` (unos 33 KB) y `sources/boe/texto.xml` (unos 4 MB).
Escrito por Albert, trozo a trozo.
**Por qué:** es la copia fija sobre la que trabajará el parser a partir del
paso 1b·2. El parser todavía lee el Markdown.

### Decisión · La petición lleva `Accept: application/xml` y un límite de 60 s
**Qué:** cada petición pide XML de forma explícita y se da por fallida si en 60
segundos no llega respuesta.
**Por qué:** sin la cabecera, la API contesta 400 (se comprobó a propósito). Sin
el límite, un servidor colgado dejaría el script esperando para siempre. En los
dos casos `urlopen` lanza una excepción antes de guardar nada, así que un fallo
nunca deja un fichero roto en `sources/`.

### Decisión · Se guardan los bytes tal cual, y git no toca sus finales de línea
**Qué:** el script guarda con `write_bytes`, sin convertir a texto. Un
`.gitattributes` nuevo marca `sources/boe/*.xml` como `-text`.
**Por qué:** la copia tiene que ser idéntica, byte a byte, a lo que envió el
BOE. Sin el `.gitattributes`, git (con `core.autocrlf` activado en Windows)
entregaría los XML con los finales de línea cambiados a quien clonara el
repositorio.

### Decisión · El PGC se toma del BOE, no del texto del OCR
**Qué:** la fuente pasa a ser el texto consolidado del BOE (`BOE-A-2007-19884`),
descargado de su API de datos abiertos y guardado en `sources/boe/` (índice y
texto completo, en XML). Se añade a la hoja de ruta la "Fase 1 bis", seis pasos
entre el 16 y el 17. Cambian las secciones 4, 5, 7 y 8 de `CLAUDE.md`.
**Por qué:** las fichas destaparon fallos que venían del OCR (ver el pendiente
del paso 16), y cada forma nueva de mirar los datos destapaba otros. El XML del
BOE no tiene OCR: trae un párrafo por elemento, el cuadro de cuentas como
tabla y los movimientos con su etiqueta original (`a<sub>1</sub>)`). Es la
fuente oficial y se puede actualizar. Las partes cuarta y quinta vigentes son
de 2021, las mismas que el texto refundido, así que las diferencias serán
fallos del OCR y no cambios de la ley. Albert lo decidió sin apego al trabajo
ya hecho: la lógica del parser se aprovecha y lo hecho queda en el historial.
Se descartó que Claude transcribiera el PDF: sus errores serían plausibles e
invisibles, peores que los del OCR.

### Decisión · Se guarda una copia fija del BOE y se trabaja sobre ella
**Qué:** el parser lee `sources/boe/`, nunca la API. Actualizar es deliberado:
descargar, `git diff sources/`, regenerar y commit.
**Por qué:** así el JSON es reproducible sin conexión, la web no cambia ni se
rompe porque cambie el BOE, y cada actualización de la ley queda en un commit
donde se ve qué cambió. Se descarga el texto completo en un solo fichero
(unos 4 MB) porque incluye ya las partes que necesitarán las fases 4 y 5.

### Decisión · Los movimientos guardarán su etiqueta original
**Qué:** a partir del paso 1b·4, cada movimiento será
`{"etiqueta": "a1", "texto": "..."}`, con `"etiqueta": null` para la frase de
entrada.
**Por qué:** la fuente ya trae la etiqueta. Tirarla para reconstruirla en la
web, con riesgo de equivocarse (como pasó con la 640), no tiene sentido.

### Cambio · Paso 16: mostrar el movimiento en columnas enfrentadas
**Qué:** la ficha tiene un apartado "Movimiento" con "Se cargará / Debe" y "Se
abonará / Haber" lado a lado (CSS flex). Cada movimiento lleva su número (a1,
b1...) y sus contrapartidas son etiquetas de color dentro de la frase. Escrito
por Albert, trozo a trozo.
**Por qué:** es lo que convierte la ficha en una herramienta para aprender
asientos: se ve qué hace subir o bajar la cuenta y contra qué otra.

### Decisión · Las frases en minúscula continúan el título y van sin número
**Qué:** una frase del movimiento que empieza en minúscula ("por el importe
íntegro de las remuneraciones devengadas:") se pinta sin número, ocupando todo
el ancho, como continuación de "Se cargará" o "Se abonará". El contador solo
avanza con las frases en mayúscula.
**Por qué:** el parser guarda lo que sigue a "Se cargará" como si fuera un
movimiento más. Al numerarlo todo, la 640 salía con la numeración desplazada
uno respecto al PGC, y unas 220 cuentas con un solo movimiento llevaban un
"a1" que el PGC no tiene. Es la misma regla que ya usa el parser (una línea en
minúscula sigue a la anterior). Albert eligió que la frase ocupe todo el
ancho, sin el hueco del número, porque se lee mejor.

### Decisión · Las contrapartidas se marcan dentro de la frase
**Qué:** cada frase se parte por los números (`split(/(\d+)/)`) y solo se
convierten en etiqueta los números que están en la lista de contrapartidas de
su columna (paso 9). El texto se cuelga con `createTextNode`, nunca con
`innerHTML`.
**Por qué:** es lo que muestran la maqueta D y la sección 6 de CLAUDE.md, y
enseña qué cuenta va con cada frase. Reutilizar la lista del paso 9 evita
volver a adivinar qué número es una cuenta: un "artículo 239" se queda como
texto.

### Decisión · Los colores cruzados se deciden solo en el CSS
**Qué:** todas las contrapartidas son `<span class="contrapartida">`. Su color
lo da la columna en la que están: `.columna-cargo .contrapartida` en ámbar
(el haber) y `.columna-abono .contrapartida` en azul (el debe).
**Por qué:** el JavaScript no sabe nada de colores. El contexto decide el
aspecto, y si un día se quiere cambiar, se cambia en un solo sitio. El azul y
el ámbar están ajustados para cumplir el contraste mínimo de 4,5 a 1.

### Pendiente · Fallos de datos que ha destapado la ficha
**Qué:** al ver las fichas completas aparecieron:
- la 642 pegada a la 641: el OCR perdió su título en un salto de página;
- 6 párrafos partidos en dos por saltos de página (1, 143, 24, 5, 548);
- 40 frases de presentación ("Las cuentas de este subgrupo figurarán...") que
  el parser guarda en la definición, porque solo reconoce las que empiezan por
  "Figurará"; mientras tanto, la ficha dice que no hay presentación cuando sí
  la hay;
- la numeración a1/b1 está reconstruida y falta comprobarla contra el texto.
**Siguiente:** antes del paso 17 se decide cómo atacarlos. Candidata: usar
como fuente el texto consolidado del BOE, que se descarga en XML, sin OCR,
desde su API de datos abiertos (`BOE-A-2007-19884`).

### Decisión · Las maquetas, en `docs/mockups/` y enlazadas desde CLAUDE.md
**Qué:** las cuatro maquetas se guardan en `docs/mockups/` con nombres en
inglés y sin espacios (`a-notebook.png`, `b-wiki.png`, `c-tool.png`,
`d-wiki-facing-movement.png`). La sección 6 de `CLAUDE.md` dice qué se toma de
cada una.
**Por qué:** cada sesión de Claude empieza sin memoria, y la maqueta solo
existía fuera del proyecto. Si `CLAUDE.md` dice dónde está, Claude la mira sin
que Albert tenga que acordarse. Al revisarlas apareció que la maqueta A tiene
los colores de las contrapartidas al revés (azul en el cargo), así que la
referencia para el movimiento es la D.

### Cambio · Paso 15: añadir la ficha de cuenta
**Qué:** al pulsar una cuenta en la lista o en el árbol se muestra su ficha:
título, etiquetas (nivel y grupo), definición y presentación en el balance. El
esqueleto de la ficha está en `index.html` y `mostrarFicha` solo rellena sus
huecos. `crearElementoDeCuenta` fabrica el `<li>` de una cuenta, con su texto y
su clic, y lo usan la lista y el árbol. Escrito por Albert, trozo a trozo.
**Por qué:** la ficha es el corazón del módulo 1. El buscador y el árbol
existen para llegar a ella. Los movimientos quedan para el paso 16.

### Decisión · El esqueleto de la ficha en el HTML y los datos con `textContent`
**Qué:** la estructura de la ficha (encabezados y huecos) se escribe en
`index.html`. JavaScript solo pone texto en los huecos, siempre con
`textContent` y nunca con `innerHTML`.
**Por qué:** cada fichero hace un trabajo: el HTML decide la forma y el
JavaScript, los datos. Además, `innerHTML` interpreta como HTML lo que recibe,
y con datos que vengan de fuera (los ejercicios importados del simulador) es la
puerta de entrada de los ataques de inyección. `textContent` escribe el texto
tal cual.

### Decisión · El grupo de la etiqueta se calcula con un índice por código
**Qué:** `cuentasPorCodigo` (`{ "430": cuenta, "4": grupo, ... }`) se construye
una vez al cargar. El grupo de una cuenta es `cuentasPorCodigo[codigo[0]]`.
**Por qué:** es lo que se decidió al revisar el JSON: el grupo no se guarda en
cada cuenta, se deduce de la primera cifra del código.

### Decisión · Los huecos se dicen, no se esconden
**Qué:** si una cuenta no tiene definición o presentación, su apartado se
muestra igualmente con un aviso en cursiva y gris: "Sin definición en el texto
del PGC."
**Por qué:** si algo no está, se dice que no está (CLAUDE.md, sección 7).
Esconder el apartado no permitiría distinguir "el PGC no lo trae" de "la web ha
fallado". El aviso se distingue a la vista para no confundirlo con el texto de
la norma. 91 cuentas y la mayoría de subcuentas no tienen definición propia.

### Decisión · Provisional: clic en el `<li>` y la página sube hasta la ficha
**Qué:** las cuentas se abren con un escuchador de `click` en su `<li>`, y
`mostrarFicha` hace `scrollIntoView()`.
**Por qué:** la ficha está arriba y las cuentas, muy abajo. Sin el desplazamiento,
el clic parecería no hacer nada. Las dos cosas son provisionales. En el paso 17
las cuentas pasarán a ser enlaces (`#430`), que además se podrán usar con el
teclado, y en el paso 18 la ficha irá al lado del árbol y el desplazamiento
sobrará.

## 2026-10-12

### Decisión · Respetar la errata "CARÁCTERÍSTICAS" del subgrupo 50
**Qué:** el nombre del subgrupo 50 se deja como "EMPRÉSTITOS, DEUDAS CON
CARÁCTERÍSTICAS ESPECIALES Y OTRAS EMISIONES ANÁLOGAS A CORTO PLAZO", con la
tilde de más.
**Por qué:** la errata está en el texto oficial. Albert la comprobó en el BOE, y
también aparece en el PDF del ICAC y en el texto refundido. La herramienta
reproduce la norma tal como está publicada, y `FE_DE_ERRATAS` solo corrige lo
que estropeó el OCR, no el texto oficial. El mismo texto lo escribe bien en el
subgrupo 15 ("CARACTERÍSTICAS").

### Cambio · Ordenar las cuentas por código antes de guardar el JSON
**Qué:** el parser hace `cuentas.sort(key=codigo_de_la_cuenta)` justo antes de
escribir `data/accounts.json`. Resuelve el pendiente del subgrupo 53, que salía
antes que el 52. El `git diff` del JSON solo mueve el bloque del 53 a su sitio,
y el verificador da el mismo informe.
**Por qué en el parser:** arreglarlo en la web habría dejado el JSON mal y
obligado a ordenar en cada sitio que lo use. Una errata más en
`FE_DE_ERRATAS` solo habría arreglado este caso. El orden del cuadro de cuentas
lo marca el propio código, así que ordenar por él es una regla, no un parche, y
cubre también cualquier desorden futuro del OCR.
**Por qué funciona:** los códigos son texto, y el texto se ordena como en un
diccionario (`"52"` < `"520"` < `"5209"` < `"53"`), que es exactamente el orden
del árbol: cada código va seguido de todo lo que cuelga de él. Si los códigos
fueran números, este orden no saldría.

### Cambio · Paso 14: añadir el árbol del cuadro de cuentas
**Qué:** un `<nav>` con el cuadro de cuentas plegable: grupos → subgrupos →
cuentas. `agruparPorPadre` recorre las cuentas una vez y construye un índice
`{ código del padre: [hijos] }`. `pintarArbol` lo recorre con tres bucles
anidados y cuelga cada pieza de la caja que le toca. Una regla de CSS
(`details details`) aplica sangría a cada nivel. Escrito por Albert, trozo a
trozo.
**Por qué:** una segunda forma de llegar a las cuentas, además del buscador,
que enseña la estructura del PGC de un vistazo. De momento va encima de la
lista: colocarlo como barra lateral es trabajo de maquetación (pasos 16 y 18).

### Decisión · Plegar con `<details>` y `<summary>`, sin JavaScript
**Qué:** cada grupo y cada subgrupo es un `<details>`, con su título en un
`<summary>`.
**Por qué:** HTML ya trae el plegado de serie, y funciona con teclado y con
lectores de pantalla. Escribirlo a mano con eventos habría sido más código para
hacer lo mismo, y peor.

### Decisión · Tres niveles en el árbol, sin subcuentas
**Qué:** el árbol baja hasta las cuentas (430) y no muestra las subcuentas
(4300).
**Por qué:** es lo que pide la hoja de ruta, y con tres bucles anidados el
código todavía se lee bien. Un cuarto nivel pediría recursión, que aún no toca.
Las subcuentas siguen siendo accesibles desde el buscador, y el índice
`hijosPorPadre` ya las contiene por si se añaden más adelante.

### Decisión · Un índice de hijos en vez de filtrar en cada nivel
**Qué:** los hijos de cada código se buscan en `hijosPorPadre`, que se
construye una sola vez, en lugar de hacer un `filter` sobre las 915 cuentas
para cada grupo y subgrupo.
**Por qué:** no es por velocidad, porque con 915 cuentas daría igual. Es el
patrón de "agrupar una vez y consultar muchas", y se volverá a usar en el
simulador (el libro mayor agrupa los asientos por cuenta).

### Pendiente · El subgrupo 53 sale antes que el 52
**Qué:** el árbol ha descubierto que, en `data/accounts.json`, el 53 va antes
que el 52. Es el único par desordenado de todo el fichero.
**Por qué pasa:** en el texto fuente, el OCR dejó la línea del 53 rota
(`# 212 53. INVERSIONES FINANCIERAS...`, línea 4408) y colocada antes que la del
52. El parser respeta el orden del texto. Se arreglará en un commit `fix:`
aparte, no dentro de este paso.

### Cambio · Paso 13: añadir el buscador de cuentas
**Qué:** una caja de búsqueda encima de la lista. Cada vez que cambia su texto
(evento `input`), `filtrarCuentas` se queda con las cuentas que encajan y
`pintarLista` vacía el `<ul>` y lo vuelve a llenar solo con ellas. `app.js` se
reorganizó para separar *cargar* (una vez) de *pintar* (en cada búsqueda), y las
cuentas se guardan en una variable de fuera, `todasLasCuentas`. Escrito por
Albert, trozo a trozo.
**Por qué:** es la puerta de entrada al módulo 1. Más adelante, de un resultado
se llegará a su ficha.

### Decisión · El código se busca por el principio y el nombre en cualquier posición
**Qué:** el código usa `startsWith` y el nombre usa `includes`.
**Por qué:** así "43" da el subgrupo 43 y todo lo que cuelga de él (430, 4300...)
y no cuentas como 143, que llevan "43" en medio. Sigue la lógica del cuadro de
cuentas. En los nombres, en cambio, la palabra buscada puede estar en cualquier
sitio ("Anticipos de clientes").

### Decisión · Comparar sin mayúsculas ni tildes
**Qué:** el texto escrito y el nombre de la cuenta pasan los dos por
`normalizar`: minúsculas, `normalize("NFD")` para separar letra y tilde, y una
expresión regular que borra las tildes sueltas.
**Por qué:** sin esto, "clien" no encontraba "Clientes" ni "caja" encontraba
"Caja, euros". Nadie escribe con mayúsculas y tildes cuando busca deprisa. Como
efecto secundario, "ñ" se convierte en "n" ("campana" encuentra "campaña"). Se
acepta, porque en un buscador es más una ayuda que un problema.

### Decisión · Filtrar con `filter` en vez de con el bucle
**Qué:** primero se escribió el filtro con `for`, `if` y `push`. Después se
cambió por `todasLasCuentas.filter(function (cuenta) { ... })` y se comprobó que
daba los mismos resultados.
**Por qué:** hace lo mismo con menos piezas: la condición queda sola y el
trabajo de recorrer y apuntar lo hace `filter`. Además, es la forma en que se
escribe en casi todo el código JavaScript y va a aparecer mucho en los pasos
siguientes. Albert la lee sin problemas, que es el criterio del proyecto. Las
funciones flecha (`=>`) quedan para más adelante.

### Cambio · Paso 12: cargar y listar las cuentas en la web
**Qué:** `web/app.js` lee `data/accounts.json` con `fetch` y escribe cada
elemento como `codigo · nombre` dentro de un `<ul>` vacío de `web/index.html`.
Se listan los 915 elementos tal cual vienen: grupos, subgrupos, cuentas y
subcuentas.
**Por qué:** es la base de toda la fase 2. El buscador, el árbol y las fichas
trabajan sobre esta lista ya cargada en el navegador. Separar los niveles es
trabajo del árbol (paso 14), no de este paso.

### Decisión · Probar la web con `python -m http.server` desde la raíz del proyecto
**Qué:** para ver la web en local se arranca el servidor en la raíz y se abre
`http://localhost:8000/web/`. Abrir `index.html` con doble clic ya no sirve.
**Por qué:** con `file://` el navegador bloquea `fetch` por seguridad (CORS:
una página sin origen no puede leer ficheros del disco). Se comprobó a propósito
y el error salió en la consola. El servidor se arranca desde la raíz para que
`web/` y `data/` sean visibles, igual que en GitHub Pages, que publica `main`
desde `/`. Así la misma ruta `../data/accounts.json` funciona en los dos sitios.

### Decisión · El grupo de cada cuenta se muestra en la ficha, no se guarda en el JSON
**Qué:** al revisar el JSON, Albert vio que para estudiar es importante saber a
qué grupo pertenece cada cuenta ("Grupo 2 · Activo no corriente"). Queda como
requisito del paso 15 en la hoja de ruta: una etiqueta de la ficha.
**Por qué:** el dato ya está en el JSON. La primera cifra del código es el
grupo, y el nombre del grupo está en su propia ficha. Guardarlo en cada una de
las 915 cuentas repetiría el mismo nombre cientos de veces, y una corrección
podría dejar copias que se contradicen. Un dato, un sitio.

### Cambio · Paso 11: corregir los casos que el parser no cogía bien
**Qué:** con el informe del verificador delante se revisaron los avisos contra
el texto y el PDF original, y se corrigió:
- **Fichas compartidas detrás del índice** (`680/681/682`, `770/771/772`,
  `790/791/792`...): la regla de la racha comparaba títulos enteros y ahora
  compara código a código.
- **Números de página pegados al principio de una línea** (`305 Cuando...`,
  `#### 222 23. INMOVILIZACIONES...`): 6 líneas, todas números de página. Se
  recupera, entre otros, el título del subgrupo 23.
- **Columnas cambiadas en 108, 109, 472 y 477**: la regla que detecta frases
  mixtas ("se cargarán ... y se abonarán") miraba la línea entera, y un "se
  cargará" dentro de un abono hacía que los abonos acabaran en los cargos.
  Ahora mira solo la primera frase de la cabecera, y una cabecera mixta ya no
  se pega al movimiento anterior.
- **Tres erratas del OCR**, comprobadas en el PDF: el `a3)` de la 400, el
  nombre del subgrupo 53 y el título perdido de la 570/571.
- **El verificador** detecta también "b) Se abonará por..." dentro de un
  movimiento, que antes se le escapaba.

Resultado: las cuentas de tres cifras sin ninguna ficha bajan de 80 a 53, las
que tienen definición suben de 308 a 330 y las que tienen movimientos, de 220
a 240. No queda ningún número de movimiento que no sea una cuenta.
**Por qué:** es la revisión que pedía la hoja de ruta para cerrar la fase 1.

### Decisión · Una fe de erratas para los fallos únicos del OCR
**Qué:** `parser.py` tiene una tabla `FE_DE_ERRATAS` con pares "texto del
OCR → texto corregido", que se aplica al texto entero nada más leerlo. Cada
entrada indica la página del PDF donde se comprobó. Si una errata deja de
aparecer en el texto, el parser avisa.
**Por qué:** una regla para un caso único sería un patrón que nadie entendería.
Así la corrección queda a la vista y documentada, y `sources/` sigue sin
tocarse. Ninguna errata se escribe sin comprobarla en el PDF (sección 7 de
CLAUDE.md).

### Decisión · El PDF original entra en `sources/`
**Qué:** se añade `PLAN_GENERAL_DE_CONTABILIDAD_accesible.pdf` (1,7 MB).
**Por qué:** es el original contra el que se comprueba todo. Su numeración de
páginas no coincide con las marcas `{N}` del `.md`, que viene del OCR de otra
edición: para buscar algo, mejor una frase con Ctrl+F.

### Problema conocido · Lo que el OCR desordenó a fondo
**Qué:** quedan sin arreglar, a propósito:
- **230/237/239:** un trozo desordenado, con un título perdido.
- **El bloque inicial del grupo 7** ("En general, todas las cuentas del grupo
  7...") aparece antes del título GRUPO 7, con el índice del subgrupo 70
  aplastado dentro. Por eso 700–706 no tienen ficha y ese texto cae en la 699.
- **490:** tiene dos alternativas de movimiento ("1. Cuando..." / "2.
  Cuando...") que no caben en dos columnas sin inventar cómo separarlas.
- **1768, 2553, 5593 y 5598:** movimientos en tres niveles (`b1) Se cargará:
  i) ii)`) que la forma de los datos no contempla.
- **El 53 aparece antes que el 52** en la lista. Solo afecta al orden.
- **Un párrafo partido en el grupo 1** ("...a las cuentas 663 y" / "763.").
- **53 cuentas sin ficha.** Muchas no la tienen en el PGC porque se explican
  en su subgrupo (por ejemplo, las del grupo 3).

**Por qué se deja:** arreglarlos exigiría reescribir párrafos enteros a mano.
Se retomarán si alguno estorba de verdad en la fase 2.

## 2026-10-10

### Cambio · Paso 10: el verificador de los datos extraídos
**Qué:** `tools/verify.py` lee `data/accounts.json` y saca un informe con seis
apartados: resumen, cuentas sin ninguna ficha (80), números de los movimientos
que no son ninguna cuenta (2), contrapartidas de una sola cifra (55), textos
sospechosos (12) y subgrupos fuera de orden (1).
**Por qué:** el parser falla en casos raros, y este informe es lo que los
enseña. Es la lista de trabajo del paso 11.

### Decisión · El verificador es un script aparte y no arregla nada
**Qué:** no forma parte de `parser.py`, solo lee el JSON y solo informa.
**Por qué:** revisa el resultado sin depender de cómo se hizo, y se puede
ejecutar después de cada corrección para ver que el problema desaparece.
Arreglar se decide a mano, caso por caso, en el paso 11.

### Decisión · Buscar los números que el filtro dejó fuera, no las referencias rotas
**Qué:** la hoja de ruta pedía contar "referencias que apuntan a cuentas que no
existen". Se cambia por "números de los movimientos que no son ninguna cuenta".
**Por qué:** el filtro del paso 9 impide guardar referencias a cuentas que no
existen, así que esa cifra sería siempre 0. Lo que sí informa es lo que el
filtro descartó: así han salido dos números de página pegados a un movimiento.

### Problema conocido · Movimientos con etiquetas `i) ii)`
**Qué:** algunas cuentas (1768, 2553, 5593, 5598) numeran los movimientos con
`i) ii)` en vez de `a1) a2)`. El parser no lo reconoce y deja las dos columnas
pegadas en una.
**Por qué se deja:** lo ha encontrado el verificador; se corrige en el paso 11.

### Cambio · Paso 9: detectar las referencias entre cuentas
**Qué:** cada cuenta tiene dos campos nuevos, `contrapartidas_cargos` y
`contrapartidas_abonos`, con los códigos que mencionan sus movimientos. La
430 da 437, 70 y 762 en los cargos, y 431, 432, 436, 437, 57, 650, 706, 708 y
709 en los abonos: las 11 que pedía la hoja de ruta. 361 cuentas tienen
alguna contrapartida.
**Por qué:** son las etiquetas de colores clicables de la ficha (pasos 16 y
17). Así la web no tiene que buscarlas en el texto.

### Decisión · Una contrapartida es cualquier número de un movimiento que sea una cuenta
**Qué:** se cogen todos los números de cada movimiento y se quedan los que
son el código de una cuenta que existe. Sin repetir, ordenados y separados
por columna.
**Por qué:** se miró qué palabra va delante de cada número de los movimientos
y casi siempre es "cuenta", "subgrupo", "cuentas", "ó" o "y". Una regla así
de sencilla basta, y el filtro de "que exista" evita que se cuelen números
sueltos. Los códigos se ordenan como texto ("437" antes que "57"), que para
unas etiquetas da igual.

### Problema conocido · Una contrapartida falsa en la 400
**Qué:** por el `a<sup>3</sup>` del OCR, la 400 tiene el grupo 3 entre sus
contrapartidas de abono.
**Por qué se deja:** es el mismo fallo del OCR ya apuntado en el paso 8. Al
corregirlo en el paso 11 desaparece también este.

## 2026-10-09

### Cambio · Paso 8: extraer las definiciones y los movimientos
**Qué:** el parser lee la Quinta Parte con una máquina de estados y añade a
cada cuenta su `definicion`, su `presentacion` ("Figurará en..."), sus
`cargos` y sus `abonos`. La 430 sale con 3 cargos y 9 abonos. De las 421
cuentas de tres cifras, 308 tienen definición y 220 tienen movimientos en
columnas.
**Por qué:** es el contenido de las fichas que mostrará la web (pasos 15 y 16).

### Decisión · La forma de la ficha
**Qué:** cuatro campos nuevos en cada cuenta del mismo `accounts.json`, con
estas reglas:
1. `cargos` y `abonos`, no `a` y `b`: se decide por el verbo ("cargará" o
   "abonará"), porque en las cuentas de pasivo el `a)` es el abono.
2. Todo son listas, aunque haya un solo elemento o ninguno. Una lista vacía
   quiere decir que el texto no dice nada de eso.
3. Las etiquetas `a1)`, `b2)` se quitan: la posición en la lista ya las da.
4. Lo que no encaja en cargos o abonos se queda en `definicion` tal cual: los
   movimientos en prosa, el "análogo al señalado para la cuenta 430" y las
   frases que hablan de cargo y abono a la vez.
5. Las fichas compartidas (`600/601/602/607`) se copian a cada cuenta.
6. Mismo fichero: una cuenta es una ficha.

**Por qué:** que la web tenga siempre la misma forma, y que no se pierda ni
se invente nada (sección 7 de CLAUDE.md).

### Problema conocido · Fichas que el OCR desordenó
**Qué:**
- El título `570/571. Caja` no está en el texto. Su definición acaba en el
  subgrupo 57, y la 570 y la 571 se quedan sin ficha.
- El trozo de `230/237` está desordenado: falta el "a) Se cargarán:" antes
  de los `a1) a2)`, y el texto de la 239 se queda en la 230 y la 237.
  Además, `230/237` seguramente quiere decir "de la 230 a la 237", y el
  parser lo lee como "la 230 y la 237".
- En la 400, el OCR escribió `a<sup>3</sup> )` en vez de `a3)`, y el tercer
  abono queda pegado al segundo.
- En el subgrupo 44, una definición empieza por un `305` que sobra.
- 113 cuentas de tres cifras no tienen definición. Muchas porque el PGC las
  define a nivel de subgrupo, pero no todas.

**Por qué se deja:** son casos sueltos, cada uno distinto. El verificador del
paso 10 los tiene que sacar a la luz, y se corrigen en el paso 11.

### Cambio · Paso 7: extraer el cuadro de cuentas a `data/accounts.json`
**Qué:** el parser recorta la Cuarta Parte del PGC y saca cada grupo,
subgrupo, cuenta y subcuenta con su código y su nombre. Salen 9 grupos, 78
subgrupos, 421 cuentas y 407 subcuentas, y la 430 se llama "Clientes".
**Por qué:** es la base de todo lo demás: el buscador, las fichas y el
simulador leen de este fichero.

### Decisión · La forma del dato: una lista plana de cuentas
**Qué:** cada cuenta es una ficha con `plan`, `codigo`, `nivel`, `nombre` y
`padre`. Todas van en una sola lista, sin anidar. Se incluyen las subcuentas
de 4 y 5 cifras. El plan se llama `pgc-general`.
**Por qué:**
- **Lista plana:** es fácil de recorrer para buscar (paso 13) y de ampliar
  con la definición y los movimientos (paso 8). El árbol se reconstruye con
  `padre` cuando haga falta (paso 14).
- **`codigo` como texto:** un código no es una cantidad, nunca se suma.
- **`plan` en cada cuenta:** cuando llegue el PGC de PYMES, sus cuentas
  (`pgc-pymes`) podrán vivir en la misma lista sin mezclarse, aunque repitan
  código.
- **`pgc-general` y no `pgc-normal`:** es el nombre oficial del plan, a
  propuesta de Albert.
- **Subcuentas incluidas:** son parte oficial del cuadro y el simulador las
  necesitará (paso 27).
- **Nombres de campo en castellano y sin tildes:** son vocabulario del
  dominio, y sin tildes se escriben sin problemas en JavaScript.
- **Los nombres, tal como vienen:** los subgrupos en mayúsculas y las cuentas
  no. El texto es la fuente de verdad; cómo se muestran lo decide la web.

### Problema conocido · El subgrupo 53 sale con basura y fuera de orden
**Qué:** el OCR leyó la línea como `# 212 53. INVERSIONES FINANCIERAS A CORTO
PLAZO EN PARTES VINCULADAS grupo asociadas`, antes del subgrupo 52. El `212`
(un número de página) se descarta solo, pero el nombre se queda con
"grupo asociadas" al final, y en la lista el 53 aparece antes que el 52.
**Por qué se deja:** es un caso único. Lo tiene que encontrar el verificador
del paso 10, y se corregirá en el paso 11.

### Cambio · Paso 6: limpiar las marcas de página del OCR
**Qué:** el parser quita las 406 marcas `{N}-----`, recorta los espacios del
final de cada línea y deja una sola línea en blanco donde había varias. El
texto pasa de 9689 a 8875 líneas y no queda ninguna llave `{`. Cada limpieza es
una función con su nombre.
**Por qué:** es la basura más regular del OCR y la que estorba a todo lo
demás. Los dobles espacios no se tocan: están todos dentro de tablas y sirven
para alinear las columnas.

### Decisión · El texto se limpia en el código, no en el fichero fuente
**Qué:** `sources/` sigue intacto. La limpieza se hace en memoria cada vez que
se ejecuta el parser. Se descartó tanto limpiar el `.md` y guardarlo encima
como regenerarlo desde el PDF sin paginado.
**Por qué:** si la limpieza tiene un fallo, se corrige el código y se vuelve a
ejecutar; el original sigue ahí para comprobar. Regenerar desde el PDF solo
quitaba las marcas, que son lo más fácil, y traía un texto nuevo con errores
desconocidos. Además, las marcas dicen en qué página está cada cosa, por si un
día se quiere citar la página.

### Problema conocido · Párrafos partidos por un salto de página
**Qué:** unas 46 veces el PGC cambiaba de página a media frase. Al quitar la
marca, la frase queda partida en dos párrafos.
**Por qué se deja:** el paso 6 ya trae dos conceptos nuevos, y unirlos bien
tiene trampas (abreviaturas, tablas). Se arreglará cuando estorbe: en el paso
8, si parte alguna definición, o en el paso 11.

### Decisión · Albert es el único que usa git
**Qué:** Claude ya no ejecuta comandos de git que cambien el repositorio. Da los
comandos explicados y Albert los escribe. Queda escrito en la sección 8 de
CLAUDE.md.
**Por qué:** git se aprende repitiéndolo, y si lo hace Claude, Albert no lo
practica.

### Cambio · Paso 5: leer el texto fuente del PGC
**Qué:** `tools/parser.py` abre `sources/Texto refundido PGC 2021.md`, lo lee
entero y dice cuántas líneas tiene (9689).
**Por qué:** es la base del parser. Antes de limpiar y extraer nada hay que
poder leer el texto sin que se rompan las tildes ni las eñes.

### Decisión · Decir siempre `encoding="utf-8"` al leer y escribir ficheros
**Qué:** todas las lecturas y escrituras de texto dicen la codificación de forma
explícita.
**Por qué:** sin ella, Python en Windows usa la tabla `cp1252` y este fichero
falla con un `UnicodeDecodeError`. Se comprobó a propósito. Las versiones más
nuevas de Python ya usan UTF-8 por defecto, pero decirlo deja claro qué se
espera y funciona igual en cualquier versión.

### Decisión · Las rutas se calculan desde el propio script
**Qué:** el parser busca el texto a partir de dónde está `parser.py`
(`Path(__file__)`), no de la carpeta desde la que se lanza.
**Por qué:** así funciona igual desde la raíz del proyecto, desde `tools/` o
desde cualquier otro sitio.

## 2026-10-08

### Cambio · Renombrar la hoja de ruta a `docs/roadmap.md`
**Qué:** `docs/hoja-de-ruta.md` pasa a llamarse `docs/roadmap.md`, y se
actualizan los enlaces de CLAUDE.md y del README.
**Por qué:** era el único fichero que no seguía la regla de nombres en inglés.

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