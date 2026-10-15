# Hoja de ruta

Cada paso es **un commit**. Se hacen en orden. Al terminar uno, se para y se
espera a que Albert pida el siguiente.

Los pasos de las fases 0, 1 y 2 están detallados. Los de las fases 3, 4 y 5 están
esbozados a propósito: cuando lleguemos, sabremos mucho más y los detallaremos
entonces. Un plan que pretende saberlo todo a un año vista miente.

**Leyenda de cada paso:** *Qué* se hace · *Aprendes* qué conceptos nuevos
aparecen · *Compruebas* cómo saber que ha funcionado.

---

## Fase 0 · Que exista algo y esté publicado

El objetivo de esta fase no es contabilidad: es que Albert tenga un ciclo
completo — escribo algo, lo guardo en git, aparece en internet — antes de meterse
en nada complicado. Son cuatro pasos cortos.

### Paso 1 · Arrancar el repositorio
**Qué:** `git init`, un `.gitignore`, un `README.md` que diga qué es esto.
**Aprendes:** qué es un repositorio, qué es un commit y por qué no es lo mismo que
guardar un fichero, qué hace `.gitignore`.
**Compruebas:** `git log` muestra un commit tuyo.
`chore: iniciar el repositorio`

### Paso 2 · La primera página
**Qué:** `web/index.html` con lo mínimo: un título y un párrafo.
**Aprendes:** la estructura de un documento HTML, qué es una etiqueta, para qué
sirven `<head>` y `<body>`.
**Compruebas:** abres el fichero con doble clic y lo ves en el navegador.
`feat: añadir la página inicial`

### Paso 3 · Publicarla en internet
**Qué:** crear el repositorio en GitHub, subirlo, activar GitHub Pages.
**Aprendes:** qué es un remoto, qué hacen `push` y `pull`, qué significa que algo
esté "desplegado".
**Compruebas:** abres la URL desde el móvil y ves tu página.
`chore: publicar en GitHub Pages`

> Este paso va aquí a propósito, tan pronto. A partir de ahora cada mejora se ve
> publicada el mismo día, y eso cambia mucho las ganas de seguir.

### Paso 4 · Un poco de estilo
**Qué:** `web/styles.css` con el fondo de papel, las tipografías y poco más.
**Aprendes:** qué es CSS, cómo se enlaza, qué es un selector, qué son las
variables CSS y por qué los colores se declaran una sola vez.
**Compruebas:** la página cambia de aspecto.
`feat: añadir la hoja de estilos base`

---

## Fase 1 · Los datos

Aquí es donde vive el valor del proyecto. Todo lo demás se apoya en esto. Es la
fase con más Python, que es el lenguaje que Albert ya conoce un poco, así que es
buen sitio para consolidar.

### Paso 5 · Leer el fichero fuente
**Qué:** `tools/parser.py` que abre el texto del PGC, cuenta sus líneas y
las imprime.
**Aprendes:** `pathlib`, abrir ficheros, por qué hay que decir `encoding="utf-8"`
y qué pasa si no lo dices.
**Compruebas:** `python tools/parser.py` imprime un número de líneas
razonable.
`feat: leer el texto fuente del PGC`

### Paso 6 · Limpiar la basura del OCR
**Qué:** quitar las marcas `{300}-----`, normalizar espacios y líneas en blanco.
**Aprendes:** qué es una expresión regular y cómo leerla despacio; cómo partir el
código en funciones pequeñas con un nombre que diga lo que hacen.
**Compruebas:** buscar `{` en el texto limpio no encuentra ninguna marca de página.
`feat: limpiar las marcas de página del OCR`

### Paso 7 · Extraer el cuadro de cuentas
**Qué:** recorrer el texto y sacar grupos, subgrupos y cuentas con su código y su
denominación. Guardarlo en `data/accounts.json`.
**Aprendes:** diccionarios y listas de diccionarios, cómo se diseña la forma de
unos datos antes de escribirlos, `json.dump`.
**Compruebas:** el JSON tiene los 9 grupos y la cuenta 430 se llama "Clientes".
`feat: extraer el cuadro de cuentas a data/accounts.json`

