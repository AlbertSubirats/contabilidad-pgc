// Lee el cuadro de cuentas, lo muestra como árbol, busca cuentas con el
// buscador de la cabecera y enseña la ficha de la cuenta que pide la URL (#430).

// Todas las cuentas del JSON. Está fuera de las funciones para que todas puedan
// usarla. Empieza vacía y la rellena cargarCuentas cuando llega el fichero.
let todasLasCuentas = [];

// Las mismas cuentas, pero indexadas por su código para encontrarlas al momento:
// { "430": cuenta 430, "4": grupo 4, ...}. La rellena cargarCuentas.
let cuentasPorCodigo = {};

// Cómo se escribe cada nivel en las etiquetas de la ficha.
const nombreDelNivel = {
    grupo:     "Grupo",
    subgrupo:  "Subgrupo",
    cuenta:    "Cuenta",
    subcuenta: "Subcuenta",
};

// Cómo se escribe cada plan en la ficha rápida. De momento solo hay uno.
const nombreDelPlan = {
    "pgc-general": "PGC normal",
};

// La caja de texto del buscador. Se busca una sola vez y se guarda aquí.
const cajaBuscador = document.getElementById("buscador");

// Fabrica un enlace a la ficha de una cuenta: <a href="#430">. El enlace solo
// cambia la URL; quien abre la ficha es mostrarCuentaDeLaUrl, que se entera
// por el evento hashchange. Lo usan la lista, el árbol y las contrapartidas.
function crearEnlaceACuenta(codigo, texto) {
    const enlace = document.createElement("a");
    enlace.href = "#" + codigo;
    enlace.textContent = texto;
    return enlace;
}

// Fabrica el <li> de una cuenta del árbol, con su enlace dentro.
function crearElementoDeCuenta(cuenta) {
    const elemento = document.createElement("li");
    const enlace = crearEnlaceACuenta(cuenta.codigo, cuenta.codigo + " · " + cuenta.nombre);
    elemento.appendChild(enlace);
    return elemento;
}

// Fabrica el <li> de un resultado del buscador. Como en la maqueta B, el
// código y el nombre van cada uno en su <span>, para que el CSS los ponga en
// dos columnas: así todos los nombres empiezan a la misma altura.
function crearResultado(cuenta) {
    const elemento = document.createElement("li");
    const enlace = crearEnlaceACuenta(cuenta.codigo, "");

    const codigo = document.createElement("span");
    codigo.className = "codigo-resultado";
    codigo.textContent = cuenta.codigo;
    enlace.appendChild(codigo);

    const nombre = document.createElement("span");
    nombre.textContent = cuenta.nombre;
    enlace.appendChild(nombre);

    elemento.appendChild(enlace);
    return elemento;
}

// Vacía la lista de resultados y la vuelve a llenar con las cuentas que reciba.
function pintarLista(cuentasAMostrar) {
    const lista = document.getElementById("lista-cuentas");
    lista.replaceChildren();

    for (const cuenta of cuentasAMostrar) {
        const elemento = crearResultado(cuenta);
        lista.appendChild(elemento);
    }
}

// Escribe en la caja cuántas cuentas se han encontrado: "34 resultados", o
// "1 resultado" en singular.
function pintarContador(cantidad) {
    const contador = document.getElementById("contador-resultados");
    if (cantidad === 1) {
        contador.textContent = "1 resultado";
    } else {
        contador.textContent = cantidad + " resultados";
    }
}

// Pasa un texto a minúsculas y le quita las tildes. Así "Amortización" y
// "Amortizacion" quedan iguales y se pueden comparar.
function normalizar(texto) {
    const enMinusculas = texto.toLowerCase();
    // NFD separa cada letra con tilde en dos piezas: la letra y la tilde suelta.
    const separado = enMinusculas.normalize("NFD");
    // Borra todas las tildes sueltas y deja solo las letras.
    const sinTildes = separado.replace(/[\u0300-\u036f]/g, "");
    return sinTildes;
}

