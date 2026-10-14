"""Modelo de ejemplares físicos para BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""


class Ejemplar:
    """Representa una copia física individual de un libro."""

    def __init__(self, codigo, titulo, autor, disponible=True):
        self._codigo = self._validar_texto(codigo, "código")
        self._titulo = self._validar_texto(titulo, "título")
        self._autor = self._validar_texto(autor, "autor")
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_texto(valor, campo):
        texto = str(valor).strip()
        if not texto:
            raise ValueError(f"El {campo} no puede estar vacío.")
        return texto

    def obtener_codigo(self):
        return self._codigo

    def obtener_titulo(self):
        return self._titulo

    def obtener_autor(self):
        return self._autor

    def esta_disponible(self):
        return self._disponible

    def actualizar_datos(self, titulo, autor):
        self._titulo = self._validar_texto(titulo, "título")
        self._autor = self._validar_texto(autor, "autor")

    def marcar_prestado(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    def obtener_informacion(self):
        estado = "Disponible" if self._disponible else "Prestado"
        return (
            f"Código: {self._codigo} | Título: {self._titulo} | "
            f"Autor: {self._autor} | Estado: {estado}"
        )

    def __str__(self):
        return self.obtener_informacion()
