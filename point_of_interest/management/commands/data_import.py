import argparse
import logging
from pathlib import Path

from django.core.management.base import BaseCommand

from point_of_interest.handler import FILE_PROVIDERS, Handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Extracts poi data from the given provider"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            nargs="+",
            required=True,
            help="File location(s)",
            type=argparse.FileType("r"),
        )

    def handle(self, *args, **kwargs):
        for file in kwargs["file"]:
            file_extension = Path(file.name).suffix.lower()
            provider = FILE_PROVIDERS[file_extension]

            Handler(provider(file)).save()
            logger.info(f"Successful data import for {file.name}")

        print("DONE")
