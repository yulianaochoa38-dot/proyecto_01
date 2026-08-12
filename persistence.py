import json
import os
from logger import registrar_log
def guardar_datos(datos, nombre_archivo="usuarios.json"):
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        registrar_log(f"Error al guardar datos en {nombre_archivo}: {e}", "ERROR") 
        return False       

def cargar_datos(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as e:
        registrar_log(f"EL arcivo {nombre_archivo} contiene JSON invalido: {e}", "ERROR")
        return []   
    except Exception as e:
        registrar_log(f"Error al cargar datos {nombre_archivo}: {e}", "ERROR")
        return []

# import json: carga el modulo en formato json
# import os: para comprobar si los archivos existen
# indet=4 Formatea el archivo json con sangria de 4 espacios
# ensure_ascii=False:Conserva las tildes y otros caracteres en lugar de convertirlos a codigos Unicode(\u00f1).
# os.path.exists comprueba si el archivo existe.
# json.load lee el contenido en formato json
# linea 17-19 si hay algun error leyendo el archivo, lo registra en el archivo de logs y retorna un lista vacia             