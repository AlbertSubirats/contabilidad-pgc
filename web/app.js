// Lee el cuadro de cuentas, lo muestra como árbol y como lista, y filtra la lista con el buscador.

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

// La caja de texto del buscador. Se busca una sola vez y se guarda aquí.
const cajaBuscador = document.getElementById("buscador");

// Fabrica el <li> de una cuenta: con su texto y con el click que abre su ficha.
// La usan la lista y el árbol, así que cómo se pinta una cuenta se decide aquí.
function crearElementoDeCuenta(cuenta) {
    const elemento = document.createElement("li");
    elemento.textContent = cuenta.codigo + " · " + cuenta.nombre;

    // La función anónima hace falta para poder decirle a mostrarFicha QUÉ
    // cuenta tiene que mostrar.
    elemento.addEventListener("click", function () {
        mostrarFicha(cuenta);
    });

    return elemento;
}

// Vacía la lista de la página y la vuelve a llenar con las cuentas que reciba.
function pintarLista(cuentasAMostrar) {
    const lista = document.getElementById("lista-cuentas");
    lista.replaceChildren();

    for (const cuenta of cuentasAMostrar) {
        const elemento = crearElementoDeCuenta(cuenta);
        lista.appendChild(elemento);
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
function filtrarCuentas() {
    const textoBuscado = normalizar(cajaBuscador.value);

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
        const tituloGrupo = document.createElement("summary");
        tituloGrupo.textContent = grupo.codigo + " · " + grupo.nombre;

        cajaGrupo.appendChild(tituloGrupo);

        // Los subgrupos de este grupo, cada uno en su propia caja plegable
        // colgada dentro de la caja del grupo.
        const subgrupos = hijosPorPadre[grupo.codigo];
        for (const subgrupo of subgrupos) {
            const cajaSubgrupo = document.createElement("details");
            const tituloSubgrupo = document.createElement("summary");
            tituloSubgrupo.textContent = subgrupo.codigo + " · " + subgrupo.nombre;
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

// Llena un hueco de la ficha con un <p> por cada párrafo de la lista.
// Si la lista está vacía, pone el aviso: si algo no está en el PGC, se dice.
function rellenarConParrafos(contenedor, parrafos, avisoSiNoHay) {
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
        parrafo.textContent = texto;
        contenedor.appendChild(parrafo);
    }
}

// Crea la frase de un movimiento con sus contrapartidas convertidas en
// etiquetas: "...con abono a la cuenta [437]." Solo son etiqueta los números
// que están en la lista de contrapartidas de la columna; los demás números
// (artículos, porcentajes...) se quedan como texto.
function crearFraseConContrapartidas(texto, contrapartidas) {
    const frase = document.createElement("span");

    // Partir por los números. El paréntesis hace que los números se queden en
    // la lista: "...a la cuenta 437." → ["...a la cuenta ", "437", "."]
    const trozos = texto.split(/(\d+)/);

    for (const trozo of trozos) {
        if (contrapartidas.includes(trozo)) {
            const etiqueta = document.createElement("span");
            etiqueta.className = "contrapartida";
            etiqueta.textContent = trozo;
            frase.appendChild(etiqueta);
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

        const frase = crearFraseConContrapartidas(movimiento.texto, contrapartidas);
        elemento.appendChild(frase);

        lista.appendChild(elemento);
    }
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

    // El grupo es la primera cifra del código. Un grupo no lleva esta
    // etiqueta, porque sería él mismo.
    if (cuenta.nivel !== "grupo") {
        const grupo = cuentasPorCodigo[cuenta.codigo[0]];
        const etiquetaGrupo = document.createElement("span");
        etiquetaGrupo.className = "etiqueta";
        etiquetaGrupo.textContent = "Grupo " + grupo.codigo + " · " + grupo.nombre;
        etiquetas.appendChild(etiquetaGrupo);
    }
    
    const definicion = document.getElementById("ficha-definicion");
    const presentacion = document.getElementById("ficha-presentacion");

    rellenarConParrafos(definicion, cuenta.definicion, "Sin definición en el texto del PGC.");
    rellenarConParrafos(presentacion, cuenta.presentacion, "Sin indicación de presentación en el balance en el texto del PGC.");

    const cargos = document.getElementById("ficha-cargos");
    const abonos = document.getElementById("ficha-abonos");

    pintarMovimientos(cargos, cuenta.cargos, cuenta.contrapartidas_cargos, "Sin cargos en el texto del PGC.");
    pintarMovimientos(abonos, cuenta.abonos, cuenta.contrapartidas_abonos, "Sin abonos en el texto del PGC.");

    ficha.hidden = false;

    // La ficha está arriba del todo: si se pulsa una cuenta de más abajo,
    // la página sube para que se vea. Cuando la ficha vaya al lado (paso 18), sobrará.
    ficha.scrollIntoView();
}

async function cargarCuentas() {
    const respuesta = await fetch("../data/accounts.json");
    todasLasCuentas = await respuesta.json();
    cuentasPorCodigo = indexarPorCodigo(todasLasCuentas);
    pintarLista(todasLasCuentas);
    pintarArbol();
}

cargarCuentas();

// Encargo al navegador: cuando cambie el texto de la caja, llama a filtrarCuentas.
cajaBuscador.addEventListener("input", filtrarCuentas);