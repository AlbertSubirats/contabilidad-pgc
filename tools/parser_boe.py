# Parser del PGC a partir del texto del BOE (sources/boe/texto.xml).
# Extrae el cuadro de cuentas, de las tablas de la cuarta parte, y le añade
# a cada cuenta su ficha, de la quinta parte. Lo guarda en
# data/accounts_boe.json. La web sigue leyendo data/accounts.json, que genera
# parser.py, hasta el paso 1b·6, porque los movimientos cambian de forma.

import json
import re
from pathlib import Path

from boe_reader import cargar_raiz, parrafos_del_bloque, filas_de_las_tablas, contenido_del_bloque

PLAN = "pgc-general"

# El título de una ficha: "430. Clientes", "600/601/602/607. Compras de...",
# "2403/2404 Participaciones..." (sin punto) o "230/237" (sin nombre).
# Grupo 1: los códigos, con sus barras.
PATRON_TITULO_DE_FICHA = r"(\d{3,5}(/\d{3,5})*)\.?( .*)?"

# La cabecera de un movimiento: "a) Se cargará:", "Se abonará:", o
# "b) Se abonará por las enajenaciones..., con cargo a...".
# Grupo 1: la letra con su paréntesis, si la hay. Grupo 2: el verbo.
# Grupo 3: lo que venga detrás, que puede ser nada.
PATRON_CABECERA_DE_MOVIMIENTO = r"([a-z]\) )?Se (cargar|abonar)án?[:,]?\s*(.*)"

# Un movimiento con su etiqueta: "a1) Por las ventas..." o "a) Al devengo...".
# Grupo 1: la letra. Grupo 2: el número, que puede faltar. Grupo 3: el texto.
PATRON_ETIQUETA = r"([a-z])(\d*)\) (.*)"

# Una frase de presentación dice en qué parte del balance figura la cuenta:
# "Figurará en el activo corriente...", "Las cuentas de este subgrupo
# figurarán en el pasivo...", "...deberá figurar en el epígrafe...".
PATRON_PRESENTACION = r"[Ff]igurar(á|án)? en el (activo|pasivo|patrimonio|epígrafe)"

# La frase con la que el PGC presenta los movimientos. No dice nada por sí
# sola: se quita cuando va sola o al final de un párrafo. Si va con algo
# delante ("Con carácter general, su movimiento..."), el párrafo se queda.
FRASE_QUE_PRESENTA_EL_MOVIMIENTO = "Su movimiento es el siguiente:"

# Los derivados de cobertura tienen un movimiento en dos niveles con una
# condición ("b) Cuando el derivado se utilice como instrumento de
# cobertura...: b1) Se cargará: i) ... ii) ..."). En dos columnas se perdería
# la condición, así que su movimiento se queda en la definición, tal cual.
CUENTAS_CON_MOVIMIENTO_ANIDADO = ["1768", "2553", "5593", "5598"]

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


def codigos_del_titulo(texto, codigos_del_cuadro):
    # Devuelve la lista de códigos si el párrafo es el título de una ficha, o
    # None si no lo es.
    coincidencia = re.fullmatch(PATRON_TITULO_DE_FICHA, texto)
    if coincidencia is None:
        return None
    codigos = coincidencia.group(1).split("/")
    for codigo in codigos:
        if codigo not in codigos_del_cuadro:
            return None

    # Con dos códigos, la barra es un intervalo, como en "Las cuentas
    # 300/309": "700/705" son de la 700 a la 705, también la 701, la 702...
    # Con tres o más, es una lista: en "600/601/602/607" no entra la 606.
    if len(codigos) == 2:
        primero = codigos[0]
        ultimo = codigos[1]
        intervalo = []
        for codigo in codigos_del_cuadro:
            # La misma longitud, porque como texto "7001" va entre "700" y "705".
            if len(codigo) == len(primero) and primero <= codigo <= ultimo:
                intervalo.append(codigo)
        return intervalo
    return codigos


def habla_de_cargo_y_abono(texto):
    # Frases como "Se cargarán por el importe de las existencias iniciales y
    # se abonarán por el de las finales" describen las dos columnas a la vez
    # y no se pueden repartir sin inventar: se quedan en la definición.
    # Solo se mira la primera frase: más allá puede salir la otra palabra sin
    # que la cabecera sea mixta.
    primera_frase = texto.split(". ")[0].lower()
    return "se cargar" in primera_frase and "se abonar" in primera_frase


def quitar_frase_que_presenta_el_movimiento(texto):
    # "Corresponde a las empresas individuales. Su movimiento es el
    # siguiente:" → "Corresponde a las empresas individuales." Si el párrafo
    # es solo la frase, queda vacío.
    texto = texto.removesuffix(FRASE_QUE_PRESENTA_EL_MOVIMIENTO)
    return texto.strip()


