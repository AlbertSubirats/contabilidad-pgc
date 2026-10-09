# Parser del texto refundido del PGC.
# Lee el fichero fuente, limpia la basura que dejó el OCR, extrae el cuadro
# de cuentas (Cuarta Parte) y le añade a cada cuenta su ficha (Quinta Parte).
# Lo guarda todo en data/accounts.json.

import json
import re
from pathlib import Path

# Una marca de página del OCR: una llave, un número, otra llave y una tira de
# guiones. Por ejemplo: {17}------------------------------------------------
PATRON_MARCA_DE_PAGINA = r"\{\d+\}-+"

# Un código de cuenta: de 2 a 5 cifras, un punto y un espacio. Por ejemplo
# "430. ". Los paréntesis forman un grupo de captura: guardan las cifras.
PATRON_CODIGO_DE_CUENTA = r"(\d{2,5})\. "

# El título de una ficha: un código y el nombre de la cuenta. Por ejemplo
# "430. Clientes". El punto es opcional porque el OCR a veces se lo comió.
PATRON_TITULO_DE_FICHA = r"(\d{2,5})\.? (.+)"

# El título de una ficha compartida por varias cuentas, con los códigos
# separados por barras. Por ejemplo "600/601/602/607. Compras de . . . ."
PATRON_TITULO_COMPARTIDO = r"(\d{3,5}(/\d{3,5})+)\.?( .*)?"

# El principio de un movimiento: "a) Se cargará:", "b) Se abonarán: b1) ..."
# o "Se cargará:" sin letra. Detrás del verbo puede ir dos puntos o una coma
# ("Se abonará, al cierre del ejercicio, ...").
# Grupo 2: el verbo. Grupo 3: lo que venga detrás.
PATRON_INICIO_DE_MOVIMIENTO = r"([a-z]\) )?Se (cargar|abonar)án?[:,]?\s*(.*)"

# La etiqueta de cada movimiento dentro de la lista: "a1) ", "b12) "...
PATRON_ETIQUETA_DE_MOVIMIENTO = r"[a-z]\d+\) "

PLAN = "pgc-general"


def quitar_marcas_de_pagina(lineas):
    lineas_sin_marcas = []
    for linea in lineas:
        if re.fullmatch(PATRON_MARCA_DE_PAGINA, linea):
            continue
        lineas_sin_marcas.append(linea)
    return lineas_sin_marcas


def quitar_espacios_al_final(lineas):
    lineas_recortadas = []
    for linea in lineas:
        lineas_recortadas.append(linea.rstrip())
    return lineas_recortadas


def juntar_lineas_en_blanco(lineas):
    # Al quitar una marca quedan juntas la línea en blanco de antes y la de
    # después. Basta con una para separar párrafos.
    lineas_juntadas = []
    anterior_era_blanca = False
    for linea in lineas:
        es_blanca = linea == ""
        if es_blanca and anterior_era_blanca:
            continue
        lineas_juntadas.append(linea)
        anterior_era_blanca = es_blanca
    return lineas_juntadas


def recortar_cuarta_parte(lineas):
    # El cuadro de cuentas es la Cuarta Parte: va desde su título hasta el
    # título de la Quinta Parte.
    lineas_de_la_parte = []
    dentro_de_la_parte = False
    for linea in lineas:
        if linea.startswith("# CUARTA PARTE"):
            dentro_de_la_parte = True
            continue
        if linea.startswith("# QUINTA PARTE"):
            break
        if dentro_de_la_parte:
            lineas_de_la_parte.append(linea)
    return lineas_de_la_parte


def quitar_simbolos_de_markdown(linea):
    # Los títulos empiezan por "#", los elementos de lista por "-", y algunos
    # textos van en negrita entre "**".
    linea = linea.strip()
    linea = linea.lstrip("#- ")
    linea = linea.replace("**", "")
    return linea


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


def extraer_cuadro_de_cuentas(lineas):
    cuentas = []
    # "GRUPO 4" va en una línea y su nombre en la siguiente, así que al ver
    # un grupo hay que acordarse de su código hasta leer la línea de después.
    grupo_sin_nombre = None
    for linea in lineas:
        texto = quitar_simbolos_de_markdown(linea)
        if texto == "":
            continue

        if re.fullmatch(r"GRUPO \d", texto):
            grupo_sin_nombre = texto[-1]
            continue

        if grupo_sin_nombre is not None:
            cuentas.append(crear_cuenta(grupo_sin_nombre, texto))
            grupo_sin_nombre = None
            continue

        # Una línea puede traer varias cuentas aplastadas:
        # "430. Clientes 4300. Clientes (euros) 4304. Clientes (moneda ..."
        # Al partir por el código, los trozos quedan alternados:
        # ["", "430", "Clientes ", "4300", "Clientes (euros) ", ...]
        trozos = re.split(PATRON_CODIGO_DE_CUENTA, texto)
        posicion = 1
        while posicion < len(trozos):
            codigo = trozos[posicion]
            nombre = trozos[posicion + 1].strip().rstrip(".")
            cuentas.append(crear_cuenta(codigo, nombre))
            posicion = posicion + 2
    return cuentas


