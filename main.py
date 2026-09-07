from app.config.settings import APP_NAME, APP_VERSION, ADMIN_USER
from app.usuarios.gestor import (
    registrar_usuario,
    listar_usuarios,
    buscar_usuario
)


def mostrar_menu():
    print("\n==============================")
    print(f"  {APP_NAME}")
    print(f"  Versión: {APP_VERSION}")
    print("==============================")
    print("1. Registrar usuario")
    print("2. Listar usuarios")
    print("3. Buscar usuario")
    print("4. Mostrar administrador")
    print("5. Salir")
    print("==============================")


def registrar():
    try:
        nombre = input("Ingrese el nombre: ")
        edad = input("Ingrese la edad: ")

        usuario = registrar_usuario(nombre, edad)

        print("\nUsuario registrado correctamente.")
        print(f"ID: {usuario['id']}")
        print(f"Nombre: {usuario['nombre']}")
        print(f"Edad: {usuario['edad']}")

    except ValueError as error:
        print(f"\nError: {error}")


def listar():
    usuarios = listar_usuarios()

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    print("\n--- USUARIOS REGISTRADOS ---")

    for usuario in usuarios:
        print(
            f"ID: {usuario['id']} | "
            f"Nombre: {usuario['nombre']} | "
            f"Edad: {usuario['edad']}"
        )


def buscar():
    nombre = input("Ingrese el nombre del usuario: ")

    usuario = buscar_usuario(nombre)

    if usuario:
        print("\nUsuario encontrado.")
        print(f"ID: {usuario['id']}")
        print(f"Nombre: {usuario['nombre']}")
        print(f"Edad: {usuario['edad']}")
    else:
        print("\nUsuario no encontrado.")


def ejecutar():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar()

        elif opcion == "2":
            listar()

        elif opcion == "3":
            buscar()

        elif opcion == "4":
            print(f"\nAdministrador configurado: {ADMIN_USER}")

        elif opcion == "5":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\nOpción no válida.")


if __name__ == "__main__":
    ejecutar()