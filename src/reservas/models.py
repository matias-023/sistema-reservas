"""Modelos simples compartidos por el servicio y la persistencia."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Equipment:
    identifier: str
    name: str


@dataclass(frozen=True)
class Reservation:
    id: int
    equipment_id: str
    requester: str
    start: datetime
    end: datetime
    status: str
