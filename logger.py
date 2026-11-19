"""
Registro de eventos y errores en un archivo plano.

No usamos base de datos: solo un .log que se va llenando mientras corre
la app. El logger se protege a sí mismo para que un fallo al escribir
no tumbe todo el sistema.
"""

import os
from datetime import datetime


class Logger:
    """Escribe eventos y errores en logs/eventos.log."""

    def __init__(self, ruta_archivo="logs/eventos.log"):
        # Guardamos la ruta y nos aseguramos de que la carpeta exista
        self.ruta_archivo = ruta_archivo
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

    def registrar_evento(self, mensaje):
        """Guarda algo que salió bien o que vale la pena dejar anotado."""
        self._escribir("EVENTO", mensaje)

    def registrar_error(self, excepcion, contexto=""):
        """Guarda un error con su tipo y contexto para poder rastrearlo."""
        mensaje = f"{type(excepcion).__name__}: {excepcion}"
        if contexto:
            mensaje += f" | contexto: {contexto}"
        self._escribir("ERROR", mensaje)

    def _escribir(self, nivel, mensaje):
        """Método interno que realmente escribe en el archivo."""
        try:
            # Abrimos en modo append para no borrar lo anterior
            with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"[{fecha}] [{nivel}] {mensaje}\n")
        except Exception as e:
            # Si falla el log, preferimos no tumbar la app; solo avisamos
            print(f"No se pudo escribir en el log: {e}")