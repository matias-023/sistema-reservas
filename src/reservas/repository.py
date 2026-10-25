"""Persistencia local de reservas mediante SQLite."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from .models import Equipment, Reservation

EQUIPMENT = (
    ("MIC-01", "Microscopio digital"),
    ("MIC-02", "Microscopio digital"),
    ("OSC-01", "Osciloscopio"),
    ("MUL-01", "Multímetro"),
    ("FUE-01", "Fuente de alimentación"),
)


class ReservationRepository:
    def __init__(self, database_path: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.database_path = Path(
            database_path or project_root / "data" / "reservas.db"
        )
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(
            self.database_path, timeout=10, isolation_level=None
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
                connection.commit()
            finally:
                if connection.in_transaction:
                    connection.rollback()

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS equipment (
                    identifier TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equipment_id TEXT NOT NULL REFERENCES equipment(identifier),
                    requester TEXT NOT NULL,
                    start_at TEXT NOT NULL,
                    end_at TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('active', 'cancelled'))
                );
                """
            )
            connection.executemany(
                "INSERT OR IGNORE INTO equipment (identifier, name) VALUES (?, ?)",
                EQUIPMENT,
            )

    def list_equipment(self) -> list[Equipment]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT identifier, name FROM equipment ORDER BY identifier"
            ).fetchall()
        return [Equipment(row["identifier"], row["name"]) for row in rows]

    def get_equipment(self, equipment_id: str) -> Equipment | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT identifier, name FROM equipment WHERE identifier = ?",
                (equipment_id,),
            ).fetchone()
        if row is None:
            return None
        return Equipment(row["identifier"], row["name"])

    def has_conflict(
        self,
        equipment_id: str,
        start: datetime,
        end: datetime,
    ) -> bool:
        with self._connect() as connection:
            return self._has_conflict(connection, equipment_id, start, end)

    @staticmethod
    def _has_conflict(
        connection: sqlite3.Connection,
        equipment_id: str,
        start: datetime,
        end: datetime,
    ) -> bool:
        query = """
            SELECT 1 FROM reservations
            WHERE equipment_id = ? AND status = 'active'
              AND start_at < ? AND end_at > ?
            LIMIT 1
        """
        params = (
            equipment_id,
            _to_utc_string(end),
            _to_utc_string(start),
        )
        return connection.execute(query, params).fetchone() is not None

    def create_reservation_if_available(
        self,
        equipment_id: str,
        requester: str,
        start: datetime,
        end: datetime,
    ) -> Reservation | None:
        with self.transaction() as connection:
            if self._has_conflict(connection, equipment_id, start, end):
                return None
            return self._insert_reservation(
                connection, equipment_id, requester, start, end
            )

    @staticmethod
    def _insert_reservation(
        connection: sqlite3.Connection,
        equipment_id: str,
        requester: str,
        start: datetime,
        end: datetime,
    ) -> Reservation:
        cursor = connection.execute(
            """
            INSERT INTO reservations
                (equipment_id, requester, start_at, end_at, status)
            VALUES (?, ?, ?, ?, 'active')
            """,
            (
                equipment_id,
                requester,
                _to_utc_string(start),
                _to_utc_string(end),
            ),
        )
        row = connection.execute(
            "SELECT * FROM reservations WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        if row is None:
            raise RuntimeError("SQLite no devolvió la reserva recién creada.")
        return _reservation_from_row(row)

    def get_reservation(
        self,
        reservation_id: int,
    ) -> Reservation | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
            ).fetchone()
        return None if row is None else _reservation_from_row(row)

    def list_reservations(self) -> list[Reservation]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM reservations ORDER BY id"
            ).fetchall()
        return [_reservation_from_row(row) for row in rows]

    def cancel_reservation(
        self, reservation_id: int
    ) -> tuple[Reservation | None, bool]:
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
            ).fetchone()
            if row is None:
                return None, False
            reservation = _reservation_from_row(row)
            if reservation.status == "cancelled":
                return reservation, False

            connection.execute(
                "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
                (reservation_id,),
            )
            return (
                Reservation(
                    id=reservation.id,
                    equipment_id=reservation.equipment_id,
                    requester=reservation.requester,
                    start=reservation.start,
                    end=reservation.end,
                    status="cancelled",
                ),
                True,
            )


def _to_utc_string(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="minutes")


def _reservation_from_row(row: sqlite3.Row) -> Reservation:
    return Reservation(
        id=row["id"],
        equipment_id=row["equipment_id"],
        requester=row["requester"],
        start=datetime.fromisoformat(row["start_at"]),
        end=datetime.fromisoformat(row["end_at"]),
        status=row["status"],
    )
