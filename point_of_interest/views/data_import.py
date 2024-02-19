from __future__ import annotations

import logging
from io import TextIOWrapper
from pathlib import Path

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from point_of_interest.handler import FILE_PROVIDERS, Handler

logger = logging.getLogger(__name__)


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        file_extension = Path(file.name).suffix.lower()

        allowed_extensions = FILE_PROVIDERS.keys()
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file format")

        return file


class DataImport(ViewSet):
    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data["file"]
        file_extension = Path(file_obj.name).suffix.lower()
        provider = FILE_PROVIDERS[file_extension]
        csv_file_wrapper = TextIOWrapper(file_obj, encoding="utf-8")

        Handler(provider(csv_file_wrapper)).save()

        return Response(
            {"message": "Data import successful"}, status=status.HTTP_201_CREATED
        )