def partir_presentacion_pegada(texto):
    # Unos pocos párrafos traen la definición y la presentación juntas:
    # "Desembolsos exigidos... Figurará en el pasivo corriente del balance."
    # Se parten en dos justo antes de "Figurará", sin cambiar ni una letra.
    posicion = texto.find(". Figurará")
    if posicion == -1:
        return [texto]
    return [texto[:posicion + 1], texto[posicion + 2:]]


def anadir_a_las_cuentas(cuentas_por_codigo, codigos, campo, valor):
    # Una ficha compartida ("600/601/602/607") se copia a cada una de sus
    # cuentas, así que todo se añade siempre a una lista de códigos.
    for codigo in codigos:
        cuentas_por_codigo[codigo][campo].append(valor)


def etiqueta_encaja_con_la_cabecera(letra, numero, letra_de_la_cabecera):
    # Bajo "b) Se abonará:" van "b1)", "b2)"... Bajo un "Se abonará:" sin
    # letra pueden ir "a)", "b)"... (la 761) o "a1)", "a2)"... (la 640).
    # Así no se cuela como movimiento un "c) Si las participaciones..." que
    # va detrás de los "b1) b2)".
    if letra_de_la_cabecera is None:
        return True
    return letra == letra_de_la_cabecera and numero != ""


def extraer_fichas(raiz, cuentas):
    # Para encontrar una cuenta por su código sin recorrer la lista entera, y
    # la lista de códigos en orden, que necesitan los títulos con intervalo.
    cuentas_por_codigo = {}
    codigos_del_cuadro = []
    for cuenta in cuentas:
        cuentas_por_codigo[cuenta["codigo"]] = cuenta
        codigos_del_cuadro.append(cuenta["codigo"])

    for numero in NUMEROS_DE_GRUPO:
        contenido = contenido_del_bloque(raiz, "grupo" + numero + "-2")

        # Los dos primeros párrafos son "Grupo 4" y su nombre, que ya están
        # en el cuadro. Lo que sigue, hasta la primera tabla, es del grupo.
        if contenido[0]["texto"] != "Grupo " + numero:
            print("AVISO: la quinta parte del grupo", numero, "empieza por", contenido[0]["texto"])

        # El estado: de qué cuentas es lo que se lee (una lista, porque una
        # ficha puede ser de varias), en qué columna del movimiento estamos
        # (None si no estamos en los movimientos) y la letra de la cabecera
        # que abrió esa columna.
        codigos_actuales = [numero]
        columna_actual = None
        letra_de_la_cabecera = None

        for elemento in contenido[2:]:
            # 1. La tabla índice abre un subgrupo. Su primera fila es la del
            # propio subgrupo: ["43.", "CLIENTES"].
            if elemento["tipo"] == "tabla":
                codigos_actuales = [elemento["filas"][0][0].rstrip(".")]
                columna_actual = None
                continue

            texto = elemento["texto"]

            # 2. El título de una ficha cambia las cuentas actuales.
            codigos = codigos_del_titulo(texto, codigos_del_cuadro)
            if codigos is not None:
                codigos_actuales = codigos
                columna_actual = None
                continue

            texto = quitar_frase_que_presenta_el_movimiento(texto)
            if texto == "":
                continue

            movimiento_en_columnas = codigos_actuales[0] not in CUENTAS_CON_MOVIMIENTO_ANIDADO

            # 3. Una cabecera ("a) Se cargará:") abre una columna. Si trae
            # texto detrás ("b) Se abonará por las enajenaciones..."), ese
            # texto es un movimiento sin etiqueta.
            cabecera = re.match(PATRON_CABECERA_DE_MOVIMIENTO, texto)
            if cabecera is not None and movimiento_en_columnas and not habla_de_cargo_y_abono(texto):
                if cabecera.group(2) == "cargar":
                    columna_actual = "cargos"
                else:
                    columna_actual = "abonos"
                if cabecera.group(1) is None:
                    letra_de_la_cabecera = None
                else:
                    letra_de_la_cabecera = cabecera.group(1)[0]
                if cabecera.group(3) != "":
                    movimiento = {"etiqueta": None, "texto": cabecera.group(3)}
                    anadir_a_las_cuentas(cuentas_por_codigo, codigos_actuales, columna_actual, movimiento)
                continue
            if cabecera is not None:
                # Una cabecera mixta ("c) Se cargará o abonará...") o de un
                # derivado de cobertura no va a ninguna columna: cierra los
                # movimientos y va a la definición (paso 5).
                columna_actual = None

            # 4. Dentro de una columna, un movimiento con su etiqueta.
            if columna_actual is not None:
                etiqueta = re.match(PATRON_ETIQUETA, texto)
                if etiqueta is not None and etiqueta_encaja_con_la_cabecera(etiqueta.group(1), etiqueta.group(2), letra_de_la_cabecera):
                    movimiento = {"etiqueta": etiqueta.group(1) + etiqueta.group(2), "texto": etiqueta.group(3)}
                    anadir_a_las_cuentas(cuentas_por_codigo, codigos_actuales, columna_actual, movimiento)
                    continue
                # Cualquier otro párrafo cierra los movimientos.
                columna_actual = None

            # 5. Texto normal: la presentación en el balance o la definición.
            for trozo in partir_presentacion_pegada(texto):
                if re.search(PATRON_PRESENTACION, trozo):
                    campo = "presentacion"
                else:
                    campo = "definicion"
                anadir_a_las_cuentas(cuentas_por_codigo, codigos_actuales, campo, trozo)


