"""
Punto de entrada del sistema Software FJ.

Ejecuta 15 operaciones que mezclan casos válidos e inválidos. El objetivo
no es solo mostrar que el sistema funciona, sino demostrar que sigue vivo
aunque ocurran errores. Todo se registra en logs/eventos.log.
"""

from excepciones import (
    DatosInvalidosError,
    ClienteDuplicadoError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)
from logger import Logger
from modelo import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorClientes, GestorServicios, GestorReservas


def ejecutar_simulacion():
    """Corre las 15 operaciones de prueba y muestra el resultado por consola."""

    # Un solo logger para toda la simulación
    logger = Logger()

    # Gestores con las listas internas en memoria
    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()
    gestor_reservas = GestorReservas(logger)

    print("=== INICIO SIMULACIÓN SOFTWARE FJ ===\n")

    # ---- OP 1: cliente válido ----
    try:
        cliente1 = Cliente("1001", "Ana Gómez", "ana@correo.com", "3001234567")
        gestor_clientes.registrar(cliente1)
        logger.registrar_evento(f"Cliente registrado: {cliente1.describir()}")
        print(f"[OK] Cliente válido: {cliente1.nombre}")
    except Exception as e:
        logger.registrar_error(e, "op1 cliente válido")

    # ---- OP 2: cliente con correo inválido ----
    try:
        Cliente("1002", "Luis Pérez", "correo-sin-arroba", "3009876543")
    except DatosInvalidosError as e:
        logger.registrar_error(e, "op2 correo inválido")
        print(f"[ERROR esperado] Correo inválido -> {e}")

    # ---- OP 3: cliente duplicado ----
    try:
        dup = Cliente("1001", "Otra Ana", "otra@correo.com", "3001112222")
        gestor_clientes.registrar(dup)
    except ClienteDuplicadoError as e:
        logger.registrar_error(e, "op3 cliente duplicado")
        print(f"[ERROR esperado] Cliente duplicado -> {e}")

    # ---- OP 4: servicio válido de sala ----
    try:
        sala = ReservaSala("S01", "Sala Juntas", 50000, 10)
        gestor_servicios.agregar(sala)
        print(f"[OK] Servicio sala: {sala.describir()}")
    except Exception as e:
        logger.registrar_error(e, "op4 crear sala")

    # ---- OP 5: servicio válido de equipo ----
    try:
        equipo = AlquilerEquipo("E01", "Proyector", 30000, requiere_deposito=True)
        gestor_servicios.agregar(equipo)
        print(f"[OK] Servicio equipo: {equipo.describir()}")
    except Exception as e:
        logger.registrar_error(e, "op5 crear equipo")

    # ---- OP 6: servicio válido de asesoría ----
    try:
        asesoria = AsesoriaEspecializada("A01", "Asesoría IA", 80000, "Ing. Torres")
        gestor_servicios.agregar(asesoria)
        print(f"[OK] Servicio asesoría: {asesoria.describir()}")
    except Exception as e:
        logger.registrar_error(e, "op6 crear asesoría")

    # ---- OP 7: polimorfismo (mismo método, distinto resultado) ----
    try:
        # Recorremos todos los servicios y cada uno responde con su propia fórmula
        for servicio in gestor_servicios.servicios:
            costo = servicio.calcular_costo(3, impuesto=0.19)
            print(f"   Costo {servicio.nombre} (3h + IVA 19%): ${costo}")
        logger.registrar_evento("Cálculo polimórfico ejecutado")
    except Exception as e:
        logger.registrar_error(e, "op7 calcular costos")

    # ---- OP 8: sobrecarga (cálculo con descuento) ----
    try:
        costo_desc = sala.calcular_costo_con_descuento(3, 0.10)
        print(f"[OK] Costo sala con 10% descuento: ${costo_desc}")
        logger.registrar_evento(f"Cálculo con descuento: {costo_desc}")
    except Exception as e:
        logger.registrar_error(e, "op8 costo con descuento")

    # ---- OP 9: reserva exitosa ----
    reserva1 = None
    try:
        reserva1 = gestor_reservas.crear(cliente1, sala, 2)
        print(f"[OK] Reserva creada: {reserva1.describir()}")
    except Exception as e:
        print(f"[ERROR no esperado] {e}")

    # ---- OP 10: reserva con duración inválida ----
    try:
        gestor_reservas.crear(cliente1, equipo, 0)
    except DatosInvalidosError as e:
        print(f"[ERROR esperado] Duración inválida -> {e}")

    # ---- OP 11: confirmar reserva ----
    try:
        if reserva1:
            gestor_reservas.confirmar(reserva1)
            print(f"[OK] Reserva confirmada: estado {reserva1.estado}")
    except Exception as e:
        print(f"[ERROR al confirmar] {e}")

    # ---- OP 12: intentar reservar servicio ya ocupado ----
    try:
        gestor_reservas.crear(cliente1, sala, 2)
    except ReservaInvalidaError as e:
        print(f"[ERROR esperado] Servicio ocupado -> {e}")

    # ---- OP 13: cancelar reserva confirmada ----
    try:
        if reserva1:
            gestor_reservas.cancelar(reserva1)
            print(f"[OK] Reserva cancelada: estado {reserva1.estado}")
    except Exception as e:
        print(f"[ERROR al cancelar] {e}")

    # ---- OP 14: intentar procesar reserva cancelada ----
    try:
        if reserva1:
            gestor_reservas.procesar(reserva1)
    except OperacionNoPermitidaError as e:
        print(f"[ERROR esperado] No se puede procesar cancelada -> {e}")

    # ---- OP 15: encadenamiento de excepciones ----
    try:
        try:
            gestor_reservas.crear(cliente1, equipo, -1)
        except DatosInvalidosError as e:
            # Encadenamos con raise ... from para no perder la causa original
            raise ReservaInvalidaError(
                "No se pudo crear la reserva por datos inválidos"
            ) from e
    except ReservaInvalidaError as e:
        logger.registrar_error(e, "op15 encadenamiento")
        print(f"[ERROR encadenado] {e}")
        print(f"        Causa original: {e.__cause__}")

    print("\n=== FIN SIMULACIÓN ===\n")
    print("Sistema sigue operativo. Revisa logs/eventos.log para más detalle.")


if __name__ == "__main__":
    # try/except/finally global: garantiza que el mensaje final siempre salga
    try:
        ejecutar_simulacion()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        print("Ejecución finalizada.")