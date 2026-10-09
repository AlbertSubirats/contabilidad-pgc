# Parser del texto refundido del PGC.
# Lee el fichero fuente, limpia la basura que dejó el OCR y extrae el cuadro
# de cuentas a data/accounts.json.

import json
import re
from pathlib import Path

# Una marca de página del OCR: una llave, un número, otra llave y una tira de
# guiones. Por ejemplo: {17}------------------------------------------------
PATRON_MARCA_DE_PAGINA = r"\{\d+\}-+"

# Un código de cuenta: de 2 a 5 cifras, un punto y un espacio. Por ejemplo
# "430. ". Los paréntesis forman un grupo de captura: guardan las cifras.
PATRON_CODIGO_DE_CUENTA = r"(\d{2,5})\. "

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

for cuenta in cuentas:
    if cuenta["codigo"] == "430":
        print("La 430 se llama:", cuenta["nombre"])
