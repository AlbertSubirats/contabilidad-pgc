# Parser del PGC a partir del texto del BOE (sources/boe/texto.xml).
# De momento extrae solo el cuadro de cuentas, de las tablas de la cuarta
# parte. Las fichas de la quinta parte llegarán en el paso 1b·4, y será
# entonces cuando se guarde el JSON. Hasta ese paso, data/accounts.json lo
# sigue generando parser.py a partir del texto refundido.

from boe_reader import cargar_raiz, parrafos_del_bloque, filas_de_las_tablas

PLAN = "pgc-general"

# Los números de los grupos, que son también los de los bloques de la cuarta
# parte: "grupo1", "grupo2"... (los de la quinta parte son "grupo1-2"...).
NUMEROS_DE_GRUPO = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Fe de erratas del cuadro de cuentas. La tabla de la cuarta parte del BOE
# tiene errores de contenido, en todas sus versiones. Las erratas que no
# cambian el sentido ("DETERIOROY") se respetan; estas no, porque dejarían
# una cuenta sin nombre correcto o fuera del cuadro. Cada corrección dice de
# dónde sale el dato bueno: nada se completa de memoria.

# Nombres equivocados: lo que dice la tabla del BOE y lo que debería decir.
# Prueba: las fichas de la quinta parte del mismo BOE (bloque "grupo5-2")
# dan "500. Obligaciones y bonos a corto plazo", "501. Obligaciones y bonos
# convertibles a corto plazo" y "502. Acciones o participaciones...". La
# tabla pega los nombres de la 500 y la 501, y a la 502 la llama 501.
NOMBRES_CORREGIDOS = {
    "500": {
        "en_el_boe": "Obligaciones y bonos a corto plazo Obligaciones y bonos convertibles a corto plazo",
        "correcto": "Obligaciones y bonos a corto plazo",
    },
    "501": {
        "en_el_boe": "Acciones o participaciones a corto plazo consideradas como pasivos financieros",
        "correcto": "Obligaciones y bonos convertibles a corto plazo",
    },
}

# Cuentas que la tabla del BOE no trae.
CUENTAS_QUE_FALTAN = {
    # La que la tabla llamaba 501 (ver arriba). Prueba: bloque "grupo5-2".
    "502": "Acciones o participaciones a corto plazo consideradas como pasivos financieros",
    # Prueba: tiene ficha en la quinta parte del BOE (bloque "grupo1-2"), y
    # está en el cuadro del texto refundido.
    "1141": "Reservas estatutarias",
    # Prueba: el cuadro del texto refundido, y el propio BOE las cita en la
    # cuenta de pérdidas y ganancias (bloque "cuenta"). Las comillas «» son
    # las que usa el BOE en sus vecinas, la 6654 y la 6657.
    "6655": "Intereses por operaciones de «factoring» con entidades de crédito asociadas",
    "6656": "Intereses por operaciones de «factoring» con otras entidades de crédito vinculadas",
}


# Las cuatro funciones siguientes están copiadas tal cual de parser.py, para
# que el dato tenga la misma forma. No se importan porque parser.py ejecuta
# todo su proceso al importarlo, y es un fichero que se va a retirar.

def nivel_de_cuenta(codigo):
    cifras = len(codigo)
    if cifras == 1:
        return "grupo"
    elif cifras == 2:
        return "subgrupo"
    elif cifras == 3:
        return "cuenta"
    else:
        return "subcuenta"


def padre_de_cuenta(codigo):
    # Las subcuentas de 4 y de 5 cifras cuelgan las dos de su cuenta de 3.
    cifras = len(codigo)
    if cifras == 1:
        return None
    elif cifras == 2:
        return codigo[:1]
    elif cifras == 3:
        return codigo[:2]
    else:
        return codigo[:3]


def crear_cuenta(codigo, nombre):
    cuenta = {
        "plan": PLAN,
        "codigo": codigo,
        "nivel": nivel_de_cuenta(codigo),
        "nombre": nombre,
        "padre": padre_de_cuenta(codigo),
        # Se rellenan después, con la Quinta Parte. Una lista vacía quiere
        # decir que el texto no dice nada de eso.
        "definicion": [],
        "presentacion": [],
        "cargos": [],
        "abonos": [],
    }
    return cuenta


def codigo_de_la_cuenta(cuenta):
    # La usa sort() para saber por qué campo ordenar las cuentas. El código es
    # texto, así que se ordena como en un diccionario: "52" < "520" < "5209" < "53".
    # Ese es justo el orden del árbol del cuadro de cuentas.
    return cuenta["codigo"]


