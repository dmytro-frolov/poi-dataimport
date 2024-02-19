import csv
import json
import logging
import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

from django.db.transaction import atomic

from point_of_interest import models

logger = logging.getLogger()

#
# ideally it would make sense to use some kind of serializer
#


class Provider(ABC):
    def __init__(self, file_obj):
        self.file = file_obj

    @abstractmethod
    def save(self):
        pass


class JsonProvider(Provider):
    @atomic
    def save(self):
        for input_poi in json.load(self.file):
            category, _ = models.Category.objects.get_or_create(
                name=input_poi["category"]
            )
            location, _ = models.Location.objects.get_or_create(
                latitude=input_poi["coordinates"]["latitude"],
                longitude=input_poi["coordinates"]["longitude"],
            )
            models.Poi.objects.create(
                external_id=input_poi["id"],
                name=input_poi["name"],
                category=category,
                description=input_poi["description"],
                location=location,
                ratings=input_poi["ratings"],
                provider="json_provider",
            )


class CSVProvider(Provider):
    # removed @atomic to see ongoing result
    # @atomic
    def save(self):
        with ThreadPoolExecutor() as executor:
            csvreader = csv.reader(self.file)
            # skip the header
            next(csvreader)

            for row in csvreader:
                executor.submit(self.process_row, row)

    def process_row(self, row):
        (
            poi_id,
            poi_name,
            poi_category,
            poi_latitude,
            poi_longitude,
            poi_ratings,
            *_,
        ) = row

        poi_ratings = re.sub(r"[{}]", "", poi_ratings).split(",")

        category, _ = models.Category.objects.get_or_create(name=poi_category)
        location, _ = models.Location.objects.get_or_create(
            latitude=poi_latitude,
            longitude=poi_longitude,
        )

        models.Poi.objects.create(
            external_id=poi_id,
            name=poi_name,
            category=category,
            location=location,
            ratings=[float(rating) for rating in poi_ratings],
            provider="csv_provider",
        )


class XMLProvider(Provider):
    @atomic
    def save(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        for data_record in root.findall("DATA_RECORD"):
            pid = data_record.find("pid").text
            pname = data_record.find("pname").text
            pcategory = data_record.find("pcategory").text
            platitude = data_record.find("platitude").text
            plongitude = data_record.find("plongitude").text
            pratings = data_record.find("pratings").text.split(",")

            category, _ = models.Category.objects.get_or_create(name=pcategory)
            location, _ = models.Location.objects.get_or_create(
                latitude=platitude,
                longitude=plongitude,
            )

            models.Poi.objects.create(
                external_id=pid,
                name=pname,
                category=category,
                location=location,
                ratings=pratings,
                provider="xml_provider",
            )


class Handler:
    def __init__(self, provider_obj: Provider):
        self._provider = provider_obj

    def save(self):
        logger.info("Data import started")
        self._provider.save()
        logger.info("Data import finished")


FILE_PROVIDERS = {
    ".json": JsonProvider,
    ".csv": CSVProvider,
    ".xml": XMLProvider,
}