def detectar_contrapartidas(movimientos, codigos_existentes):
    # Copiada de parser.py, con un cambio: ahora cada movimiento es un
    # diccionario y el texto está en movimiento["texto"].
    # Devuelve, ordenados y sin repetir, los códigos de cuenta que aparecen
    # en los movimientos: "...con abono a la cuenta 437" → "437".
    codigos_encontrados = set()
    for movimiento in movimientos:
        for numero in re.findall(r"\d+", movimiento["texto"]):
            # Solo cuenta si es el código de una cuenta que existe.
            if numero in codigos_existentes:
                codigos_encontrados.add(numero)
    return sorted(codigos_encontrados)


# El proceso y el resumen solo se ejecutan al lanzar este fichero.
# tools/check_chart.py lo importa para pedirle el cuadro, y ahí no hacen falta.
if __name__ == "__main__":
    raiz = cargar_raiz()
    cuentas = extraer_cuadro_de_cuentas(raiz)
    extraer_fichas(raiz, cuentas)

    codigos_existentes = set()
    for cuenta in cuentas:
        codigos_existentes.add(cuenta["codigo"])
    for cuenta in cuentas:
        cuenta["contrapartidas_cargos"] = detectar_contrapartidas(cuenta["cargos"], codigos_existentes)
        cuenta["contrapartidas_abonos"] = detectar_contrapartidas(cuenta["abonos"], codigos_existentes)

    # La ruta se calcula desde este script, como en parser.py.
    raiz_del_proyecto = Path(__file__).parent.parent
    ruta_del_json = raiz_del_proyecto / "data" / "accounts_boe.json"
    # ensure_ascii=False deja las tildes como tildes, e indent=2 pone cada
    # campo en su línea para poder leerlo. None se escribe como null.
    texto_json = json.dumps(cuentas, ensure_ascii=False, indent=2)
    ruta_del_json.write_text(texto_json, encoding="utf-8")

    print("Guardado en:", ruta_del_json)
    cuentas_por_nivel = {"grupo": 0, "subgrupo": 0, "cuenta": 0, "subcuenta": 0}
    for cuenta in cuentas:
        cuentas_por_nivel[cuenta["nivel"]] += 1
    print("Grupos:", cuentas_por_nivel["grupo"])
    print("Subgrupos:", cuentas_por_nivel["subgrupo"])
    print("Cuentas:", cuentas_por_nivel["cuenta"])
    print("Subcuentas:", cuentas_por_nivel["subcuenta"])

    print()
    cuentas_de_tres_cifras = 0
    con_definicion = 0
    con_presentacion = 0
    con_movimientos = 0
    for cuenta in cuentas:
        if cuenta["nivel"] == "cuenta":
            cuentas_de_tres_cifras += 1
            if len(cuenta["definicion"]) > 0:
                con_definicion += 1
            if len(cuenta["presentacion"]) > 0:
                con_presentacion += 1
            if len(cuenta["cargos"]) > 0 or len(cuenta["abonos"]) > 0:
                con_movimientos += 1
    print("De las", cuentas_de_tres_cifras, "cuentas de tres cifras:")
    print("  con definición:", con_definicion)
    print("  con presentación:", con_presentacion)
    print("  con movimientos en columnas:", con_movimientos)

    print()
    for cuenta in cuentas:
        if cuenta["codigo"] == "430":
            etiquetas_de_cargos = []
            for movimiento in cuenta["cargos"]:
                etiquetas_de_cargos.append(movimiento["etiqueta"])
            etiquetas_de_abonos = []
            for movimiento in cuenta["abonos"]:
                etiquetas_de_abonos.append(movimiento["etiqueta"])
            print("La 430 se llama:", cuenta["nombre"])
            print("  presentación:", cuenta["presentacion"])
            print("  cargos:", etiquetas_de_cargos)
            print("  abonos:", etiquetas_de_abonos)
            print("  contrapartidas en cargos:", cuenta["contrapartidas_cargos"])
            print("  contrapartidas en abonos:", cuenta["contrapartidas_abonos"])
        if cuenta["codigo"] == "642":
            print("La 642 empieza así:", cuenta["definicion"][0][:60] + "...")