def recortar_quinta_parte(lineas):
    # Las fichas de las cuentas son la Quinta Parte, que llega hasta el final.
    lineas_de_la_parte = []
    dentro_de_la_parte = False
    for linea in lineas:
        if linea.startswith("# QUINTA PARTE"):
            dentro_de_la_parte = True
            continue
        if dentro_de_la_parte:
            lineas_de_la_parte.append(linea)
    return lineas_de_la_parte


def codigos_del_titulo(texto, cuentas_por_codigo):
    # Devuelve la lista de códigos si la línea es el título de una ficha, o
    # None si no lo es.
    coincidencia = re.fullmatch(PATRON_TITULO_COMPARTIDO, texto)
    if coincidencia:
        codigos = coincidencia.group(1).split("/")
        for codigo in codigos:
            if codigo not in cuentas_por_codigo:
                return None
        return codigos

    coincidencia = re.fullmatch(PATRON_TITULO_DE_FICHA, texto)
    if coincidencia:
        codigo = coincidencia.group(1)
        nombre_en_el_titulo = coincidencia.group(2)
        if codigo not in cuentas_por_codigo:
            return None
        # A veces el OCR parte un movimiento justo después de un número, y
        # una línea empieza por "57. b2) Por su traspaso...". Para no tomarla
        # por un título, la primera palabra tiene que ser la del nombre de la
        # cuenta. Solo la primera, porque la Quinta Parte a veces cambia
        # alguna palabra del nombre respecto de la Cuarta.
        nombre_en_el_cuadro = cuentas_por_codigo[codigo]["nombre"]
        primera_palabra_titulo = nombre_en_el_titulo.split()[0].lower()
        primera_palabra_cuadro = nombre_en_el_cuadro.split()[0].lower()
        if primera_palabra_titulo == primera_palabra_cuadro:
            return [codigo]
    return None


def elegir_titulo_de_la_racha(racha):
    # Una racha es una serie de títulos seguidos, sin texto entre ellos.
    # Si solo hay uno, es el título de una ficha.
    if len(racha) == 1:
        return racha[0]
    # Si hay varios, es el índice con el que empieza cada subgrupo:
    #   43. CLIENTES / 430. Clientes / 431. ... / 438. Anticipos de clientes
    # Si el último repite un código del índice, es el título de la primera
    # ficha, que viene justo detrás del índice (como "430. Clientes").
    ultimo = racha[-1]
    anteriores = racha[:-1]
    if ultimo in anteriores:
        return ultimo
    # Si no, el texto que sigue es del subgrupo, que va el primero.
    return racha[0]


def partir_movimientos(texto):
    # "a1) Por las ventas... a2) Por los envases..." → una lista con un
    # movimiento por elemento y sin las etiquetas.
    movimientos = []
    for trozo in re.split(PATRON_ETIQUETA_DE_MOVIMIENTO, texto):
        trozo = trozo.strip()
        if trozo != "":
            movimientos.append(trozo)
    return movimientos


def habla_de_cargo_y_abono(texto):
    # Frases como "Se cargarán a la entrada ... y se abonarán a su salida"
    # describen las dos columnas a la vez y no se pueden repartir sin
    # inventar. Esas se quedan enteras en la definición.
    texto_en_minusculas = texto.lower()
    return "se cargar" in texto_en_minusculas and "se abonar" in texto_en_minusculas


