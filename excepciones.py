"""
Excepciones propias del sistema Software FJ.

La idea es no depender solo de ValueError o TypeError, sino tener errores
con nombre claro que digan exactamente qué pasó en el negocio.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base: todas las demás heredan de esta."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato no cumple el formato o las reglas del negocio."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un dato obligatorio para completar una operación."""
    pass


class ClienteDuplicadoError(ErrorSistemaFJ):
    """Se lanza al intentar registrar un cliente cuya identificación ya existe."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva no cumple las condiciones mínimas."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta una transición de estado que no está permitida."""
    pass