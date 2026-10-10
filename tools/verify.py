# Verificador de data/accounts.json.
# No arregla nada: lee el fichero que genera parser.py y avisa de lo que
# parece mal, para revisarlo a mano contra el texto original.

import json
import re
from pathlib import Path


def fragmento_alrededor(texto, numero):
    # Devuelve el trozo de texto que rodea a un número, para poder ver en qué
    # frase aparece sin imprimir un movimiento entero de 600 caracteres.
    # \b es un "límite de palabra": así, buscando el 2, no encaja el 2 de "242".
    coincidencia = re.search(r"\b" + numero + r"\b", texto)
    if coincidencia is None:
        return texto[:80]
    # .start() es la posición donde empieza el número dentro del texto.
    # max(0, ...) evita una posición negativa si el número está al principio.
    inicio = max(0, coincidencia.start() - 50)
    fin = coincidencia.start() + 30
    return "..." + texto[inicio:fin] + "..."


def contar_por_nivel(cuentas):
    contador = {"grupo": 0, "subgrupo": 0, "cuenta": 0, "subcuenta": 0}
    for cuenta in cuentas:
        contador[cuenta["nivel"]] += 1
    return contador


def cuentas_sin_ficha(cuentas):
    # Cuentas de tres cifras que no tienen nada: ni definición, ni
    # presentación, ni movimientos. Unas no tienen ficha propia en el PGC
    # (se explican en su subgrupo) y otras son fallos del parser: hay que
    # mirarlas una a una.
    codigos = []
    for cuenta in cuentas:
        if cuenta["nivel"] != "cuenta":
            continue
        tiene_algo = (
            len(cuenta["definicion"]) > 0
            or len(cuenta["presentacion"]) > 0
            or len(cuenta["cargos"]) > 0
            or len(cuenta["abonos"]) > 0
        )
        if not tiene_algo:
            codigos.append(cuenta["codigo"])
    return codigos


def numeros_que_no_son_cuentas(cuentas, codigos_existentes):
    # Los números de los movimientos que el filtro del paso 9 dejó fuera.
    # Si un número no es ninguna cuenta, o es basura del OCR o es un código
    # que el parser leyó mal.
    problemas = []
    for cuenta in cuentas:
        for columna in ["cargos", "abonos"]:
            for movimiento in cuenta[columna]:
                for numero in re.findall(r"\d+", movimiento):
                    if numero not in codigos_existentes:
                        problemas.append(
                            cuenta["codigo"] + " · " + columna + " · el " + numero + ": "
                            + fragmento_alrededor(movimiento, numero)
                        )
    return problemas


def contrapartidas_de_una_cifra(cuentas):
    # Una contrapartida de una cifra es un grupo entero. A veces es cierto
    # ("los grupos 6 y 7"), pero a menudo sale de un "apartado 2" o de una
    # numeración, y la regla del paso 9 lo toma por un grupo.
    problemas = []
    for cuenta in cuentas:
        for columna in ["cargos", "abonos"]:
            for codigo in cuenta["contrapartidas_" + columna]:
                if len(codigo) != 1:
                    continue
                # Se busca en qué movimiento aparece, para poder juzgarlo.
                for movimiento in cuenta[columna]:
                    if codigo in re.findall(r"\d+", movimiento):
                        problemas.append(
                            cuenta["codigo"] + " · " + columna + " · grupo " + codigo + ": "
                            + fragmento_alrededor(movimiento, codigo)
                        )
                        # Con enseñar el primer movimiento donde sale, basta.
                        break
    return problemas


