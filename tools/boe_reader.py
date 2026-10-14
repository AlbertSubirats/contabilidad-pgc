# Lee el texto del PGC desde la copia del BOE (sources/boe/texto.xml).
# El texto está partido en bloques, y cada bloque trae una versión por cada
# reforma de la ley. Aquí nos quedamos siempre con la última y quitamos las
# notas que añade el BOE, que no son texto del PGC (CLAUDE.md, sección 7).

import xml.etree.ElementTree as ET
from pathlib import Path

carpeta_del_script = Path(__file__).parent
raiz_del_proyecto = carpeta_del_script.parent
RUTA_DEL_TEXTO = raiz_del_proyecto / "sources" / "boe" / "texto.xml"

# Las clases de los párrafos que el BOE añade por su cuenta ("Se modifica la
# introducción al Grupo 4 por el art. 1.17.10 del Real Decreto 1/2021...").
CLASES_DE_NOTA = ["nota_pie", "nota_pie_2"]


def cargar_raiz():
    # No hace falta decir encoding="utf-8": el XML lo declara en su primera
    # línea y ElementTree la lee.
    arbol = ET.parse(RUTA_DEL_TEXTO)
    return arbol.getroot()


def buscar_bloque(raiz, id_del_bloque):
    for bloque in raiz.iter("bloque"):
        if bloque.get("id") == id_del_bloque:
            return bloque
    return None


def ultima_version(bloque):
    # El BOE da las versiones en orden de fecha: la última es la vigente.
    versiones = bloque.findall("version")
    return versiones[-1]


def texto_del_elemento(elemento):
    # Sirve para un párrafo, una celda de tabla o cualquier otro elemento.
    # Puede tener etiquetas dentro, como "b<sub>1</sub>) La empresa...".
    # itertext() da todos los trozos de texto, también los de dentro de esas
    # etiquetas, y join los pega: "b1) La empresa...".
    trozos = elemento.itertext()
    texto = "".join(trozos)
    return texto.strip()


def version_vigente(raiz, id_del_bloque):
    bloque = buscar_bloque(raiz, id_del_bloque)
    if bloque is None:
        # Mejor fallar aquí que devolver una lista vacía: un id mal escrito
        # parecería un bloque sin texto.
        raise ValueError("No hay ningún bloque con id " + id_del_bloque)
    return ultima_version(bloque)


def filas_de_la_tabla(tabla):
    # Devuelve una lista por fila con el texto de sus celdas, en orden:
    # ["", "400.", "Proveedores"]. Las celdas vacías se quedan como "",
    # porque su posición importa: dice en qué columna empieza el texto.
    filas = []
    # iter y no findall: en unas tablas las filas son hijas directas de
    # <table> y en otras van dentro de un <tbody>. iter las encuentra a
    # cualquier profundidad.
    for fila in tabla.iter("tr"):
        celdas = []
        for celda in fila.findall("td"):
            celdas.append(texto_del_elemento(celda))
        filas.append(celdas)
    return filas


def contenido_del_bloque(raiz, id_del_bloque):
    # Los párrafos y las tablas del bloque, en el orden en que vienen. Cada
    # elemento es un diccionario: {"tipo": "parrafo", "texto": "..."} o
    # {"tipo": "tabla", "filas": [...]}.
    version = version_vigente(raiz, id_del_bloque)
    contenido = []
    # Un for sobre un elemento recorre sus hijos directos, en orden. Los
    # <blockquote>, que es donde el BOE mete sus notas, no se añaden: así las
    # notas quedan fuera.
    for elemento in version:
        if elemento.tag == "p":
            # Hoy esto no salta nunca, por lo dicho arriba. Se deja de reserva
            # por si una versión futura del BOE sacara las notas del <blockquote>.
            if elemento.get("class") in CLASES_DE_NOTA:
                continue
            texto = texto_del_elemento(elemento)
            if texto == "":
                continue
            contenido.append({"tipo": "parrafo", "texto": texto})
        elif elemento.tag == "table":
            contenido.append({"tipo": "tabla", "filas": filas_de_la_tabla(elemento)})
    return contenido


def parrafos_del_bloque(raiz, id_del_bloque):
    parrafos = []
    for elemento in contenido_del_bloque(raiz, id_del_bloque):
        if elemento["tipo"] == "parrafo":
            parrafos.append(elemento["texto"])
    return parrafos


def filas_de_las_tablas(raiz, id_del_bloque):
    # Las filas de todas las tablas del bloque, seguidas.
    version = version_vigente(raiz, id_del_bloque)
    filas = []
    for tabla in version.findall("table"):
        filas.extend(filas_de_la_tabla(tabla))
    return filas


# Esta prueba solo se ejecuta al lanzar este fichero directamente
# (python tools/boe_reader.py), no cuando otro fichero lo importa.
if __name__ == "__main__":
    # Prueba: los párrafos del Grupo 4 de la quinta parte.
    raiz = cargar_raiz()
    parrafos = parrafos_del_bloque(raiz, "grupo4-2")
    print("Bloque grupo4-2:", len(parrafos), "párrafos")

    print()
    print("Los cinco primeros:")
    for parrafo in parrafos[:5]:
        print("-", parrafo[:100])

    notas_coladas = 0
    for parrafo in parrafos:
        if parrafo.startswith("Se modifica"):
            notas_coladas = notas_coladas + 1

    print()
    print("¿Está '430. Clientes'?", "430. Clientes" in parrafos)
    print("Notas del BOE coladas:", notas_coladas)
