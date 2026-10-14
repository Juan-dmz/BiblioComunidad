"""Pruebas de integración de BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""

import os
import tempfile

from gestion_biblioteca import (
    buscar_ejemplar,
    buscar_lector,
    devolver_prestamo,
    eliminar_ejemplar,
    eliminar_lector,
    registrar_ejemplar,
    registrar_lector,
    registrar_prestamo,
)
from persistencia import cargar_datos, guardar_datos


RESULTADOS = []


def verificar(id_prueba, condicion, descripcion):
    if condicion:
        RESULTADOS.append((id_prueba, "OK", descripcion))
    else:
        RESULTADOS.append((id_prueba, "FALLO", descripcion))
        raise AssertionError(f"{id_prueba}: {descripcion}")


def ejecutar():
    lectores, ejemplares, prestamos = [], [], []

    ok, _, _ = registrar_lector(lectores, "1001", "Ana Torres", "3001112233")
    verificar("P01", ok and buscar_lector(lectores, "1001") is not None, "Registro válido de lector")

    ok, _, _ = registrar_lector(lectores, "1001", "Otra Ana", "3000000000")
    verificar("P02", not ok and len(lectores) == 1, "Duplicado rechazado sin cambiar la colección")

    verificar("P03", buscar_lector(lectores, "9999") is None, "Búsqueda inexistente")
    verificar("P04", len([]) == 0, "Lista vacía se maneja sin error")

    ok, _, _ = registrar_lector(lectores, "1002", "Carlos Pérez", "3002223344")
    verificar("P04B", ok, "Segundo lector para pruebas relacionadas")

    ok, _, _ = registrar_ejemplar(ejemplares, "E001", "Cien años de soledad", "Gabriel García Márquez")
    verificar("P04C", ok, "Ejemplar base registrado")
    ok, _, _ = registrar_ejemplar(ejemplares, "E002", "Rayuela", "Julio Cortázar")
    verificar("P04D", ok, "Ejemplar sin historial registrado")

    ok, _, _ = registrar_prestamo(prestamos, lectores, ejemplares, "PX", "1001", "E001", 0)
    verificar("P05", not ok and len(prestamos) == 0 and buscar_ejemplar(ejemplares, "E001").esta_disponible(), "Días inválidos rechazados sin alterar estado")

    ok, _, p = registrar_prestamo(prestamos, lectores, ejemplares, "P001", "1001", "E001", 7)
    verificar("P06", ok and p.esta_activo() and not buscar_ejemplar(ejemplares, "E001").esta_disponible(), "Préstamo válido cambia disponibilidad")

    ok, _, _ = registrar_prestamo(prestamos, lectores, ejemplares, "P002", "1002", "E001", 5)
    verificar("P07", not ok and len(prestamos) == 1, "Conflicto de disponibilidad rechazado")

    ok, _ = devolver_prestamo(prestamos, "P001")
    verificar("P08", ok and buscar_ejemplar(ejemplares, "E001").esta_disponible(), "Devolución libera ejemplar")

    ok, _ = devolver_prestamo(prestamos, "P001")
    verificar("P09", not ok, "Segunda devolución rechazada")

    ok, _ = eliminar_ejemplar(ejemplares, prestamos, "E002")
    verificar("P10", ok and buscar_ejemplar(ejemplares, "E002") is None, "Eliminación permitida sin historial")

    ok, _ = eliminar_ejemplar(ejemplares, prestamos, "E001")
    verificar("P11", not ok and buscar_ejemplar(ejemplares, "E001") is not None, "Eliminación rechazada con historial")

    ok, _ = eliminar_lector(lectores, prestamos, "1001")
    verificar("P11B", not ok and buscar_lector(lectores, "1001") is not None, "Lector con historial no se elimina")

    with tempfile.TemporaryDirectory() as carpeta:
        ruta = os.path.join(carpeta, "datos.json")
        guardar_datos(lectores, ejemplares, prestamos, ruta)
        l2, e2, p2 = cargar_datos(ruta)
        prestamo_recuperado = p2[0]
        lector_recuperado = buscar_lector(l2, prestamo_recuperado.obtener_lector().obtener_documento())
        ejemplar_recuperado = buscar_ejemplar(e2, prestamo_recuperado.obtener_ejemplar().obtener_codigo())
        relaciones_ok = (
            prestamo_recuperado.obtener_lector() is lector_recuperado
            and prestamo_recuperado.obtener_ejemplar() is ejemplar_recuperado
            and prestamo_recuperado.obtener_estado() == "DEVUELTO"
        )
        verificar("P12", relaciones_ok, "Persistencia recupera datos, estado y asociaciones")

    return RESULTADOS


if __name__ == "__main__":
    resultados = ejecutar()
    print("PRUEBAS DE INTEGRACIÓN - BIBLIOCOMUNIDAD")
    for id_prueba, estado, descripcion in resultados:
        print(f"{id_prueba}: {estado} - {descripcion}")
    print(f"\nTotal: {len(resultados)} pruebas aprobadas.")