> Aquí se decide la forma del dato. Es la decisión más importante de todo el
> proyecto. Deja sitio para el campo `plan` desde ahora, aunque solo haya un plan.

### Paso 8 · Extraer las fichas de la parte quinta
**Qué:** para cada cuenta, su definición, la frase de "Figurará en...", y los
movimientos `a1) a2)...` y `b1) b2)...` como listas separadas.
**Aprendes:** recorrer un texto guardando "dónde estoy" (una máquina de estados
sencilla), que es el patrón que resuelve la mitad de los problemas de parseo.
**Compruebas:** la 430 sale con 3 cargos y 9 abonos.
`feat: extraer las definiciones y los movimientos`

### Paso 9 · Detectar las referencias entre cuentas
**Qué:** encontrar dentro de cada movimiento las menciones a otras cuentas
("con abono a la cuenta 437") y guardarlas como enlaces.
**Aprendes:** grupos de captura en las expresiones regulares, conjuntos (`set`)
para no repetir.
**Compruebas:** la 430 apunta a 70, 437, 762, 431, 432, 436, 57, 650, 706, 708, 709.
`feat: detectar las referencias entre cuentas`

### Paso 10 · Verificar los datos
**Qué:** un script que informa: cuántas cuentas hay, cuántas sin definición,
cuántas referencias apuntan a cuentas que no existen.
**Aprendes:** por qué se verifica en vez de confiar, y cómo un informe pequeño te
ahorra horas.
**Compruebas:** el informe sale y las cifras tienen sentido.
`feat: añadir el verificador de los datos extraídos`

> Este paso parece prescindible y no lo es. El parser va a fallar en casos raros
> y este script es lo que te los enseña.

### Paso 11 · Revisión a mano
**Qué:** Albert revisa una muestra de fichas contra el texto original y se
corrigen los fallos que aparezcan.
**Aprendes:** que ningún parser sale bien a la primera. Y de paso, contabilidad.
`fix: corregir los casos que el parser no cogía bien`

---

## Fase 2 · El buscador y las fichas (módulo 1)

### Paso 12 · Cargar los datos desde el navegador
**Qué:** JavaScript que lee `accounts.json` y pinta una lista sin formato.
**Aprendes:** qué es el DOM, `fetch`, por qué hace falta `python -m http.server`
para esto y no basta con abrir el fichero (la primera lección de seguridad web).
**Compruebas:** ves la lista de cuentas en la página.
`feat: cargar y listar las cuentas en la web`

### Paso 13 · El buscador
**Qué:** una caja de texto que filtra por código y por nombre según escribes.
**Aprendes:** eventos, `addEventListener`, `filter`, normalizar texto para que
"amortizacion" encuentre "amortización".
**Compruebas:** escribes "clien" y salen las cuentas de clientes.
`feat: añadir el buscador de cuentas`

### Paso 14 · El árbol del cuadro de cuentas
**Qué:** la barra lateral con grupos → subgrupos → cuentas, plegable.
**Aprendes:** agrupar datos en memoria, generar HTML desde JavaScript.
**Compruebas:** despliegas el grupo 4 y ves el subgrupo 43.
`feat: añadir el árbol del cuadro de cuentas`

### Paso 15 · La ficha de cuenta
**Qué:** al pulsar una cuenta, su ficha: título, etiquetas, definición,
presentación en balance. Entre las etiquetas, **el grupo al que pertenece**
("Grupo 4 · Acreedores y deudores por operaciones comerciales"), buscado a
partir de la primera cifra del código: no se guarda en cada cuenta del JSON.
**Aprendes:** plantillas de HTML en JavaScript, separar "los datos" de "cómo se
pintan".
**Compruebas:** pulsas 430 y ves su ficha.
`feat: añadir la ficha de cuenta`

