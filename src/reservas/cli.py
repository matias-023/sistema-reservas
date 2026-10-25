from .repository import ReservationRepository
from .service import ReservationError, ReservationService


def main() -> None:
    service = ReservationService(ReservationRepository())
    while True:
        print(
            "\nSistema de reservas\n"
            "1. Consultar equipos\n"
            "2. Consultar disponibilidad\n"
            "3. Crear reserva\n"
            "4. Cancelar reserva\n"
            "0. Salir"
        )
        option = input("Opcion: ").strip()
        try:
            if option == "1":
                for equipment in service.list_equipment():
                    print(f"{equipment.identifier}: {equipment.name}")
            elif option == "2":
                equipment_id = input("Equipo: ")
                start = input("Inicio (AAAA-MM-DD HH:MM): ")
                end = input("Fin (AAAA-MM-DD HH:MM): ")
                available = service.is_available(equipment_id, start, end)
                print("Disponible." if available else "No disponible.")
            elif option == "3":
                equipment_id = input("Equipo: ")
                requester = input("Solicitante: ")
                start = input("Inicio (AAAA-MM-DD HH:MM): ")
                end = input("Fin (AAAA-MM-DD HH:MM): ")
                reservation = service.create_reservation(
                    equipment_id, requester, start, end
                )
                print(f"Reserva creada. ID: {reservation.id}")
            elif option == "4":
                reservation_id = int(input("ID de reserva: "))
                reservation = service.cancel_reservation(reservation_id)
                print(f"Reserva {reservation.id} cancelada.")
            elif option == "0":
                return
            else:
                print("Opcion no valida.")
        except ReservationError as error:
            print(f"Error: {error}")
        except ValueError:
            print("El ID debe ser un numero entero.")
