# Compara, cuenta a cuenta, el JSON que sale del texto refundido del OCR
# (data/accounts.json, de parser.py) con el que sale del BOE
# (data/accounts_boe.json, de parser_boe.py). No arregla nada: clasifica las
# diferencias en grupos para revisarlas a mano (paso 1b·5).

import difflib
import json
from pathlib import Path

# Los apartados de la ficha que se comparan.
CAMPOS_DE_LA_FICHA = ["definicion", "presentacion", "cargos", "abonos"]

# Parecido entre dos textos, de 0 (nada que ver) a 1 (idénticos). Por encima
# de esta cifra, la diferencia son unas pocas palabras: un fallo del OCR o
# una errata del BOE, que se enseñan palabra a palabra.
PARECIDO_CASI_IGUAL = 0.95

# El OCR escribía comillas rectas ("factoring", ''Pasivos'') donde el BOE
# escribe «factoring» y ‘‘Pasivos’’. Para saber si el texto es el mismo, se
# quitan, igual que los espacios.
CARACTERES_QUE_NO_CUENTAN = [" ", '"', "'", "«", "»", "‘", "’", "“", "”"]


def cargar_cuentas(ruta):
    cuentas = json.loads(ruta.read_text(encoding="utf-8"))
    cuentas_por_codigo = {}
    for cuenta in cuentas:
        cuentas_por_codigo[cuenta["codigo"]] = cuenta
    return cuentas_por_codigo


def textos_del_campo(cuenta, campo):
    # En el JSON del OCR un movimiento es un texto, y en el del BOE, un
    # diccionario con su etiqueta. Para compararlos se saca solo el texto.
    # isinstance(elemento, dict) pregunta si el elemento es un diccionario.
    textos = []
    for elemento in cuenta[campo]:
        if isinstance(elemento, dict):
            textos.append(elemento["texto"])
        else:
            textos.append(elemento)
    return textos


def texto_completo(cuenta):
    # Todo el texto de la ficha seguido, sin importar en qué apartado esté.
    textos = []
    for campo in CAMPOS_DE_LA_FICHA:
        textos.extend(textos_del_campo(cuenta, campo))
    return " ".join(textos)


def sin_espacios_ni_comillas(texto):
    for caracter in CARACTERES_QUE_NO_CUENTAN:
        texto = texto.replace(caracter, "")
    return texto


def parecido(texto_ocr, texto_boe):
    # SequenceMatcher compara dos listas (aquí, de palabras) y ratio() da un
    # número de 0 a 1. El None dice que no se ignora ningún elemento, y
    # autojunk=False, que no se salte las palabras muy repetidas ("de",
    # "la"...), como hace por su cuenta con las listas largas para ir rápido.
    comparador = difflib.SequenceMatcher(None, texto_ocr.split(), texto_boe.split(), autojunk=False)
    return comparador.ratio()


def clasificar(cuenta_ocr, cuenta_boe):
    apartados_iguales = True
    for campo in CAMPOS_DE_LA_FICHA:
        if textos_del_campo(cuenta_ocr, campo) != textos_del_campo(cuenta_boe, campo):
            apartados_iguales = False
    if apartados_iguales:
        return "igual"

    texto_ocr = texto_completo(cuenta_ocr)
    texto_boe = texto_completo(cuenta_boe)
    if sin_espacios_ni_comillas(texto_ocr) == sin_espacios_ni_comillas(texto_boe):
        return "reparto"
    if texto_ocr == "":
        return "nueva"
    if texto_boe == "":
        return "desaparece"
    if parecido(texto_ocr, texto_boe) > PARECIDO_CASI_IGUAL:
        return "casi_igual"
    return "distinta"


def palabras_cambiadas(texto_ocr, texto_boe):
    # get_opcodes() da la receta para pasar de un texto al otro: una lista de
    # pasos de cinco valores, ("replace", 7, 8, 7, 8) = "sustituir las
    # palabras 7 a 8 del OCR por las 7 a 8 del BOE". Se enseña todo lo que no
    # es "equal": «registral» → «registra)». Si se ha añadido o borrado
    # algo, un lado queda vacío: «» → «Con carácter general...».
    palabras_ocr = texto_ocr.split()
    palabras_boe = texto_boe.split()
    comparador = difflib.SequenceMatcher(None, palabras_ocr, palabras_boe, autojunk=False)
    cambios = []
    for que_hacer, inicio_ocr, fin_ocr, inicio_boe, fin_boe in comparador.get_opcodes():
        if que_hacer == "equal":
            continue
        trozo_ocr = " ".join(palabras_ocr[inicio_ocr:fin_ocr])
        trozo_boe = " ".join(palabras_boe[inicio_boe:fin_boe])
        cambios.append("«" + trozo_ocr + "» → «" + trozo_boe + "»")
    return cambios