def textos_sospechosos(cuentas):
    problemas = []
    for cuenta in cuentas:
        codigo = cuenta["codigo"]

        # En el PGC, los nombres de grupos y subgrupos van en mayúsculas. Si
        # no, es que se le ha pegado algo.
        if cuenta["nivel"] in ["grupo", "subgrupo"] and not cuenta["nombre"].isupper():
            problemas.append(codigo + " · nombre: " + cuenta["nombre"])

        for campo in ["definicion", "presentacion", "cargos", "abonos"]:
            for texto in cuenta[campo]:
                inicio = codigo + " · " + campo + ": " + texto[:70]

                # Un texto que empieza por un número suele ser un número de
                # página o un código que se ha colado. A veces es una
                # numeración de verdad ("1. Cuando..."): por eso se revisa a mano.
                if texto[0].isdigit():
                    problemas.append(inicio)
                # Restos del formato del OCR.
                elif "<sup>" in texto or "**" in texto or "#" in texto or "{" in texto:
                    problemas.append(inicio)
                # Un movimiento que lleva dentro "Se cargará:" o "Se abonará:"
                # tiene pegadas las dos columnas.
                elif campo in ["cargos", "abonos"] and re.search(r"Se (cargar|abonar)án?[:,]", texto):
                    problemas.append(inicio)
    return problemas


def subgrupos_fuera_de_orden(cuentas):
    # Dentro de cada grupo, los subgrupos deberían ir en orden: 10, 11, 12...
    # Se recuerda el último subgrupo visto de cada grupo y se compara.
    problemas = []
    ultimo_subgrupo_del_grupo = {}
    for cuenta in cuentas:
        if cuenta["nivel"] != "subgrupo":
            continue
        grupo = cuenta["padre"]
        if grupo in ultimo_subgrupo_del_grupo:
            anterior = ultimo_subgrupo_del_grupo[grupo]
            if cuenta["codigo"] < anterior:
                problemas.append("el " + cuenta["codigo"] + " aparece después del " + anterior)
        ultimo_subgrupo_del_grupo[grupo] = cuenta["codigo"]
    return problemas


def imprimir_apartado(titulo, problemas):
    print()
    print(titulo, "(" + str(len(problemas)) + ")")
    if len(problemas) == 0:
        print("  Nada que revisar.")
    for problema in problemas:
        print("  -", problema)


carpeta_del_script = Path(__file__).parent
ruta_del_json = carpeta_del_script.parent / "data" / "accounts.json"

# json.loads hace el camino inverso de json.dumps: del texto del fichero
# vuelve a la lista de diccionarios.
cuentas = json.loads(ruta_del_json.read_text(encoding="utf-8"))

codigos_existentes = set()
for cuenta in cuentas:
    codigos_existentes.add(cuenta["codigo"])

print("INFORME DE VERIFICACIÓN DE", ruta_del_json)

# 1. Resumen
print()
print("1. Resumen")
por_nivel = contar_por_nivel(cuentas)
print("  Grupos:", por_nivel["grupo"])
print("  Subgrupos:", por_nivel["subgrupo"])
print("  Cuentas:", por_nivel["cuenta"])
print("  Subcuentas:", por_nivel["subcuenta"])
con_definicion = 0
con_movimientos = 0
for cuenta in cuentas:
    if cuenta["nivel"] == "cuenta":
        if len(cuenta["definicion"]) > 0:
            con_definicion += 1
        if len(cuenta["cargos"]) > 0 or len(cuenta["abonos"]) > 0:
            con_movimientos += 1
print("  Cuentas de tres cifras con definición:", con_definicion, "de", por_nivel["cuenta"])
print("  Cuentas de tres cifras con movimientos:", con_movimientos, "de", por_nivel["cuenta"])

# 2. Cuentas sin ficha. Son muchas y cortas: se imprimen en un párrafo.
sin_ficha = cuentas_sin_ficha(cuentas)
print()
print("2. Cuentas de tres cifras sin ninguna ficha", "(" + str(len(sin_ficha)) + ")")
print("  " + ", ".join(sin_ficha))

# 3 a 6. El resto, un problema por línea.
imprimir_apartado("3. Números de los movimientos que no son ninguna cuenta",
                  numeros_que_no_son_cuentas(cuentas, codigos_existentes))
imprimir_apartado("4. Contrapartidas de una sola cifra (un grupo entero)",
                  contrapartidas_de_una_cifra(cuentas))
imprimir_apartado("5. Textos sospechosos", textos_sospechosos(cuentas))
imprimir_apartado("6. Subgrupos fuera de orden", subgrupos_fuera_de_orden(cuentas))
