from datetime import datetime
from persistence import cargar_datos, guardar_datos
from logger import registrar_log

archivo_prestamos = "prestamos.json"
archivo_herramientas = "herramientas.json"
archivo_usuarios = "usuarios.json"


def obtener_prestamos():
    prestamos = cargar_datos(archivo_prestamos)
    if not isinstance(prestamos, list):
        return []
    return prestamos


def registrar_prestamo(usuario_actual=None):
    prestamos = obtener_prestamos()
    herramientas = cargar_datos(archivo_herramientas)
    usuarios = cargar_datos(archivo_usuarios)

    if not isinstance(herramientas, dict):
        herramientas = {}

    print("\n--- REGISTRAR PRÉSTAMO ---")
    if usuario_actual and "id" in usuario_actual:
        id_usuario = usuario_actual["id"]
        print(f"Usuario solicitante: {usuario_actual.get('nombres', '')} {usuario_actual.get('apellidos', '')} (ID: {id_usuario})")
    else:
        id_usuario = input("ID del usuario que solicita el préstamo: ").strip()
        usuario_existe = any(u.get("id") == id_usuario for u in usuarios) if isinstance(usuarios, list) else False
        if not usuario_existe:
            print("Error: El usuario no existe.")
            registrar_log(f"Intento fallido de préstamo: Usuario {id_usuario} no existe.", "WARNING")
            return

    id_herramienta = input("ID de la herramienta a solicitar: ").strip()

    if id_herramienta not in herramientas:
        print("Error: La herramienta no existe.")
        registrar_log(f"Intento fallido de préstamo: Herramienta {id_herramienta} no existe.", "WARNING")
        return

    herramienta = herramientas[id_herramienta]

    if herramienta.get("estado") != "activa":
        print(f"Error: La herramienta no está disponible/activa (Estado: {herramienta.get('estado')}).")
        return

    try:
        cantidad = int(input(f"Cantidad a solicitar (Disponible: {herramienta['cantidad']}): "))
        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor a 0.")
            return

        if herramienta["cantidad"] < cantidad:
            print("Error: No hay suficiente stock disponible.")
            registrar_log(f"Stock insuficiente para herramienta {id_herramienta}.", "WARNING")
            return

        fecha_inicio = input("Fecha de inicio (YYYY-MM-DD) [Dejar vacío para hoy]: ").strip()
        if not fecha_inicio:
            fecha_inicio = datetime.now().strftime("%Y-%m-%d")

        fecha_devolucion = input("Fecha estimada de devolución (YYYY-MM-DD): ").strip()
        observaciones = input("Observaciones: ").strip()

        id_prestamo = len(prestamos) + 1

        nuevo_prestamo = {
            "id": id_prestamo,
            "usuario_id": id_usuario,
            "herramienta_id": id_herramienta,
            "herramienta_nombre": herramienta["nombre"],
            "cantidad": cantidad,
            "fecha_inicio": fecha_inicio,
            "fecha_devolucion": fecha_devolucion,
            "estado": "Prestado",
            "observaciones": observaciones
        }

        # Descontar stock
        herramientas[id_herramienta]["cantidad"] -= cantidad

        # Guardar en JSON
        prestamos.append(nuevo_prestamo)
        guardar_datos(prestamos, archivo_prestamos)
        guardar_datos(herramientas, archivo_herramientas)

        print(f"\nPréstamo #{id_prestamo} registrado correctamente.")
        registrar_log(f"Préstamo registrado #{id_prestamo} a usuario {id_usuario}.", "INFO")

    except ValueError:
        print("Error: Debe ingresar una cantidad numérica válida.")
        registrar_log("Error al registrar préstamo: dato inválido.", "ERROR")


def mostrar_prestamos(id_usuario=None):
    prestamos = obtener_prestamos()
    
    # Filtrar préstamos si se especifica un usuario (para la vista residente)
    if id_usuario:
        prestamos = [p for p in prestamos if str(p.get("usuario_id")) == str(id_usuario)]

    if not prestamos:
        print("\nNo existen préstamos registrados.")
        return

    print("\n------------ LISTA DE PRÉSTAMOS ------------")
    for p in prestamos:
        print("---------------------------------------")
        print(f"ID Préstamo: {p['id']}")
        print(f"ID Usuario: {p['usuario_id']}")
        print(f"Herramienta: {p['herramienta_nombre']} (ID: {p['herramienta_id']})")
        print(f"Cantidad: {p['cantidad']}")
        print(f"Fecha Inicio: {p['fecha_inicio']}")
        print(f"Fecha Est. Devolución: {p['fecha_devolucion']}")
        print(f"Estado: {p['estado']}")
        print(f"Observaciones: {p['observaciones']}")
    print("---------------------------------------")


def devolver_herramienta():
    prestamos = obtener_prestamos()
    herramientas = cargar_datos(archivo_herramientas)

    if not prestamos:
        print("\nNo hay préstamos pendientes.")
        return

    try:
        id_buscar = int(input("Ingrese ID del préstamo a devolver: "))
        prestamo_encontrado = None

        for p in prestamos:
            if p["id"] == id_buscar:
                prestamo_encontrado = p
                break

        if not prestamo_encontrado:
            print("Error: Préstamo no encontrado.")
            return

        if prestamo_encontrado["estado"] == "Devuelto":
            print("Este préstamo ya fue devuelto.")
            return

        # Cambiar estado a devuelto
        prestamo_encontrado["estado"] = "Devuelto"

        # Restaurar la cantidad prestada al stock
        id_herramienta = prestamo_encontrado["herramienta_id"]
        if id_herramienta in herramientas:
            herramientas[id_herramienta]["cantidad"] += prestamo_encontrado["cantidad"]

        guardar_datos(prestamos, archivo_prestamos)
        guardar_datos(herramientas, archivo_herramientas)

        print("\nHerramienta devuelta y stock actualizado.")
        registrar_log(f"Devolución registrada para préstamo #{id_buscar}.", "INFO")

    except ValueError:
        print("Error: Ingrese un ID numérico válido.")


