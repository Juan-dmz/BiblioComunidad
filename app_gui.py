"""Interfaz gráfica Tkinter de BiblioComunidad.

Integrantes:
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina
"""

import tkinter as tk
from tkinter import messagebox, ttk

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


class AppBiblioteca:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("BiblioComunidad")
        self.ventana.geometry("980x680")
        self.ventana.minsize(860, 600)

        self.persistencia_habilitada = True
        try:
            self.lectores, self.ejemplares, self.prestamos = cargar_datos()
        except ErrorPersistencia as exc:
            self.lectores, self.ejemplares, self.prestamos = [], [], []
            self.persistencia_habilitada = False
            self.ventana.after(
                150,
                lambda: messagebox.showwarning(
                    "Problema de persistencia",
                    f"{exc}\n\nSe iniciará con colecciones vacías y no se sobrescribirá el archivo dañado.",
                ),
            )

        titulo = ttk.Label(
            ventana,
            text="BiblioComunidad - Biblioteca comunitaria",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=(14, 8))

        self.notebook = ttk.Notebook(ventana)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=8)

        self.tab_lectores = ttk.Frame(self.notebook)
        self.tab_ejemplares = ttk.Frame(self.notebook)
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lectores, text="Lectores")
        self.notebook.add(self.tab_ejemplares, text="Ejemplares")
        self.notebook.add(self.tab_prestamos, text="Préstamos")

        self._crear_tab_lectores()
        self._crear_tab_ejemplares()
        self._crear_tab_prestamos()
        self._refrescar_todo()

    def _guardar(self):
        if not self.persistencia_habilitada:
            messagebox.showwarning(
                "Persistencia deshabilitada",
                "El archivo inicial presentó un error y no se sobrescribirá automáticamente.",
            )
            return False
        try:
            guardar_datos(self.lectores, self.ejemplares, self.prestamos)
            return True
        except ErrorPersistencia as exc:
            messagebox.showerror("Error de guardado", str(exc))
            return False

    @staticmethod
    def _limpiar_listbox(lista):
        lista.delete(0, tk.END)

    @staticmethod
    def _insertar(lista, elementos, mensaje_vacio):
        lista.delete(0, tk.END)
        if not elementos:
            lista.insert(tk.END, mensaje_vacio)
            return
        for elemento in elementos:
            lista.insert(tk.END, elemento.obtener_informacion())

    # ------------------------- Lectores -------------------------
    def _crear_tab_lectores(self):
        formulario = ttk.LabelFrame(self.tab_lectores, text="Datos del lector")
        formulario.pack(fill="x", padx=12, pady=10)

        ttk.Label(formulario, text="Documento:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.ent_doc = ttk.Entry(formulario, width=24)
        self.ent_doc.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.ent_nombre = ttk.Entry(formulario, width=30)
        self.ent_nombre.grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(formulario, text="Teléfono:").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.ent_tel = ttk.Entry(formulario, width=20)
        self.ent_tel.grid(row=0, column=5, padx=6, pady=6)

        botones = ttk.Frame(self.tab_lectores)
        botones.pack(fill="x", padx=12)
        ttk.Button(botones, text="Registrar", command=self.gui_registrar_lector).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar", command=self.gui_buscar_lector).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.gui_actualizar_lector).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.gui_eliminar_lector).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self.gui_listar_lectores).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_campos_lector).pack(side="left", padx=4)

        self.lista_lectores = tk.Listbox(self.tab_lectores, height=20, width=130)
        self.lista_lectores.pack(fill="both", expand=True, padx=12, pady=12)

    def _limpiar_campos_lector(self):
        for entrada in (self.ent_doc, self.ent_nombre, self.ent_tel):
            entrada.delete(0, tk.END)

    def gui_registrar_lector(self):
        ok, mensaje, _ = registrar_lector(
            self.lectores, self.ent_doc.get(), self.ent_nombre.get(), self.ent_tel.get()
        )
        (messagebox.showinfo if ok else messagebox.showwarning)("Lectores", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_lectores()
            self._limpiar_campos_lector()

    def gui_buscar_lector(self):
        lector = buscar_lector(self.lectores, self.ent_doc.get())
        if lector is None:
            self._insertar(self.lista_lectores, [], "Lector no encontrado.")
            return
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, lector.obtener_nombre())
        self.ent_tel.delete(0, tk.END)
        self.ent_tel.insert(0, lector.obtener_telefono())
        self._insertar(self.lista_lectores, [lector], "Lector no encontrado.")

    def gui_actualizar_lector(self):
        ok, mensaje = actualizar_lector(
            self.lectores, self.ent_doc.get(), self.ent_nombre.get(), self.ent_tel.get()
        )
        (messagebox.showinfo if ok else messagebox.showwarning)("Lectores", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_lectores()

    def gui_eliminar_lector(self):
        ok, mensaje = eliminar_lector(self.lectores, self.prestamos, self.ent_doc.get())
        (messagebox.showinfo if ok else messagebox.showwarning)("Lectores", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_lectores()
            self._limpiar_campos_lector()

    def gui_listar_lectores(self):
        self._insertar(self.lista_lectores, listar_lectores(self.lectores), "No hay lectores registrados.")

    # ------------------------- Ejemplares -------------------------
    def _crear_tab_ejemplares(self):
        formulario = ttk.LabelFrame(self.tab_ejemplares, text="Datos del ejemplar")
        formulario.pack(fill="x", padx=12, pady=10)

        ttk.Label(formulario, text="Código:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.ent_codigo = ttk.Entry(formulario, width=18)
        self.ent_codigo.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(formulario, text="Título:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.ent_titulo = ttk.Entry(formulario, width=34)
        self.ent_titulo.grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(formulario, text="Autor:").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.ent_autor = ttk.Entry(formulario, width=28)
        self.ent_autor.grid(row=0, column=5, padx=6, pady=6)

        botones = ttk.Frame(self.tab_ejemplares)
        botones.pack(fill="x", padx=12)
        ttk.Button(botones, text="Registrar", command=self.gui_registrar_ejemplar).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar código", command=self.gui_buscar_ejemplar).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar título", command=self.gui_buscar_titulo).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.gui_actualizar_ejemplar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.gui_eliminar_ejemplar).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self.gui_listar_ejemplares).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_campos_ejemplar).pack(side="left", padx=4)

        self.lista_ejemplares = tk.Listbox(self.tab_ejemplares, height=20, width=130)
        self.lista_ejemplares.pack(fill="both", expand=True, padx=12, pady=12)

    def _limpiar_campos_ejemplar(self):
        for entrada in (self.ent_codigo, self.ent_titulo, self.ent_autor):
            entrada.delete(0, tk.END)

    def gui_registrar_ejemplar(self):
        ok, mensaje, _ = registrar_ejemplar(
            self.ejemplares, self.ent_codigo.get(), self.ent_titulo.get(), self.ent_autor.get()
        )
        (messagebox.showinfo if ok else messagebox.showwarning)("Ejemplares", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_ejemplares()
            self._limpiar_campos_ejemplar()

    def gui_buscar_ejemplar(self):
        ejemplar = buscar_ejemplar(self.ejemplares, self.ent_codigo.get())
        if ejemplar is None:
            self._insertar(self.lista_ejemplares, [], "Ejemplar no encontrado.")
            return
        self.ent_titulo.delete(0, tk.END)
        self.ent_titulo.insert(0, ejemplar.obtener_titulo())
        self.ent_autor.delete(0, tk.END)
        self.ent_autor.insert(0, ejemplar.obtener_autor())
        self._insertar(self.lista_ejemplares, [ejemplar], "Ejemplar no encontrado.")

    def gui_buscar_titulo(self):
        resultados = buscar_por_titulo(self.ejemplares, self.ent_titulo.get())
        self._insertar(self.lista_ejemplares, resultados, "No se encontraron coincidencias.")

    def gui_actualizar_ejemplar(self):
        ok, mensaje = actualizar_ejemplar(
            self.ejemplares, self.ent_codigo.get(), self.ent_titulo.get(), self.ent_autor.get()
        )
        (messagebox.showinfo if ok else messagebox.showwarning)("Ejemplares", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_ejemplares()

    def gui_eliminar_ejemplar(self):
        ok, mensaje = eliminar_ejemplar(self.ejemplares, self.prestamos, self.ent_codigo.get())
        (messagebox.showinfo if ok else messagebox.showwarning)("Ejemplares", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_ejemplares()
            self._limpiar_campos_ejemplar()

    def gui_listar_ejemplares(self):
        self._insertar(
            self.lista_ejemplares, listar_ejemplares(self.ejemplares), "No hay ejemplares registrados."
        )

    # ------------------------- Préstamos -------------------------
    def _crear_tab_prestamos(self):
        formulario = ttk.LabelFrame(self.tab_prestamos, text="Datos del préstamo")
        formulario.pack(fill="x", padx=12, pady=10)

        ttk.Label(formulario, text="ID préstamo:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.ent_id_prestamo = ttk.Entry(formulario, width=16)
        self.ent_id_prestamo.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(formulario, text="Documento lector:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.ent_prestamo_doc = ttk.Entry(formulario, width=18)
        self.ent_prestamo_doc.grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(formulario, text="Código ejemplar:").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.ent_prestamo_codigo = ttk.Entry(formulario, width=16)
        self.ent_prestamo_codigo.grid(row=0, column=5, padx=6, pady=6)

        ttk.Label(formulario, text="Días:").grid(row=0, column=6, padx=6, pady=6, sticky="w")
        self.ent_dias = ttk.Entry(formulario, width=8)
        self.ent_dias.grid(row=0, column=7, padx=6, pady=6)

        botones = ttk.Frame(self.tab_prestamos)
        botones.pack(fill="x", padx=12)
        ttk.Button(botones, text="Registrar préstamo", command=self.gui_registrar_prestamo).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar", command=self.gui_buscar_prestamo).pack(side="left", padx=4)
        ttk.Button(botones, text="Devolver", command=self.gui_devolver_prestamo).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self.gui_listar_prestamos).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar activos", command=self.gui_listar_activos).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_campos_prestamo).pack(side="left", padx=4)

        self.lista_prestamos = tk.Listbox(self.tab_prestamos, height=20, width=130)
        self.lista_prestamos.pack(fill="both", expand=True, padx=12, pady=12)

    def _limpiar_campos_prestamo(self):
        for entrada in (
            self.ent_id_prestamo,
            self.ent_prestamo_doc,
            self.ent_prestamo_codigo,
            self.ent_dias,
        ):
            entrada.delete(0, tk.END)

    def gui_registrar_prestamo(self):
        ok, mensaje, _ = registrar_prestamo(
            self.prestamos,
            self.lectores,
            self.ejemplares,
            self.ent_id_prestamo.get(),
            self.ent_prestamo_doc.get(),
            self.ent_prestamo_codigo.get(),
            self.ent_dias.get(),
        )
        (messagebox.showinfo if ok else messagebox.showwarning)("Préstamos", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_prestamos()
            self.gui_listar_ejemplares()
            self._limpiar_campos_prestamo()

    def gui_buscar_prestamo(self):
        prestamo = buscar_prestamo(self.prestamos, self.ent_id_prestamo.get())
        self._insertar(
            self.lista_prestamos,
            [prestamo] if prestamo else [],
            "Préstamo no encontrado.",
        )

    def gui_devolver_prestamo(self):
        ok, mensaje = devolver_prestamo(self.prestamos, self.ent_id_prestamo.get())
        (messagebox.showinfo if ok else messagebox.showwarning)("Préstamos", mensaje)
        if ok:
            self._guardar()
            self.gui_listar_prestamos()
            self.gui_listar_ejemplares()

    def gui_listar_prestamos(self):
        self._insertar(self.lista_prestamos, listar_prestamos(self.prestamos), "No hay préstamos registrados.")

    def gui_listar_activos(self):
        self._insertar(self.lista_prestamos, listar_activos(self.prestamos), "No hay préstamos activos.")

    def _refrescar_todo(self):
        self.gui_listar_lectores()
        self.gui_listar_ejemplares()
        self.gui_listar_prestamos()


def main():
    ventana = tk.Tk()
    AppBiblioteca(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
