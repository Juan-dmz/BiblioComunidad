"""Interfaz de consola de BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""

from gestion_biblioteca import (
    actualizar_ejemplar,
    actualizar_lector,
    buscar_ejemplar,
    buscar_lector,
    buscar_por_titulo,
    buscar_prestamo,
    devolver_prestamo,
    eliminar_ejemplar,
    eliminar_lector,
    listar_activos,
    listar_ejemplares,
    listar_lectores,
    listar_prestamos,
    registrar_ejemplar,
    registrar_lector,
    registrar_prestamo,
)
from persistencia import ErrorPersistencia, cargar_datos, guardar_datos


def _mostrar_lista(elementos, mensaje_vacio="No hay registros."):
    if not elementos:
        print(mensaje_vacio)
        return
    for elemento in elementos:
        print(elemento.obtener_informacion())


def _guardar(lectores, ejemplares, prestamos, persistencia_habilitada):
    if not persistencia_habilitada:
        print("ADVERTENCIA: no se guardó porque el archivo inicial presentó un error de lectura.")
        return False
    try:
        guardar_datos(lectores, ejemplares, prestamos)
        return True
    except ErrorPersistencia as exc:
        print(exc)
        return False


def menu_lectores(lectores, ejemplares, prestamos, persistencia_habilitada):
    while True:
        print("\n--- GESTIÓN DE LECTORES ---")
        print("1. Registrar lector")
        print("2. Listar lectores")
        print("3. Buscar lector")
        print("4. Actualizar lector")
        print("5. Eliminar lector")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ok, mensaje, _ = registrar_lector(
                lectores,
                input("Documento: "),
                input("Nombre: "),
                input("Teléfono: "),
            )
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "2":
            _mostrar_lista(listar_lectores(lectores), "No hay lectores registrados.")
        elif opcion == "3":
            lector = buscar_lector(lectores, input("Documento: "))
            print(lector.obtener_informacion() if lector else "Lector no encontrado.")
        elif opcion == "4":
            documento = input("Documento del lector: ")
            ok, mensaje = actualizar_lector(
                lectores, documento, input("Nuevo nombre: "), input("Nuevo teléfono: ")
            )
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "5":
            ok, mensaje = eliminar_lector(lectores, prestamos, input("Documento: "))
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def menu_ejemplares(lectores, ejemplares, prestamos, persistencia_habilitada):
    while True:
        print("\n--- GESTIÓN DE EJEMPLARES ---")
        print("1. Registrar ejemplar")
        print("2. Listar ejemplares")
        print("3. Buscar por código")
        print("4. Buscar por título")
        print("5. Actualizar ejemplar")
        print("6. Eliminar ejemplar")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ok, mensaje, _ = registrar_ejemplar(
                ejemplares,
                input("Código: "),
                input("Título: "),
                input("Autor: "),
            )
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "2":
            _mostrar_lista(listar_ejemplares(ejemplares), "No hay ejemplares registrados.")
        elif opcion == "3":
            ejemplar = buscar_ejemplar(ejemplares, input("Código: "))
            print(ejemplar.obtener_informacion() if ejemplar else "Ejemplar no encontrado.")
        elif opcion == "4":
            resultados = buscar_por_titulo(ejemplares, input("Título o parte del título: "))
            _mostrar_lista(resultados, "No se encontraron coincidencias.")
        elif opcion == "5":
            codigo = input("Código del ejemplar: ")
            ok, mensaje = actualizar_ejemplar(
                ejemplares, codigo, input("Nuevo título: "), input("Nuevo autor: ")
            )
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "6":
            ok, mensaje = eliminar_ejemplar(ejemplares, prestamos, input("Código: "))
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def menu_prestamos(lectores, ejemplares, prestamos, persistencia_habilitada):
    while True:
        print("\n--- GESTIÓN DE PRÉSTAMOS ---")
        print("1. Registrar préstamo")
        print("2. Listar préstamos")
        print("3. Buscar préstamo")
        print("4. Listar préstamos activos")
        print("5. Registrar devolución")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ok, mensaje, _ = registrar_prestamo(
                prestamos,
                lectores,
                ejemplares,
                input("ID del préstamo: "),
                input("Documento del lector: "),
                input("Código del ejemplar: "),
                input("Cantidad de días: "),
            )
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "2":
            _mostrar_lista(listar_prestamos(prestamos), "No hay préstamos registrados.")
        elif opcion == "3":
            prestamo = buscar_prestamo(prestamos, input("ID del préstamo: "))
            print(prestamo.obtener_informacion() if prestamo else "Préstamo no encontrado.")
        elif opcion == "4":
            _mostrar_lista(listar_activos(prestamos), "No hay préstamos activos.")
        elif opcion == "5":
            ok, mensaje = devolver_prestamo(prestamos, input("ID del préstamo: "))
            print(mensaje)
            if ok:
                _guardar(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def main():
    persistencia_habilitada = True
    try:
        lectores, ejemplares, prestamos = cargar_datos()
    except ErrorPersistencia as exc:
        print(f"ADVERTENCIA: {exc}")
        print("El programa continuará con colecciones vacías y no sobrescribirá el archivo dañado.")
        lectores, ejemplares, prestamos = [], [], []
        persistencia_habilitada = False

    while True:
        print("\n===============================")
        print("        BIBLIOCOMUNIDAD")
        print("===============================")
        print("1. Gestión de lectores")
        print("2. Gestión de ejemplares")
        print("3. Gestión de préstamos")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            menu_lectores(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "2":
            menu_ejemplares(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "3":
            menu_prestamos(lectores, ejemplares, prestamos, persistencia_habilitada)
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
