import io
from subprocess import CompletedProcess
from unittest import TestCase, mock

from django.core.management import call_command

from point_of_interest.handler import CSVProvider, Handler
from point_of_interest.models import Poi


class TestCli(TestCase):
    def test_single_file(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch("subprocess.run", autospec=True) as subprocess_run:
            subprocess_run.side_effect = [CompletedProcess([], returncode=0)]

            return_code = call_command(
                "data_import",
                "--file",
                "examples/short_pois.csv",
                stdout=stdout,
                stderr=stderr,
            )

        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(return_code, None)

    def test_handler(self):
        with open("examples/short_pois.csv") as f:
            Handler(CSVProvider(f)).save()
            self.assertTrue(Poi.objects.filter(name="ちぬまん").exists())
