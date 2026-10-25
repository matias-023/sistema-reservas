"""Reglas de negocio y operaciones de reservas."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .models import Equipment, Reservation
from .repository import ReservationRepository

TIME_ZONE_NAME = "America/Argentina/Cordoba"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
DATETIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}")


class ReservationError(Exception):
    """Error esperado al validar o ejecutar una operación de reservas."""


class InvalidReservationError(ReservationError):
    """Los datos proporcionados no cumplen las reglas de reservas."""


class ReservationConflictError(ReservationError):
    """El intervalo se superpone con otra reserva activa del equipo."""


class ReservationNotFoundError(ReservationError):
    """No existe una reserva con el identificador indicado."""


class ReservationAlreadyCancelledError(ReservationError):
    """La reserva ya está cancelada."""


def parse_local_datetime(value: str) -> datetime:
    """Parsea una fecha local y rechaza horas inválidas, inexistentes o ambiguas."""
    if not DATETIME_PATTERN.fullmatch(value):
        raise InvalidReservationError(
            "La fecha y hora debe respetar el formato AAAA-MM-DD HH:MM."
        )

    try:
        local_value = datetime.strptime(value, DATETIME_FORMAT)
    except ValueError as error:
        raise InvalidReservationError(
            "La fecha u hora indicada no es válida."
        ) from error

    try:
        zone = ZoneInfo(TIME_ZONE_NAME)
    except ZoneInfoNotFoundError as error:
        raise ReservationError(
            f"No están disponibles los datos de zona horaria {TIME_ZONE_NAME}."
        ) from error

    candidates: list[datetime] = []
    for fold in (0, 1):
        candidate = local_value.replace(tzinfo=zone, fold=fold)
        round_trip = candidate.astimezone(timezone.utc).astimezone(zone)
        if round_trip.replace(tzinfo=None) == local_value:
            candidates.append(candidate)

    if not candidates:
        raise InvalidReservationError(
            "La hora local no existe por un cambio en las reglas horarias."
        )

    if len({candidate.utcoffset() for candidate in candidates}) > 1:
        raise InvalidReservationError(
            "La hora local es ambigua por un cambio en las reglas horarias."
        )

    return candidates[0]


class ReservationService:
    def __init__(self, repository: ReservationRepository) -> None:
        self.repository = repository

    def list_equipment(self) -> list[Equipment]:
        return self.repository.list_equipment()

    def is_available(
        self, equipment_id: str, start: str, end: str
    ) -> bool:
        equipment_id = self._validate_equipment(equipment_id)
        parsed_start, parsed_end = self._validate_datetimes(start, end)
        return not self._has_conflict(
            equipment_id, parsed_start, parsed_end
        )

    def create_reservation(
        self, equipment_id: str, requester: str, start: str, end: str
    ) -> Reservation:
        equipment_id = self._validate_equipment(equipment_id)
        requester = requester.strip()
        if not requester:
            raise InvalidReservationError("El nombre del solicitante no puede estar vacío.")

        parsed_start, parsed_end = self._validate_datetimes(start, end)
        reservation = self.repository.create_reservation_if_available(
            equipment_id, requester, parsed_start, parsed_end
        )
        if reservation is None:
            raise ReservationConflictError(
                "El equipo ya tiene una reserva activa que se superpone "
                "con ese intervalo."
            )
        return reservation

    def cancel_reservation(self, reservation_id: int) -> Reservation:
        reservation, changed = self.repository.cancel_reservation(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(
                f"No existe una reserva con ID {reservation_id}."
            )
        if not changed:
            raise ReservationAlreadyCancelledError(
                f"La reserva {reservation_id} ya está cancelada."
            )
        return reservation

    def get_reservation(self, reservation_id: int) -> Reservation | None:
        return self.repository.get_reservation(reservation_id)

    def list_reservations(self) -> list[Reservation]:
        return self.repository.list_reservations()

    def _validate_equipment(self, equipment_id: str) -> str:
        equipment_id = equipment_id.strip().upper()
        if self.repository.get_equipment(equipment_id) is None:
            raise InvalidReservationError(
                f"El equipo {equipment_id or '(vacío)'} no está registrado."
            )
        return equipment_id

    @staticmethod
    def _validate_datetimes(start: str, end: str) -> tuple[datetime, datetime]:
        parsed_start = parse_local_datetime(start)
        parsed_end = parse_local_datetime(end)
        if parsed_start.astimezone(timezone.utc) >= parsed_end.astimezone(
            timezone.utc
        ):
            raise InvalidReservationError(
                "El inicio debe ser anterior al fin de la reserva."
            )
        return parsed_start, parsed_end

    def _has_conflict(
        self, equipment_id: str, start: datetime, end: datetime
    ) -> bool:
        return self.repository.has_conflict(equipment_id, start, end)