// La llama el navegador cada vez que cambia el texto de la caja de búsqueda.
// Enseña los resultados en el desplegable, o lo esconde si la caja se ha
// quedado vacía.
function filtrarCuentas() {
    const desplegable = document.getElementById("desplegable-buscador");
    const lista = document.getElementById("lista-cuentas");
    const textoBuscado = normalizar(cajaBuscador.value);

    // Sin texto no hay nada que buscar: el desplegable se esconde, el
    // contador se vacía y ya está.
    if (textoBuscado === "") {
        desplegable.hidden = true;
        document.getElementById("contador-resultados").textContent = "";
        return;
    }

    // filter recorre todas las cuentas y se queda con aquellas para las que
    // la función de dentro devuelve true.
    const encontradas = todasLasCuentas.filter(function (cuenta) {
        // El código, por el principio: "43" encuentra 430, pero no 143.
        const coincideCodigo = cuenta.codigo.startsWith(textoBuscado);
        // El nombre, en cualquier posición.
        const coincideNombre = normalizar(cuenta.nombre).includes(textoBuscado);
        return coincideCodigo || coincideNombre;
    });

    pintarLista(encontradas);
    pintarContador(encontradas.length);

    // Si nada coincide, se dice, en vez de enseñar una lista vacía.
    if (encontradas.length === 0) {
        const aviso = document.createElement("li");
        aviso.className = "aviso-sin-texto";
        aviso.textContent = "Ninguna cuenta coincide con «" + cajaBuscador.value + "».";
        lista.appendChild(aviso);
    }

    desplegable.hidden = false;
}

// Cierra el buscador: vacía la caja y el contador y esconde el desplegable.
// Se llama al pulsar un resultado, porque entonces ya se ha encontrado lo que
// se buscaba.
function cerrarBuscador() {
    cajaBuscador.value = "";
    document.getElementById("contador-resultados").textContent = "";
    document.getElementById("desplegable-buscador").hidden = true;
}

// La llama el navegador cada vez que se pulsa una tecla dentro de la caja.
// Si es Enter, abre la ficha del primer resultado de la lista.
// "evento" lo pone el navegador: es un objeto con los detalles de lo que ha
// pasado. evento.key dice qué tecla ha sido ("Enter", "a", "Escape"...).
function abrirPrimerResultado(evento) {
    if (evento.key !== "Enter") {
        return;
    }

    // Con el desplegable escondido no hay resultados que abrir. Hay que
    // mirarlo: al cerrar el buscador, se esconde pero sus enlaces se quedan.
    if (document.getElementById("desplegable-buscador").hidden) {
        return;
    }

    const lista = document.getElementById("lista-cuentas");

    // querySelector busca dentro de la lista el primer elemento que cumpla
    // el selector, escrito igual que en el CSS: "a" es el primer enlace. Si
    // no hay ninguno (solo el aviso "Ninguna cuenta coincide"), da null.
    const primerEnlace = lista.querySelector("a");
    if (primerEnlace === null) {
        return;
    }

    // El mismo camino que al pulsar el resultado con el ratón: se cierra el
    // buscador y se cambia la URL. primerEnlace.hash es la parte "#430" de
    // su dirección, y el enrutador se entera por el evento hashchange.
    cerrarBuscador();
    location.hash = primerEnlace.hash;
}

// Construye un índice para encontrar rápido los hijos de cualquier código:
// { "4": [subgrupos del 4], "43": [cuentas del 43], ...}
function agruparPorPadre(cuentas) {
    const hijosPorPadre = {};

    for (const cuenta of cuentas) {
        const padre = cuenta.padre;

        // Los grupos no tienen padre: no son hijos de nadie, así que se saltan.
        if (padre === null) {
            continue;
        }

        // La primera vez que aparece un padre, todavía no tiene lista: se la creamos vacía.
        if (hijosPorPadre[padre] === undefined) {
            hijosPorPadre[padre] = [];
        }

        hijosPorPadre[padre].push(cuenta);
    }
    return hijosPorPadre;
}

