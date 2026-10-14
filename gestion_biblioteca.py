"""Funciones de gestión y reglas de negocio de BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""

from lector import Lector
from ejemplar import Ejemplar
from prestamo import Prestamo


def _texto(valor):
    return str(valor).strip()


# ------------------------- Lectores -------------------------

def buscar_lector(lectores, documento):
    documento = _texto(documento)
    for lector in lectores:
        if lector.obtener_documento() == documento:
            return lector
    return None


def listar_lectores(lectores):
    return list(lectores)


def registrar_lector(lectores, documento, nombre, telefono):
    documento = _texto(documento)
    if not documento:
        return False, "El documento no puede estar vacío.", None
    if buscar_lector(lectores, documento) is not None:
        return False, "Ya existe un lector con ese documento.", None
    try:
        lector = Lector(documento, nombre, telefono)
    except ValueError as exc:
        return False, str(exc), None
    lectores.append(lector)
    return True, "Lector registrado correctamente.", lector


def actualizar_lector(lectores, documento, nombre, telefono):
    lector = buscar_lector(lectores, documento)
    if lector is None:
        return False, "Lector no encontrado."
    try:
        lector.actualizar_datos(nombre, telefono)
    except ValueError as exc:
        return False, str(exc)
    return True, "Lector actualizado correctamente."


def eliminar_lector(lectores, prestamos, documento):
    lector = buscar_lector(lectores, documento)
    if lector is None:
        return False, "Lector no encontrado."
    if any(p.obtener_lector() is lector for p in prestamos):
        return False, "No se puede eliminar: el lector tiene historial de préstamos."
    lectores.remove(lector)
    return True, "Lector eliminado correctamente."


# ------------------------- Ejemplares -------------------------

def buscar_ejemplar(ejemplares, codigo):
    codigo = _texto(codigo)
    for ejemplar in ejemplares:
        if ejemplar.obtener_codigo() == codigo:
            return ejemplar
    return None


def buscar_por_titulo(ejemplares, texto):
    texto = _texto(texto).lower()
    if not texto:
        return []
    return [e for e in ejemplares if texto in e.obtener_titulo().lower()]


def listar_ejemplares(ejemplares):
    return list(ejemplares)


def registrar_ejemplar(ejemplares, codigo, titulo, autor):
    codigo = _texto(codigo)
    if not codigo:
        return False, "El código no puede estar vacío.", None
    if buscar_ejemplar(ejemplares, codigo) is not None:
        return False, "Ya existe un ejemplar con ese código.", None
    try:
        ejemplar = Ejemplar(codigo, titulo, autor, True)
    except ValueError as exc:
        return False, str(exc), None
    ejemplares.append(ejemplar)
    return True, "Ejemplar registrado correctamente.", ejemplar


def actualizar_ejemplar(ejemplares, codigo, titulo, autor):
    ejemplar = buscar_ejemplar(ejemplares, codigo)
    if ejemplar is None:
        return False, "Ejemplar no encontrado."
    try:
        ejemplar.actualizar_datos(titulo, autor)
    except ValueError as exc:
        return False, str(exc)
    return True, "Ejemplar actualizado correctamente."


def eliminar_ejemplar(ejemplares, prestamos, codigo):
    ejemplar = buscar_ejemplar(ejemplares, codigo)
    if ejemplar is None:
        return False, "Ejemplar no encontrado."
    if any(p.obtener_ejemplar() is ejemplar for p in prestamos):
        return False, "No se puede eliminar: el ejemplar tiene historial de préstamos."
    ejemplares.remove(ejemplar)
    return True, "Ejemplar eliminado correctamente."


# ------------------------- Préstamos -------------------------

def buscar_prestamo(prestamos, id_prestamo):
    id_prestamo = _texto(id_prestamo)
    for prestamo in prestamos:
        if prestamo.obtener_id() == id_prestamo:
            return prestamo
    return None


def listar_prestamos(prestamos):
    return list(prestamos)


def listar_activos(prestamos):
    return [p for p in prestamos if p.esta_activo()]


def registrar_prestamo(prestamos, lectores, ejemplares, id_prestamo, documento, codigo, dias):
    id_prestamo = _texto(id_prestamo)
    if not id_prestamo:
        return False, "El ID del préstamo no puede estar vacío.", None
    if buscar_prestamo(prestamos, id_prestamo) is not None:
        return False, "Ya existe un préstamo con ese ID.", None

    lector = buscar_lector(lectores, documento)
    if lector is None:
        return False, "El lector no existe.", None

    ejemplar = buscar_ejemplar(ejemplares, codigo)
    if ejemplar is None:
        return False, "El ejemplar no existe.", None

    if not ejemplar.esta_disponible():
        return False, "El ejemplar no está disponible.", None

    try:
        prestamo = Prestamo(id_prestamo, lector, ejemplar, dias)
    except ValueError as exc:
        return False, str(exc), None

    # Los cambios de estado solo ocurren después de validar todo.
    ejemplar.marcar_prestado()
    prestamos.append(prestamo)
    return True, "Préstamo registrado correctamente.", prestamo


def devolver_prestamo(prestamos, id_prestamo):
    prestamo = buscar_prestamo(prestamos, id_prestamo)
    if prestamo is None:
        return False, "Préstamo no encontrado."
    if not prestamo.esta_activo():
        return False, "El préstamo ya fue devuelto."

    prestamo.marcar_devuelto()
    prestamo.obtener_ejemplar().marcar_disponible()
    return True, "Devolución registrada correctamente."