def parrafos_solo_en_uno(cuenta_ocr, cuenta_boe):
    # Para cada apartado, los párrafos que están en un lado y no en el otro.
    # Cada línea empieza por "OCR" o "BOE" y dice el apartado.
    lineas = []
    for campo in CAMPOS_DE_LA_FICHA:
        textos_ocr = textos_del_campo(cuenta_ocr, campo)
        textos_boe = textos_del_campo(cuenta_boe, campo)
        for texto in textos_ocr:
            if texto not in textos_boe:
                lineas.append("OCR · " + campo + ": " + texto[:110])
        for texto in textos_boe:
            if texto not in textos_ocr:
                lineas.append("BOE · " + campo + ": " + texto[:110])
    return lineas


carpeta_de_datos = Path(__file__).parent.parent / "data"
cuentas_ocr = cargar_cuentas(carpeta_de_datos / "accounts.json")
cuentas_boe = cargar_cuentas(carpeta_de_datos / "accounts_boe.json")

print("COMPARACIÓN DEL JSON DEL OCR CON EL DEL BOE")

codigos_comunes = []
for codigo in cuentas_boe:
    if codigo in cuentas_ocr:
        codigos_comunes.append(codigo)
    else:
        print("AVISO: la", codigo, "está en el BOE y no en el OCR")
for codigo in cuentas_ocr:
    if codigo not in cuentas_boe:
        print("AVISO: la", codigo, "está en el OCR y no en el BOE")

# Cada grupo es una lista de códigos.
grupos = {"igual": [], "reparto": [], "casi_igual": [], "nueva": [], "desaparece": [], "distinta": []}
nombres_distintos = []
for codigo in codigos_comunes:
    cuenta_ocr = cuentas_ocr[codigo]
    cuenta_boe = cuentas_boe[codigo]
    grupos[clasificar(cuenta_ocr, cuenta_boe)].append(codigo)
    if cuenta_ocr["nombre"] != cuenta_boe["nombre"]:
        nombres_distintos.append(codigo + " · OCR: " + cuenta_ocr["nombre"] + " · BOE: " + cuenta_boe["nombre"])

print()
print("Cuentas comparadas:", len(codigos_comunes))
print("  A. Ficha idéntica:", len(grupos["igual"]))
print("  B. Mismo texto, en otro apartado:", len(grupos["reparto"]))
print("  C. Casi igual (unas pocas palabras):", len(grupos["casi_igual"]))
print("  D. Ficha que el OCR no tenía:", len(grupos["nueva"]))
print("  E. Ficha que el BOE no tiene:", len(grupos["desaparece"]))
print("  F. Diferencias grandes:", len(grupos["distinta"]))
print("  Nombres distintos:", len(nombres_distintos))

print()
print("NOMBRES DISTINTOS")
for linea in nombres_distintos:
    print("  -", linea)

print()
print("B. MISMO TEXTO, EN OTRO APARTADO")
print("  " + ", ".join(grupos["reparto"]))

print()
print("C. CASI IGUAL: las palabras que cambian, del OCR al BOE")
for codigo in grupos["casi_igual"]:
    cambios = palabras_cambiadas(texto_completo(cuentas_ocr[codigo]), texto_completo(cuentas_boe[codigo]))
    print("  -", codigo, "·", " · ".join(cambios))

print()
print("D. FICHA QUE EL OCR NO TENÍA")
print("  " + ", ".join(grupos["nueva"]))

print()
print("E. FICHA QUE EL BOE NO TIENE: lo que tenía el OCR")
for codigo in grupos["desaparece"]:
    print("  -", codigo, "·", texto_completo(cuentas_ocr[codigo])[:110])

print()
print("F. DIFERENCIAS GRANDES: los párrafos que solo están en un lado")
for codigo in grupos["distinta"]:
    cuenta_ocr = cuentas_ocr[codigo]
    cuenta_boe = cuentas_boe[codigo]
    # round(numero, 2) redondea a dos decimales: 0.7412... → 0.74.
    cuanto_se_parecen = round(parecido(texto_completo(cuenta_ocr), texto_completo(cuenta_boe)), 2)
    print()
    print("  " + codigo + " · " + cuenta_boe["nombre"] + " · parecido " + str(cuanto_se_parecen))
    for linea in parrafos_solo_en_uno(cuenta_ocr, cuenta_boe):
        print("    " + linea)
