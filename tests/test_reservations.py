from contextlib import redirect_stdout
from io import StringIO
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reservas.cli import main
from reservas.repository import ReservationRepository
from reservas.service import (
    InvalidReservationError,
    ReservationAlreadyCancelledError,
    ReservationConflictError,
    ReservationNotFoundError,
    ReservationService,
)


class ReservationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_directory.name) / "test-reservas.db"
        self.repository = ReservationRepository(database_path)
        self.service = ReservationService(self.repository)

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_lists_initial_equipment_catalog(self) -> None:
        self.assertEqual(
            [equipment.identifier for equipment in self.service.list_equipment()],
            ["FUE-01", "MIC-01", "MIC-02", "MUL-01", "OSC-01"],
        )

    def test_creates_valid_reservation_and_trims_requester(self) -> None:
        reservation = self.service.create_reservation(
            "MIC-01", "  Ada Lovelace  ", "2026-10-26 14:30", "2026-10-26 15:45"
        )

        self.assertEqual(reservation.requester, "Ada Lovelace")
        self.assertEqual(reservation.status, "active")
        self.assertGreater(reservation.id, 0)

    def test_allows_reservations_in_the_past(self) -> None:
        reservation = self.service.create_reservation(
            "MIC-01", "Ada", "2020-01-01 10:00", "2020-01-01 11:00"
        )

        self.assertEqual(reservation.status, "active")

    def test_rejects_start_equal_to_or_after_end(self) -> None:
        for start, end in (
            ("2026-10-26 14:30", "2026-10-26 14:30"),
            ("2026-10-26 15:00", "2026-10-26 14:30"),
        ):
            with self.subTest(start=start, end=end):
                with self.assertRaises(InvalidReservationError):
                    self.service.create_reservation("MIC-01", "Ada", start, end)

    def test_rejects_overlapping_active_reservation_for_same_equipment(self) -> None:
        self.service.create_reservation(
            "MIC-01", "Ada", "2026-10-26 14:00", "2026-10-26 15:00"
        )

        with self.assertRaises(ReservationConflictError):
            self.service.create_reservation(
                "MIC-01", "Grace", "2026-10-26 14:59", "2026-10-26 16:00"
            )

    def test_availability_and_creation_share_overlap_rules(self) -> None:
        self.service.create_reservation(
            "MIC-01", "Ada", "2026-10-26 14:00", "2026-10-26 15:00"
        )

        self.assertFalse(
            self.service.is_available(
                "mic-01", "2026-10-26 14:30", "2026-10-26 15:30"
            )
        )
        self.assertTrue(
            self.service.is_available(
                "MIC-01", "2026-10-26 15:00", "2026-10-26 16:00"
            )
        )
        with self.assertRaises(ReservationConflictError):
            self.service.create_reservation(
                "MIC-01", "Grace", "2026-10-26 14:30", "2026-10-26 15:30"
            )

    def test_accepts_consecutive_reservations(self) -> None:
        self.service.create_reservation(
            "OSC-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
        )
        next_reservation = self.service.create_reservation(
            "OSC-01", "Grace", "2026-10-26 11:00", "2026-10-26 12:00"
        )

        self.assertEqual(next_reservation.status, "active")

    def test_accepts_simultaneous_reservations_for_different_equipment(self) -> None:
        first = self.service.create_reservation(
            "MIC-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
        )
        second = self.service.create_reservation(
            "MIC-02", "Grace", "2026-10-26 10:00", "2026-10-26 11:00"
        )

        self.assertNotEqual(first.equipment_id, second.equipment_id)

    def test_cancellation_releases_interval_and_preserves_history(self) -> None:
        reservation = self.service.create_reservation(
            "MUL-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
        )

        cancelled = self.service.cancel_reservation(reservation.id)

        self.assertEqual(cancelled.status, "cancelled")
        self.assertTrue(
            self.service.is_available(
                "MUL-01", "2026-10-26 10:00", "2026-10-26 11:00"
            )
        )
        self.assertEqual(len(self.service.list_reservations()), 1)
        self.assertEqual(self.service.list_reservations()[0].status, "cancelled")
        reopened = ReservationService(
            ReservationRepository(self.repository.database_path)
        )
        self.assertEqual(
            reopened.get_reservation(reservation.id).status, "cancelled"
        )

    def test_rejects_unknown_equipment_and_empty_requester(self) -> None:
        with self.assertRaises(InvalidReservationError):
            self.service.create_reservation(
                "BAD-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
            )
        with self.assertRaises(InvalidReservationError):
            self.service.create_reservation(
                "MIC-01", "   ", "2026-10-26 10:00", "2026-10-26 11:00"
            )
        with self.assertRaises(InvalidReservationError):
            self.service.is_available(
                "BAD-01", "2026-10-26 10:00", "2026-10-26 11:00"
            )

    def test_rejects_invalid_format_date_and_clock_time(self) -> None:
        for value in (
            "2026-10-26 14",
            "2026-10-26 14:30:00",
            "2026-02-30 14:30",
            "2026-10-26 24:00",
        ):
            with self.subTest(value=value):
                with self.assertRaises(InvalidReservationError):
                    self.service.is_available(
                        "MIC-01", value, "2026-10-26 15:00"
                    )
                with self.assertRaises(InvalidReservationError):
                    self.service.create_reservation(
                        "MIC-01", "Ada", value, "2026-10-26 15:00"
                    )

    def test_rejects_nonexistent_local_time_for_creation_and_query(self) -> None:
        for operation in (
            lambda: self.service.is_available(
                "MIC-01", "2008-10-19 00:30", "2008-10-19 02:00"
            ),
            lambda: self.service.create_reservation(
                "MIC-01", "Ada", "2008-10-19 00:30", "2008-10-19 02:00"
            ),
        ):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(InvalidReservationError, "no existe"):
                    operation()

    def test_rejects_ambiguous_local_time_for_creation_and_query(self) -> None:
        for operation in (
            lambda: self.service.is_available(
                "MIC-01", "2008-03-15 23:30", "2008-03-16 01:30"
            ),
            lambda: self.service.create_reservation(
                "MIC-01", "Ada", "2008-03-15 23:30", "2008-03-16 01:30"
            ),
        ):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(InvalidReservationError, "ambigua"):
                    operation()

    def test_rejects_cancelling_already_cancelled_reservation(self) -> None:
        reservation = self.service.create_reservation(
            "FUE-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
        )
        self.service.cancel_reservation(reservation.id)

        with self.assertRaises(ReservationAlreadyCancelledError):
            self.service.cancel_reservation(reservation.id)

    def test_rejects_cancelling_unknown_reservation(self) -> None:
        with self.assertRaises(ReservationNotFoundError):
            self.service.cancel_reservation(999)

    def test_persists_reservations_when_repository_is_reopened(self) -> None:
        reservation = self.service.create_reservation(
            "OSC-01", "Ada", "2026-10-26 10:00", "2026-10-26 11:00"
        )
        reopened = ReservationService(
            ReservationRepository(self.repository.database_path)
        )

        self.assertEqual(reopened.get_reservation(reservation.id), reservation)

    def test_cli_routes_equipment_booking_availability_and_cancellation(self) -> None:
        inputs = [
            "1",
            "3",
            "MIC-01",
            "Ada",
            "2026-10-26 10:00",
            "2026-10-26 11:00",
            "2",
            "MIC-01",
            "2026-10-26 10:00",
            "2026-10-26 11:00",
            "4",
            "1",
            "0",
        ]
        output = StringIO()
        with (
            patch("reservas.cli.ReservationRepository", return_value=self.repository),
            patch("builtins.input", side_effect=inputs),
            redirect_stdout(output),
        ):
            main()

        self.assertIn("MIC-01: Microscopio digital", output.getvalue())
        self.assertIn("Reserva creada. ID: 1", output.getvalue())
        self.assertIn("No disponible.", output.getvalue())
        self.assertIn("Reserva 1 cancelada.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
