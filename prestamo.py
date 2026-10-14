"""Modelo de préstamos para BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""


class Prestamo:
    """Asocia un lector con un ejemplar durante una cantidad de días."""

    ESTADO_ACTIVO = "ACTIVO"
    ESTADO_DEVUELTO = "DEVUELTO"

    def __init__(self, id_prestamo, lector, ejemplar, dias, estado=ESTADO_ACTIVO):
        self._id_prestamo = self._validar_texto(id_prestamo, "ID del préstamo")
        if lector is None:
            raise ValueError("El préstamo requiere un lector.")
        if ejemplar is None:
            raise ValueError("El préstamo requiere un ejemplar.")
        self._lector = lector
        self._ejemplar = ejemplar
        self._dias = self._validar_dias(dias)
        estado_normalizado = str(estado).strip().upper()
        if estado_normalizado not in (self.ESTADO_ACTIVO, self.ESTADO_DEVUELTO):
            raise ValueError("Estado de préstamo inválido.")
        self._estado = estado_normalizado

    @staticmethod
    def _validar_texto(valor, campo):
        texto = str(valor).strip()
        if not texto:
            raise ValueError(f"El {campo} no puede estar vacío.")
        return texto

    @staticmethod
    def _validar_dias(dias):
        if isinstance(dias, bool):
            raise ValueError("La cantidad de días debe ser un entero mayor que cero.")
        try:
            valor = int(dias)
        except (TypeError, ValueError) as exc:
            raise ValueError("La cantidad de días debe ser un entero mayor que cero.") from exc
        if valor <= 0:
            raise ValueError("La cantidad de días debe ser un entero mayor que cero.")
        return valor

    def obtener_id(self):
        return self._id_prestamo

    def obtener_lector(self):
        return self._lector

    def obtener_ejemplar(self):
        return self._ejemplar

    def obtener_dias(self):
        return self._dias

    def obtener_estado(self):
        return self._estado

    def esta_activo(self):
        return self._estado == self.ESTADO_ACTIVO

    def marcar_devuelto(self):
        if not self.esta_activo():
            return False
        self._estado = self.ESTADO_DEVUELTO
        return True

    def obtener_informacion(self):
        return (
            f"ID: {self._id_prestamo} | "
            f"Lector: {self._lector.obtener_documento()} - {self._lector.obtener_nombre()} | "
            f"Ejemplar: {self._ejemplar.obtener_codigo()} - {self._ejemplar.obtener_titulo()} | "
            f"Días: {self._dias} | Estado: {self._estado}"
        )

    def __str__(self):
        return self.obtener_informacion()
