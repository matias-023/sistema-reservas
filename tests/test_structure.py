import unittest
from contextlib import redirect_stdout
from io import StringIO

from reservas.cli import main


class ProjectStructureTests(unittest.TestCase):
    def test_cli_entry_point_reports_application_is_under_construction(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            main()

        self.assertIn("aplicacion en construccion", output.getvalue())


if __name__ == "__main__":
    unittest.main()