// Construye un índice para encontrar cualquier cuenta por su código.
function indexarPorCodigo(cuentas) {
    const indice = {};

    for (const cuenta of cuentas) {
        indice[cuenta.codigo] = cuenta;
    }

    return indice;
}

// Construye el árbol del cuadro de cuentas dentro del <nav>: grupos y
// subgrupos como cajas plegables (<details>), y las cuentas como lista.
function pintarArbol() {
    const arbol = document.getElementById("arbol-cuentas");
    arbol.replaceChildren();

    const grupos = todasLasCuentas.filter(function (cuenta) {
        return cuenta.nivel === "grupo";
    });

    const hijosPorPadre = agruparPorPadre(todasLasCuentas);

    for (const grupo of grupos) {
        const cajaGrupo = document.createElement("details");
        // El título es un enlace a la ficha del grupo; el triángulo de la
        // izquierda es el que pliega y despliega.
        const tituloGrupo = document.createElement("summary");
        tituloGrupo.appendChild(crearEnlaceACuenta(grupo.codigo, grupo.codigo + " · " + grupo.nombre));

        cajaGrupo.appendChild(tituloGrupo);

        // Los subgrupos de este grupo, cada uno en su propia caja plegable
        // colgada dentro de la caja del grupo.
        const subgrupos = hijosPorPadre[grupo.codigo];
        for (const subgrupo of subgrupos) {
            const cajaSubgrupo = document.createElement("details");
            const tituloSubgrupo = document.createElement("summary");
            tituloSubgrupo.appendChild(crearEnlaceACuenta(subgrupo.codigo, subgrupo.codigo + " · " + subgrupo.nombre));
            cajaSubgrupo.appendChild(tituloSubgrupo);

            // Las cuentas de este subgrupo, como una lista normal dentro de su caja.
            const listaCuentas = document.createElement("ul");
            const cuentas = hijosPorPadre[subgrupo.codigo];

            for (const cuenta of cuentas) {
                const elemento = crearElementoDeCuenta(cuenta);
                listaCuentas.appendChild(elemento);
            }

            cajaSubgrupo.appendChild(listaCuentas);
            cajaGrupo.appendChild(cajaSubgrupo);
        }

        arbol.appendChild(cajaGrupo);
    }
}

// Llena un hueco de la ficha con un <p> por cada párrafo de la lista, con las
// remisiones a otras cuentas convertidas en enlaces ("...para la cuenta [100]").
// Si la lista está vacía, pone el aviso: si algo no está en el PGC, se dice.
function rellenarConParrafos(contenedor, parrafos, remisiones, avisoSiNoHay) {
    contenedor.replaceChildren();

    if (parrafos.length === 0) {
        const aviso = document.createElement("p");
        aviso.className = "aviso-sin-texto";
        aviso.textContent = avisoSiNoHay;
        contenedor.appendChild(aviso);
        return;
    }

    for (const texto of parrafos) {
        const parrafo = document.createElement("p");
        parrafo.appendChild(crearTextoConEnlaces(texto, remisiones, "remision"));
        contenedor.appendChild(parrafo);
    }
}

// Crea un texto con algunos de sus números convertidos en enlaces a su
// cuenta: "...con abono a la cuenta [437]." Solo son enlace los números que
// están en la lista de códigos (las contrapartidas de una columna, o las
// remisiones de un apartado); los demás (artículos, porcentajes...) se quedan
// como texto. La clase dice cómo se pinta el enlace: "contrapartida" o "remision".
function crearTextoConEnlaces(texto, codigos, clase) {
    const frase = document.createElement("span");

    // Partir por los números. El paréntesis hace que los números se queden en
    // la lista: "...a la cuenta 437." → ["...a la cuenta ", "437", "."]
    const trozos = texto.split(/(\d+)/);

    for (const trozo of trozos) {
        if (codigos.includes(trozo)) {
            const enlace = crearEnlaceACuenta(trozo, trozo);
            enlace.className = clase;
            frase.appendChild(enlace);
        } else {
            const textoNormal = document.createTextNode(trozo);
            frase.appendChild(textoNormal);
        }
    }

    return frase;
}

