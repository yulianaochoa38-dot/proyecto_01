from persistence import cargar_datos, guardar_datos
from logger import registrar_log

archivo_herramientas = "herramientas.json"
# REGISTRAR HERRAMIENTA
def registrar_herramienta():
    herramientas = cargar_datos(archivo_herramientas)

    # Verificar que sea un diccionario
    if not isinstance(herramientas, dict):
        herramientas = {}

    try:
        id_herramienta = input("ID de la herramienta: ").strip()

        # Verificar si el ID ya existe
        if id_herramienta in herramientas:
            print("El ID ya existe.")
            registrar_log(f"Intento fallido: el ID {id_herramienta} ya existe.","WARNING")
            return

        nombre = input("Nombre: ").strip()
        categoria = input("Categoría: ").strip()
        cantidad = int(input("Cantidad disponible: "))
        if cantidad < 0:
            print("La cantidad no puede ser negativa.")
            return
        estado = input("Estado (activa, en reparacion, fuera de servicio): ").strip().lower()
        estados_validos = ["activa","en reparacion","fuera de servicio"]
        if estado not in estados_validos:
            print("Estado inválido.")
            return
        valor = float(input("Valor estimado: "))
        if valor < 0:
            print("El valor no puede ser negativo.")
            return

        herramientas[id_herramienta] = {
            "id": id_herramienta,
            "nombre": nombre,
            "categoria": categoria,
            "cantidad": cantidad,
            "estado": estado,
            "valor": valor
        }
        guardar_datos(herramientas, archivo_herramientas)
        print("Herramienta registrada correctamente.")
        registrar_log(f"Herramienta registrada correctamente: {id_herramienta}","INFO")
    except ValueError:
        print("Error: debe ingresar números donde corresponda.")
        registrar_log("Error al registrar herramienta: dato inválido.","ERROR")

# LISTAR HERRAMIENTAS
def listar_herramientas():
    herramientas = cargar_datos(archivo_herramientas)
    if not herramientas:
        print("No hay herramientas registradas.")
        return
    print("\n------------ LISTA DE HERRAMIENTAS ------------")
    for id_herramienta, datos in herramientas.items():
        print("---------------------------------------")
        print("ID:", datos["id"])
        print("Nombre:", datos["nombre"])
        print("Categoría:", datos["categoria"])
        print("Cantidad:", datos["cantidad"])
        print("Estado:", datos["estado"])
        print("Valor:", datos["valor"])
    print("---------------------------------------")

# BUSCAR HERRAMIENTA
def buscar_herramienta():
    herramientas = cargar_datos(archivo_herramientas)
    id_herramienta = input("Ingrese el ID de la herramienta: ").strip()
    if id_herramienta in herramientas:
        datos = herramientas[id_herramienta]
        print("\n------------ HERRAMIENTA ------------")
        print("ID:", datos["id"])
        print("Nombre:", datos["nombre"])
        print("Categoría:", datos["categoria"])
        print("Cantidad:", datos["cantidad"])
        print("Estado:", datos["estado"])
        print("Valor:", datos["valor"])
    else:
        print("Herramienta no encontrada.")
        registrar_log(f"Herramienta no encontrada: {id_herramienta}","WARNING")

# ACTUALIZAR HERRAMIENTA
def actualizar_herramienta():
    herramientas = cargar_datos(archivo_herramientas)
    id_herramienta = input("ID de la herramienta: ").strip()
    if id_herramienta not in herramientas:
        print("La herramienta no existe.")
        return
    try:
        print("\nIngrese los nuevos datos:")
        nombre = input("Nuevo nombre: ").strip()
        categoria = input("Nueva categoría: ").strip()
        cantidad = int(input("Nueva cantidad: "))
        if cantidad < 0:
            print("La cantidad no puede ser negativa.")
            return
        estado = input("Nuevo estado ""(activa, en reparacion, fuera de servicio): ").strip().lower()
        estados_validos = ["activa","en reparacion","fuera de servicio"]
        if estado not in estados_validos:
            print("Estado inválido.")
            return
        valor = float(input("Nuevo valor: "))
        if valor < 0:
            print("El valor no puede ser negativo.")
            return

        herramientas[id_herramienta]["nombre"] = nombre
        herramientas[id_herramienta]["categoria"] = categoria
        herramientas[id_herramienta]["cantidad"] = cantidad
        herramientas[id_herramienta]["estado"] = estado
        herramientas[id_herramienta]["valor"] = valor

        guardar_datos(
            herramientas,
            archivo_herramientas
        )
        print("Herramienta actualizada correctamente.")
        registrar_log(f"Herramienta actualizada: {id_herramienta}","INFO")
    except ValueError:
        print("Dato inválido.")
        registrar_log(f"Error al actualizar herramienta {id_herramienta}.","ERROR")

# ELIMINAR / INACTIVAR HERRAMIENTA
def eliminar_herramienta():
    herramientas = cargar_datos(archivo_herramientas)
    id_herramienta = input("ID de la herramienta: ").strip()
    if id_herramienta not in herramientas:
        print("La herramienta no existe.")
        return
    # Eliminación lógica:
    # La herramienta permanece registrada,
    # pero pasa a estado inactiva.
    herramientas[id_herramienta]["estado"] = "inactiva"
    guardar_datos(herramientas,archivo_herramientas)
    print("Herramienta inactivada correctamente.")
    registrar_log(f"Herramienta inactivada: {id_herramienta}","INFO")

# MENÚ PRINCIPAL
def menu_herramientas():

    opcion = 0

    while opcion != 6:

        print("\n======================================")
        print("       SISTEMA DE HERRAMIENTAS")
        print("======================================")
        print("1. Registrar herramienta")
        print("2. Listar herramientas")
        print("3. Buscar herramienta")
        print("4. Actualizar herramienta")
        print("5. Eliminar/Inactivar herramienta")
        print("6. Salir")
        print("======================================")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                registrar_herramienta()
            elif opcion == 2:
                listar_herramientas()
            elif opcion == 3:
                buscar_herramienta()
            elif opcion == 4:
                actualizar_herramienta()
            elif opcion == 5:
                eliminar_herramienta()
            elif opcion == 6:
                print("Gracias por usar el sistema de herramientas.")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Error: debe ingresar un número entero.")

# EJECUTAR PROGRAMA
if __name__ == "__main__":
    menu_herramientas()
