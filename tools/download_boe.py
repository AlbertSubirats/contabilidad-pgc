# Descarga del BOE el texto consolidado del PGC y lo guarda tal cual en
# sources/boe/. El parser trabaja siempre sobre esta copia, nunca sobre
# internet. Se ejecuta solo cuando se decide actualizar (CLAUDE.md, sección 7).

import urllib.request
from pathlib import Path

# La API de datos abiertos del BOE. BOE-A-2007-19884 es el identificador del
# Real Decreto 1514/2007, el que aprueba el PGC.
URL_BASE = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2007-19884"
URL_DEL_INDICE = URL_BASE + "/texto/indice"
URL_DEL_TEXTO = URL_BASE + "/texto"


def descargar(url, ruta_destino):
    # La cabecera Accept le dice a la API en qué formato queremos la
    # respuesta. Sin ella, la API contesta con un error 400.
    peticion = urllib.request.Request(url, headers={"Accept": "application/xml"})

    # timeout: si en 60 segundos no llega respuesta, se da por fallida en vez
    # de esperar para siempre.
    with urllib.request.urlopen(peticion, timeout=60) as respuesta:
        contenido = respuesta.read()

    # Se guardan los bytes tal como llegan, sin convertirlos en texto: así la
    # copia es idéntica, byte a byte, a lo que envió el BOE.
    ruta_destino.write_bytes(contenido)
    return len(contenido)


carpeta_del_script = Path(__file__).parent
raiz_del_proyecto = carpeta_del_script.parent
carpeta_boe = raiz_del_proyecto / "sources" / "boe"

# parents=True crea también las carpetas de por medio si faltan, y
# exist_ok=True evita el error si la carpeta ya existe (la segunda vez).
carpeta_boe.mkdir(parents=True, exist_ok=True)

ruta_del_indice = carpeta_boe / "indice.xml"
bytes_del_indice = descargar(URL_DEL_INDICE, ruta_del_indice)
print("Índice guardado en:", ruta_del_indice, "-", bytes_del_indice, "bytes")

ruta_del_texto = carpeta_boe / "texto.xml"
bytes_del_texto = descargar(URL_DEL_TEXTO, ruta_del_texto)
print("Texto guardado en:", ruta_del_texto, "-", bytes_del_texto, "bytes")

# Recordatorio de los pasos siguientes del proceso de actualización.
print()
print("Siguiente: revisa qué ha cambiado con 'git diff sources/',")
print("vuelve a ejecutar el parser y el verificador, y haz el commit.")