// Llena una columna del movimiento: un <li> por movimiento, con su etiqueta
// delante ("a1", "b3"...) tal como la escribe el PGC. En las cuentas de pasivo
// los cargos son la "b", así que la etiqueta no se puede deducir de la columna.
// Si no hay movimientos, pone el aviso.
function pintarMovimientos(lista, movimientos, contrapartidas, avisoSiNoHay) {
    lista.replaceChildren();

    if (movimientos.length === 0) {
        const aviso = document.createElement("li");
        aviso.className = "aviso-sin-texto";
        aviso.textContent = avisoSiNoHay;
        lista.appendChild(aviso);
        return;
    }

    for (const movimiento of movimientos) {
        const elemento = document.createElement("li");

        // Un movimiento sin etiqueta es la frase de entrada de la columna, lo
        // que va detrás de "Se cargará" ("por el importe íntegro..."). Va sin
        // número, ocupando todo el ancho.
        if (movimiento.etiqueta === null) {
            elemento.className = "entrada-movimiento";
        } else {
            const etiquetaDelMovimiento = document.createElement("span");
            etiquetaDelMovimiento.className = "numero-movimiento";
            etiquetaDelMovimiento.textContent = movimiento.etiqueta;
            elemento.appendChild(etiquetaDelMovimiento);
        }

        const frase = crearTextoConEnlaces(movimiento.texto, contrapartidas, "contrapartida");
        elemento.appendChild(frase);

        lista.appendChild(elemento);
    }
}

// Pinta las migas de pan encima del título: "Grupo 4 › Subgrupo 43 › 430".
// Para saber de quién cuelga una cuenta se sube por el árbol: el padre, el
// padre del padre... hasta el grupo, que no tiene padre.
function pintarMigas(cuenta) {
    const migas = document.getElementById("ficha-migas");
    migas.replaceChildren();

    // Primero se apuntan los antepasados, de abajo arriba. No se sabe cuántos
    // hay (un subgrupo tiene uno; una subcuenta, tres), por eso es un while:
    // se repite mientras la cuenta de la que vamos tenga padre.
    // unshift mete cada uno al PRINCIPIO de la lista (push lo mete al final):
    // así, aunque se suba de la 430 al 43 y luego al 4, la lista queda
    // en el orden en que se lee: [grupo 4, subgrupo 43].
    const antepasados = [];
    let actual = cuenta;
    while (actual.padre !== null) {
        actual = cuentasPorCodigo[actual.padre];
        antepasados.unshift(actual);
    }

    // Cada antepasado, como enlace a su ficha y seguido de la flecha.
    for (const antepasado of antepasados) {
        const texto = nombreDelNivel[antepasado.nivel] + " " + antepasado.codigo;
        migas.appendChild(crearEnlaceACuenta(antepasado.codigo, texto));

        const separador = document.createElement("span");
        separador.className = "separador-migas";
        separador.textContent = " › ";
        migas.appendChild(separador);
    }

    // Y al final la cuenta en la que estamos, sin enlace: ya estás en ella.
    const actualSinEnlace = document.createElement("span");
    actualSinEnlace.textContent = cuenta.codigo;
    migas.appendChild(actualSinEnlace);
}

// Añade un par "dato: valor" a la lista de definiciones de la ficha rápida:
// <dt>Grupo</dt><dd>4 · Acreedores...</dd>. El valor llega ya fabricado
// (un texto o un enlace), para que sirva para los dos casos.
function anadirDato(lista, termino, valor) {
    const elementoTermino = document.createElement("dt");
    elementoTermino.textContent = termino;
    lista.appendChild(elementoTermino);

    const elementoValor = document.createElement("dd");
    elementoValor.appendChild(valor);
    lista.appendChild(elementoValor);
}

