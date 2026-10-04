from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_id(texto):
    try:
        return int(input(texto))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<14}{'NOMBRE':<25}{'EMAIL':<28}{'PROMEDIO':<8}")
    print("-" * 80)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.carnet:<14}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.obtener_promedio():<8}")
    print("-" * 80)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(campo.capitalize() + ": ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if len(estudiantes) == 0:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)

    if len(encontrados) == 0:
        imprimir_info("Ningún estudiante coincide con '" + termino + "'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    id_estudiante = pedir_id("Id del estudiante: ")
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error("No existe un estudiante con id " + str(id_estudiante))
    else:
        print("  Id       :", estudiante.id)
        print("  Nombre   :", estudiante.obtener_nombre_completo())
        print("  Email    :", estudiante.email)
        print("  Carnet   :", estudiante.carnet)
        print("  Materias :", ", ".join(sorted(estudiante.materias)))
        print("  Notas:")
        for materia, lista_notas in estudiante.notas.items():
            print("    ", materia, "->", lista_notas)
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_id("Id del estudiante: ")
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error("No existe un estudiante con id " + str(id_estudiante))
        pausa()
        return

    imprimir_info("Editando a " + estudiante.obtener_nombre_completo())
    print("Deje en blanco el campo que no quiera cambiar.\n")

    datos_actuales = estudiante.a_diccionario()
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        nuevo = input(f"{campo.capitalize()} [{datos_actuales[campo]}]: ").strip()
        if nuevo != "":
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_id("Id del estudiante: ")
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error("No existe un estudiante con id " + str(id_estudiante))
        pausa()
        return

    imprimir_info("Se eliminará: " + str(estudiante))
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = pedir_id("Id del estudiante: ")
    if id_estudiante is None:
        pausa()
        return

    materia = input("Materia: ")
    nota = input("Nota (0 a 20): ")

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    id_estudiante = pedir_id("Id del estudiante: ")
    if id_estudiante is None:
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error("No existe un estudiante con id " + str(id_estudiante))
    else:
        print(estudiante.obtener_nombre_completo(), "tiene un promedio de", estudiante.obtener_promedio())
    pausa()


def opcion_materias_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    id_a = pedir_id("Id del primer estudiante: ")
    if id_a is None:
        pausa()
        return
    id_b = pedir_id("Id del segundo estudiante: ")
    if id_b is None:
        pausa()
        return

    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif len(resultado) == 0:
        imprimir_info("Estos dos estudiantes no comparten materias.")
    else:
        imprimir_exito("Materias en común: " + ", ".join(sorted(resultado)))
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    if len(materias) == 0:
        imprimir_info("Todavía no hay materias inscritas.")
    else:
        for materia in sorted(materias):
            print("  -", materia)
    pausa()


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    print("  1. Crear estudiante")
    print("  2. Ver todos")
    print("  3. Buscar")
    print("  4. Ver por id")
    print("  5. Actualizar")
    print("  6. Eliminar")
    print("  7. Agregar nota")
    print("  8. Ver promedio")
    print("  9. Materias en común")
    print("  10. Materias ofertadas")
    print("  0. Salir")
    print()


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_crear()
        elif opcion == "2":
            opcion_ver_todos()
        elif opcion == "3":
            opcion_buscar()
        elif opcion == "4":
            opcion_ver_por_id()
        elif opcion == "5":
            opcion_actualizar()
        elif opcion == "6":
            opcion_eliminar()
        elif opcion == "7":
            opcion_agregar_nota()
        elif opcion == "8":
            opcion_ver_promedio()
        elif opcion == "9":
            opcion_materias_comun()
        elif opcion == "10":
            opcion_materias_ofertadas()
        elif opcion == "0":
            imprimir_info("¡Hasta luego!")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    main()