### Paso 16 · El movimiento en dos columnas
**Qué:** "Se cargará" y "Se abonará" enfrentados, con las contrapartidas como
etiquetas de color.
**Aprendes:** CSS flex, que es la herramienta con la que se resuelve el 80% de los
problemas de colocación.
**Compruebas:** la 430 muestra sus dos columnas con los colores cruzados.
`feat: mostrar el movimiento en columnas enfrentadas`

## Fase 1 bis · El BOE como fuente

Se añade a mitad de la fase 2. Al ver las fichas completas aparecieron fallos
que venían del OCR del texto refundido (títulos perdidos, párrafos partidos,
numeración reconstruida). En lugar de ir arreglándolos uno a uno, se cambia de
fuente: el texto consolidado del BOE en XML, sin OCR. El parser conserva su
lógica; cambia la parte que lee el texto.

### Paso 1b·1 · Descargar el BOE
**Qué:** `tools/download_boe.py` pide a la API de datos abiertos del BOE el
índice y el texto completo de `BOE-A-2007-19884` y los guarda tal cual en
`sources/boe/indice.xml` y `sources/boe/texto.xml`.
**Aprendes:** qué es una API, qué es una petición HTTP, `urllib`, los códigos de
respuesta (200, 404).
**Compruebas:** existen los dos ficheros y el texto pesa unos 4 MB.
`feat: descargar el texto del PGC desde el BOE`

### Paso 1b·2 · Leer un bloque del XML
**Qué:** encontrar un bloque por su `id`, quedarse con su última versión y
sacar sus párrafos sin las notas del BOE.
**Aprendes:** qué es XML, `xml.etree.ElementTree`, recorrer un árbol (el mismo
concepto que el DOM).
**Compruebas:** el bloque `grupo4-2` da, entre otros, el párrafo
"430. Clientes".
`feat: leer los bloques del XML del BOE`

### Paso 1b·3 · El cuadro de cuentas desde las tablas
**Qué:** recorrer las tablas de la cuarta parte (una fila por cuenta) y sacar
grupos, subgrupos, cuentas y subcuentas con la misma forma de dato de siempre.
**Aprendes:** recorrer filas y celdas; deducir el nivel por la columna.
**Compruebas:** 9 grupos, y la 430 se llama "Clientes" y cuelga del 43.
`feat: extraer el cuadro de cuentas del BOE`

### Paso 1b·4 · Las fichas desde la quinta parte
**Qué:** definición, presentación y movimientos de cada cuenta, con la máquina
de estados adaptada. Los movimientos guardan su etiqueta original:
`{"etiqueta": "a1", "texto": "..."}`, y `null` en la frase de entrada.
**Aprendes:** adaptar código que ya funciona a una entrada nueva.
**Compruebas:** la 430 sale con a1-a3 y b1-b9; la 642 tiene su propia ficha.
`feat: extraer las fichas del BOE con sus etiquetas originales`

