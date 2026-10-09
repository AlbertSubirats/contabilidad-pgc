# Parser del texto refundido del PGC.
# Lee el fichero fuente y limpia la basura que dejó el OCR.

import re
from pathlib import Path

# Una marca de página del OCR: una llave, un número, otra llave y una tira de
# guiones. Por ejemplo: {17}------------------------------------------------
PATRON_MARCA_DE_PAGINA = r"\{\d+\}-+"


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


# La ruta se calcula a partir de dónde está este script, no de la carpeta
# desde la que se ejecuta. Así funciona igual lo lances desde donde lo lances.
carpeta_del_script = Path(__file__).parent
raiz_del_proyecto = carpeta_del_script.parent
ruta_del_texto = raiz_del_proyecto / "sources" / "Texto refundido PGC 2021.md"

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
