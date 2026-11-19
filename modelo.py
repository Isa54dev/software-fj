"""
Entidades del negocio: clientes, servicios y reservas.

Aquí vive la lógica central. Las clases abstractas están pensadas para
que, si mañana se agrega otro tipo de servicio, solo haya que heredar
y sobrescribir métodos.
"""

from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)


class EntidadBase(ABC):
    """Clase abstracta común a clientes y servicios."""

    def __init__(self, identificacion, nombre):
        # Datos mínimos que toda entidad comparte
        self._identificacion = identificacion
        self._nombre = nombre

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def describir(self):
        """Cada entidad debe saber describirse a su manera."""
        pass


class Cliente(EntidadBase):
    """Cliente del sistema. Valida todos sus datos y encapsula los personales."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)
        # Atributos privados para encapsular los datos personales
        self.__correo = None
        self.__telefono = None
        # Validamos desde el constructor
        self._validar_identificacion(identificacion)
        self._validar_nombre(nombre)
        self.correo = correo
        self.telefono = telefono

    def _validar_identificacion(self, identificacion):
        # No permitimos identificaciones vacías
        if not identificacion or not str(identificacion).strip():
            raise DatosInvalidosError("La identificación del cliente está vacía")

    def _validar_nombre(self, nombre):
        # El nombre debe tener al menos 3 letras reales
        if not nombre or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres")

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Validación sencilla: que tenga arroba y punto después
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"Correo inválido: {valor}")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Solo números y con al menos 7 dígitos
        if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
            raise DatosInvalidosError(f"Teléfono inválido: {valor}")
        self.__telefono = valor

    def describir(self):
        return f"Cliente {self.nombre} (ID: {self.identificacion}) - {self.__correo}"


class Servicio(ABC):
    """Clase abstracta para todos los servicios que ofrece Software FJ."""

    def __init__(self, codigo, nombre, tarifa_base):
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        # Todo servicio arranca disponible
        self._disponible = True

    def validar_parametros(self, duracion):
        # La duración es obligatoria
        if duracion is None:
            raise ParametroFaltanteError("Falta la duración del servicio")
        # Y debe ser un número positivo
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError(f"Duración inválida: {duracion}")

    def esta_disponible(self):
        return self._disponible

    def ocupar(self):
        # Se marca como no disponible al confirmarse una reserva
        self._disponible = False

    def liberar(self):
        # Se vuelve a marcar disponible cuando se cancela
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """Cada servicio calcula su costo a su manera (polimorfismo)."""
        pass

    def calcular_costo_con_impuesto(self, duracion, impuesto):
        # Variante del cálculo solo con impuesto (simula sobrecarga en Python)
        return self.calcular_costo(duracion, impuesto=impuesto)

    def calcular_costo_con_descuento(self, duracion, descuento):
        # Variante del cálculo solo con descuento (simula sobrecarga en Python)
        return self.calcular_costo(duracion, descuento=descuento)

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    """Reserva de salas. Se cobra por hora."""

    def __init__(self, codigo, nombre, tarifa_base, capacidad):
        super().__init__(codigo, nombre, tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        # Primero validamos la duración antes de calcular
        self.validar_parametros(duracion)
        # Costo base: tarifa por hora
        costo = self.tarifa_base * duracion
        # Aplicamos descuento y luego impuesto
        costo = costo * (1 - descuento)
        costo = costo * (1 + impuesto)
        return round(costo, 2)

    def describir(self):
        return f"Sala '{self.nombre}' para {self.capacidad} personas (código {self.codigo})"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos. Se cobra por día."""

    def __init__(self, codigo, nombre, tarifa_base, requiere_deposito=False):
        super().__init__(codigo, nombre, tarifa_base)
        self.requiere_deposito = requiere_deposito

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        self.validar_parametros(duracion)
        # Aquí la duración se interpreta en días
        costo = self.tarifa_base * duracion
        # Si pide depósito, sumamos un 20% al costo base
        if self.requiere_deposito:
            costo = costo * 1.20
        costo = costo * (1 - descuento)
        costo = costo * (1 + impuesto)
        return round(costo, 2)

    def describir(self):
        extra = "con depósito" if self.requiere_deposito else "sin depósito"
        return f"Equipo '{self.nombre}' {extra} (código {self.codigo})"


class AsesoriaEspecializada(Servicio):
    """Asesoría con especialista. Se cobra por hora con recargo fijo."""

    def __init__(self, codigo, nombre, tarifa_base, especialista):
        super().__init__(codigo, nombre, tarifa_base)
        self.especialista = especialista

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        self.validar_parametros(duracion)
        # Las asesorías llevan un recargo del 15% por ser especializadas
        costo = self.tarifa_base * duracion * 1.15
        costo = costo * (1 - descuento)
        costo = costo * (1 + impuesto)
        return round(costo, 2)

    def describir(self):
        return f"Asesoría '{self.nombre}' con {self.especialista} (código {self.codigo})"


class Reserva:
    """Vincula un cliente con un servicio en una duración determinada."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, cliente, servicio, duracion):
        # Validamos la duración aquí para que no se creen reservas inválidas
        if duracion is None:
            raise ParametroFaltanteError("La reserva requiere una duración")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError(f"Duración inválida para reserva: {duracion}")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Toda reserva arranca pendiente
        self.estado = "PENDIENTE"

    def confirmar(self):
        # Solo se confirma lo que está pendiente
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self.estado}"
            )
        # Además, el servicio debe seguir disponible
        if not self.servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio {self.servicio.codigo} no está disponible"
            )
        self.estado = "CONFIRMADA"
        self.servicio.ocupar()

    def cancelar(self):
        # No tiene sentido cancelar algo ya cancelado o procesado
        if self.estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self.estado}"
            )
        self.estado = "CANCELADA"
        # Al cancelar, el servicio vuelve a quedar libre
        self.servicio.liberar()

    def procesar(self):
        # Solo se procesa lo confirmado
        if self.estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se procesa una reserva CONFIRMADA, estado actual: {self.estado}"
            )
        self.estado = "PROCESADA"

    def describir(self):
        return (
            f"Reserva de {self.cliente.nombre} para {self.servicio.nombre} "
            f"por {self.duracion} - estado: {self.estado}"
        )