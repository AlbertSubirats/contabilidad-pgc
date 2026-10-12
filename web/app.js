// Lee el cuadro de cuentas, lo escribe en la página como una lista y lo filtra con el buscador.

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

async function cargarCuentas() {
    const respuesta = await fetch("../data/accounts.json");
    todasLasCuentas = await respuesta.json();
    pintarLista(todasLasCuentas);
}

cargarCuentas();

// Encargo al navegador: cuando cambie el texto de la caja, llama a filtrarCuentas.
cajaBuscador.addEventListener("input", filtrarCuentas);