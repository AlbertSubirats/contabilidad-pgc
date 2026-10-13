# Changelog

El historial de **decisiones** y **cambios** del proyecto, con su *por qué*.

- La entrada más reciente va **arriba**.
- Cada entrada es una *Decisión* (qué se eligió y por qué) o un *Cambio* (qué se
  consiguió en un paso).
- Las decisiones de partida no se repiten aquí: están en la tabla de la
  sección 4 de [CLAUDE.md](CLAUDE.md#4-decisiones-ya-tomadas).

---

## 2026-10-14

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