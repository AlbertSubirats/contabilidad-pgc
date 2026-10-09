# Parser del texto refundido del PGC.
# De momento solo abre el fichero fuente y cuenta sus líneas.

from pathlib import Path

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
print("Número de líneas:", len(lineas))