// Llena una lista de la ficha rápida con las contrapartidas de una columna del
// movimiento: cada una, solo con su código en cajita (el mismo enlace que en
// las frases). El nombre va en el atributo title, que el navegador enseña en
// un recuadro al dejar el ratón encima. Si no hay, pone el aviso.
function pintarContrapartidas(lista, codigos, avisoSiNoHay) {
    lista.replaceChildren();

    if (codigos.length === 0) {
        const aviso = document.createElement("li");
        aviso.className = "aviso-sin-texto";
        aviso.textContent = avisoSiNoHay;
        lista.appendChild(aviso);
        return;
    }

    for (const codigo of codigos) {
        const elemento = document.createElement("li");

        const enlace = crearEnlaceACuenta(codigo, codigo);
        enlace.className = "contrapartida";

        const contrapartida = cuentasPorCodigo[codigo];
        enlace.title = contrapartida.nombre;

        elemento.appendChild(enlace);
        lista.appendChild(elemento);
    }
}

// Rellena la ficha rápida del margen derecho: solo datos que están en el
// JSON o que salen del código (el grupo es su primera cifra; el subgrupo, sus
// dos primeras). Nada que haya que deducir del texto del PGC.
function pintarFichaRapida(cuenta) {
    const datos = document.getElementById("ficha-rapida-datos");
    datos.replaceChildren();

    // createTextNode fabrica un trozo de texto suelto, para los valores que
    // no son enlace.
    anadirDato(datos, "Plan", document.createTextNode(nombreDelPlan[cuenta.plan]));
    anadirDato(datos, "Nivel", document.createTextNode(nombreDelNivel[cuenta.nivel]));

    // El grupo y el subgrupo, como enlaces a su ficha. Cada uno solo si la
    // cuenta está por debajo: un grupo no lleva grupo, porque sería él mismo.
    if (cuenta.nivel !== "grupo") {
        const grupo = cuentasPorCodigo[cuenta.codigo.slice(0, 1)];
        anadirDato(datos, "Grupo", crearEnlaceACuenta(grupo.codigo, grupo.codigo + " · " + grupo.nombre));
    }
    if (cuenta.nivel === "cuenta" || cuenta.nivel === "subcuenta") {
        const subgrupo = cuentasPorCodigo[cuenta.codigo.slice(0, 2)];
        anadirDato(datos, "Subgrupo", crearEnlaceACuenta(subgrupo.codigo, subgrupo.codigo + " · " + subgrupo.nombre));
    }

    const cargos = document.getElementById("ficha-rapida-cargos");
    const abonos = document.getElementById("ficha-rapida-abonos");

    pintarContrapartidas(cargos, cuenta.contrapartidas_cargos, "Ninguna.");
    pintarContrapartidas(abonos, cuenta.contrapartidas_abonos, "Ninguna.");
}

// Rellena los huecos de la ficha con los datos de una cuenta y la muestra.
function mostrarFicha(cuenta) {
    const ficha = document.getElementById("ficha-cuenta");
    const titulo = document.getElementById("ficha-titulo");
    const etiquetas = document.getElementById("ficha-etiquetas");

    titulo.textContent = cuenta.codigo + " · " + cuenta.nombre;

    // Las etiquetas se vacían primero: si antes se mostró otra cuenta,
    // sus etiquetas no deben quedarse.
    etiquetas.replaceChildren();

    const etiquetaNivel = document.createElement("span");
    etiquetaNivel.className = "etiqueta";
    etiquetaNivel.textContent = nombreDelNivel[cuenta.nivel];
    etiquetas.appendChild(etiquetaNivel);

    const definicion = document.getElementById("ficha-definicion");
    const presentacion = document.getElementById("ficha-presentacion");

    rellenarConParrafos(definicion, cuenta.definicion, cuenta.remisiones_definicion, "Sin definición en el texto del PGC.");
    rellenarConParrafos(presentacion, cuenta.presentacion, cuenta.remisiones_presentacion, "Sin indicación de presentación en el balance en el texto del PGC.");

    const cargos = document.getElementById("ficha-cargos");
    const abonos = document.getElementById("ficha-abonos");

    pintarMovimientos(cargos, cuenta.cargos, cuenta.contrapartidas_cargos, "Sin cargos en el texto del PGC.");
    pintarMovimientos(abonos, cuenta.abonos, cuenta.contrapartidas_abonos, "Sin abonos en el texto del PGC.");

    pintarMigas(cuenta);
    pintarFichaRapida(cuenta);

    ficha.hidden = false;
    document.getElementById("ficha-rapida").hidden = false;

    // Si se pulsa una contrapartida al final de un movimiento largo, la página
    // está desplazada hacia abajo: sube para que la ficha nueva se lea desde
    // el principio.
    ficha.scrollIntoView();
}