> **Ojo, esto no lo arregla el BOE:** frases de presentación que no empiezan por
> "Figurará" ("Las cuentas de este subgrupo figurarán en el pasivo corriente
> del balance", unas 40, sobre todo en subgrupos) acababan en la definición.
> Es la regla del parser, no el OCR. Hay que resolverlo en este paso para que
> la ficha no diga "sin presentación" cuando sí la hay.

### Paso 1b·5 · Comparar con los datos anteriores
**Qué:** `tools/compare.py` compara, cuenta a cuenta, el JSON nuevo con el que
salía del texto refundido, y se revisa la lista de diferencias con Albert.
Después se decide si el Markdown viejo se retira.
**Aprendes:** por qué se contrasta con una segunda fuente.
**Compruebas:** cada diferencia tiene explicación (un fallo del OCR que
desaparece o un caso nuevo que arreglar).
`feat: comparar los datos del BOE con los del texto refundido`

### Paso 1b·6 · La web con los datos nuevos
**Qué:** la web pinta la etiqueta que viene en el dato; se retira la regla de
la minúscula de `pintarMovimientos`. Se retiran también el texto del OCR y
`parser.py`, con lo que dependa de ellos (decidido en el paso 1b·5).
**Aprendes:** cambiar el formato de unos datos sin romper quien los usa.
**Compruebas:** la 430 y la 640 se ven igual que antes, ahora con la
numeración del propio PGC.
`refactor: usar las etiquetas del BOE en el movimiento`

---

## Fase 2 (continuación)

### Paso 17 · Navegar entre cuentas
**Qué:** las etiquetas de contrapartida llevan a la ficha de esa cuenta, y la URL
cambia (`#430`), así que el botón "atrás" funciona y se puede compartir un enlace.
**Aprendes:** el `hash` de la URL y qué es "enrutar" en una página.
**Compruebas:** de la 430 llegas a la 436, vuelves con "atrás", y el enlace
directo a `#436` funciona.
`feat: navegar entre cuentas por la URL`

> **Decidido en este paso:** en el árbol, el título de un grupo o subgrupo es
> el enlace a su ficha y el triángulo es el que pliega. Un enlace a una cuenta
> que no existe enseña un aviso. Las remisiones del texto van en un paso propio,
> el 17 bis.

### Paso 17 bis · Las remisiones del texto, como enlaces
**Qué:** idea de Albert. En la definición y la presentación, las remisiones a
otras cuentas ("análogo al señalado para la cuenta 100", en la 101; "cuentas
663 y 763"; "subgrupo 58") pasan a ser enlaces, como las contrapartidas. El
parser las detecta y las guarda en el JSON, como hizo con las contrapartidas
en el paso 9.
**Aprendes:** una regla de datos que mira el contexto, no solo el número: de
los 448 números que coinciden con una cuenta, unos 15 no son remisiones
("artículo 170", "artículos 239 a 243", "Ley 46/1998").
**Compruebas:** en la 101, el 100 es un enlace; en la que cite el "artículo
239", el 239 no lo es.
`feat: convertir en enlaces las remisiones del texto`

### Paso 18 · El índice y la ficha rápida
**Qué:** el índice de contenidos a la izquierda de la ficha y el panel de ficha
rápida + contrapartidas a la derecha.
**Compruebas:** se parece a la maqueta.
`feat: añadir el índice y el panel lateral de la ficha`

> **Decidido en este paso:** a la izquierda va el árbol del cuadro de cuentas,
> no el índice de la ficha (la ficha tiene tres apartados y cabe en una
> pantalla). La ficha rápida lleva solo datos del JSON: plan, nivel, grupo,
> subgrupo y las contrapartidas con su nombre. El buscador sube a la cabecera,
> con los resultados en una lista desplegable. De lo que dibujan las maquetas
> entran las migas de pan; "Ver también", "Vecinas" y el menú de módulos se
> quedan fuera. La etiqueta del grupo de debajo del título (paso 15) se quita.
> El commit cambia de nombre: `feat: repartir la página en árbol, ficha y ficha rápida`.

### Paso 19 · Que funcione en el móvil
**Qué:** las columnas se apilan, la barra lateral se esconde.
**Aprendes:** media queries y por qué se diseña primero para pantalla estrecha.
**Compruebas:** lo abres en tu móvil desde la URL publicada.
`feat: adaptar la interfaz a pantallas estrechas`

> **Decidido en este paso:** dos puntos de corte, 64em (tres columnas) y 40em
> (movimiento enfrentado). En el móvil no se ven el árbol ni la ficha rápida.
> La cabecera se queda solo con el buscador, centrado: el título y el
> subtítulo se quitan.

### Paso 19 bis · El árbol en el móvil
**Qué:** un botón "☰ Cuadro de cuentas" en la cabecera, solo en pantalla
estrecha, que abre el árbol por encima de la ficha. Se cierra al elegir una
cuenta. Idea de Albert (él lo pensó como un gesto con el dedo; se cambió por
un botón, ver CHANGELOG).
**Aprendes:** cambiar el aspecto desde JavaScript poniendo y quitando una
clase, y dejar el "cómo se ve" en el CSS.
**Compruebas:** en el móvil, pulsas el botón, eliges la 430 y el árbol se cierra.
`feat: abrir el árbol desde un botón en el móvil`

### Paso 19 ter · La ficha rápida como en la maqueta D
**Qué:** idea de Albert. La ficha rápida en dos cajas con su título
("Ficha rápida" y "Contrapartidas"); las contrapartidas, solo con el
número en cajitas de colores cruzados, y el nombre al pasar el ratón.
**Aprendes:** el atributo `title`, `flex-wrap`, `overflow: hidden` para
recortar por el borde redondeado.
**Compruebas:** en la 430, los números van en dos apartados y al dejar el
ratón sobre el 431 sale "Clientes, efectos comerciales a cobrar".
`feat: mostrar la ficha rápida en cajas, como en la maqueta D`

### Paso 19 quater · Enter abre el primer resultado
**Qué:** idea de Albert. En el buscador, Enter abre la ficha del primer
resultado de la lista; si no hay ninguno, no hace nada.
**Aprendes:** el evento `keydown` y `event.key`.
**Compruebas:** escribes "clien", pulsas Enter y se abre la ficha del
primer resultado.
`feat: abrir el primer resultado del buscador con Enter`

### Paso 20 · Pulido
**Qué:** tipografías definitivas, espaciados, estados de foco visibles para quien
navegue con teclado. **Pendiente del paso 19:** la página se quedó sin `<h1>`;
hay que decidir cómo se presenta la web y devolverle un título principal.
`feat: pulir el aspecto del buscador`

> **Aquí ya hay algo que enseñar a los compañeros del máster.** Buen momento para
> parar, usarlo unas semanas y apuntar qué echas en falta antes de seguir.

---

## Fase 3 · El simulador (módulo 3)

Esbozado. Se detalla al llegar.

- **21.** Diseñar la forma de un ejercicio y de un asiento. Sin interfaz todavía,
  solo los datos y las funciones que los manipulan.
- **22.** Formulario para registrar un asiento, con validación de que cuadra.
- **23.** Guardar el ejercicio en `localStorage`.
- **24.** El libro diario: la lista de asientos, editar y borrar.
- **25.** El libro mayor, **derivado** de los asientos. No se guarda: se calcula.
- **26.** El balance de sumas y saldos, derivado del mayor.
- **27.** Subcuentas propias (4300001 Molins SL) que heredan la naturaleza de su
  cuenta oficial.
- **28.** Exportar e importar el ejercicio como fichero. Con esto ya se pueden
  intercambiar ejercicios con los compañeros.
- **29.** Conectar con el módulo 1: autocompletar la cuenta al escribir el asiento
  y ver su definición sin salir del ejercicio.

## Fase 4 · Cierre y cuentas anuales

- **30.** La tabla de correspondencias cuenta → línea del balance. **Contempla
  desde el principio el signo** (las 28x y 29x restan) y las cuentas que cambian
  de lado según el saldo. Si esto se hace mal, hay que rehacerlo entero.
- **31.** El Balance de Situación, modelo normal.
- **32.** La Cuenta de Pérdidas y Ganancias, modelo normal.
- **33.** Asientos de regularización y de cierre.
- **34.** Exportar el mayor y el balance a Excel o CSV.

## Fase 5 · La wiki del articulado (módulo 2)

- **35.** Trocear el Marco Conceptual y las Normas de Registro y Valoración en
  fichas, con el mismo motor de la fase 1.
- **36.** Enlazar en las dos direcciones: de la NRV a sus cuentas y de la cuenta a
  su NRV.
- **37.** Búsqueda unificada sobre cuentas y articulado.

## Fase 6 · PGC de PYMES

- **38.** Conseguir el texto consolidado del RD 1515/2007 y meterlo en `sources/`.
- **39.** Extenderlo todo a dos planes. **PYMES no es un subconjunto del normal**:
  tiene su propio cuadro de cuentas y sus propias normas simplificadas.
- **40.** Selector de plan en la interfaz.

---

## Cosas que NO están en esta hoja de ruta

Y que no deben colarse sin hablarlo antes:

- Corrección automática de ejercicios.
- Cuentas de usuario, servidor, base de datos.
- Amortizaciones, periodificaciones o IVA automáticos.
- Cualquier framework de JavaScript.
