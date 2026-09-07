from app.usuarios.validaciones import validar_nombre, validar_edad


usuarios = []


def registrar_usuario(nombre, edad):
    nombre = validar_nombre(nombre)
    edad = validar_edad(edad)

    usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "edad": edad
    }

    usuarios.append(usuario)
    return usuario


def listar_usuarios():
    return usuarios


def buscar_usuario(nombre):
    nombre = nombre.strip().lower()

    for usuario in usuarios:
        if usuario["nombre"].lower() == nombre:
            return usuario

    return None