"""Persistencia JSON para BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""

import json
import os
import tempfile

from lector import Lector
from ejemplar import Ejemplar
from prestamo import Prestamo
from gestion_biblioteca import buscar_lector, buscar_ejemplar


ARCHIVO_DATOS = os.path.join(os.path.dirname(__file__), "datos_biblioteca.json")


class ErrorPersistencia(Exception):
    pass


def lector_a_diccionario(lector):
    return {
        "documento": lector.obtener_documento(),
        "nombre": lector.obtener_nombre(),
        "telefono": lector.obtener_telefono(),
    }


def ejemplar_a_diccionario(ejemplar):
    return {
        "codigo": ejemplar.obtener_codigo(),
        "titulo": ejemplar.obtener_titulo(),
        "autor": ejemplar.obtener_autor(),
        "disponible": ejemplar.esta_disponible(),
    }


def prestamo_a_diccionario(prestamo):
    return {
        "id": prestamo.obtener_id(),
        "lector": prestamo.obtener_lector().obtener_documento(),
        "ejemplar": prestamo.obtener_ejemplar().obtener_codigo(),
        "dias": prestamo.obtener_dias(),
        "estado": prestamo.obtener_estado(),
    }


def guardar_datos(lectores, ejemplares, prestamos, ruta=ARCHIVO_DATOS):
    datos = {
        "lectores": [lector_a_diccionario(l) for l in lectores],
        "ejemplares": [ejemplar_a_diccionario(e) for e in ejemplares],
        "prestamos": [prestamo_a_diccionario(p) for p in prestamos],
    }

    carpeta = os.path.dirname(os.path.abspath(ruta))
    os.makedirs(carpeta, exist_ok=True)

    # Escritura atómica: primero se escribe un temporal y luego se reemplaza el archivo.
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", delete=False, dir=carpeta, encoding="utf-8", suffix=".tmp"
        ) as archivo:
            temporal = archivo.name
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        os.replace(temporal, ruta)
        return True
    except (OSError, TypeError, ValueError) as exc:
        if temporal and os.path.exists(temporal):
            try:
                os.remove(temporal)
            except OSError:
                pass
        raise ErrorPersistencia(f"No fue posible guardar los datos: {exc}") from exc


def cargar_datos(ruta=ARCHIVO_DATOS):
    if not os.path.exists(ruta):
        return [], [], []

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (OSError, json.JSONDecodeError) as exc:
        raise ErrorPersistencia(
            "El archivo JSON no pudo leerse. No se sobrescribirá automáticamente."
        ) from exc

    try:
        lectores = [
            Lector(item["documento"], item["nombre"], item["telefono"])
            for item in datos.get("lectores", [])
        ]

        ejemplares = [
            Ejemplar(
                item["codigo"],
                item["titulo"],
                item["autor"],
                item.get("disponible", True),
            )
            for item in datos.get("ejemplares", [])
        ]

        prestamos = []
        for item in datos.get("prestamos", []):
            lector = buscar_lector(lectores, item["lector"])
            ejemplar = buscar_ejemplar(ejemplares, item["ejemplar"])
            if lector is None or ejemplar is None:
                raise ErrorPersistencia(
                    f"El préstamo {item.get('id', '?')} referencia datos inexistentes."
                )
            prestamo = Prestamo(
                item["id"],
                lector,
                ejemplar,
                item["dias"],
                item["estado"],
            )
            prestamos.append(prestamo)

        # Recalcular disponibilidad a partir de los préstamos activos evita inconsistencias.
        for ejemplar in ejemplares:
            ejemplar.marcar_disponible()
        for prestamo in prestamos:
            if prestamo.esta_activo():
                prestamo.obtener_ejemplar().marcar_prestado()

        return lectores, ejemplares, prestamos
    except (KeyError, TypeError, ValueError) as exc:
        raise ErrorPersistencia(
            "El archivo JSON contiene datos inconsistentes. No se sobrescribirá automáticamente."
        ) from exc
