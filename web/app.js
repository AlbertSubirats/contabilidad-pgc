// Lee el cuadro de cuentas, lo muestra como árbol y como lista, y filtra la lista con el buscador.

// Todas las cuentas del JSON. Está fuera de las funciones para que todas puedan
// usarla. Empieza vacía y la rellena cargarCuentas cuando llega el fichero.
let todasLasCuentas = [];

// La caja de texto del buscador. Se busca una sola vez y se guarda aquí.
const cajaBuscador = document.getElementById("buscador");

// Vacía la lista de la página y la vuelve a llenar con las cuentas que reciba.
function pintarLista(cuentasAMostrar) {
    const lista = document.getElementById("lista-cuentas");
    lista.replaceChildren();

    for (const cuenta of cuentasAMostrar) {
        const elemento = document.createElement("li");
        elemento.textContent = cuenta.codigo + " · " + cuenta.nombre;
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
                const elemento = document.createElement("li");
                elemento.textContent = cuenta.codigo + " · " + cuenta.nombre;
                listaCuentas.appendChild(elemento);
            }

            cajaSubgrupo.appendChild(listaCuentas);
            cajaGrupo.appendChild(cajaSubgrupo);
        }

        arbol.appendChild(cajaGrupo);
    }
}

async function cargarCuentas() {
    const respuesta = await fetch("../data/accounts.json");
    todasLasCuentas = await respuesta.json();
    pintarLista(todasLasCuentas);
    pintarArbol();
}

cargarCuentas();

// Encargo al navegador: cuando cambie el texto de la caja, llama a filtrarCuentas.
cajaBuscador.addEventListener("input", filtrarCuentas);