def extraer_grupo(raiz, numero):
    # El grupo no va en la tabla: son los dos primeros párrafos del bloque,
    # "Grupo 4" y "Acreedores y deudores por operaciones comerciales".
    parrafos = parrafos_del_bloque(raiz, "grupo" + numero)
    if parrafos[0] != "Grupo " + numero:
        print("AVISO: el bloque del grupo", numero, "empieza por", parrafos[0])
    return crear_cuenta(numero, parrafos[1])


def extraer_cuentas_de_la_tabla(raiz, numero_de_grupo):
    cuentas = []
    for celdas in filas_de_las_tablas(raiz, "grupo" + numero_de_grupo):
        # La tabla sangra los niveles con celdas vacías delante:
        #   ["40.", "PROVEEDORES"]
        #   ["", "400.", "Proveedores"]
        #   ["", "", "4000.", "Proveedores (euros)"]
        # La primera celda con texto es el código y la siguiente, el nombre.
        columna = 0
        while celdas[columna] == "":
            columna = columna + 1

        codigo = celdas[columna].rstrip(".")
        # Ocho nombres del BOE acaban en punto y los demás no. Se quita para
        # que todos queden iguales (decisión de Albert, ver CHANGELOG.md).
        nombre = celdas[columna + 1].rstrip(".")

        # Segunda opinión: un código de 2 cifras va en la columna 0, uno de 3
        # en la 1, y así. Si no cuadra, la tabla tiene algo raro.
        columna_esperada = len(codigo) - 2
        if columna != columna_esperada:
            print("AVISO: la", codigo, "está en la columna", columna, "y se esperaba la", columna_esperada)

        cuentas.append(crear_cuenta(codigo, nombre))
    return cuentas


def aplicar_fe_de_erratas_del_cuadro(cuentas):
    # Para encontrar una cuenta por su código sin recorrer la lista entera.
    cuentas_por_codigo = {}
    for cuenta in cuentas:
        cuentas_por_codigo[cuenta["codigo"]] = cuenta

    for codigo, errata in NOMBRES_CORREGIDOS.items():
        cuenta = cuentas_por_codigo[codigo]
        if cuenta["nombre"] != errata["en_el_boe"]:
            # Si el BOE ya lo ha corregido, mejor enterarse que seguir
            # corrigiendo a ciegas.
            print("AVISO: la errata de la", codigo, "ya no aparece en el BOE")
            continue
        cuenta["nombre"] = errata["correcto"]

    for codigo, nombre in CUENTAS_QUE_FALTAN.items():
        if codigo in cuentas_por_codigo:
            print("AVISO: la", codigo, "ya aparece en el BOE")
            continue
        cuentas.append(crear_cuenta(codigo, nombre))


def extraer_cuadro_de_cuentas(raiz):
    cuentas = []
    for numero in NUMEROS_DE_GRUPO:
        cuentas.append(extraer_grupo(raiz, numero))
        # extend añade las cuentas de la tabla una a una; append añadiría la
        # lista entera como si fuera un solo elemento.
        cuentas.extend(extraer_cuentas_de_la_tabla(raiz, numero))

    aplicar_fe_de_erratas_del_cuadro(cuentas)

    # Las cuentas que faltaban se han añadido al final: se ordena por código.
    cuentas.sort(key=codigo_de_la_cuenta)
    return cuentas


# El resumen solo sale al lanzar este fichero. tools/check_chart.py lo
# importa para pedirle el cuadro, y ahí no hace falta.
if __name__ == "__main__":
    raiz = cargar_raiz()
    cuentas = extraer_cuadro_de_cuentas(raiz)

    print("Cuadro de cuentas del BOE")
    cuentas_por_nivel = {"grupo": 0, "subgrupo": 0, "cuenta": 0, "subcuenta": 0}
    for cuenta in cuentas:
        cuentas_por_nivel[cuenta["nivel"]] += 1
    print("Grupos:", cuentas_por_nivel["grupo"])
    print("Subgrupos:", cuentas_por_nivel["subgrupo"])
    print("Cuentas:", cuentas_por_nivel["cuenta"])
    print("Subcuentas:", cuentas_por_nivel["subcuenta"])

    print()
    for cuenta in cuentas:
        if cuenta["codigo"] in ["4", "43", "430", "500", "501", "502", "1141"]:
            print(cuenta["codigo"], "-", cuenta["nombre"], "- cuelga de:", cuenta["padre"])
