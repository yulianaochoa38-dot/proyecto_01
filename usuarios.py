from persistence import cargar_datos, guardar_datos
from logger import registrar_log
archivo_usuarios = "usuarios.json" #Define la variable con el nombre del archivo JSON donde se almacenara la lista de usuarios

def obtener_usuarios():  #para recupperar el listado de usuarios
    usuarios = cargar_datos(archivo_usuarios) #retorna la lissta de usuarios cargada
    #Si el archivo esta vacio o no contiene una lista
    if not isinstance(usuarios, list):
        return []
    return usuarios

def guardar_usuarios(usuarios):
    return guardar_datos(usuarios, archivo_usuarios)

def crear_usuarios(id_u, nom, ape, tel, dir_u, tipo):
    usuarios = obtener_usuarios() #obtiene la lista de usuarios desde el archivo json
    if any(us.get('id') == id_u for us in usuarios): #verifica si ya existe algun usuario en la lista igual al id agregado
        registrar_log(f"Intento fallido: Ya existe un usuario con ID {id_u}", " ERROR")
        return False, "El ID de usuario ya esta registrado."
    
    tipo = tipo.lower().strip()
    tipo_valido = ["administrador", "residente"]
    if tipo not in tipo_valido:
        registrar_log(f"Tipo de usuario invalido para el ID {id_u}: {tipo}", "ERROR")
        return False, "El tipo debe ser administrador o residente."

    nuevo_usuario = {
        "id": id_u,
        "nombres": nom,
        "apellidos": ape,
        "telefono": tel,
        "direccion": dir_u,
        "tipo": tipo # Administrador  o residente
    }    

    usuarios.append(nuevo_usuario) #agrega el nuevo diccionario a la lista de usuarios en memoria
    #Guardado final
    if guardar_usuarios(usuarios):
        registrar_log(f"Usuario creado existosamente: {id_u} - {nom} {ape}", "INFO")
        return True, f"Usuario {id_u} registrado correctamente."
    else:
        return False, "No se pudo guardar el usuario."

def listar_usuarios():
    usuarios = obtener_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    print("\n------------ LISTA DE USUARIOS ------------")
    for u in usuarios:
        print("---------------------------------------")
        print("ID:", u.get("id"))
        print("Nombres:", u.get("nombres"))
        print("Apellidos:", u.get("apellidos"))
        print("Teléfono:", u.get("telefono"))
        print("Dirección:", u.get("direccion"))
        print("Tipo:", u.get("tipo"))
    print("---------------------------------------")    

def buscar_usuario(id_u):
    usuarios = obtener_usuarios()
    for us in usuarios:
        if us.get("id") == id_u: # #compara si el ID del usuario iterado coincide con el id_u buscado
            return us
    return None

def actualizar_usuario(id_u, nombres=None, apellidos=None, telefono=None, direccion=None, tipo=None):
    usuarios = obtener_usuarios() #carga la lista de usuarios almacenados
    for us in usuarios: #recorre cada usuario de la lista
        if us.get("id") == id_u: 
            #Actualiza en el diccionario unicamente los atributos para los cuales se haya enviado un valor diferebte de none
            if nombres: us["nombres"] = nombres
            if apellidos: us["apellidos"] = apellidos
            if telefono: us["telefono"] = telefono  
            if direccion: us["direccion"] = direccion
            if tipo: us["tipo"] = tipo
            if guardar_usuarios(usuarios):
                registrar_log(f"Usuario {id_u} actualizado correctamente.")
                return True, "Usuario actualizado."
        return False, "No se pudo guadar la actualizacion."

def eliminar_usuario(id_u):
    usuarios = obtener_usuarios()
    usuarios_filtrados = [us for us in usuarios if us["id"] != id_u] #Utiliza una lista por compresion para crear una nueva losta omitiendo el usuario que coincida con id_u
    if len(usuarios) == len(usuarios_filtrados):
        registrar_log(f"Intento de eliminar usuario inexistente: {id_u}", "WARNING")
        return False, "Usuario no encontrado." #Si el tamaño de la lista antes y despues de filtar es igual, significa que no existia el usuario y retorna False
    if guardar_usuarios(usuarios_filtrados):
        registrar_log(f"Usuario {id_u} eliminado.", "INFO")
        return True, "Usuario eliminado correctamente."
    return False, "No se pudo eliminar el usuario."


           
    
                         