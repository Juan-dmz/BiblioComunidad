# BiblioComunidad

Sistema local para gestionar lectores, ejemplares físicos, préstamos y devoluciones de una biblioteca comunitaria.

## Integrantes
- Juan Felipe Valencia Melenje
- Juan José Domínguez Botina

## Requisitos
- Python 3.10 o superior.
- Tkinter incluido con la instalación estándar de Python en Windows.
- No requiere librerías externas.

## Ejecutar la versión de consola
Desde la carpeta del proyecto:

```bash
python app_consola.py
```

## Ejecutar la interfaz gráfica
Desde la carpeta del proyecto:

```bash
python app_gui.py
```

## Ejecutar pruebas de integración

```bash
python pruebas_integracion.py
```

## Persistencia
Los datos se guardan en `datos_biblioteca.json`. Al iniciar, el programa reconstruye primero lectores y ejemplares y luego los préstamos, enlazando las relaciones mediante documento y código.

Si el JSON no existe, el sistema inicia con colecciones vacías. Si el archivo existe pero no puede leerse, se informa el problema y no se sobrescribe automáticamente.

## Funcionalidades
- CRUD de lectores.
- CRUD de ejemplares.
- Búsqueda de ejemplares por código y por título parcial.
- Registro y consulta de préstamos.
- Consulta de préstamos activos.
- Registro de devoluciones.
- Bloqueo de un segundo préstamo activo sobre el mismo ejemplar.
- Bloqueo de eliminación de lectores o ejemplares con historial asociado.
- Persistencia JSON de datos, estados y asociaciones.
- Interfaz de consola y GUI con la misma lógica de gestión.

## Estructura
- `lector.py`: clase `Lector`.
- `ejemplar.py`: clase `Ejemplar`.
- `prestamo.py`: clase `Prestamo`.
- `gestion_biblioteca.py`: CRUD, búsquedas y reglas de negocio.
- `persistencia.py`: carga y guardado JSON.
- `app_consola.py`: interfaz de consola.
- `app_gui.py`: interfaz Tkinter.
- `datos_biblioteca.json`: datos de demostración.
- `pruebas_integracion.py`: pruebas mínimas de integración.

## Repositorio GitHub
https://github.com/Juan-dmz/BiblioComunidad
