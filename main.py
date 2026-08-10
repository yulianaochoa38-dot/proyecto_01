from usuarios import obtener_usuarios, crear_usuarios, buscar_usuario, actualizar_usuario, eliminar_usuario, guardar_usuarios


#def precargar_datos_iniciales():
#    if not obtener_usuarios():
#        crear_usuarios("101", "pablo", "martinez", "3003505540", "Calle 27 #17", "administrados")
#        crear_usuarios("102", "juan", "lopez", "3108765444", "Carrera 15 #41-13", "residente")

def menu_administrador(user):
    while True:
        print("-----MENU ADMINISTRADOR------ ")
        print("1. Gestionar Usuarios")
        print("2. Gestionar Herramientas")
        print("3. Aprobar / Rechazar Prestamos")
        print("4. Registrar Devolucion")
        print("5. Consultas y Reportes")
        print("6. Cerrar Sesion")
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
                for u in obtener_usuarios():
                    print(u)
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

                          
        if opcion == "6":
            break        


def menu_residente(user):
    while True:
        print("-----MENU RESIDENTE-----")
        print("1. Consultar Catalogo de Herramientas")
        print("2. Solicitar Prestamo")
        print("3. Ver Mis Prestamos")
        print("4. Cerrar Sesion")
        opcion = input("Seleccione una opcion: ")


#def main():
    #precargar_datos_iniciales()
    #while True:
        #print("-----------------------------------")
        #print(" SISTEMA DE COMUNIDAD - PRESTAMOS ")
        #print("-----------------------------------")
        #id_u = input("Ingrese su ID de usuario (o 'Salir'): ")
        #if id_u.lower() == 'salir':
        #    break
          
        #usuario = buscar_usuario(id_u)
        #if not usuario:
        #    print("Usuario no encontrado.")
        #    continue

        #print(f"Bienvenido/a {usuario['nombres']} ({usuario['tipo'].upper()})")
        #if usuario("tipo") == "administrador":
            #menu_administrador(usuario)
        #else:
            #menu_residente(usuario) 
#Evalua si el archivo se esta ejecutando como programa principal.
#if __name__ == "__main__":
#    main()               

