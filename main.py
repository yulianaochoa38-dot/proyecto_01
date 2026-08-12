import os
os.system('cls')

from usuarios import obtener_usuarios, crear_usuarios, buscar_usuario, actualizar_usuario, eliminar_usuario, guardar_usuarios, listar_usuarios
from prestamos import menu_prestamos, registrar_prestamo, mostrar_prestamos, menu_consultas_y_reportes
from gestion_herramientas import menu_herramientas, consultar_catalogo
from persistence import guardar_datos, cargar_datos

def precargar_datos_iniciales():
    #Asegura que existan los archivo JSON con estructuras base validas
    if not cargar_datos("usuarios.json"):
        guardar_datos([], "usuarios.json")
    if not cargar_datos("herramientas.json"):
        guardar_datos({}, "herramientas.json")
    if not cargar_datos("prestamos.json"):
        guardar_datos([], "prestamos.json")

  
def menu_administrador(user):
    while True:
        print("-----MENU ADMINISTRADOR------ ")
        print("1. Gestionar Usuarios")
        print("2. Gestionar Herramientas")
        print("3. Gestionar Prestamos")
        print("4. Consultas y Reportes")
        print("5. Cerrar Sesion")
        opcion = input("Seleccione una opcion del menu: ")

        if opcion == "1":
            print("-----GESTION DE USUARIOS-----")
            print("1. Crear 2. Listar 3. Buscar 4. Actualizar 5. Eliminar")
            sub = input("Opcion: ")
            if sub == "1":
                id_u = input("ID: ")
                nom = input("Nombres: ")
                ape = input("Apellidos: ")
                tel = input("Telefono: ")
                dir_u = input("Direccion: ")
                tipo = input("Tipo (administrador/residente): ")
                ok, msg = crear_usuarios(id_u, nom, ape, tel, dir_u, tipo)
                print(msg)

            elif sub == "2": 
                listar_usuarios()
            elif sub == "3":
                id_u = input("ID a buscar: ")
                print(buscar_usuario(id_u) or "No encontrado")
            elif sub == "4":
                id_u = input("Ingrese el ID del usuario a actualizar: ")
                print("Deje en blanco los campos de no desee cambiar: ")
                nom = input("Nuevo Nombre: ") or None
                ape = input("Nuevo Apellido: ") or None
                tel = input("Nuevo telefono: ") or None
                dir_u = input("Nueva dirrecion: ") or None
                tipo = input("Nuevo tipo (administrador/residente): ") or None
                ok, msg = actualizar_usuario(id_u, nom, ape, tel, dir_u, tipo)
                print(msg)
            elif sub == "5":
                id_u = input("Ingrese el ID del usuario a eliminar: ")   
                ok, msg = eliminar_usuario(id_u)
                print(msg)
        elif opcion == "2":
            menu_herramientas()       

        elif opcion == "3": 
            menu_prestamos() 

        elif opcion == "4":
            menu_consultas_y_reportes()

        elif opcion == "5":
            print("Cerrando sesion...")
            break
        else:
            print("Opcion invalida.") 


def menu_residente(user):
    while True:
        print("-----MENU RESIDENTE-----")
        print("1. Consultar Catalogo de Herramientas")
        print("2. Solicitar Prestamo")
        print("3. Ver Mis Prestamos")
        print("4. Cerrar Sesion")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            consultar_catalogo()
        if opcion == "2":
            menu_prestamos()
        if opcion == "3":
            id_u = user["id"] if isinstance(user, dict) else user
            mostrar_prestamos(id_u)
        elif opcion == "4":
            print("Cerrando sesion..")
            break
        else:
            print("Opcion invalida.")    

def main():
    precargar_datos_iniciales()

    while True:
        print("\n-----------------------------------")
        print(" SISTEMA DE COMUNIDAD - PRESTAMOS ")
        print("-----------------------------------")
        id_u = input("Ingrese su ID de usuario (o 'Salir'): ")
        if id_u.lower() == 'salir':
            print("¡Hasta Luego!")
            break
          
        usuario = buscar_usuario(id_u)
        if not usuario:
            print("Usuario no encontrado.")
            continue

        print(f"\nBienvenido/a {usuario ['nombres']} ({usuario['tipo'].upper()})")
        if str(usuario.get("tipo", "")).lower() == "administrador":
            menu_administrador(usuario)
        else:
            menu_residente(usuario) 
#Evalua si el archivo se esta ejecutando como programa principal.
if __name__ == "__main__":
    main()               

