# Verificador del cuadro de cuentas que saca parser.py del BOE.
# No arregla nada: comprueba lo que tiene que ser verdad si el cuadro está
# completo, y cruza el cuadro con otras partes del mismo BOE que también
# nombran cuentas. Si una parte se equivoca, las otras lo delatan.

import re

from boe_reader import cargar_raiz, version_vigente, parrafos_del_bloque, texto_del_elemento
from parser import extraer_cuadro_de_cuentas, NUMEROS_DE_GRUPO, CUENTAS_QUE_FALTAN

# Los modelos de cuentas anuales (tercera parte) citan las cuentas entre
# paréntesis: "(6654), (6655)". El estado de flujos no cita ninguna.
BLOQUES_DE_MODELOS = [
    "balance",
    "cuenta",
    "estadodecambios",
    "balanceabreviado-2",
    "cuentaabreviada",
    "estadoabreviado",
]


def imprimir_apartado(titulo, problemas):
    # Copiada de verify.py, que ejecuta todo su informe al importarlo.
    print()
    print(titulo, "(" + str(len(problemas)) + ")")
    if len(problemas) == 0:
        print("  Nada que revisar.")
    for problema in problemas:
        print("  -", problema)


def codigos_de_las_tablas_que_faltan(raiz, codigos_existentes):
    # Lee el XML por otro camino que el parser: no recorre filas y celdas,
    # sino todos los párrafos del bloque, y se queda con los que son solo un
    # código y su punto ("400."). Si el parser se saltara filas, como pasó
    # con las tablas que llevan <tbody>, este camino sí las vería.
    problemas = []
    for numero in NUMEROS_DE_GRUPO:
        version = version_vigente(raiz, "grupo" + numero)
        for parrafo in version.iter("p"):
            texto = texto_del_elemento(parrafo)
            if re.fullmatch(r"\d{2,5}\.", texto):
                codigo = texto.rstrip(".")
                if codigo not in codigos_existentes:
                    problemas.append("la " + codigo + " está en la tabla del grupo " + numero + " y no en el cuadro")
    return problemas


def grupos_y_subgrupos_vacios(cuentas):
    # Cuántos hijos tiene cada código: {"43": 9, "430": 6, ...}.
    hijos_por_padre = {}
    for cuenta in cuentas:
        padre = cuenta["padre"]
        if padre in hijos_por_padre:
            hijos_por_padre[padre] += 1
        else:
            hijos_por_padre[padre] = 1

    problemas = []
    for cuenta in cuentas:
        if cuenta["nivel"] in ["grupo", "subgrupo"] and cuenta["codigo"] not in hijos_por_padre:
            problemas.append("el " + cuenta["nivel"] + " " + cuenta["codigo"] + " no tiene ninguna cuenta")
    return problemas


def codigos_repetidos_o_sin_padre(cuentas, codigos_existentes):
    problemas = []
    codigos_vistos = set()
    for cuenta in cuentas:
        codigo = cuenta["codigo"]
        if codigo in codigos_vistos:
            problemas.append("la " + codigo + " está repetida")
        codigos_vistos.add(codigo)

        padre = cuenta["padre"]
        if padre is not None and padre not in codigos_existentes:
            problemas.append("la " + codigo + " cuelga de la " + padre + ", que no está en el cuadro")
    return problemas


def fichas_sin_cuenta_en_el_cuadro(raiz, codigos_existentes):
    # Los títulos de las fichas de la quinta parte: "430. Clientes" o, si la
    # ficha es de varias cuentas, "600/601/602/607. Compras de...".
    problemas = []
    for numero in NUMEROS_DE_GRUPO:
        for parrafo in parrafos_del_bloque(raiz, "grupo" + numero + "-2"):
            coincidencia = re.match(r"(\d{2,5}(/\d{2,5})*)\. ", parrafo)
            if coincidencia is None:
                continue
            for codigo in coincidencia.group(1).split("/"):
                if codigo not in codigos_existentes:
                    problemas.append("la " + codigo + " tiene ficha y no está en el cuadro: " + parrafo[:70])
    return problemas


def codigos_de_los_modelos_sin_cuenta(raiz, codigos_existentes):
    # Los modelos citan las cuentas entre paréntesis: "(6654), (6655)".
    # En el patrón, \( y \) son los paréntesis del texto; los de en medio,
    # sin barra, son el grupo de captura que se queda con las cifras.
    problemas = []
    for id_del_bloque in BLOQUES_DE_MODELOS:
        version = version_vigente(raiz, id_del_bloque)
        for parrafo in version.iter("p"):
            for codigo in re.findall(r"\((\d{2,5})\)", texto_del_elemento(parrafo)):
                if codigo not in codigos_existentes:
                    problemas.append("la " + codigo + " sale en el bloque " + id_del_bloque + " y no está en el cuadro")
    return problemas


def nombres_distintos_en_la_ficha(raiz, cuentas):
    # No es un error: la ley a veces escribe el nombre de dos maneras ("Beneficio
    # transferido (gestor)" en el cuadro, "Beneficio transferido" en la
    # ficha). Se listan para revisarlos, y así se vería también un nombre
    # cambiado de sitio, como los de la 500 y la 501.
    nombre_por_codigo = {}
    for cuenta in cuentas:
        nombre_por_codigo[cuenta["codigo"]] = cuenta["nombre"]

    problemas = []
    for numero in NUMEROS_DE_GRUPO:
        for parrafo in parrafos_del_bloque(raiz, "grupo" + numero + "-2"):
            coincidencia = re.fullmatch(r"(\d{2,5})\. (.+)", parrafo)
            if coincidencia is None:
                continue
            codigo = coincidencia.group(1)
            nombre_en_la_ficha = coincidencia.group(2).rstrip(".")
            if codigo not in nombre_por_codigo:
                continue
            if nombre_en_la_ficha != nombre_por_codigo[codigo]:
                problemas.append(codigo + " · cuadro: " + nombre_por_codigo[codigo] + " · ficha: " + nombre_en_la_ficha)
    return problemas


raiz = cargar_raiz()
cuentas = extraer_cuadro_de_cuentas(raiz)

codigos_existentes = set()
for cuenta in cuentas:
    codigos_existentes.add(cuenta["codigo"])

print("INFORME DE VERIFICACIÓN DEL CUADRO DE CUENTAS DEL BOE")
print()
print("Cuentas en el cuadro:", len(cuentas), "- de ellas, añadidas por la fe de erratas:", len(CUENTAS_QUE_FALTAN))

imprimir_apartado("1. Códigos de las tablas que no están en el cuadro",
                  codigos_de_las_tablas_que_faltan(raiz, codigos_existentes))
imprimir_apartado("2. Grupos y subgrupos sin ninguna cuenta",
                  grupos_y_subgrupos_vacios(cuentas))
imprimir_apartado("3. Códigos repetidos o que cuelgan de una cuenta que no existe",
                  codigos_repetidos_o_sin_padre(cuentas, codigos_existentes))
imprimir_apartado("4. Fichas de la quinta parte sin cuenta en el cuadro",
                  fichas_sin_cuenta_en_el_cuadro(raiz, codigos_existentes))
imprimir_apartado("5. Códigos citados en los modelos de cuentas anuales que no están en el cuadro",
                  codigos_de_los_modelos_sin_cuenta(raiz, codigos_existentes))
imprimir_apartado("6. Nombres que la ficha escribe distinto (para revisar, no son errores)",
                  nombres_distintos_en_la_ficha(raiz, cuentas))
