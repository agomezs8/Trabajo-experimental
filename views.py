from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def emails_registrados(excepto_id=None):
    emails = set()
    for registro in gestor.leer():
        if registro["id"] != excepto_id:
            emails.add(registro["email"].lower())
    return emails


def carnets_registrados(excepto_id=None):
    carnets = set()
    for registro in gestor.leer():
        if registro["id"] != excepto_id:
            carnets.add(registro["carnet"].lower())
    return carnets


def siguiente_id():
    registros = gestor.leer()
    if len(registros) == 0:
        return 1
    mayor = 0
    for registro in registros:
        if registro["id"] > mayor:
            mayor = registro["id"]
    return mayor + 1


def crear_estudiante(datos):
    valores = {}
    for campo in CAMPOS_ESTUDIANTE:
        valores[campo] = str(datos.get(campo, "")).strip()

    for campo in CAMPOS_ESTUDIANTE:
        if valores[campo] == "":
            return False, "Falta el campo obligatorio: " + campo

    if not es_email_valido(valores["email"]):
        return False, "El email no tiene un formato válido"

    if valores["email"].lower() in emails_registrados():
        return False, "Ese email ya está registrado"

    if valores["carnet"].lower() in carnets_registrados():
        return False, "Ese carnet ya está registrado"

    estudiante = Estudiante(siguiente_id(), valores["nombre"], valores["apellido"],
                            valores["email"], valores["carnet"])
    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"

    return True, "Estudiante " + estudiante.obtener_nombre_completo() + " creado con id " + str(estudiante.id)


def obtener_todos():
    estudiantes = []
    for registro in gestor.leer():
        estudiantes.append(Estudiante.desde_diccionario(registro))
    return estudiantes


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if termino == "":
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


def actualizar_estudiante(id_estudiante, cambios):
    if len(cambios) == 0:
        return False, "No se indicó ningún cambio"

    for campo in cambios:
        if campo not in CAMPOS_ESTUDIANTE:
            return False, "Campo no válido: " + campo

    registros = gestor.leer()
    posicion = None
    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            posicion = indice
            break

    if posicion is None:
        return False, "No existe un estudiante con id " + str(id_estudiante)

    if "email" in cambios:
        if not es_email_valido(cambios["email"]):
            return False, "El email no tiene un formato válido"
        if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
            return False, "Ese email ya lo usa otro estudiante"

    if "carnet" in cambios:
        if cambios["carnet"].lower() in carnets_registrados(excepto_id=id_estudiante):
            return False, "Ese carnet ya lo usa otro estudiante"

    registros[posicion].update(cambios)
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"
    return True, "Estudiante " + str(id_estudiante) + " actualizado"


def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()

    quedan = []
    for registro in registros:
        if registro["id"] != id_estudiante:
            quedan.append(registro)

    if len(quedan) == len(registros):
        return False, "No existe un estudiante con id " + str(id_estudiante)

    if not gestor.guardar(quedan):
        return False, "No se pudo escribir el archivo"
    return True, "Estudiante " + str(id_estudiante) + " eliminado"


def agregar_nota(id_estudiante, materia, nota):
    materia = materia.strip().title()
    if materia == "":
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except ValueError:
        return False, "La nota debe ser un número"

    if not (0 <= nota <= 20):
        return False, "La nota debe estar entre 0 y 20"

    if nota == int(nota):
        nota = int(nota)

    registros = gestor.leer()
    posicion = None
    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            posicion = indice
            break

    if posicion is None:
        return False, "No existe un estudiante con id " + str(id_estudiante)

    estudiante = Estudiante.desde_diccionario(registros[posicion])
    estudiante.agregar_nota(materia, nota)
    registros[posicion] = estudiante.a_diccionario()
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"
    return True, "Nota " + str(nota) + " agregada en " + materia


def materias_ofertadas():
    todas = set()
    for estudiante in obtener_todos():
        todas = todas | estudiante.materias
    return todas


def estudiantes_en_comun(id_a, id_b):
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None:
        return False, "No existe un estudiante con id " + str(id_a)
    if estudiante_b is None:
        return False, "No existe un estudiante con id " + str(id_b)

    comunes = estudiante_a.materias & estudiante_b.materias
    return True, comunes
