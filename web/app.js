// Lee el cuadro de cuentas y lo escribe en la página como una lista sin formato.

// "async" marca la función como asíncrona: dentro de ella podemos usar "await"
// para esperar a cosas que tardan, como pedir un fichero por la red.
async function cargarCuentas() {
    // fetch pide el fichero al servidor. La ruta es relativa a index.html:
    // ".." sube de web/ a la raíz del proyecto, y de ahí entra en data/.
    const respuesta = await fetch("../data/accounts.json");

    // La respuesta llega como texto; .json() lo convierte en datos de JavaScript.
    // Como el JSON es una lista, "cuentas" es una lista de objetos.
    const cuentas = await respuesta.json();

    // Buscamos en la página el <ul> vacío por su id.
    const lista = document.getElementById("lista-cuentas");

    for (const cuenta of cuentas) {
        const elemento = document.createElement("li");
        elemento.textContent = cuenta.codigo + " · " + cuenta.nombre;
        lista.appendChild(elemento);
    }
}

cargarCuentas();
