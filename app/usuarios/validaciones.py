def validar_nombre(nombre):
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    if not nombre.replace(" ", "").isalpha():
        raise ValueError("El nombre solo debe contener letras.")

    return nombre


def validar_edad(edad):
    try:
        edad = int(edad)
    except ValueError:
        raise ValueError("La edad debe ser un número entero.")

    if edad <= 0:
        raise ValueError("La edad debe ser mayor que cero.")

    if edad > 120:
        raise ValueError("La edad ingresada no es válida.")

    return edad