// El enrutador: mira qué código hay en la URL (#430) y decide qué se enseña.
// La llama el navegador cada vez que cambia la URL (un enlace, el botón
// "atrás", alguien que lo escribe a mano), y cargarCuentas al empezar, por si
// se ha abierto un enlace directo a una cuenta.
function mostrarCuentaDeLaUrl() {
    const ficha = document.getElementById("ficha-cuenta");
    const fichaRapida = document.getElementById("ficha-rapida");
    const aviso = document.getElementById("aviso-cuenta");

    // location.hash es "#430": slice(1) quita la "#". El navegador codifica
    // en la URL las letras que no son simples ("é" → "%C3%A9");
    // decodeURIComponent las devuelve a como se escribieron. Pero si alguien
    // escribe un "%" suelto (#50%), decodeURIComponent lanza un error; con
    // try/catch, en vez de cortarlo todo, se usa el texto tal cual.
    let codigo;
    try {
        codigo = decodeURIComponent(location.hash.slice(1));
    } catch (error) {
        codigo = location.hash.slice(1);
    }

    aviso.hidden = true;

    // Sin código, la página queda como al entrar: sin ficha.
    if (codigo === "") {
        ficha.hidden = true;
        fichaRapida.hidden = true;
        return;
    }

    const cuenta = cuentasPorCodigo[codigo];
    if (cuenta === undefined) {
        ficha.hidden = true;
        fichaRapida.hidden = true;
        aviso.textContent = "No hay ninguna cuenta con el código «" + codigo + "» en el PGC.";
        aviso.hidden = false;
        aviso.scrollIntoView();
        return;
    }

    mostrarFicha(cuenta);
}

async function cargarCuentas() {
    const respuesta = await fetch("../data/accounts.json");
    todasLasCuentas = await respuesta.json();
    cuentasPorCodigo = indexarPorCodigo(todasLasCuentas);
    pintarArbol();

    // Ahora que ya hay cuentas, se mira si la URL pide alguna.
    mostrarCuentaDeLaUrl();
}

cargarCuentas();

// Encargo al navegador: cuando cambie el código de la URL, enseña su cuenta.
window.addEventListener("hashchange", mostrarCuentaDeLaUrl);

// Encargo al navegador: cuando cambie el texto de la caja, llama a filtrarCuentas.
cajaBuscador.addEventListener("input", filtrarCuentas);

// Encargo al navegador: cuando se pulse una tecla en la caja, llama a
// abrirPrimerResultado. "keydown" es "tecla hacia abajo": salta en cuanto
// se pulsa, sea la que sea; la función mira si ha sido Enter.
cajaBuscador.addEventListener("keydown", abrirPrimerResultado);

// Encargo al navegador: cuando se pulse dentro de la lista de resultados,
// cierra el buscador. Se escucha el clic y no el cambio de URL porque, si
// pulsas la cuenta que ya está abierta, la URL no cambia y la lista se
// quedaría abierta. El enlace sigue funcionando: primero se cierra la lista
// y después el navegador cambia la URL como siempre.
document.getElementById("lista-cuentas").addEventListener("click", cerrarBuscador);