def reporte_stock_bajo():
    herramientas = cargar_datos(archivo_herramientas)
    if not isinstance(herramientas, dict) or not herramientas:
        print("\nNo hay herramientas en el sistema.")
        return

    limite = 3
    print(f"\n--- HERRAMIENTAS CON STOCK BAJO (Menos de {limite} unidades) ---")
    encontradas = False
    for id_h, h in herramientas.items():
        if h.get("cantidad", 0) < limite:
            print(f"- ID: {id_h} | Nombre: {h.get('nombre')} | Stock Actual: {h.get('cantidad')} | Estado: {h.get('estado')}")
            encontradas = True

    if not encontradas:
        print("No hay herramientas con stock bajo.")


def reporte_prestamos_activos_y_vencidos():
    prestamos = obtener_prestamos()
    if not prestamos:
        print("\nNo hay préstamos registrados.")
        return

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"\n--- REPORTES DE PRÉSTAMOS (Fecha Actual: {fecha_hoy}) ---")

    prestamos_activos = []
    prestamos_vencidos = []

    for p in prestamos:
        if p.get("estado") == "Prestado":
            fecha_dev = p.get("fecha_devolucion", "")
            if fecha_dev and fecha_dev < fecha_hoy:
                prestamos_vencidos.append(p)
            else:
                prestamos_activos.append(p)

    print("\n>> PRÉSTAMOS ACTIVOS (A tiempo):")
    if prestamos_activos:
        for p in prestamos_activos:
            print(f"   [ID #{p['id']}] Usuario: {p['usuario_id']} | Herramienta: {p['herramienta_nombre']} | Devolución: {p['fecha_devolucion']}")
    else:
        print("   Ninguno.")

    print("\n>> PRÉSTAMOS VENCIDOS:")
    if prestamos_vencidos:
        for p in prestamos_vencidos:
            print(f"   [ID #{p['id']}] Usuario: {p['usuario_id']} | Herramienta: {p['herramienta_nombre']} | Debía devolver: {p['fecha_devolucion']} (¡VENCIDO!)")
    else:
        print("   Ninguno.")


def reporte_historial_usuario():
    id_usuario = input("\nIngrese el ID del usuario a consultar: ").strip()
    mostrar_prestamos(id_usuario)


def reporte_herramientas_mas_solicitadas():
    prestamos = obtener_prestamos()
    if not prestamos:
        print("\nNo hay registro de préstamos para calcular solicitudes.")
        return

    conteo = {}
    for p in prestamos:
        nombre = p.get("herramienta_nombre", "Desconocida")
        cantidad = p.get("cantidad", 1)
        conteo[nombre] = conteo.get(nombre, 0) + cantidad

    # Ordenar de mayor a menor
    ordenadas = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    print("\n--- HERRAMIENTAS MÁS SOLICITADAS ---")
    for pos, (herramienta, total) in enumerate(ordenadas, 1):
        print(f"{pos}. {herramienta}: {total} unidad(es) prestada(s)")


def reporte_usuarios_mas_solicitantes():
    prestamos = obtener_prestamos()
    if not prestamos:
        print("\nNo hay registro de préstamos para calcular usuarios.")
        return

    conteo = {}
    for p in prestamos:
        u_id = p.get("usuario_id", "Desconocido")
        conteo[u_id] = conteo.get(u_id, 0) + 1

    ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    print("\n--- USUARIOS CON MÁS SOLICITUDES DE PRÉSTAMOS ---")
    for pos, (u_id, total) in enumerate(ordenados, 1):
        print(f"{pos}. Usuario ID {u_id}: {total} préstamo(s) solicitado(s)")


def menu_consultas_y_reportes():
    opcion = "0"
    while opcion != "6":
        print("\n======================================")
        print("        CONSULTAS Y REPORTES")
        print("======================================")
        print("1. Herramientas con stock bajo (< 3)")
        print("2. Préstamos activos y vencidos")
        print("3. Historial de préstamos de un usuario")
        print("4. Herramientas más solicitadas")
        print("5. Usuarios que más solicitan")
        print("6. Volver")
        print("======================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            reporte_stock_bajo()
        elif opcion == "2":
            reporte_prestamos_activos_y_vencidos()
        elif opcion == "3":
            reporte_historial_usuario()
        elif opcion == "4":
            reporte_herramientas_mas_solicitadas()
        elif opcion == "5":
            reporte_usuarios_mas_solicitantes()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


def menu_prestamos(usuario_actual=None):
    
    opcion = "0"
    while opcion != "4":
        print("\n======================================")
        print("       GESTIÓN DE PRÉSTAMOS")
        print("======================================")
        print("1. Registrar préstamo")
        print("2. Consultar préstamos")
        print("3. Registrar devolución")
        print("4. Volver")
        print("======================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_prestamo(usuario_actual)
        elif opcion == "2":
            mostrar_prestamos()
        elif opcion == "3":
            devolver_herramienta()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")