def extraer_fichas(lineas, cuentas):
    # Para encontrar una cuenta por su código sin recorrer la lista entera.
    cuentas_por_codigo = {}
    for cuenta in cuentas:
        cuentas_por_codigo[cuenta["codigo"]] = cuenta

    # El estado: qué cuentas se están leyendo (una lista, porque una ficha
    # puede ser de varias) y en qué parte de la ficha estamos: None si es
    # texto, "cargos" o "abonos" si estamos dentro de los movimientos.
    codigos_actuales = []
    parte_actual = None
    racha_de_titulos = []
    viene_nombre_de_grupo = False

    for linea in lineas:
        texto = quitar_simbolos_de_markdown(linea)
        if texto == "":
            continue

        # 1. Títulos: cambian la cuenta actual.
        if re.fullmatch(r"GRUPO \d", texto):
            codigos_actuales = [texto[-1]]
            parte_actual = None
            racha_de_titulos = []
            viene_nombre_de_grupo = True
            continue
        if viene_nombre_de_grupo:
            # Es "FINANCIACIÓN BÁSICA" o similar: ya lo tenemos del cuadro.
            viene_nombre_de_grupo = False
            continue

        codigos = codigos_del_titulo(texto, cuentas_por_codigo)
        if codigos is not None:
            racha_de_titulos.append(codigos)
            continue

        # Si llegamos aquí, la línea no es un título. Si veníamos de una
        # racha de títulos, ya sabemos de qué cuenta es lo que sigue.
        if len(racha_de_titulos) > 0:
            codigos_actuales = elegir_titulo_de_la_racha(racha_de_titulos)
            parte_actual = None
            racha_de_titulos = []

        if len(codigos_actuales) == 0:
            # Texto anterior al primer grupo: no es de ninguna cuenta.
            continue

        # 2. La frase que presenta los movimientos no se guarda.
        if texto.lower().endswith("su movimiento es el siguiente:"):
            continue

        # 3. "Se cargará:" o "Se abonará:": cambian la parte actual.
        coincidencia = re.match(PATRON_INICIO_DE_MOVIMIENTO, texto)
        if coincidencia and not habla_de_cargo_y_abono(texto):
            if coincidencia.group(2) == "cargar":
                parte_actual = "cargos"
            else:
                parte_actual = "abonos"
            for codigo in codigos_actuales:
                cuenta = cuentas_por_codigo[codigo]
                cuenta[parte_actual].extend(partir_movimientos(coincidencia.group(3)))
            continue

        # 4. Dentro de los movimientos.
        if parte_actual is not None:
            if re.match(PATRON_ETIQUETA_DE_MOVIMIENTO, texto):
                for codigo in codigos_actuales:
                    cuenta = cuentas_por_codigo[codigo]
                    cuenta[parte_actual].extend(partir_movimientos(texto))
                continue
            if texto[0].islower() or texto[0].isdigit():
                # La línea sigue una frase que el OCR partió. Su primer trozo
                # completa el último movimiento, y el resto son movimientos
                # nuevos, si los hay.
                trozos = partir_movimientos(texto)
                for codigo in codigos_actuales:
                    cuenta = cuentas_por_codigo[codigo]
                    if len(cuenta[parte_actual]) > 0:
                        cuenta[parte_actual][-1] = cuenta[parte_actual][-1] + " " + trozos[0]
                    cuenta[parte_actual].extend(trozos[1:])
                continue
            # Una frase que empieza en mayúscula es un párrafo nuevo: los
            # movimientos se han acabado.
            parte_actual = None

        # 5. Texto normal: la presentación en el balance o la definición.
        if re.match(r"Figurarán? ", texto):
            campo = "presentacion"
        else:
            campo = "definicion"
        for codigo in codigos_actuales:
            cuentas_por_codigo[codigo][campo].append(texto)


# La ruta se calcula a partir de dónde está este script, no de la carpeta
# desde la que se ejecuta. Así funciona igual lo lances desde donde lo lances.
carpeta_del_script = Path(__file__).parent
raiz_del_proyecto = carpeta_del_script.parent
ruta_del_texto = raiz_del_proyecto / "sources" / "Texto refundido PGC 2021.md"
ruta_del_json = raiz_del_proyecto / "data" / "accounts.json"

# El fichero está guardado en UTF-8. Si no se dice, Windows usa otra tabla
# (cp1252) y las tildes y las eñes salen rotas o el programa falla.
texto = ruta_del_texto.read_text(encoding="utf-8")

lineas = texto.splitlines()
print("Fichero:", ruta_del_texto)
print("Líneas del texto original:", len(lineas))

# El orden importa: los espacios se recortan antes de juntar las líneas en
# blanco, para que una línea que solo tenía espacios cuente como blanca.
lineas = quitar_marcas_de_pagina(lineas)
lineas = quitar_espacios_al_final(lineas)
lineas = juntar_lineas_en_blanco(lineas)
print("Líneas después de limpiar:", len(lineas))

# Comprobación: en el texto original no hay ninguna llave que no sea de una
# marca de página, así que en el texto limpio no debería quedar ni una.
lineas_con_llave = 0
for linea in lineas:
    if "{" in linea:
        lineas_con_llave += 1
print("Líneas que aún tienen una llave {:", lineas_con_llave)

lineas_del_cuadro = recortar_cuarta_parte(lineas)
cuentas = extraer_cuadro_de_cuentas(lineas_del_cuadro)

lineas_de_las_fichas = recortar_quinta_parte(lineas)
extraer_fichas(lineas_de_las_fichas, cuentas)

# ensure_ascii=False deja las tildes como tildes; si no, "ó" se guardaría
# como "ó". indent=2 pone cada campo en su línea para poder leerlo.
texto_json = json.dumps(cuentas, ensure_ascii=False, indent=2)
ruta_del_json.write_text(texto_json, encoding="utf-8")

print()
print("Cuadro de cuentas guardado en:", ruta_del_json)
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
con_movimientos = 0
for cuenta in cuentas:
    if cuenta["nivel"] == "cuenta":
        cuentas_de_tres_cifras += 1
        if len(cuenta["definicion"]) > 0:
            con_definicion += 1
        if len(cuenta["cargos"]) > 0 or len(cuenta["abonos"]) > 0:
            con_movimientos += 1
print("De las", cuentas_de_tres_cifras, "cuentas de tres cifras:")
print("  con definición:", con_definicion)
print("  con movimientos en columnas:", con_movimientos)

print()
for cuenta in cuentas:
    if cuenta["codigo"] == "430":
        print("La 430 se llama:", cuenta["nombre"])
        print("  cargos:", len(cuenta["cargos"]))
        print("  abonos:", len(cuenta["abonos"]))
