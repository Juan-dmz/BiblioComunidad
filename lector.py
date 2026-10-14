"""Modelo de lectores para BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""


class Lector:
    """Representa a una persona registrada en la biblioteca."""

    def __init__(self, documento, nombre, telefono):
        self._documento = self._validar_texto(documento, "documento")
        self._nombre = self._validar_texto(nombre, "nombre")
        self._telefono = self._validar_texto(telefono, "telefono")

    @staticmethod
    def _validar_texto(valor, campo):
        texto = str(valor).strip()
        if not texto:
            raise ValueError(f"El {campo} no puede estar vacío.")
        return texto

    def obtener_documento(self):
        return self._documento

    def obtener_nombre(self):
        return self._nombre

    def obtener_telefono(self):
        return self._telefono

    def actualizar_datos(self, nombre, telefono):
        self._nombre = self._validar_texto(nombre, "nombre")
        self._telefono = self._validar_texto(telefono, "telefono")

    def obtener_informacion(self):
        return (
            f"Documento: {self._documento} | "
            f"Nombre: {self._nombre} | Teléfono: {self._telefono}"
        )

    def __str__(self):
        return self.obtener_informacion()
